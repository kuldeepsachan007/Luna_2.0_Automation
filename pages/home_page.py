from pages.base_page import BasePage
from utility.liberaries.decorators import logger
import allure

class HomePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.homepage_locator = self.get_locators().HOME_PAGE

    def verify_home_page(self):
        self.waits.wait_for_presence(self.driver, self.homepage_locator.HOME_PAGE_ELEMENT )
        self.capture_screenshot(name='HomePage')

    def go_to_home_page(self):
        """Ensure the app is on the Home page, wherever it currently is. If it
        is not already on Home (e.g. left on a detail page from a prior run),
        relaunch the app — noReset keeps the session logged in, so it returns to
        the Home tab."""
        if self.forms.is_element_displayed(
            self.driver, self.homepage_locator.HOME_PAGE_ELEMENT, timeout=3,
        ):
            self.capture_screenshot(name='HomePage')
            return
        pkg = self.driver.current_package or "com.noisefit.luna.dev"
        logger.info("Not on Home; relaunching %s to return to the Home page", pkg)
        try:
            self.driver.terminate_app(pkg)
            self.driver.activate_app(pkg)
        except Exception as e:
            logger.warning("Could not relaunch app to Home: %s", e)
        self.waits.wait_for_presence(
            self.driver, self.homepage_locator.HOME_PAGE_ELEMENT, timeout=20,
        )
        self.capture_screenshot(name='HomePage')
