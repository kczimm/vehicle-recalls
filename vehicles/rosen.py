from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


def close_cookie_banner(driver, timeout=2):
    """
    Attempts to close a cookie banner by clicking the 'Allow all cookies' button
    
    Args:
        driver: Selenium WebDriver instance
        timeout: Maximum time to wait for button in seconds
    """
    try:
        # Try multiple common selectors for cookie consent buttons
        selectors = [
            "//button[contains(text(), 'Allow all cookies')]",
            "//button[contains(text(), 'Accept all')]",
            "//button[contains(@class, 'accept-cookies')]",
            "//*[contains(text(), 'Allow all cookies')]"
        ]
        
        for selector in selectors:
            try:
                button = WebDriverWait(driver, timeout).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                button.click()
                return True
            except TimeoutException:
                continue
                
        raise TimeoutException("Could not find cookie consent button")
        
    except Exception as e:
        print(f"Error closing cookie banner: {str(e)}")
        return False


def click_next_link(driver, timeout=2):
    """
    Scrolls to bottom and clicks link with rel="next"
    
    Args:
        driver: Selenium WebDriver instance
        timeout: Maximum time to wait for link in seconds
    """
    try:
        # Scroll to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)  # Allow time for any dynamic content to load
        
        # Find and click the next link
        next_page_link = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[rel="next"]'))
        )

        # Get fresh reference to element and click
        next_link = driver.find_element(By.CSS_SELECTOR, 'a[rel="next"]')
        is_disabled = 'disabled' in next_page_link.get_attribute('class') or next_page_link.get_attribute('disabled') == 'true'

        if is_disabled:
            return True
        else:   
            next_page_link.click()
            time.sleep(1)
            return False
        
    except Exception as e:
        print(f"Error clicking next link: {str(e)}")
        return True


def get_vins(driver):
    # Navigate to the Rosen Automotive website
    driver.get('https://www.rosenautomotive.com/used-vehicles/?_dFR%5Bmake%5D%5B0%5D%3DFord')

    close_cookie_banner(driver)

    # Gather contents of each "vin-row" div into a list
    vins = []

    while True:
        # Wait for the divs with class "vin-row" to load
        vin_rows = WebDriverWait(driver, 2).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "vin-row"))
        )

        for row in vin_rows:
            # Get the text content of each div
            vin = row.text.split(' ')[-1]
            vins.append(vin)

        done = click_next_link(driver)

        if done:
            break

    return vins
