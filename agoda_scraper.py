import json

from utils import agoda_list_scraping

# Define user-agents specific to each browser
with open('user_agents.json') as f:
    USER_AGENTS = json.load(f)
    

if __name__ == "__main__":
    hotels = agoda_list_scraping(
        city_name='batam island', 
        star_rating="4", 
        USER_AGENTS=USER_AGENTS
        # min_price=20,  # Example minimum price
        # max_price=30,  # Example maximum price
    )
    
    # Print a summary of the results
    if hotels:
        print(f"\nFound {len(hotels)} hotels matching the criteria:")
        for i, hotel in enumerate(hotels[:5], 1):
            print(f"{i}. {hotel['hotel_name']} - ${hotel['hotel_price']} - {hotel['hotel_rating']} stars")
        
        if len(hotels) > 5:
            print(f"...and {len(hotels) - 5} more hotels")