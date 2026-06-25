from appium.webdriver.common.appiumby import AppiumBy

# Home Screen - Sleep Card
SLEEP_CARD = (AppiumBy.XPATH, '//android.view.View[contains(@content-desc,"Sleep")]')
SLEEP_SCORE_HOME = (AppiumBy.XPATH, '//android.widget.TextView[contains(@resource-id,"tvSleepScore")]')
SLEEP_DURATION_HOME = (AppiumBy.XPATH, '//android.widget.LinearLayout[contains(@resource-id,"lytSleepActual")]')

# Sleep Detail Screen Header
SLEEP_DETAIL_TITLE = (AppiumBy.XPATH, '//android.widget.TextView[contains(@text,"Sleep") and contains(@resource-id,"tvTitle")]')
BACK_BUTTON = (AppiumBy.XPATH, '//android.widget.ImageButton[@content-desc="Navigate up"]')

# Sleep Score & Duration
SLEEP_SCORE = (AppiumBy.XPATH, '//android.widget.TextView[contains(@resource-id,"tvSleepScore")]')
TOTAL_SLEEP_DURATION = (AppiumBy.XPATH, '//android.widget.TextView[contains(@resource-id,"tvTotalSleep")]')

# Sleep Stages
SLEEP_STAGES_SECTION = (AppiumBy.XPATH, '//android.view.View[contains(@resource-id,"sleepStagesContainer")]')
DEEP_SLEEP_DURATION = (AppiumBy.XPATH, '//android.widget.TextView[contains(@resource-id,"tvDeepSleep")]')
LIGHT_SLEEP_DURATION = (AppiumBy.XPATH, '//android.widget.TextView[contains(@resource-id,"tvLightSleep")]')
REM_SLEEP_DURATION = (AppiumBy.XPATH, '//android.widget.TextView[contains(@resource-id,"tvRemSleep")]')
AWAKE_TIME_DURATION = (AppiumBy.XPATH, '//android.widget.TextView[contains(@resource-id,"tvAwakeTime")]')

# Heart Rate During Sleep
HEART_RATE_SECTION = (AppiumBy.XPATH, '//android.view.View[contains(@resource-id,"heartRateSleepContainer")]')
AVG_HEART_RATE = (AppiumBy.XPATH, '//android.widget.TextView[contains(@resource-id,"tvAvgHeartRate")]')
MIN_HEART_RATE = (AppiumBy.XPATH, '//android.widget.TextView[contains(@resource-id,"tvMinHeartRate")]')
MAX_HEART_RATE = (AppiumBy.XPATH, '//android.widget.TextView[contains(@resource-id,"tvMaxHeartRate")]')

# Blood Oxygen (SpO2)
BLOOD_OXYGEN_SECTION = (AppiumBy.XPATH, '//android.view.View[contains(@resource-id,"spO2Container")]')
AVG_SPO2 = (AppiumBy.XPATH, '//android.widget.TextView[contains(@resource-id,"tvAvgSpO2")]')

# Sleep History / Trends
SLEEP_HISTORY_SECTION = (AppiumBy.XPATH, '//android.view.View[contains(@resource-id,"sleepHistoryContainer")]')
WEEKLY_SLEEP_CHART = (AppiumBy.XPATH, '//android.view.View[contains(@resource-id,"weeklyChart")]')
AVG_WEEKLY_SLEEP = (AppiumBy.XPATH, '//android.widget.TextView[contains(@resource-id,"tvAvgWeeklySleep")]')

# Sleep Tips
SLEEP_TIPS_SECTION = (AppiumBy.XPATH, '//android.view.View[contains(@resource-id,"sleepTipsContainer")]')
SLEEP_TIP_ITEM = (AppiumBy.XPATH, '//android.widget.TextView[contains(@resource-id,"tvSleepTip")]')

# Date Navigation
PREVIOUS_DAY_BUTTON = (AppiumBy.XPATH, '//android.widget.ImageButton[contains(@resource-id,"btnPreviousDay")]')
NEXT_DAY_BUTTON = (AppiumBy.XPATH, '//android.widget.ImageButton[contains(@resource-id,"btnNextDay")]')
SLEEP_DATE_LABEL = (AppiumBy.XPATH, '//android.widget.TextView[contains(@resource-id,"tvSleepDate")]')

# Sleep Navigation Tab (bottom nav)
SLEEP_TAB = (AppiumBy.XPATH, '//android.widget.ImageView[contains(@resource-id,"ivSleep")]')
SLEEP_SCREEN = (AppiumBy.XPATH, '//android.widget.TextView[contains(@resource-id,"tvTitle") and @text="Sleep"]')
SLEEP_SCORE  = (AppiumBy.XPATH, '(//android.widget.TextView[contains(@resource-id,"tvScore")])[1]')

