from playwright.sync_api import Page, expect

from recalls.ford import get_vehicle_information, submit_vin, recall_campaigns


def test_vehicle_information(page: Page):
    page.set_extra_http_headers({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"})
    vin = 'MAJ3S2GE0KC267392'
    submit_vin(page, vin)
    vehicle = get_vehicle_information(page)
    assert vehicle, '2019 EcoSport'


def test_vehicle_with_no_recalls(page: Page):
    page.set_extra_http_headers({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"})
    vin = '1FMCU9J90HUD57021'
    submit_vin(page, vin)
    campaigns = recall_campaigns(page)
    assert len(campaigns) == 0


def test_vehicle_with_one_recalls(page: Page):
    page.set_extra_http_headers({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"})
    vin = '3FTTW8A37RRB83347'
    submit_vin(page, vin)
    campaigns = recall_campaigns(page)
    assert len(campaigns) > 0
    assert campaigns[0] == '24S59/24V684'


def test_vehicle_with_more_than_one_recalls(page: Page):
    pass
