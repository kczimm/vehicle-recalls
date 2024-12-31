from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def recall_campaigns(driver):
    # Wait for all buttons with class "accordian-header" to be present
    accordian_headers = WebDriverWait(driver, 3).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "accordion-header"))
    )

    campaigns = []
    for i, header in enumerate(accordian_headers, 1):
        try:
            # Wait for each button to be clickable before clicking
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable(header))
            header.click()
            # Add a small delay to allow for animations or JS to update the page
            time.sleep(0.5)  # Adjust this delay as needed based on the website's behavior

            content = WebDriverWait(driver, 3).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "support-accordion-description-content"))
            )
            campaign = content[0].text
            print(campaign)
            campaigns.append(campaign)
            
        except Exception as e:
            print(f"Failed to click button {i}: {e}")

    return campaigns


def submit_vin(driver, vin):
    driver.get('https://www.ford.com/support/recalls')

    wait = WebDriverWait(driver, 1)
    vin_field = wait.until(
        EC.presence_of_element_located((By.ID, "vin-field-vin-selector-label"))
    )
    # vin_field = driver.find_element(By.ID, "vin-field-vin-selector-label")
    vin_field.send_keys(vin)

    submit_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Search']"))
    )
    submit_button.click()
    time.sleep(1)


def get_vehicle_information(driver):
    # Assumes we have already submitted the VIN    
    with open('page_source.html', 'w', encoding='utf-8') as file:
        file.write(driver.page_source)
    vehicle = WebDriverWait(driver, 1).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "vehicle-information-ym"))
    )[0]
    return vehicle.text


def recall_from_vin(driver, vin):
    submit_vin(driver, vin)

    recall = dict()

    recall["vehicle"] = get_vehicle_information(driver)
    recall["campaigns"] = recall_campaigns(driver)

    return recall
