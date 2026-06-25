from pages.base_page import BasePage
import allure

class HomePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.homepage_locator = self.get_locators().HOME_PAGE

    def verify_home_page(self):
        self.waits.wait_for_presence(self.driver, self.homepage_locator.HOME_PAGE_ELEMENT )  
        self.capture_screenshot(name='HomePage')
