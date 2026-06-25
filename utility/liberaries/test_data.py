import os
class TestData:
    SAMPLE_TEXT = "This is a sample text for testing purposes."
    SAMPLE_NUMBERS = [1, 2, 3, 4, 5]
    SAMPLE_DICT = {"key1": "value1", "key2": "value2", "key3": "value3"}
    SAMPLE_TUPLE = (10, 20, 30)
    SAMPLE_SET = {100, 200, 300}
    username = os.getenv("username", "testuser")
    password = os.getenv("password", "password123")
    app_url = os.getenv("APP_URL", "http://localhost:8000")
    appium_server = os.getenv("APPIUM_SERVER", "http://127.0.0.1:4723")
    platform_name = os.getenv("PLATFORM_NAME", "Android")
    device_name = os.getenv("DEVICE_NAME", "emulator-5554")
    platform_version = os.getenv("PLATFORM_VERSION", "11")
    automation_name = os.getenv("AUTOMATION_NAME", "UiAutomator2")
    app_package = os.getenv("APP_PACKAGE", "com.anonymous.DairyRecords")
    app_activity = os.getenv("APP_ACTIVITY", ".MainActivity")
    udid = os.getenv("UDID", "emulator-5554")
    implicit_wait = int(os.getenv("IMPLICIT_WAIT", "5"))
    explicit_wait = int(os.getenv("EXPLICIT_WAIT", "10"))
    page_load_timeout = int(os.getenv("PAGE_LOAD_TIMEOUT", "30"))
    app_path = os.getenv("APP_PATH", "APP/Android/DairyRecords.apk")