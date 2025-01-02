from playwright.sync_api import Page, expect

from vehicles.rosen import get_vins


def test_vehicle_information(page: Page):
    page.set_extra_http_headers({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"})
    vins = get_vins(page)
    assert len(vins) > 0
