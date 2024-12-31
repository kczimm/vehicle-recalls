import argparse
import importlib

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('vehicles')
    
    args = parser.parse_args()

    options = Options()
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')  # Disable GPU acceleration for headless mode

    driver = webdriver.Chrome(options=options)

    try:
        if args.vehicles == 'rosen':
            from vehicles.rosen import get_vins
            vins = get_vins(driver)
        else:
            print(f"Error: vehicles '{args.vehicles}' not supported")
            return

        from recalls.ford import recall_from_vin

        print(vins)
        for vin in vins:
            print(vin)
            recall = recall_from_vin(driver, vin)        
            print(recall)

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
