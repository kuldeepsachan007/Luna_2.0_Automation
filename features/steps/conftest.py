import pytest

from pages.login_page import LoginPage
from pages.signup_page import SignUpPage
from pages.sleep_page import SleepPage
from pages.home_page import HomePage
from pages.health_page import HealthPage
from pages.heart_rate_page import HeartRatePage
from pages.stress_page import StressPage


@pytest.fixture
def login_page(app):
    return  LoginPage(app)


@pytest.fixture
def health_page(app):
    return HealthPage(app)


@pytest.fixture
def heart_rate_page(app):
    return HeartRatePage(app)


@pytest.fixture
def stress_page(app):
    return StressPage(app)

@pytest.fixture
def signup_page(app):
    return  SignUpPage(app)

@pytest.fixture
def sleep_page(app):
    return SleepPage(app)

@pytest.fixture
def luna_home_page(app):
    return HomePage(app)

