from appium.webdriver.common.appiumby import AppiumBy

# The old resource-id locator does not exist on the current Compose Home page
# (no resource-ids). "PEAK SCORE" is a stable, Home-only section header.
# Confirmed from a uiautomator dump (home.xml, 2026-06-27).
HOME_PAGE_ELEMENT = (AppiumBy.XPATH, '//android.widget.TextView[@text="PEAK SCORE"]')

