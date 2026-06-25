# Minimal context switching helpers
from appium.webdriver.webdriver import WebDriver as AppiumWebDriver


def switch_context(driver: AppiumWebDriver, context_name: str, timeout: int = 10) -> None:
    try:
        contexts = driver.contexts
        for ctx in contexts:
            if context_name in ctx:
                driver.switch_to.context(ctx)
                return
    except Exception:
        pass
