from appium.webdriver.common.appiumby import AppiumBy

#//android.widget.TextView[@resource-id="com.noisefit.luna.dev:id/textView16"]


LOGIN_TITLE = (AppiumBy.XPATH, '//android.widget.TextView[contains(@resource-id,"hello_from_")]')

LOGIN_BUTTON = (AppiumBy.XPATH, '//android.widget.Button[@content-desc="Get started"]')
LOGIN_WELCOME = (AppiumBy.XPATH, '//android.widget.TextView[contains(@resource-id,"textView16")]')
LOGIN_EMAIL = (AppiumBy.XPATH, '//android.view.View[@content-desc="Login via Email"]') 

LOGIN_EMAILID_MESSAGE =(AppiumBy.XPATH, '//android.widget.TextView[contains(@resource-id,"textView")]')
LOGIN_EMAIL_TEXTFIELD =(AppiumBy.XPATH, '//android.widget.EditText[@content-desc="Enter Email Id here"]')

CONTINUE = (AppiumBy.XPATH, '//android.widget.Button[@content-desc="Continue"]')
LOGIN_EMAIL_OTP = (AppiumBy.XPATH, '//android.widget.EditText[contains(@resource-id,"etOtp")]')
TERM_CONDITIONS = (AppiumBy.XPATH, '//android.widget.Button[contains(@resource-id,"btnAgree")]')
OTP_CONTINUE_BUTTON = (AppiumBy.XPATH, '//android.widget.Button[contains(@resource-id,"bContinue")]')