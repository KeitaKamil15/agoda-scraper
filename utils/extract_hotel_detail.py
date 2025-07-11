from .visit_hotel_detail import visit_hotel_detail
from .change_date_book import change_date_book
from .change_date_manual import change_date_manual
from .extract_amenities_facilities import extract_amenities_facilities
from .click_all_show_more import click_all_show_more
from playwright.sync_api import sync_playwright, TimeoutError
import time


def extract_hotel_detail(USER_AGENTS: dict, link, max_retries=3):

    list_hotel= []

    for attempt in range(max_retries+1):

        try:
            with sync_playwright() as p:
                # Masuk ke browser dan visi halaman hotel
                page, context, browser = visit_hotel_detail(p, USER_AGENTS=USER_AGENTS, link=link)

                hotel_name = page.locator('.HeaderCerebrum h1').text_content()
                hotel_loc = page.locator('.HeaderCerebrum__Location span').first.text_content()
                # list_type_room = page.locator('.roomGridContent')
                
                
                try:
                    # Tunggu elemen muncul maksimal 5 detik
                    page.wait_for_selector('.RoomGrid-searchTimeOutText', timeout=5000)
                    fail_list_type_room = page.locator('.RoomGrid-searchTimeOutText').first.text_content().strip()

                    if "Sorry, we have no rooms" in fail_list_type_room:
                        print("Kamar penuh, lakukan pilih tanggal lain")
                        # panggil fungsi ganti tanggal di sini
                        change_date_book(page)
                        # page = change_date_book(page)
                    else:
                        print("Ada kamar, lanjut proses")
                except TimeoutError:
                    # Elemen tidak muncul → kamar tersedia
                    print("Elemen pesan kamar penuh tidak muncul → kamar ada, lanjut proses")

                # print(hotel_name)
                # print(hotel_loc)

                # change_date_manual(page)

                # extract amenities & facilities list
                # list_facilities,page = extract_amenities_facilities(page)
                list_facilities = extract_amenities_facilities(page)


                # Click all Show More Deals
                click_all_show_more(page)
                

                type_room = page.locator('div[data-selenium="MasterRoom"]')
                print("tipe room nya ada = ", type_room.count())

                # Lakukan looping berdasarkan tipe roomnya
                for i in range(type_room.count()):
                    type_room_name = type_room.nth(i).locator('span[data-selenium="masterroom-title-name"]').text_content()
                    print("Nama tipe roomnya ==> ", type_room_name)

                    # room_size = type_room.nth(i).locator('div:has-text("Room size")')
                    room_size_locator = type_room.nth(i).locator('div.MasterRoom-amenitiesTitle:has-text("Room size:")')
                    room_size = ""

                    if room_size_locator.count() > 0:
                        room_size = room_size_locator.first.text_content()
                        # print("Room size:", room_size)
                    else:
                        print("Tidak ditemukan ukuran kamar")
                    
                    price_tipe = type_room.nth(i).locator('div[data-element-name="child-room-item"]')
                    price = None
                    for y in range(price_tipe.count()):
                        list_benefit = price_tipe.nth(y).locator('div.ChildRoomsList-room-featurebuckets')
                        # print(price.text_content())
                        
                        # Ambil div pertama di dalam container tersebut
                        first_inner_div = list_benefit.locator(":scope > div").first

                        # Mengambil list benefit dari jenis harga
                        benefit = first_inner_div.locator("p").all_inner_texts()

                        # price = price_tipe.locator('div.PriceContainer').locator('div[data-selenium="CrossedOutPrice"]')
                        price_locator = price_tipe.locator('div.PriceContainer').locator('div[data-element-name="fpc-cor-price"]')
                        if price_locator.count() > 0:
                            print("Ini harganya dengan promo ")
                            price = price_locator.first.get_attribute("data-fpc-value")
                            # price = price.get_attribute("data-fpc-value").first
                        else:
                            price_locator = price_tipe.locator('div.PriceContainer').locator('div[data-selenium="CrossedOutPrice"]')
                            if price_locator.count() > 0:
                                print('data-selenium="CrossedOutPrice"')
                                price = price_locator.first.get_attribute("data-element-value")
                            else:
                                print("Menggunakan harga tanpa promo")
                                price_locator = price_tipe.locator('div.PriceContainer').locator('div[data-element-name="fpc-room-price"]')
                                if price_locator.count() > 0:
                                    price = price_locator.first.get_attribute("data-fpc-value")
                                    # price = price.get_attribute("data-fpc-value").first
                                else:
                                    print("Menggunakan element STRONG")
                                    price_locator = price_tipe.locator('div.PriceContainer').locator('strong[data-ppapi="room-price"]')
                                    price = price_locator.first.text_content()

                        
                        # print(benefit)
                        data = {
                        "hotel_name" : hotel_name,
                        "address" : hotel_loc,
                        "room_type" : type_room_name,
                        "room size" : room_size,
                        "price" : price,
                        "Benefit" : benefit
                        }

                        # tambahkan list fasilitas 
                        data.update(list_facilities)

                        # hasil scraping di array
                        list_hotel.append(data)

                page.wait_for_timeout(5000)

            return list_hotel
        
        
        except Exception as e:
            print(f"❌ Gagal mengambil detail hotel ({link}) - Percobaan ke-{attempt}")
            print(f"   Error: {e}")
            
            delay = 3
            if attempt < max_retries:
                print(f"⏳ Menunggu {delay} detik sebelum mencoba ulang...")
                time.sleep(delay)
            else:
                print("🚫 Gagal setelah maksimal percobaan. Lewati hotel ini.")
                return []


    # print("============================== HASIL =============================")
    # print(list_hotel)
    