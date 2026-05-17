import re
from playwright.sync_api import Page, expect

def test_negative_login(page: Page):

    page.goto("https://www.saucedemo.com/")

    expect(page.get_by_placeholder("Username")).to_be_visible()
    expect(page.get_by_placeholder("Password")).to_be_visible()

    expect(page.get_by_role("heading", name="Accepted usernames are:")).to_be_visible()
    expect(page.get_by_role("heading", name="Password for all users:")).to_be_visible()
    
    login_button = page.get_by_role("button", name="Login")
    expect(login_button).to_be_visible()

    username_input = page.locator("#user-name")
    password_input = page.locator("#password")

    username_input.press("Enter")
    expect(page.get_by_text("Epic sadface: Username is required")).to_be_visible()

    username_input.fill("test_user")
    username_input.press("Tab")
    login_button.click()
    expect(page.get_by_text("Epic sadface: Password is required")).to_be_visible()

    # XPath locator
    expect(page.locator("xpath=//h3[@data-test='error']")).to_be_visible()

    username_input.fill("standard_user")
    password_input.fill("12345")
    login_button.click()

    error_message = page.get_by_text(
        "Epic sadface: Username and password do not match any user in this service")
    expect(error_message).to_be_visible()

    page.screenshot(path="test_results/test_login/screenshot_negative_login.png")

def test_positive_login(page: Page):
    page.goto("https://www.saucedemo.com/")

    username_input = page.locator("#user-name")
    username_input.fill("standard_user")
    expect(username_input).to_have_value("standard_user")

    password_input = page.locator("#password")
    password_input.fill("secret_sauce")
    expect(password_input).to_have_value("secret_sauce")

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

    page.screenshot(path="test_results/test_login/screenshot_positive_login.png")
