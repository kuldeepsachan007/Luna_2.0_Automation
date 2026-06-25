from pages.base_page import BasePage
from utility.liberaries.decorators import logger


class SignUpPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.name = "SignUp Page"
        self.sign_up_page_locator = self.get_locators().SIGN_UP_PAGE
        self.phone_number = None

    def verify_phone_number_screen(self):
        title = "What’s your number?"
        actual_title = self.forms.get_value(self.driver, self.sign_up_page_locator.PHONE_NUMBER_SCREEN_TITLE)
        assert title == actual_title, f"Expected title '{title}' but got '{actual_title}'"
        self.capture_screenshot("Phone_Number_Screen_Visible")

    def enter_phone_number(self, phone_number):
        self.mouse.click(self.driver,self.sign_up_page_locator.PHONE_NUMBER_INPUT) 
        self.forms.safe_send_keys(self.driver,self.sign_up_page_locator.PHONE_NUMBER_INPUT,phone_number)
        self.capture_screenshot("Phone_Number_Entered" ) 

    def click_phone_number_continue_button(self,phone_number):
        self.navigation.go_back(self.driver)
        self.mouse.click(self.driver, self.sign_up_page_locator.PHONE_CONTINUE_BUTTON)
        self.capture_screenshot("Phone_Number_Continue_Button_Clicked")
        otp = self.otp_reader.read_otp_by_mobile(mobile=phone_number)
        return otp
    def enter_phone_number_otp(self,otp):
        self.forms.safe_send_keys(self.driver,self.sign_up_page_locator.PHONE_NUMBER_OTP,otp)
        self.capture_screenshot("Otp_Entered" ) 

    def click_otp_continue_button(self):
        self.mouse.click(self.driver, self.sign_up_page_locator.OTP_CONTINUE_BUTTON)
        self.capture_screenshot("Otp_Continue_Button_Clicked")

    def verify_language_screen(self):
        title = "Choose your language"
        actual_title = self.forms.get_value(self.driver, self.sign_up_page_locator.LANGUAGE_SCREEN_TITLE)
        assert title == actual_title, f"Expected title '{title}' but got '{actual_title}'"
        self.capture_screenshot("Language_Screen_Visible")

    def click_language_continue_button(self):
        self.mouse.click(self.driver, self.sign_up_page_locator.LANGUAGE_CONTINUE_BUTTON)
        self.capture_screenshot("Language_Continue_Button_Clicked")

    def select_language(self, language):
        by, value = self.sign_up_page_locator.ENGLISH_LANGUAGE_OPTION
        self.sign_up_page_locator.ENGLISH_LANGUAGE_OPTION = (by, value.replace("English", language))
        self.mouse.click(self.driver, self.sign_up_page_locator.ENGLISH_LANGUAGE_OPTION)
        self.capture_screenshot("Language_Selected")    

    def verify_connect_ring_screen(self):
        title = "Connect your Luna Ring"
        actual_title = self.forms.get_value(self.driver, self.sign_up_page_locator.CONNECT_RING_TITLE)
        assert title == actual_title, f"Expected title '{title}' but got '{actual_title}'"
        self.capture_screenshot("Connect_Ring_Screen_Visible")


    def click_search_now_button(self):        
        self.mouse.click(self.driver, self.sign_up_page_locator.SEARCH_NOW_BUTTON)

    def verify_permissions_popup(self):
        message = 'Permissions to use your location' 
        actual_message = self.forms.get_value(self.driver, self.sign_up_page_locator.PERMISSION_MESSAGE)
        assert message == actual_message, f"Expected message '{message}' but got '{actual_message}'"
        self.capture_screenshot("Permissions_Popup_Visible")

    def click_allow_button(self):
        self.mouse.click(self.driver, self.sign_up_page_locator.PERMISSION_ALLOW)
        self.mouse.click(self.driver, self.sign_up_page_locator.PERMISSION_ALLOW_FOREGROUND)
        self.mouse.click(self.driver, self.sign_up_page_locator.PERMISSION_ANDROID_ALLOW)   
        self.capture_screenshot("Allow_Button_Clicked")

    def verify_ring_devices_found(self):
        
        import re
        self.waits.wait_for_presence(self.driver, self.sign_up_page_locator.RING_DEVICE_ITEM)
        self.waits.wait_for_element_text_matches(self.driver, self.sign_up_page_locator.RING_DEVICE_ITEM, r'\d', timeout=15)
        number_of_ring_devices = self.forms.get_value(self.driver, self.sign_up_page_locator.RING_DEVICE_ITEM)
     
        ring_devices = self.forms.find_elements(self.driver, self.sign_up_page_locator.RING_DEVICES_FOUND)
        actual_number_of_ring_devices = len(ring_devices)
        number_of_ring_devices = int(re.findall(r'\d+', number_of_ring_devices)[0]) 
        assert number_of_ring_devices == actual_number_of_ring_devices, f"Expected number of ring devices '{number_of_ring_devices}' but got '{actual_number_of_ring_devices}'"
        mac_address = self.forms.get_value(self.driver, self.sign_up_page_locator.BEFORE_PAIRING_MAC)   
        self.capture_screenshot("Ring_Devices_Found")
        return mac_address

    
    def select_luna_ring(self,mac_address):
      
        ring_devices = self.forms.find_elements(self.driver, self.sign_up_page_locator.RING_DEVICES_FOUND)
        ring_mac_addresses = self.forms.find_elements(self.driver, self.sign_up_page_locator.BEFORE_PAIRING_MAC)     
        for device, actual_mac_address in zip(ring_devices, ring_mac_addresses):
            actual_mac_address = self.forms_rfn.get_value(actual_mac_address)
            if actual_mac_address == mac_address:
                self.mouse_rfn.click_element(device)   
                self.capture_screenshot("Luna_Ring_Selected")
                break   


    def verify_pairing_progress(self):  
        self.waits.wait_for_presence(self.driver, self.sign_up_page_locator.PAIRING_PROGRESS)
        is_pairing_successful = self.forms.is_element_displayed(self.driver, self.sign_up_page_locator.PAIRING_SUCCESSFUL)
        if is_pairing_successful:
            self.capture_screenshot("Pairing_Successful")
        else:
            self.capture_screenshot("Pairing_Progress")
       

    def verify_mac_address(self,mac_address):
        actual_mac_address = self.forms.get_value(self.driver, self.sign_up_page_locator.AFTER_PAIRING_MAC)
        assert actual_mac_address == mac_address, f"Expected mac address '{mac_address}' but got '{actual_mac_address}'"
        self.capture_screenshot("Mac_Address_Verified")

    def click_get_start_button(self): 
        self.mouse.click(self.driver, self.sign_up_page_locator.GET_STARTED)
        self.capture_screenshot("Get_Started_Button_Clicked")
        self.waits.wait_for_text_present(self.driver, self.sign_up_page_locator.LETS_GO_BUTTON, "Let's go", timeout=10)
        self.mouse.click(self.driver, self.sign_up_page_locator.LETS_GO_BUTTON)
        self.capture_screenshot("Lets_Go_Button_Clicked")



                   
   
        
        

