from pprint import pprint

def extract_amenities_facilities(page):
    print("================================================")
    data = {}
    facilities = page.locator('div[data-element-name="abouthotel-amenities-facilities"]').locator('div.Box-sc-kv6pi1-0.cTxLvk.FeatureGroup').first

    # Hanya mengambil elemen induk/tingkat pertama saja
    type_faci = facilities.locator(":scope > div.Box-sc-kv6pi1-0.dtSdUZ")
    # print('jumlah elemen',type_faci.count())

    # looping berdasarkan jumlah jenis/kategori fasilitas
    for i in range(type_faci.count()):
        # Mengambil nama jenis/kategori fasilitas
        type_facilities_name = type_faci.nth(i).locator('h5').text_content()
        list_faci = []

        # melakukan looping berdasarkan jumlah fasilitas
        for y in range(type_faci.nth(i).locator('li').count()):
            # Mengambil nama fasilitas
            facilities_name = type_faci.nth(i).locator('li').nth(y).text_content()
            # menyimpan nama fasilitas di list
            list_faci.append(facilities_name)

        # Membuat record baru tentang jenis dan fasilitasnya
        data[type_facilities_name] = list_faci
    # pprint(data, sort_dicts=False)
    print("================================================")

    # return data,page
    return data