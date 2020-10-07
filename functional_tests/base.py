from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Chrome("chromedriver.exe")
        self.browser.implicitly_wait(3)
        self.server_url = 'https://localhost:8000'

    def tearDown(self) -> None:
        self.browser.refresh()
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])
