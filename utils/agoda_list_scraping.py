from playwright.sync_api import sync_playwright
from .visit_agoda_homepage import visit_agoda_homepage
from .search_agoda_homepage import search_agoda_homepage
from .apply_hotel_filter import apply_hotel_filter
from .scroll_and_navigate_all_results import scroll_and_navigate_all_results

import json
import os


def agoda_list_scraping(USER_AGENTS: dict, city_name: str = "", star_rating: str = "5", min_price: int = None, max_price: int = None,output_folder: str = 'jsons'):
    """
    Orchestrates the Agoda scraping process with filters for star rating and price range.
    
    Args:
        city_name: The city to search for
        star_rating: The star rating to filter by (e.g., "5", "4", "3")
        min_price: The minimum price to filter by (optional)
        max_price: The maximum price to filter by (optional)
        
    Returns:
        list: List of dictionaries containing hotel information that matches the criteria
    """
    hotel_results = []
    try:
        with sync_playwright() as p:
            # Initialize browser and visit Agoda homepage
            page, context, browser = visit_agoda_homepage(p, USER_AGENTS)
            print("="*50)
            print(page)
            print("="*50)

            # Ambil daftar halaman sebelum menjalankan search
            pages_before = context.pages
            print(f"Jumlah tab sebelum search: {len(pages_before)}")

            # Perform the search on the homepage
            with context.expect_page() as new_page_info:
                search_agoda_homepage(page, city_name)

            new_page = new_page_info.value

            html = new_page.content()
            with open("debug.html", "w", encoding="utf-8") as f:
                f.write(html)

            # 🔍 DEBUG (opsional): Simpan screenshot halaman
            new_page.screenshot(path="screenshots/debug.png", full_page=True)

            # Wait for the search results to load
            new_page.wait_for_selector('//div[@id="contentContainer"]', state="attached")
            
            # Apply star rating and price filters
            results_found = apply_hotel_filter(new_page, star_rating, min_price, max_price)
            print("="*50)
            print(f"Results found after applying filters: {results_found}")
            print("="*50)
            
            if results_found:
                # Scroll through all pages and navigate using the Next button
                # Also extract hotel information
                hotel_results = scroll_and_navigate_all_results(new_page, city_name, star_rating, min_price, max_price)
            else:
                hotel_results = []
                print("No results found after applying filters.")
            
            # Close the context and browser
            context.close()
            browser.close()
    except Exception as e:
        print(f"Error during Agoda scraping: {e}")
    
    # Save results to a JSON file
    output_filename = f"{city_name}_{star_rating}star_hotels.json"
    output_filename = os.path.join(output_folder, output_filename)
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(hotel_results, f, indent=4, ensure_ascii=False)
    print(f"Saved {len(hotel_results)} hotel results to {output_filename}")
    
    return hotel_results