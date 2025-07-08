import json

from utils import extract_hotel_detail

with open('jsons/batam island_5star_hotels.json', 'r') as file:
    hotels = json.load(file)

with open('user_agents.json') as f:
    USER_AGENTS = json.load(f)

print(len(hotels))

if __name__ == "__main__":
    # hotel_details = extract_hotel_detail(
    #         link = "https://www.agoda.com/ibis-styles-batam-nagoya/hotel/batam-island-id.html?countryId=192&finalPriceView=1&isShowMobileAppPrice=false&cid=-1&numberOfBedrooms=&familyMode=false&adults=2&children=0&rooms=1&maxRooms=0&isCalendarCallout=false&childAges=&numberOfGuest=0&missingChildAges=false&travellerType=1&showReviewSubmissionEntry=false&currencyCode=IDR&isFreeOccSearch=false&los=2&searchrequestid=7579bc5c-ff23-4f50-ab2f-1297340af23c&checkin=2025-07-10",
    #         USER_AGENTS = USER_AGENTS
    #     )
    
    list_hotel = []
    # time = 0
    for hotel in hotels:
        # time += 1
        # if time == 2:
        #     break
        print(f'Extract {hotel['hotel_name']}')
        hotel_details = extract_hotel_detail(
            # p = p,
            link = hotel['booking_url'],
            USER_AGENTS = USER_AGENTS
        )

        list_hotel.extend(hotel_details)
    
    # print(list_hotel)
    output_json = "jsons/batam island_5star_hotels_detail.json"

    try:
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(list_hotel, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Terjadi error saat menyimpan file jason {e}")