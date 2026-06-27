from appium.webdriver.common.appiumby import AppiumBy

# ═══════════════════════════════════════════════════════════════════════════
# Luna 2.0 — Health page locators (Android)
#
# This is a Jetpack Compose app: the view hierarchy exposes NO resource-ids on
# content, so every locator targets visible `text` or `content-desc`.
#
# CONFIRMED locators were derived from a uiautomator dump of the Health LANDING
# page (2026-06-27). Locators marked PROVISIONAL belong to screens we do not yet
# have a dump for (measure popups, Heart Rate / Stress / Activity / Sleep detail
# pages) — derive/replace them from a dump of each screen as the flow reaches it
# (per the dump-driven workflow: no guessing).
# ═══════════════════════════════════════════════════════════════════════════

# ── Bottom navigation ──────────────────────────────────────────────────────
NAV_HEALTH = (AppiumBy.XPATH, '//android.view.View[@content-desc="Health"]')
NAV_HOME   = (AppiumBy.XPATH, '//android.view.View[@content-desc="Home"]')

# ── Top app-bar title ───────────────────────────────────────────────────────
# "Health" text also appears in the bottom nav, so pin to the FIRST match
# (the title sits at the top of the screen, first in document order).
HEALTH_PAGE_TITLE = (AppiumBy.XPATH, '(//android.widget.TextView[@text="Health"])[1]')

# ── Vital tile labels ───────────────────────────────────────────────────────
SPO2_LABEL       = (AppiumBy.XPATH, '//android.widget.TextView[@text="SPO2"]')
STRESS_LABEL     = (AppiumBy.XPATH, '//android.widget.TextView[@text="STRESS"]')
# "HEART RATE" appears twice (tile near the top + a card lower down); [1] = tile.
HEART_RATE_LABEL = (AppiumBy.XPATH, '(//android.widget.TextView[@text="HEART RATE"])[1]')
SKIN_TEMP_LABEL  = (AppiumBy.XPATH, '//android.widget.TextView[@text="SKIN TEMP"]')
SLEEP_CARD_LABEL = (AppiumBy.XPATH, '//android.widget.TextView[@text="SLEEP"]')

# ── MEASURE buttons ─────────────────────────────────────────────────────────
# The label TextViews report clickable=false; the clickable Compose container is
# an ancestor. Appium taps the element centre, which the ancestor's click
# modifier catches. There are two "MEASURE NOW" (SpO2, Skin Temp) and two
# "MEASURE" (Stress, Heart Rate), separated by document order.
SPO2_MEASURE_BTN       = (AppiumBy.XPATH, '(//android.widget.TextView[@text="MEASURE NOW"])[1]')
SKIN_TEMP_MEASURE_BTN  = (AppiumBy.XPATH, '(//android.widget.TextView[@text="MEASURE NOW"])[2]')
STRESS_MEASURE_BTN     = (AppiumBy.XPATH, '(//android.widget.TextView[@text="MEASURE"])[1]')
HEART_RATE_MEASURE_BTN = (AppiumBy.XPATH, '(//android.widget.TextView[@text="MEASURE"])[2]')

# ── Tile values (PROVISIONAL) ────────────────────────────────────────────────
# On the landing dump only Stress (11) and Heart Rate (83 bpm) had numeric
# values; SpO2 and Skin Temp showed an icon until first measured. These anchor
# off the nearby unit text and should be re-checked against a post-measurement
# dump.
STRESS_TILE_VALUE     = (AppiumBy.XPATH, '//android.widget.TextView[@text="/100"]/preceding-sibling::android.widget.TextView[1]')
HEART_RATE_TILE_VALUE = (AppiumBy.XPATH, '(//android.widget.TextView[@text="bpm"])[1]/preceding-sibling::android.widget.TextView[1]')
SPO2_TILE_VALUE       = (AppiumBy.XPATH, '//android.widget.TextView[@text="%"]/preceding-sibling::android.widget.TextView[1]')
SKIN_TEMP_TILE_VALUE  = (AppiumBy.XPATH, '//android.widget.TextView[contains(@text,"°")]')

# ── Measurement popup (PROVISIONAL — needs a dump of the measure sheet) ───────
# Button texts taken from the feature-file flow description.
POPUP_TRY_AGAIN   = (AppiumBy.XPATH, '//android.widget.TextView[@text="Try Again" or @text="TRY AGAIN"]')
POPUP_DONE        = (AppiumBy.XPATH, '//android.widget.TextView[@text="Done" or @text="DONE"]')
POPUP_CLOSE       = (AppiumBy.XPATH, '//android.view.View[@content-desc="Close" or @content-desc="Dismiss"]')
POPUP_NO_READING  = (AppiumBy.XPATH, '//android.widget.TextView[contains(@text,"Couldn") and contains(@text,"reading")]')
POPUP_READING_VALUE = (AppiumBy.XPATH, '//android.widget.TextView')  # refine with popup dump

# ── Cards below the tiles (PROVISIONAL — confirm after scrolling/dump) ────────
# The Heart Rate card uses "BPM" (uppercase) vs the tile's "bpm" (lowercase).
HEART_RATE_CARD       = (AppiumBy.XPATH, '(//android.widget.TextView[@text="HEART RATE"])[2]')
HEART_RATE_CARD_VALUE = (AppiumBy.XPATH, '//android.widget.TextView[@text="BPM"]/preceding-sibling::android.widget.TextView[1]')
STRESS_CARD           = (AppiumBy.XPATH, '(//android.widget.TextView[@text="STRESS"])[2]')
ACTIVITY_CARD         = (AppiumBy.XPATH, '//android.widget.TextView[@text="ACTIVITY"]')
STRESS_CARD_VALUE     = (AppiumBy.XPATH, '//android.widget.TextView[@text="/100"]/preceding-sibling::android.widget.TextView[1]')
ACTIVITY_CARD_STEPS   = (AppiumBy.XPATH, '//android.widget.TextView[contains(@text,"steps") or contains(@text,"Steps")]')
OPEN_DETAIL_ARROW     = (AppiumBy.XPATH, '//android.view.View[@content-desc="Open detail"]')

# ── Detail-page headers (PROVISIONAL — needs a dump of each detail page) ──────
HEART_RATE_PAGE_TITLE = (AppiumBy.XPATH, '//android.widget.TextView[@text="Heart Rate" or @text="HEART RATE"]')
STRESS_PAGE_TITLE     = (AppiumBy.XPATH, '//android.widget.TextView[@text="Stress" or @text="STRESS"]')
ACTIVITY_PAGE_TITLE   = (AppiumBy.XPATH, '//android.widget.TextView[@text="Activity" or @text="ACTIVITY"]')
SLEEP_PAGE_TITLE      = (AppiumBy.XPATH, '//android.widget.TextView[@text="Sleep" or @text="SLEEP"]')
BACK_BUTTON           = (AppiumBy.XPATH, '//android.view.View[@content-desc="Navigate up" or @content-desc="Back"]')

# ── Sleep card values on the Health page (CONFIRMED from landing dump) ────────
SLEEP_ACTUAL   = (AppiumBy.XPATH, '//android.widget.TextView[contains(@text,"of ")]/preceding-sibling::android.widget.TextView[1]')
SLEEP_NEEDED   = (AppiumBy.XPATH, '//android.widget.TextView[starts-with(@text,"of ")]')
SLEEP_DEFICIT  = (AppiumBy.XPATH, '//android.widget.TextView[contains(@text,"short")]')
SLEEP_RHR      = (AppiumBy.XPATH, '//android.widget.TextView[@text="RHR"]/preceding-sibling::android.widget.TextView[1]')
SLEEP_HRV      = (AppiumBy.XPATH, '//android.widget.TextView[@text="HRV"]/preceding-sibling::android.widget.TextView[1]')
