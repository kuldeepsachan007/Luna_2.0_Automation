from appium.webdriver.common.appiumby import AppiumBy

# ═══════════════════════════════════════════════════════════════════════════
# Luna 2.0 — Stress detail page (Android, Jetpack Compose)
#
# Opened from the Health page's Stress card. This is a FULL PAGE (not a
# bottom-sheet dialog) and has NO WEEK/MONTH/6M tabs. Locate by text /
# content-desc (no resource-ids). Confirmed from a uiautomator dump 2026-06-28.
# ═══════════════════════════════════════════════════════════════════════════

# ── Page identity / navigation ───────────────────────────────────────────────
PAGE_TITLE   = (AppiumBy.XPATH, '//android.widget.TextView[@text="Stress"]')
CLOSE        = (AppiumBy.XPATH, '//android.view.View[@content-desc="Close"]')   # top-left
PREVIOUS_DAY = (AppiumBy.XPATH, '//android.view.View[@content-desc="Previous day"]')
NEXT_DAY     = (AppiumBy.XPATH, '//android.view.View[@content-desc="Next day"]')

# ── Status + values ──────────────────────────────────────────────────────────
# Status word varies (FOCUSED / NORMAL / STRESSED / …) — match the row above the
# big average value. PROVISIONAL: only FOCUSED seen so far.
STATUS    = (AppiumBy.XPATH, '//android.widget.TextView[@text="FOCUSED" or @text="NORMAL" or @text="STRESSED" or @text="RELAXED"]')
# Big centre value = average for the day ("AVG of the day" sits just below it).
AVG_LABEL = (AppiumBy.XPATH, '//android.widget.TextView[@text="AVG of the day"]')
# The avg value sits just above "AVG of the day". Appium's preceding-sibling[1]
# is unreliable (returns the furthest, not nearest), so locate the value as the
# TextView whose NEXT sibling is "AVG of the day".
AVG_VALUE = (AppiumBy.XPATH, '//android.widget.TextView[following-sibling::android.widget.TextView[1][@text="AVG of the day"]]')
MAX_LABEL = (AppiumBy.XPATH, '//android.widget.TextView[@text="Max"]')
MAX_VALUE = (AppiumBy.XPATH, '//android.widget.TextView[@text="Max"]/following-sibling::android.widget.TextView[1]')
MIN_LABEL = (AppiumBy.XPATH, '//android.widget.TextView[@text="Min"]')
MIN_VALUE = (AppiumBy.XPATH, '//android.widget.TextView[@text="Min"]/following-sibling::android.widget.TextView[1]')

# ── "How your day unfolded" timeline (Y-axis is Canvas-drawn, not queryable) ──
DAY_GRAPH_TITLE = (AppiumBy.XPATH, '//android.widget.TextView[@text="How your day unfolded"]')

# Further down: "Stress trends" then the "Is today typical?" comparison section.
STRESS_TRENDS_TITLE = (AppiumBy.XPATH, '//android.widget.TextView[@text="Stress trends"]')
IS_TODAY_TYPICAL    = (AppiumBy.XPATH, '//android.widget.TextView[@text="Is today typical?"]')

# ── Stress trends: WEEK / MONTH / 6 MONTHS range tabs ────────────────────────
# Tab labels are plain text whose parent handles the click (use clickGesture).
TRENDS_TAB_WEEK    = (AppiumBy.XPATH, '//android.widget.TextView[@text="WEEK"]')
TRENDS_TAB_MONTH   = (AppiumBy.XPATH, '//android.widget.TextView[@text="MONTH"]')
TRENDS_TAB_6MONTHS = (AppiumBy.XPATH, '//android.widget.TextView[@text="6 MONTHS"]')
TRENDS_AVG_LABEL   = (AppiumBy.XPATH, '//android.widget.TextView[@text="AVG"]')
# The period date-range, e.g. "JUN 21 – JUN 27". It is the only text with an
# en-dash (U+2013) in the trends area and CHANGES per tab, so it proves each tab
# re-plots its own period. The stacked bars + Y-axis are Canvas (not queryable).
TRENDS_RANGE       = (AppiumBy.XPATH, '(//android.widget.TextView[contains(@text,"–")])[1]')

# ── "Is today typical?" comparison: TODAY / NON-ACTIVITY tabs ─────────────────
TYPICAL_TAB_TODAY       = (AppiumBy.XPATH, '//android.widget.TextView[@text="TODAY"]')
TYPICAL_TAB_NONACTIVITY = (AppiumBy.XPATH, '//android.widget.TextView[@text="NON-ACTIVITY"]')
# Comparison heading switches text with the tab: "Today vs typical <day>" vs
# "Non-activity – today vs typical <day>" — used to confirm each tab is active.
TYPICAL_TODAY_COMPARE   = (AppiumBy.XPATH, '//android.widget.TextView[starts-with(@text,"Today vs typical")]')
TYPICAL_NONACT_COMPARE  = (AppiumBy.XPATH, '//android.widget.TextView[starts-with(@text,"Non-activity")]')

# ── The three stress stages below the timeline (mixed-case labels; the top
#    status word "FOCUSED" is UPPERCASE, so these match only the stage rows). ──
STAGE_RELAXED  = (AppiumBy.XPATH, '//android.widget.TextView[@text="Relaxed"]')
STAGE_FOCUSED  = (AppiumBy.XPATH, '//android.widget.TextView[@text="Focused"]')
STAGE_STRESSED = (AppiumBy.XPATH, '//android.widget.TextView[@text="Stressed"]')
TOTAL_DURATION = (AppiumBy.XPATH, '//android.widget.TextView[@text="TOTAL DURATION"]')

# Each stage is a clickable row: [label, "+Xm vs avg", duration, "N%"].
# The duration is the label's 2nd following sibling. Tap the row to select it.
STAGE_RELAXED_ROW  = (AppiumBy.XPATH, '//android.widget.TextView[@text="Relaxed"]/parent::*[@clickable="true"]')
STAGE_FOCUSED_ROW  = (AppiumBy.XPATH, '//android.widget.TextView[@text="Focused"]/parent::*[@clickable="true"]')
STAGE_STRESSED_ROW = (AppiumBy.XPATH, '//android.widget.TextView[@text="Stressed"]/parent::*[@clickable="true"]')
RELAXED_DURATION   = (AppiumBy.XPATH, '//android.widget.TextView[@text="Relaxed"]/following-sibling::android.widget.TextView[2]')
FOCUSED_DURATION   = (AppiumBy.XPATH, '//android.widget.TextView[@text="Focused"]/following-sibling::android.widget.TextView[2]')
STRESSED_DURATION  = (AppiumBy.XPATH, '//android.widget.TextView[@text="Stressed"]/following-sibling::android.widget.TextView[2]')
TOTAL_DURATION_VALUE = (AppiumBy.XPATH, '//android.widget.TextView[@text="TOTAL DURATION"]/following-sibling::android.widget.TextView[1]')
