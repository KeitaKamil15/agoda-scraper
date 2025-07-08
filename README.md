# Agoda Scraping

This project is an improvement and further development of an open-source project originally from [this repository](https://github.com/rukshar69/hotel-scraper). Several features have been updated, added, or optimized to suit specific needs.


## 🚀 How to Run This Project

Follow the steps below to run the project locally:

### 1. Clone This Repository

```bash
git clone https://github.com/SundayBPM/agoda-scraper.git
cd agoda-scraper
```
### 2. Creating & activating a Python Virtual Environment (Optional)
To ensure a clean and isolated environment for your project, we recommend creating a Python virtual environment. This can be done using the venv module, which comes bundled with Python 3.

```bash
# Create a new virtual environment
python3 -m venv venv
```
This will create a new directory named venv in your project directory, which will contain the virtual environment.

To activate the virtual environment, run the following command:
```bash
# On Linux/Mac
source venv/bin/activate
```
You should now see the name of the virtual environment printed on your command line, indicating that it is active.

### 3. Installing Required Libraries
Once the virtual environment is activated, you can install the required libraries using the requirements.txt file.
```bash
pip install -r requirements.txt
```
This will install all the libraries listed in the requirements.txt file, making them available for your project.

### 4. Installing Required Libraries
The following command will install the required browsers.

```bash
playwright install --with-deps
```
It does two things:

1️⃣ Installs browser binaries (Chromium, Firefox, WebKit) required by Playwright.
2️⃣ Installs system dependencies (needed for browsers to run properly, especially on Linux).

### 5. Running the Script
There are two main scripts in this project:
> 🏨 agoda_scraper.py

Use this script to scrape a list of hotels based on your desired search criteria (location, dates, etc.).

Example:
```bash
python agoda_scraper.py
```
This script will generate a list of hotel links, typically saved into a file jsons/hotels_list.json.


> 🛏️ scrape_hotel_details.py

After obtaining the hotel list, use this script to extract detailed information from each hotel, such as:

* Facilities
* Pricing
* Room types
* Promotions

Example:
```bash
python scrape_hotel_details.py
```
Make sure that the list file generated from the first script is available and correctly referenced in this second script.

## 🤝 Credits
Thanks to rukshar69/hotel-scraper for the original foundation of this project.