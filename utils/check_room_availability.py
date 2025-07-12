from .change_date_book import change_date_book

def check_room_availability(page):
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