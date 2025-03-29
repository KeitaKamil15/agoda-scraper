Some screenshots of the UI are provided in the **screenshots** folder.
Demo video is provided in the **[demo.mp4](https://youtu.be/J8MO0kXbmws)**

# Playwright vs Scrapy

The scraping of hotel info. is done in Playwright. For JavaScript-heavy websites like Booking.com & Agoda, Playwright is the better choice. Here's why:

    Handles JavaScript Execution: Playwright can interact with dynamically loaded content, ensuring you scrape fully rendered data.

    Efficient Scrolling & Pagination: It supports automated scrolling and clicking "Load More" buttons to fetch additional hotel listings.

    Easier Search Input Handling: You can directly fill in search fields and submit forms as a real user would.

    Headless & Fast Execution: Playwright can run in headless mode for better performance.

    Better User Experience: Playwright simulates a real user's interaction, providing a better user experience.

    Since no deep crawling is required, it's easier to code than Scrapy. Scrapy requires a whole project for deep crawling. But in Playwright, you can use a single script for scraping, browsing & interaction.

When to Use Scrapy?

    If Booking.com & Agoda had a predictable API or loaded data without JavaScript.

    If the content was available in the initial HTML response.

**Since Booking.com & Agoda dynamically load hotel listings with JavaScript, Playwright is the way to go.**

# Setting Up a Python Virtual Environment and Installing Libraries

## Creating a Python Virtual Environment

To ensure a clean and isolated environment for your project, we recommend creating a Python virtual environment. This can be done using the `venv` module, which comes bundled with Python 3.

```bash
# Navigate to your project directory
cd /path/to/your/project

# Create a new virtual environment
python3 -m venv venv
```

This will create a new directory named **venv** in your project directory, which will contain the virtual environment.

## Activating the Virtual Environment

To activate the virtual environment, run the following command:

```bash
# On Linux/Mac
source venv/bin/activate
```

You should now see the name of the virtual environment printed on your command line, indicating that it is active.

## Installing Required Libraries

Once the virtual environment is activated, you can install the required libraries using the **requirements.txt** file.

```bash
pip install -r requirements.txt
```

This will install all the libraries listed in the **requirements.txt** file, making them available for your project.

## Install Playwright Browsers

I have used Chrome and Firefox for the simulation and scraping. So, the following command will install the required browsers.

The command:  
```sh
playwright install --with-deps
```  
It does two things:  

1️⃣ **Installs browser binaries** (Chromium, Firefox, WebKit) required by Playwright.  
2️⃣ **Installs system dependencies** (needed for browsers to run properly, especially on Linux).  

This is useful when setting up Playwright in a fresh environment or when running it in a container.

## Deactivating the Virtual Environment

To deactivate the virtual environment, run the following command:

```bash
deactivate
```

This will exit the virtual environment and return to the default environment.

# Running the Application

To run the application, navigate to the project directory (that contains the **app** folder) and run the following command:

```bash
uvicorn app.main:app --reload
```

This will start the FastAPI application, which will listen on port 8000 by default. So, open a browser and navigate to http://localhost:8000 to access the application.

# Running Scraping Scripts

To run the scraping scripts, navigate to the project directory: **playwright_scraper**. Folder **agoda** contains the scraping scripts for Agoda and **booking** contains the scraping scripts for Booking (uses **Playwright**). 

For the **agoda** folder, run the following command inside the **agoda** folder:

```bash
python agoda_scraper.py
```

For the **booking** folder, run the following command inside the **booking** folder:

```bash
python booking_scraper.py
```

To retrieve the list of hotel info. for booking.com(uses **BeautifulSoup**) run the following command inside the **booking** folder:

```bash
python booking_hotel_info_retriver.py
```

# Database Setup(Using Docker)

To set up the database using Docker, navigate to the project directory's **postgres** folder and run the following command:

```bash
docker-compose up -d
```

This will start the Docker containers for the database. The docker compose file contains the necessary credentials.

Note: Docker desktop is required to run the docker containers.