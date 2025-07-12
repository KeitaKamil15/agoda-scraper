def extract_room_type(page, hotel_name, hotel_loc, list_facilities, other_information):
    rooms = []

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
            room_data = {
            "hotel_name" : hotel_name,
            "address" : hotel_loc,
            "room_type" : type_room_name,
            "room size" : room_size,
            "price" : price,
            "Benefit" : benefit
            }

            # tambahkan list fasilitas 
            room_data.update(list_facilities)
            room_data.update(other_information)

            # hasil scraping di array
            rooms.append(room_data)
    return rooms