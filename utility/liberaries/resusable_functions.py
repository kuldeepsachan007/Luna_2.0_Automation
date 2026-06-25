from appium.webdriver.webdriver import WebDriver as AppiumWebDriver
from . import forms_rfn as fr  # type: ignore
from . import mouse_rfn as mr  # type: ignore
from . import waits as wr  # type: ignore
from . import gestures_rfn as gr  # type: ignore
from . import navigation_rfn as nr  # type: ignore
from . import alerts_rfn as ar  # type: ignore
from . import context_rfn as cr  # type: ignore
from . import device_rfn as dr  # type: ignore

class ReusableFunctions:
    def __init__(self, driver: AppiumWebDriver):
        self.driver = driver
        self.forms = fr
        self.mouse = mr
        self.waits = wr
        self.gestures = gr
        self.navigation = nr
        self.alerts = ar
        self.context = cr
        self.device = dr

    def get_driver(self) -> AppiumWebDriver:
        return self.driver

    def handle_alert(self, accept: bool = True, timeout: int = 5) -> None:
        self.alerts.handle_alert(self.driver, accept=accept, timeout=timeout)

    def switch_context(self, context_name: str, timeout: int = 10) -> None:
        self.context.switch_context(self.driver, context_name, timeout=timeout)

    def go_back(self) -> None:
        self.navigation.go_back(self.driver)

    def swipe_up(self, duration: int = 800) -> None:
        self.gestures.swipe_up(self.driver, duration=duration)

    def wait_for_element(self, locator: tuple, timeout: int = 10):
        return self.waits.wait_for_element(self.driver, locator, timeout=timeout)

    def click_element(self, locator: tuple, timeout: int = 10) -> None:
        el = self.waits.wait_for_element(self.driver, locator, timeout=timeout)
        self.mouse.click_element(el, driver=self.driver)

    def set_input_value(self, locator: tuple, value: str, timeout: int = 10) -> None:
        el = self.waits.wait_for_element(self.driver, locator, timeout=timeout)
        self.forms.set_input_value(el, value, driver=self.driver)

    def take_screenshot(self, file_path: str) -> None:
        self.device.take_screenshot(self.driver, file_path)

    def refresh_page(self) -> None:
        self.navigation.refresh_page(self.driver)

    def scroll_to_element(self, locator: tuple, max_swipes: int = 5) -> None:
        self.gestures.scroll_to_element(self.driver, locator, max_swipes=max_swipes)

    def click_coordinates(self, x: int, y: int) -> bool:
        return self.mouse.click_coordinates(self.driver, x, y)

    def hadle_modal_dialog(self, accept: bool = True, timeout: int = 5) -> None:
        self.alerts.handle_modal_dialog(self.driver, accept=accept, timeout=timeout)

    def send_app_to_background(self, seconds: int) -> None:
        self.device.send_app_to_background(self.driver, seconds)

    def bring_app_to_foreground(self) -> None:
        self.device.bring_app_to_foreground(self.driver)

    def switch_activity(self, app_package: str, app_activity: str) -> None:
        self.device.switch_activity(self.driver, app_package, app_activity)
