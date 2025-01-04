from playwright.sync_api import sync_playwright
import json
import math
import time
from typing import List, Dict
import os


def get_total_pages(page) -> int:
    try:
        results_text = page.query_selector('.total-entries').text_content()
        if results_text:
            total_results = int(''.join(filter(str.isdigit, results_text)))
            return math.ceil(total_results / 100)  # 100 results per page
    except:
        return 1
    return 1


def remove_duplicates(vehicles: List[Dict]) -> List[Dict]:
    vins = []
    uniques = []
    for vehicle in vehicles:
        vin = vehicle["vin"]
        if vin not in vins:
            vins.append(vin)
            uniques.append(vehicle)
    return uniques


def get_vehicles(page, radius: int, zipcode: str) -> List[Dict]:
    page.set_extra_http_headers({
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
    })
    
    page.set_viewport_size({"width": 1920, "height": 1080})

    base_url = os.getenv("VEHICLES_SITE_1_URL")
    url = f"{base_url}?dealer_id=&keyword=&list_price_max=&list_price_min=&makes[]=ford&maximum_distance={radius}&mileage_max=&page_size=100&sort=listed_at_desc&stock_type=used&year_max=&year_min=&zip={zipcode}"
    
    page.goto(url, wait_until='domcontentloaded')
    total_pages = get_total_pages(page)
    print(f"Found {total_pages} pages to scrape")
    
    vehicles = []
    
    for page_num in range(1, total_pages + 1):
        try:
            current_url = f"{url}&page={page_num}"
            if page_num > 1:
                page.goto(current_url, wait_until='domcontentloaded')
            
            page.wait_for_selector('.vehicle-card', timeout=10000)
            cards = page.query_selector_all('.vehicle-card')
            
            print(f"Processing page {page_num}/{total_pages} - Found {len(cards)} vehicles")
            
            for card in cards:
                try:
                    vin_element = card.query_selector('[data-vin]')
                    if vin_element:
                        vin = vin_element.get_attribute('data-vin')
                        dealer_element = card.query_selector('.dealer-name')
                        model_element = card.query_selector('.title')
                        
                        vehicles.append({
                            'vin': vin,
                            'model': model_element.text_content().strip() if model_element else 'N/A',
                            'dealer': dealer_element.text_content().strip() if dealer_element else 'N/A'
                        })

                except Exception as e:
                    print(f"Error processing vehicle: {e}")
                    continue
            
            time.sleep(1)  # Delay between pages
            
        except Exception as e:
            print(f"Error processing page {page_num}: {e}")
            continue

    vehicles = remove_duplicates(vehicles)
    
    return vehicles


def save_to_file(vehicles: List[Dict], filename: str = 'vehicles_site1.json'):
    with open(filename, 'w') as f:
        json.dump(vehicles, f, indent=2)


def main():
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
