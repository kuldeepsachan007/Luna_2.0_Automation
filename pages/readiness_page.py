import time
from pages.base_page import BasePage


class ReadinessPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.name = "Readiness Page"
        self.locator = self.get_locators().READINESS_PAGE

    def click_readiness_button(self):
        el = self.mouse.find_element(self.driver, self.locator.READINESS_BUTTON)
        self.gesture_control.tap(self.driver, element=el)
        time.sleep(5)
        self.capture_screenshot("Readiness_Button_Clicked")

    def click_get_started_button(self):
        self.mouse.click(self.driver, self.locator.GET_STARTED_BUTTON)
        time.sleep(5)
        self.capture_screenshot("Readiness_Get_Started_Clicked")

    def click_readiness_score(self):
        self.mouse.click(self.driver, self.locator.READINESS_SCORE_BUTTON)
        time.sleep(5)
        self.capture_screenshot("Readiness_Score_Clicked")

    def click_back_button(self):
        self.mouse.click(self.driver, self.locator.BACK_BUTTON)
        time.sleep(5)
        self.capture_screenshot("Back_Button_Clicked")

    def click_resting_heart_rate(self):
        self.mouse.click(self.driver, self.locator.RESTING_HEART_RATE_BUTTON)
        time.sleep(5)
        self.capture_screenshot("Resting_Heart_Rate_Clicked")

    def click_hrv(self):
        self.mouse.click(self.driver, self.locator.HRV_BUTTON)
        time.sleep(5)
        self.capture_screenshot("HRV_Clicked")

    def click_skin_temp(self):
        self.mouse.click(self.driver, self.locator.SKIN_TEMP_BUTTON)
        time.sleep(5)
        self.capture_screenshot("Skin_Temp_Clicked")

    def click_respiratory_rate(self):
        self.mouse.click(self.driver, self.locator.RESPIRATORY_RATE_BUTTON)
        time.sleep(5)
        self.capture_screenshot("Respiratory_Rate_Clicked")
