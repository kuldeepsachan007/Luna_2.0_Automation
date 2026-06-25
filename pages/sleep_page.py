from pages.base_page import BasePage
from utility.liberaries.decorators import logger


class SleepPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.name = "Sleep Page"
        self.locator = self.get_locators().SLEEP_PAGE

    # ── Home Screen ──────────────────────────────────────────────────────────

    def tap_sleep_button(self):
        self.mouse.click(self.driver, self.locator.SLEEP_TAB)
        self.capture_screenshot("Sleep_Button_Tapped")

    def verify_sleep_score_on_home(self):
        sleep_score = self.forms.get_value(self.driver, self.locator.SLEEP_SCORE)
        assert sleep_score is not None and sleep_score != "", "Sleep score is not visible on home screen"
        self.capture_screenshot("Sleep_Score_Home_Visible")

    def verify_sleep_duration_on_home(self):
        duration = self.forms.get_value(self.driver, self.locator.SLEEP_DURATION_HOME)
        assert duration is not None and duration != "", "Sleep duration is not visible on home screen"
        self.capture_screenshot("Sleep_Duration_Home_Visible")

    def tap_sleep_card(self):
        self.mouse.click(self.driver, self.locator.SLEEP_CARD)
        self.capture_screenshot("Sleep_Card_Tapped")

    # ── Sleep Detail Screen ──────────────────────────────────────────────────

    def verify_sleep_detail_screen(self):
        actual_title = self.forms.get_value(self.driver, self.locator.SLEEP_DETAIL_TITLE)
        assert actual_title is not None and "Sleep" in actual_title, \
            f"Sleep detail screen not displayed. Got: '{actual_title}'"
        self.capture_screenshot("Sleep_Detail_Screen_Visible")

    def verify_total_sleep_duration(self):
        duration = self.forms.get_value(self.driver, self.locator.TOTAL_SLEEP_DURATION)
        assert duration is not None and duration != "", "Total sleep duration not visible"
        self.capture_screenshot("Total_Sleep_Duration_Visible")

    def verify_sleep_score(self):
        score = self.forms.get_value(self.driver, self.locator.SLEEP_SCORE)
        assert score is not None and score != "", "Sleep score not visible on detail screen"
        self.capture_screenshot("Sleep_Score_Visible")

    # ── Sleep Stages ─────────────────────────────────────────────────────────

    def verify_sleep_stages_section(self):
        self.waits.wait_for_element_visible(self.driver, self.locator.SLEEP_STAGES_SECTION)
        self.capture_screenshot("Sleep_Stages_Section_Visible")

    def verify_deep_sleep_duration(self):
        duration = self.forms.get_value(self.driver, self.locator.DEEP_SLEEP_DURATION)
        assert duration is not None and duration != "", "Deep sleep duration not visible"
        self.capture_screenshot("Deep_Sleep_Duration_Visible")

    def verify_light_sleep_duration(self):
        duration = self.forms.get_value(self.driver, self.locator.LIGHT_SLEEP_DURATION)
        assert duration is not None and duration != "", "Light sleep duration not visible"
        self.capture_screenshot("Light_Sleep_Duration_Visible")

    def verify_rem_sleep_duration(self):
        duration = self.forms.get_value(self.driver, self.locator.REM_SLEEP_DURATION)
        assert duration is not None and duration != "", "REM sleep duration not visible"
        self.capture_screenshot("REM_Sleep_Duration_Visible")

    def verify_awake_time_duration(self):
        duration = self.forms.get_value(self.driver, self.locator.AWAKE_TIME_DURATION)
        assert duration is not None and duration != "", "Awake time duration not visible"
        self.capture_screenshot("Awake_Time_Duration_Visible")

    # ── Heart Rate ────────────────────────────────────────────────────────────

    def scroll_to_heart_rate_section(self):
        self.gesture_control.scroll_to_element(self.driver, self.locator.HEART_RATE_SECTION)
        self.capture_screenshot("Heart_Rate_Section_Visible")

    def verify_avg_heart_rate(self):
        value = self.forms.get_value(self.driver, self.locator.AVG_HEART_RATE)
        assert value is not None and value != "", "Average heart rate not visible"
        self.capture_screenshot("Avg_Heart_Rate_Visible")

    def verify_min_heart_rate(self):
        value = self.forms.get_value(self.driver, self.locator.MIN_HEART_RATE)
        assert value is not None and value != "", "Minimum heart rate not visible"
        self.capture_screenshot("Min_Heart_Rate_Visible")

    def verify_max_heart_rate(self):
        value = self.forms.get_value(self.driver, self.locator.MAX_HEART_RATE)
        assert value is not None and value != "", "Maximum heart rate not visible"
        self.capture_screenshot("Max_Heart_Rate_Visible")

    # ── SpO2 ──────────────────────────────────────────────────────────────────

    def scroll_to_blood_oxygen_section(self):
        self.gesture_control.scroll_to_element(self.driver, self.locator.BLOOD_OXYGEN_SECTION)
        self.capture_screenshot("SpO2_Section_Visible")

    def verify_avg_spo2(self):
        value = self.forms.get_value(self.driver, self.locator.AVG_SPO2)
        assert value is not None and value != "", "Average SpO2 level not visible"
        self.capture_screenshot("Avg_SpO2_Visible")

    # ── Sleep History ─────────────────────────────────────────────────────────

    def scroll_to_sleep_history_section(self):
        self.gesture_control.scroll_to_element(self.driver, self.locator.SLEEP_HISTORY_SECTION)
        self.capture_screenshot("Sleep_History_Section_Visible")

    def verify_weekly_sleep_trend(self):
        self.waits.wait_for_element_visible(self.driver, self.locator.WEEKLY_SLEEP_CHART)
        self.capture_screenshot("Weekly_Sleep_Chart_Visible")

    def verify_avg_weekly_sleep(self):
        value = self.forms.get_value(self.driver, self.locator.AVG_WEEKLY_SLEEP)
        assert value is not None and value != "", "Average weekly sleep duration not visible"
        self.capture_screenshot("Avg_Weekly_Sleep_Visible")

    # ── Sleep Tips ────────────────────────────────────────────────────────────

    def scroll_to_sleep_tips_section(self):
        self.gesture_control.scroll_to_element(self.driver, self.locator.SLEEP_TIPS_SECTION)
        self.capture_screenshot("Sleep_Tips_Section_Visible")

    def verify_sleep_tip_present(self):
        tip = self.forms.get_value(self.driver, self.locator.SLEEP_TIP_ITEM)
        assert tip is not None and tip != "", "No sleep tip/recommendation is visible"
        self.capture_screenshot("Sleep_Tip_Visible")

    # ── Navigation ────────────────────────────────────────────────────────────

    def tap_back_button(self):
        self.mouse.click(self.driver, self.locator.BACK_BUTTON)
        self.capture_screenshot("Back_Button_Tapped")

    def navigate_to_previous_day(self):
        self.mouse.click(self.driver, self.locator.PREVIOUS_DAY_BUTTON)
        self.capture_screenshot("Previous_Day_Sleep_Loaded")

    def navigate_to_next_day(self):
        self.mouse.click(self.driver, self.locator.NEXT_DAY_BUTTON)
        self.capture_screenshot("Next_Day_Sleep_Loaded")

    def verify_sleep_data_visible(self):
        self.waits.wait_for_element_visible(self.driver, self.locator.SLEEP_SCORE)
        self.capture_screenshot("Sleep_Data_Visible")
