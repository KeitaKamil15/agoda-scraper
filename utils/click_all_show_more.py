def click_all_show_more(page):
    while True:
        show_button = page.locator('div[data-element-name="room-grid-show-more"]')
        # print('show_button = ',show_button)
        print('Jumlah show_button yang muncul = ',show_button.count())

        if show_button.count() == 0:
            print("Sudah tidak ada show more button lagi!!....")
            break
        show_button.first.click()
        page.wait_for_timeout(500)