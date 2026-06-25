from pages.base_page import BasePage
import allure

class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.name = "Login Page"
        self.locator = self.get_locators().LOGIN_PAGE
        self.homepage_locator = self.get_locators().HOME_PAGE
        

    def click_login_button_on_user_screen(self):
       
        self.mouse.click(self.driver, self.locator.LOGIN_BUTTON)
        expected_title = 'Welcome to Luna Ring'
        actual_title = self.forms.get_value(self.driver, self.locator.LOGIN_WELCOME)
        self.capture_screenshot("Login_Page_Opened")
      
        assert expected_title == actual_title, f"Expected title '{expected_title}' but got '{actual_title}'"


    def enter_username(self, username):
        self.mouse.click(self.driver, self.locator.LOGIN_EMAIL)
        self.forms.safe_send_keys(self.driver, self.locator.LOGIN_EMAIL_TEXTFIELD, username)
        self.capture_screenshot("Username_Entered")

    def enter_otp(self, otp):
        self.forms.safe_send_keys(self.driver, self.locator.LOGIN_EMAIL_OTP, otp)
        self.capture_screenshot("OTP_Entered")

    def click_otp_continue_button(self):
        self.mouse.click(self.driver, self.locator.OTP_CONTINUE_BUTTON)
        self.capture_screenshot("Login_Button_Clicked")

    def click_on_the_continue_button(self,email):
       
        self.mouse.click(self.driver, self.locator.CONTINUE)
        OTP =self.otp_reader.read_otp_by_email(email=email)
        self.capture_screenshot("Continue_Button_Clicked")
        return OTP
