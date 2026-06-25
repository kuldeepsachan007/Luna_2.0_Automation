from appium.webdriver.common.appiumby import AppiumBy


# Activity button on home page bottom nav
ACTIVITY_BUTTON = (AppiumBy.XPATH, '//android.widget.ImageView[contains(@resource-id,"ivActivity")]')

# Activity Score button
ACTIVITY_SCORE_BUTTON = (AppiumBy.XPATH, '//android.view.ViewGroup[contains(@resource-id,"lytScore")]')

# Back arrow button
BACK_BUTTON = (AppiumBy.XPATH, '//android.widget.ImageButton[@content-desc="Back Button"]')

# Goal Progress button
GOAL_PROGRESS_BUTTON = (AppiumBy.XPATH, '//android.view.ViewGroup[contains(@resource-id,"lytSec1")]')

# Total Calories button
TOTAL_CALORIES_BUTTON = (AppiumBy.XPATH, '//android.view.ViewGroup[contains(@resource-id,"lytSec2")]')

# Steps button
STEPS_BUTTON = (AppiumBy.XPATH, '//android.view.ViewGroup[contains(@resource-id,"lytSec3")]')

# Distance button
DISTANCE_BUTTON = (AppiumBy.XPATH, '//android.view.ViewGroup[contains(@resource-id,"lytSec4")]')

# Get Started button (appears after tapping Activity for first time)
GET_STARTED_BUTTON = (AppiumBy.XPATH, '//android.widget.Button[contains(@resource-id,"bGoToSettings")]')
