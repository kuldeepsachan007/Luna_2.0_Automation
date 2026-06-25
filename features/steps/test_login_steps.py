
from  pytest_bdd import given, when, scenarios, then, step

from pages.login_page import LoginPage
from utility.liberaries.decorators import logger



@step('the user enters valid email id and otp')
def enter_valid_credentials(login_page: LoginPage,datatable=None):
    if datatable is not None:
        row = datatable[1]
        email = row[0]
    else:
        email = login_page.random_data_generator.generate_random_email()
    logger.info(f"Entering Email: {email} ")
    login_page.click_login_button_on_user_screen()
    login_page.enter_username(email)
    OTP =login_page.click_on_the_continue_button(email)
    assert OTP is not None, "OTP is None"
    logger.info(f"Entering OTP: {OTP} ")
    login_page.enter_otp(OTP)
    

@step('clicks the otp continue button')
def click_otp_continue_button(login_page: LoginPage):
    logger.info("Clicking the login button")
    # Here you would add the code to click the login button
    login_page.click_otp_continue_button()





