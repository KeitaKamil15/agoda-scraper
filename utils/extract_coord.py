import re


def extract_coord(page):
    
    maps_loc = page.locator('div.MapCompact')
    maps_loc.click()

    coor_loc = page.locator('a[title="Open this area in Google Maps (opens a new window)"]')
    coor = coor_loc.get_attribute('href')

    match = re.search(r'll=([-\d.]+),([-\d.]+)', coor)
    if match:
        print('mengambil latite dan longtitude')
        latitude = match.group(1)
        longitude = match.group(2)

    page.locator('button[data-component="hotelMap-modal-close"]').click()

    return latitude,longitude



