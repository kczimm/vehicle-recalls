import json
import os

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

from vehicles.site1 import get_vehicles, save_to_file
from recalls.ford import recall_from_vin


def main():
    load_dotenv()

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-infobars',
                '--window-position=0,0',
                '--ignore-certifcate-errors',
                '--ignore-certifcate-errors-spki-list',
            ]
        )
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080},
            java_script_enabled=True,
        )
        page = context.new_page()
        page.set_extra_http_headers({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
        })
    
        page.set_viewport_size({"width": 1920, "height": 1080})

        try:
            zipcode = os.getenv('ZIPCODE')
            vehicles = get_vehicles(page, radius=20, zipcode=zipcode)
            save_to_file(vehicles)
            print(f"Scraped {len(vehicles)} vehicles successfully")
        except Exception as e:
            print(f"Error during scraping: {e}")
        finally:
            browser.close()


if __name__ == "__main__":
    main()
