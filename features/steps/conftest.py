import pytest

from pages.login_page import LoginPage
from pages.signup_page import SignUpPage
from pages.sleep_page import SleepPage
from pages.home_page import HomePage


@pytest.fixture
def login_page(app):
    return  LoginPage(app)

@pytest.fixture
def signup_page(app):
    return  SignUpPage(app)

@pytest.fixture
def sleep_page(app):
    return SleepPage(app)

@pytest.fixture
def luna_home_page(app):
    return HomePage(app)

