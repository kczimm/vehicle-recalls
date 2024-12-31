import unittest
from recalls.ford import recall_from_vin, submit_vin, get_vehicle_information, recall_campaigns
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class TestFordRecalls(unittest.TestCase):
    def setUp(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')  # Disable GPU acceleration for headless mode
        options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"')
        self.driver = webdriver.Chrome(options=options)
        self.vin = 'MAJ3S2GE0KC267392'

    def tearDown(self):
        self.driver.quit()

    def test_vehicle_information(self):
        submit_vin(self.driver, self.vin)
        vehicle = get_vehicle_information(self.driver)
        self.assertEqual(vehicle, "2019 EcoSport")

    def test_recall_campaigns(self):
        submit_vin(self.driver, self.vin)
        campaigns = recall_campaigns(self.driver)
        self.assertEqual(len(campaigns), 1)
        self.assertEqual(campaigns[0], "23S64/23V905")


if __name__ == '__main__':
    unittest.main()
