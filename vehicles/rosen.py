from playwright.sync_api import Page
import time


def click_next_link(page: Page):
    next_page_link = page.get_by_test_id('pagination-next-link')
    is_disabled = next_page_link.get_attribute('disabled') == 'true'

    if not is_disabled:
        next_page_link.click()
        time.sleep(1)

    return is_disabled


def get_vins(page: Page):
    # Navigate to the Rosen Automotive website
    page.goto('https://www.rosenautomotive.com/used-vehicles/?_dFR%5Bmake%5D%5B0%5D%3DFord')

    vins = []

    while True:
        vin_rows = page.query_selector_all('div.vin-row')

        for row in vin_rows:
            vin = row.inner_text().split(' ')[-1]
            vins.append(vin)

        done = click_next_link(page)

        if done:
            break

    return vins
