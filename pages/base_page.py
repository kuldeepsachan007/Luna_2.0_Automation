from appium.webdriver.webdriver import WebDriver as AppiumWebDriver
from utility.liberaries import filepaths as filepaths_mod  # type: ignore
from utility.liberaries import forms as forms_mod, forms_rfn as forms_rfn_mod
from utility.liberaries import gesture_control as gesture_mod, locators as locators_mod
from utility.liberaries import mouse_rfn as mouse_rfn_mod, mouse as mouse_mod
from utility.liberaries import otp_reader as otp_reader_mod, random_data_generator as rand_mod, navigation_rfn as navigation_mod
from utility.liberaries import resusable_functions as reusable_mod, waits as waits_mod
from utility.liberaries import allure_logs as allure_logs_mod, decorators as decorators_mod
from utility.platform_locators import AndroidLocators, IOSLocators
from test_data import download, upload, screenshots
from utility.liberaries.sql_database import SQLDatabase


class BasePage:
    def __init__(self, driver: AppiumWebDriver):
        self.driver = driver
        self.download_dir = download
        self.upload_dir = upload
        self.screenshot_dir = screenshots

        self.allure_logs = allure_logs_mod.AllureLogger()

        self.decorators = decorators_mod
        self.forms = forms_mod
        self.forms_rfn = forms_rfn_mod
        self.gesture_control = gesture_mod
        self.locators = locators_mod
        self.mouse_rfn = mouse_rfn_mod
        self.mouse = mouse_mod
        self.navigation = navigation_mod
        self.otp_reader = otp_reader_mod
        self.random_data_generator = rand_mod
        self.reusable_functions = reusable_mod
        self.waits = waits_mod
        self.filepaths = filepaths_mod

        self.android_locators = AndroidLocators()
        self.ios_locators = IOSLocators()

        sql_data_base = SQLDatabase()
        sql_data_base.connect()

    def get_platform_name(self) -> str:
        return self.driver.capabilities.get('platformName', '').lower()

    def capture_screenshot(self, name: str) -> None:
        "Capture screenshot and attach to Allure report using allure logger."
        base64_data = self.driver.get_screenshot_as_base64()
        self.allure_logs.attach_screenshot_from_base64(base64_data, name=name)

    def get_locators(self):
        platform_name = self.get_platform_name()
        if platform_name == 'android':
            return self.android_locators
        elif platform_name == 'ios':
            return self.ios_locators
        else:
            raise ValueError(f"Unsupported platform: {platform_name}")

    def get_driver(self) -> AppiumWebDriver:
        return self.driver

    def take_screenshot(self, file_name: str) -> str:
        file_path = f"{self.screenshot_dir}/{file_name}"
        self.driver.save_screenshot(file_path)
        return file_path

    def refresh_page(self) -> None:
        # Native apps don't support page refresh; keep stub for compatibility
        try:
            self.driver.refresh()
        except Exception:
            # ignore for native apps
            pass
