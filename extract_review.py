from playwright.sync_api import sync_playwright, TimeoutError
from utils import visit_hotel
import traceback
import time

from utils import parse_review

def extract_review(link, USER_AGENTS:dict,max_retries=3):
    list_hotel= []
    review = []
    for attempt in range(max_retries+1):

        try:
            with sync_playwright() as p:
                # Masuk ke browser dan visi halaman hotel
                page, context, browser = visit_hotel(p, USER_AGENTS=USER_AGENTS, link=link)

                hotel_name = page.locator('.HeaderCerebrum h1').text_content()
                
                page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
                time.sleep(5)
                
                nav_loc = page.locator('nav[data-element-name="review-paginator-step"]').first
                
                if nav_loc.count() > 0:
                    max_page = int(nav_loc.locator('li').last.text_content())
                    print('Jumlah halaman: ',max_page)
                    for i in range(1,max_page+1):
                        count_review = page.locator('div.Review-comment')
                        for y in range(count_review.count()):
                            review_loc = count_review.nth(y)
                            dec_review = parse_review(
                                review_loc=review_loc,
                                hotel_name=hotel_name,
                                page=page)
                            review.append(dec_review)
                        
                            print(f"✅ Berhasil menambahkan komentar ke-{y} pada halaman ke-{i}")

                        if i < max_page:
                            page.locator('button[aria-label="Next reviews page"]').first.click()
                            time.sleep(5)
                else:
                    print("hanya 1 halaman")
                    count_review = page.locator('div.Review-comment')
                    for y in range(count_review.count()):
                        review_loc = count_review.nth(y)
                        dec_review = parse_review(
                            review_loc=review_loc,
                            hotel_name=hotel_name,
                            page=page)
                        review.append(dec_review)

                page.wait_for_timeout(5000)

            return review
        
        
        except Exception as e:
            print(f"❌ Gagal mengambil detail hotel ({link}) - Percobaan ke-{attempt}")
            print(f"   Error: {e}")
            traceback.print_exc()
            
            delay = 3
            if attempt < max_retries:
                print(f"⏳ Menunggu {delay} detik sebelum mencoba ulang...")
                time.sleep(delay)
            else:
                print("🚫 Gagal setelah maksimal percobaan. Lewati hotel ini.")
                return []
