import re
from playwright.sync_api import Page, expect
import pytest
from pages.login_page import LoginPage

@pytest.mark.parametrize("username, password, expected_error", [
    ("",              "",             "Epic sadface: Username is required"),
    ("test_user",     "",             "Epic sadface: Password is required"),
    ("standard_user", "12345",        "Epic sadface: Username and password do not match any user in this service"),
    ("locked_out_user", "secret_sauce", "Epic sadface: Sorry, this user has been locked out."),
])

def test_negative_login(page: Page, username, password, expected_error):

    page.goto("https://www.saucedemo.com/")

    login_page = LoginPage(page)
    login_page.login(username, password)

    login_button = page.get_by_role("button", name="Login")
    login_button.click()

    expect(page.get_by_text(expected_error)).to_be_visible()
    expect(page.locator("xpath=//h3[@data-test='error']")).to_be_visible()

    expect(page.get_by_placeholder("Username")).to_be_visible()
    expect(page.get_by_placeholder("Password")).to_be_visible()

    expect(page.get_by_role("heading", name="Accepted usernames are:")).to_be_visible()
    expect(page.get_by_role("heading", name="Password for all users:")).to_be_visible()
    
    expect(login_button).to_be_visible()
    
    page.screenshot(path="test_results/test_auth/screenshot_negative_login.png")

@pytest.mark.parametrize("username, password", [
    ("standard_user",  "secret_sauce"),
    ("visual_user", "secret_sauce"),
    ("performance_glitch_user", "secret_sauce"),
    pytest.param("error_user", "secret_sauce", marks=pytest.mark.xfail(reason="error_user: wrong product opens, sort broken")),
    pytest.param("problem_user",   "secret_sauce", marks=pytest.mark.xfail(reason="problem_user: sort dropdown broken")),
])

def test_positive_login(page: Page, username, password):
    page.goto("https://www.saucedemo.com/")

    username_input = page.locator("#user-name")
    username_input.fill(username)
    expect(username_input).to_have_value(username)

    password_input = page.locator("#password")
    password_input.fill(password)
    expect(password_input).to_have_value(password)

    login_button = page.get_by_role("button", name="Login")
    login_button.hover()
    login_button.click()

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

    # xPath locator for the title element
    expect(page.locator("xpath=//span[@class='title']")).to_have_text("Products")

    page.get_by_text("Sauce Labs Backpack").click()
    expect(page).to_have_url(re.compile(r".*inventory-item.*"))
    expect(page.locator(".inventory_details_name")).to_have_text(
        "Sauce Labs Backpack"
    )

    page.go_back()

    sort_dropdown = page.locator(".product_sort_container")
    sort_dropdown.select_option("za")  # Sort Z → A
    expect(sort_dropdown).to_have_value("za")

    page.screenshot(path="test_results/test_auth/screenshot_positive_login.png")

@pytest.mark.parametrize("username, password", [
    ("standard_user",  "secret_sauce"),
    ("problem_user",   "secret_sauce"),
    ("performance_glitch_user", "secret_sauce"),
    ("error_user", "secret_sauce"),
    ("visual_user", "secret_sauce"),
])

def test_logout(page: Page, username, password):
    page.goto("https://www.saucedemo.com/")

    username_input = page.locator("#user-name")
    username_input.fill(username)
    expect(username_input).to_have_value(username)

    password_input = page.locator("#password")
    password_input.fill(password)
    expect(password_input).to_have_value(password)

    login_button = page.get_by_role("button", name="Login")
    login_button.click()

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    expect(page.locator(".inventory_list")).to_be_visible()

    menu_button = page.get_by_role("button", name="Open Menu")
    menu_button.click()

    expect(page.locator(".bm-menu-wrap")).to_have_attribute("aria-hidden", "false")
    
    expect(page.locator("#logout_sidebar_link")).to_be_visible()

    logout_link = page.get_by_role("link", name="Logout")
    expect(logout_link).to_be_visible()

    logout_link.hover()
    logout_link.press("Enter")

    expect(page).to_have_url("https://www.saucedemo.com/")

    expect(page.get_by_placeholder("Username")).to_be_visible()
    expect(page.get_by_placeholder("Password")).to_be_visible()
    expect(page.get_by_role("button", name="Login")).to_be_visible()

    page.screenshot(path="test_results/test_auth/screenshot_logout.png")
