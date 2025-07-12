def extract_helpful_fact(page):
    info = {}

    info_loc = page.locator('div[data-element-name="about-hotel-useful-info"]')
    div_child = info_loc.locator(":scope > div")
    
    for i in range(div_child.count()):
        content_tittle = div_child.nth(i).locator('h5').text_content()
        content = div_child.nth(i).locator('li')
        data = []
        for y in range(content.count()):
            get_info = content.nth(y).text_content()
            data.append(get_info)

        info[content_tittle] = data

    print(info)
    return info