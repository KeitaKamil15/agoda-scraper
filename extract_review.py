from playwright.sync_api import sync_playwright, TimeoutError
from utils import visit_hotel
import traceback
import time

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
                    for i in range(1,max_page):
                        count_review = page.locator('div.Review-comment')
                        for y in range(count_review.count()):
                            review_loc = count_review.nth(y)
                            review_id = review_loc.get_attribute('data-review-id')
                            review_name_origin = review_loc.locator('div[data-info-type="reviewer-name"]').text_content()
                            review_score = review_loc.locator('div.Review-comment-leftScore').text_content()
                            review_score_text_loc = review_loc.locator('div.Review-comment-leftScoreText')
                            if review_score_text_loc.count() > 0:
                                review_score_text = review_score_text_loc.text_content()
                            else:
                                review_score_text = None
                            trip_type = review_loc.locator('div[data-info-type="group-name"]').text_content()
                            room_type = review_loc.locator('div[data-info-type="room-type"]').text_content()
                            stay_date = review_loc.locator('div[data-info-type="stay-detail"]').text_content()
                            review_title = review_loc.locator('h4[data-testid="review-title"]').text_content()
                            review_comment = review_loc.locator('p[data-testid="review-comment"]').text_content()
                            review_date_loc = review_loc.locator('div.Review-statusBar-left')
                            if review_date_loc.count() > 0:
                                review_date = review_date_loc.first.text_content()
                            else:
                                review_date = page.locator('div.Review-comment-bubble').locator(':scope > div').nth(1).text_content()

                            dec_review = {
                                'hotel_name': hotel_name,
                                'review_id':review_id,
                                'review_name_origin': review_name_origin,
                                'review_score':review_score,
                                'review_score_text':review_score_text,
                                'trip_type':trip_type,
                                'room_type':room_type,
                                'stay_date':stay_date,
                                'review_title':review_title,
                                'review_comment':review_comment,
                                'review_date':review_date
                            }
                            review.append(dec_review)
                            print(f"Berhasil menambahkan komentar ke {y} pada hal ke {i}")

                        page.locator('button[aria-label="Next reviews page"]').first.click()
                        time.sleep(5)
                else:
                    print("hanya 1 halaman")



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
