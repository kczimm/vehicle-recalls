import argparse
import importlib

from playwright.sync_api import sync_playwright

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('vehicles')
    
    args = parser.parse_args()


    with sync_playwright() as p:
        # Channel can be "chrome", "msedge", "chrome-beta", "msedge-beta" or "msedge-dev".
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.set_extra_http_headers({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"})

        if args.vehicles == 'rosen':
            from vehicles.rosen import get_vins
            vins = get_vins(page)
        else:
            print(f"Error: vehicles '{args.vehicles}' not supported")
            return

        from recalls.ford import recall_from_vin

        for vin in vins:
            print(vin)
            try:
                recall = recall_from_vin(page, vin)        
            except:
                print('failed')
                continue
            if len(recall["campaigns"]) > 0:
                print(recall)



if __name__ == "__main__":
    main()
