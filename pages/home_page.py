from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class HomePage:
    URL = "http://localhost:8000"

    SEARCH_INPUT = (By.CSS_SELECTOR, '[data-testid="search-input-field"]')
    SEARCH_BUTTON = (By.CSS_SELECTOR, ".search-button")
    RESULTS_CONTAINER = (By.ID, "results")

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def load(self):
        self.driver.get(self.URL)

    def search(self, term: str):
        search_field = self.driver.find_element(*self.SEARCH_INPUT)
        search_field.send_keys(term)
        self.driver.find_element(*self.SEARCH_BUTTON).click()

    def is_search_result_present(self, term: str) -> bool:
        return term in self.driver.find_element(*self.RESULTS_CONTAINER).text
