from utils import visit_hotel, check_room_availability, change_date_book, extract_amenities_facilities, click_all_show_more, extract_room_type, extract_helpful_fact, extract_coord, extract_room_price, change_date_manual, generate_weekend_dates

from playwright.sync_api import sync_playwright, TimeoutError

import time
from datetime import datetime, timedelta
import traceback


def extract_hotel_detail(USER_AGENTS: dict, link, max_retries=3):

    """
    Example output : 
    [
        {
            key:value,
            key:value,
            key: ['list1','list2']
        }
    ]
    """

    list_hotel= []

    for attempt in range(max_retries+1):

        try:
            with sync_playwright() as p:
                # Masuk ke browser dan visi halaman hotel
                page, context, browser = visit_hotel(p, USER_AGENTS=USER_AGENTS, link=link)

                hotel_name = page.locator('.HeaderCerebrum h1').text_content()
                hotel_loc = page.locator('.HeaderCerebrum__Location span').first.text_content()
                # list_type_room = page.locator('.roomGridContent')
                
                # Check if the room is available
                check_room_availability(page)

                start_date = datetime.now()
                print("Start_Date ", start_date)
                end_date = start_date + timedelta(days=365)
                print("End Date ", end_date)
                weekend_dates = generate_weekend_dates(start_date, end_date)
                print('weekend_dates :', weekend_dates)

                
                
                for date in weekend_dates:
                    print(f"Checking for date: {date.strftime('%Y-%m-%d')}")
                    change_date_manual(page, date)

                    # extract amenities & facilities list
                    list_facilities = extract_amenities_facilities(page)

                    # extract some helpful facts section
                    other_information = extract_helpful_fact(page)

                    # Click all Show More Deals
                    click_all_show_more(page)

                    latitude,longitude = extract_coord(page)

                    # Extract all room & price
                    room_detials = extract_room_price(
                        page=page, 
                        hotel_name=hotel_name,
                        hotel_loc=hotel_loc,
                        list_facilities=list_facilities,
                        other_information = other_information,
                        latitude=latitude,
                        longitude=longitude,
                        extraction_date = start_date.strftime('%Y-%m-%d'),  # convert to string
                        effective_date = date.strftime('%Y-%m-%d')
                        )
                    
                    # room_detials.update(other_information)


                    list_hotel.extend(room_detials)

                    page.wait_for_timeout(5000)

            return list_hotel
        
        
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


    # print("============================== HASIL =============================")
    # print(list_hotel)
    