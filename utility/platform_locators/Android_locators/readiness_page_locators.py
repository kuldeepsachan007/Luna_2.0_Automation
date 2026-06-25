from appium.webdriver.common.appiumby import AppiumBy


# Readiness button on home page bottom nav
READINESS_BUTTON = (AppiumBy.XPATH, '//android.widget.ImageView[contains(@resource-id,"ivReadiness")]')

# Get Started button (appears after tapping Readiness for first time)
GET_STARTED_BUTTON = (AppiumBy.XPATH, '//android.widget.Button[contains(@resource-id,"bGoToSettings")]')

# Readiness Score button
READINESS_SCORE_BUTTON = (AppiumBy.XPATH, '//android.view.ViewGroup[contains(@resource-id,"lytScore")]')

# Back button
BACK_BUTTON = (AppiumBy.XPATH, '//android.widget.ImageButton[@content-desc="Back Button"]')

# Resting Heart Rate button
RESTING_HEART_RATE_BUTTON = (AppiumBy.XPATH, '//android.view.ViewGroup[contains(@resource-id,"lytSec1")]')

# HRV button
HRV_BUTTON = (AppiumBy.XPATH, '//android.view.ViewGroup[contains(@resource-id,"lytSec2")]')

# Skin Temperature button
SKIN_TEMP_BUTTON = (AppiumBy.XPATH, '//android.view.ViewGroup[contains(@resource-id,"lytSec3")]')

# Respiratory Rate button
RESPIRATORY_RATE_BUTTON = (AppiumBy.XPATH, '//android.view.ViewGroup[contains(@resource-id,"lytSec4")]')
