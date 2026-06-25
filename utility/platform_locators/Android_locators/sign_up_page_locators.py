from appium.webdriver.common.appiumby import AppiumBy

# Phone Number Screen
PHONE_NUMBER_SCREEN_TITLE = (AppiumBy.XPATH, '//android.widget.TextView[contains(@resource-id,"textView") and contains(@text, "your number")]')
PHONE_NUMBER_INPUT = (AppiumBy.XPATH, '//android.widget.EditText')
PHONE_NUMBER_OTP = (AppiumBy.XPATH, '//android.widget.EditText[@content-desc="Enter OTP here"]')
PHONE_CONTINUE_BUTTON = (AppiumBy.XPATH, '//android.widget.Button[@content-desc="Continue"]')

# OTP Screen
OTP_SENT_MESSAGE = (AppiumBy.XPATH, '//android.widget.TextView[contains(@text, "OTP sent")]')
OTP_INPUT = (AppiumBy.XPATH, '//android.widget.EditText[contains(@resource-id, "otp")]')
OTP_CONTINUE_BUTTON = (AppiumBy.XPATH, '//android.widget.Button[@content-desc="Continue"]')

# Language Screen
LANGUAGE_SCREEN_TITLE = (AppiumBy.XPATH, '//android.widget.TextView[contains(@text, "Choose your language")]')
ENGLISH_LANGUAGE_OPTION = (AppiumBy.XPATH, '//android.widget.TextView[@text="English"]')
LANGUAGE_CONTINUE_BUTTON = (AppiumBy.XPATH, '//android.widget.Button[contains(@resource-id,"btnContinue")]')

# Connect Ring
CONNECT_RING_TITLE = (AppiumBy.XPATH, '//android.widget.TextView[contains(@text, "Connect your Luna Ring")]')
SEARCH_NOW_BUTTON = (AppiumBy.XPATH, '//android.widget.Button[contains(@resource-id,"btnSearchNow")]')

# Permissions
PERMISSION_MESSAGE = (AppiumBy.XPATH, '//android.widget.TextView[contains(@resource-id,"tvTitle")]')
PERMISSION_ALLOW = (AppiumBy.XPATH, '//android.widget.Button[contains(@resource-id,"/btnYes")]')
PERMISSION_ANDROID_MESSAGE = (AppiumBy.ID, 'com.android.permissioncontroller:id/permission_message')
PERMISSION_ALLOW_FOREGROUND = (AppiumBy.ID, 'com.android.permissioncontroller:id/permission_allow_foreground_only_button')
PERMISSION_ANDROID_ALLOW = (AppiumBy.ID, 'com.android.permissioncontroller:id/permission_allow_button')

# Scanning/Pairing
RING_DEVICE_ITEM = (AppiumBy.XPATH, '//android.widget.TextView[contains(@resource-id,"tvDevicesFound")]')
RING_DEVICES_FOUND = (AppiumBy.XPATH, '//androidx.recyclerview.widget.RecyclerView[contains(@resource-id,"rvDevices")]/android.view.ViewGroup')
BEFORE_PAIRING_MAC = (AppiumBy.XPATH, '//android.widget.TextView[contains(@resource-id,"tvWatchMacAddress")]')
PAIRING_PROGRESS = (AppiumBy.XPATH, '//android.widget.TextView[contains(@resource-id,"textView")]')
PAIRING_SUCCESSFUL = (AppiumBy.XPATH, '//android.widget.TextView[contains(@resource-id,"textView")]')
AFTER_PAIRING_MAC = (AppiumBy.XPATH, '//android.widget.TextView[contains(@resource-id,"tvWatchMac")]')
GET_STARTED = (AppiumBy.XPATH, '//android.widget.Button[contains(@resource-id,"btnStart")]')

# User Details
NAME_INPUT_SCREEN = (AppiumBy.XPATH, '//android.widget.TextView[contains(@text, "What should we call you")]')
NAME_INPUT = (AppiumBy.XPATH, '//android.widget.EditText')
NAME_CONTINUE_BUTTON = (AppiumBy.XPATH, '//android.widget.Button[@content-desc="Continue"]')

DOB_SCREEN = (AppiumBy.XPATH, '//android.widget.TextView[contains(@text, "When were you born")]')
DOB_CONTINUE_BUTTON = (AppiumBy.XPATH, '//android.widget.Button[@content-desc="Continue"]')

GENDER_SCREEN = (AppiumBy.XPATH, '//android.widget.TextView[contains(@text, "What is your gender")]')
GENDER_MALE = (AppiumBy.XPATH, '//android.widget.TextView[@text="Male"]')
GENDER_CONTINUE_BUTTON = (AppiumBy.XPATH, '//android.widget.Button[@content-desc="Continue"]')

HEIGHT_SCREEN = (AppiumBy.XPATH, '//android.widget.TextView[contains(@text, "How tall are you")]')
HEIGHT_CONTINUE_BUTTON = (AppiumBy.XPATH, '//android.widget.Button[@content-desc="Continue"]')

WEIGHT_SCREEN = (AppiumBy.XPATH, '//android.widget.TextView[contains(@text, "How much do you weigh")]')
WEIGHT_CONTINUE_BUTTON = (AppiumBy.XPATH, '//android.widget.Button[@content-desc="Continue"]')

INTENT_SCREEN = (AppiumBy.XPATH, '//android.widget.TextView[contains(@text, "What brings you here")]')
INTENT_OPTION_1 = (AppiumBy.XPATH, '//android.view.ViewGroup[1]')
INTENT_CONTINUE_BUTTON = (AppiumBy.XPATH, '//android.widget.Button[@content-desc="Continue"]')

ALL_DONE_SCREEN = (AppiumBy.XPATH, '//android.widget.TextView[contains(@text, "All Done")]')
LETS_GO_BUTTON = (AppiumBy.XPATH, '//android.widget.Button[contains(@resource-id,"btnLetsGo")]')

HOME_PAGE_ELEMENT = (AppiumBy.XPATH, '//android.widget.TextView[contains(@resource-id, "home")]')