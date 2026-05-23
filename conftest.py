import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "slow_mo": 500, 
    }

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
    }

@pytest.fixture()
def login_page(page: Page):
    return LoginPage(page)

@pytest.fixture()
def logged_in_page(page: Page):
    login = LoginPage(page)
    login.open()
    login.login("standard_user", "secret_sauce")
    page.wait_for_url("**/inventory.html")

    yield page