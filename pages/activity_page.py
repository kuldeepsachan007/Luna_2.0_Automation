import time
from pages.base_page import BasePage


class ActivityPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.name = "Activity Page"
        self.locator = self.get_locators().ACTIVITY_PAGE

    def click_activity_button(self):
        el = self.mouse.find_element(self.driver, self.locator.ACTIVITY_BUTTON)
        self.gesture_control.tap(self.driver, element=el)
        time.sleep(5)
        self.capture_screenshot("Activity_Button_Clicked")

    def click_get_started_button(self):
        self.mouse.click(self.driver, self.locator.GET_STARTED_BUTTON)
        time.sleep(5)
        self.capture_screenshot("Activity_Get_Started_Clicked")

    def click_activity_score(self):
        self.mouse.click(self.driver, self.locator.ACTIVITY_SCORE_BUTTON)
        time.sleep(5)
        self.capture_screenshot("Activity_Score_Clicked")

    def click_back_button(self):
        self.mouse.click(self.driver, self.locator.BACK_BUTTON)
        time.sleep(5)
        self.capture_screenshot("Back_Button_Clicked")

    def click_goal_progress(self):
        self.mouse.click(self.driver, self.locator.GOAL_PROGRESS_BUTTON)
        time.sleep(5)
        self.capture_screenshot("Goal_Progress_Clicked")

    def click_total_calories(self):
        self.mouse.click(self.driver, self.locator.TOTAL_CALORIES_BUTTON)
        time.sleep(5)
        self.capture_screenshot("Total_Calories_Clicked")

    def click_steps(self):
        self.mouse.click(self.driver, self.locator.STEPS_BUTTON)
        time.sleep(5)
        self.capture_screenshot("Steps_Clicked")

    def click_distance(self):
        self.mouse.click(self.driver, self.locator.DISTANCE_BUTTON)
        time.sleep(5)
        self.capture_screenshot("Distance_Clicked")
