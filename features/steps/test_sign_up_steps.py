from pytest_bdd import given, when, scenarios, then, step

from pages.signup_page import SignUpPage
from utility.liberaries.decorators import logger

@step('the user should be asked to enter the phone number')
def verify_phone_number_screen(signup_page: SignUpPage, test_data):
    logger.info("Verifying phone number screen")
    signup_page.verify_phone_number_screen()
    a = 2
    b = 3
    test_data.c = a + b

@step('user enters the phone number')
def enter_phone_number(signup_page: SignUpPage, test_data,datatable=None):
    logger.info("Entering phone number")
    if datatable is not None:
        row = datatable[1]
        test_data.phone_number = row[0]
    else:
        test_data.phone_number = signup_page.random_data_generator.generate_random_indian_number()
        
    signup_page.enter_phone_number(test_data.phone_number)

@step('click on the phone number continue button')
def click_phone_number_continue_button(signup_page: SignUpPage,test_data):
    logger.info("Clicking phone number continue button")
    test_data.phone_number_otp = signup_page.click_phone_number_continue_button(test_data.phone_number)

@step('user enters the OTP and clicks on the continue button')
def enter_otp_and_click_continue(signup_page: SignUpPage,test_data):
    logger.info("Entering OTP and clicking continue button")
    signup_page.enter_phone_number_otp(test_data.phone_number_otp)
    signup_page.click_otp_continue_button()

@step('user asked to select the language')    
def verify_language_screen(signup_page: SignUpPage):
    logger.info("Verifying language screen")
    signup_page.verify_language_screen()

@step('user selects the language and clicks on continue button')   
def click_language_continue_button(signup_page: SignUpPage):
    logger.info("Clicking language continue button")
    signup_page.select_language('English')
    signup_page.click_language_continue_button()
  

     
@step('user should be asked to connect the Luna Ring')
def verify_connect_ring_screen(signup_page: SignUpPage):
    logger.info("Verifying connect ring screen")
    signup_page.verify_connect_ring_screen()

@step('user click on search now button')
def click_search_now_button(signup_page: SignUpPage):
    logger.info("Clicking search now button")
    signup_page.click_search_now_button()   

@step('user should be asked to allow to access location permission')
def verify_permissions_popup(signup_page: SignUpPage):
    logger.info("Verifying permissions popup")
    signup_page.verify_permissions_popup()

@step('user grands the location access')
def click_allow_button(signup_page: SignUpPage):
    logger.info("Clicking allow button")
    signup_page.click_allow_button() 

@step('near by luna rings shoudld be detected and displayed')    
def verify_ring_devices_found(signup_page: SignUpPage,test_data):
    logger.info("Verifying ring devices found")
    test_data.mac_address = signup_page.verify_ring_devices_found()

@step('user selects the luna ring') 
def select_luna_ring(signup_page: SignUpPage,test_data):
    logger.info("Selecting luna ring")
    mac_address = test_data.mac_address 
    signup_page.select_luna_ring(mac_address)

@step('pairing should start')       
def verify_pairing_progress(signup_page: SignUpPage):
    logger.info("Verifying pairing progress")
    signup_page.verify_pairing_progress()

@step('user verifies the mac address of the ring is correct')
def verify_mac_address(signup_page: SignUpPage,test_data):
    logger.info("Verifying mac address")
    mac_address = test_data.mac_address
    signup_page.verify_mac_address(mac_address)

@step('user clicks on the Get started button')
def click_get_start_button(signup_page: SignUpPage):
    logger.info("Clicking get started button")
    signup_page.click_get_start_button()



    

 



    

 


    
    
    









