from playwright.sync_api import Page

def submit_vin(page: Page, vin):
    page.goto('https://www.ford.com/support/recalls')
    page.get_by_placeholder('Enter Your 17-digit Ford VIN').fill(vin)
    page.get_by_test_id('vin-submit-button').click()    


def get_vehicle_information(page: Page):
    vehicle = page.locator('.vehicle-information-ym')
    return vehicle.text_content()


def recall_campaigns(page: Page):
    campaigns = []

    recalls_heading = page.locator(".recalls-section-heading h2").nth(0)

    heading_text = recalls_heading.inner_text()

    if heading_text == "Recalls *":
        label = page.get_by_text("Campaign/NHTSA#")
        sibling_div = label.locator(" + div")
        campaign = sibling_div.inner_text()
        campaigns.append(campaign)

    return campaigns
    

def recall_from_vin(page: Page, vin):
    submit_vin(page, vin)

    recall = dict()

    recall["vehicle"] = get_vehicle_information(page)
    recall["campaigns"] = recall_campaigns(page)

    return recall
