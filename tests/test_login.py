import re
from playwright.sync_api import Page, expect, sync_playwright

def launch_browser(p):
    return p.chromium.launch(
        headless=True,
        slow_mo=1000,
        args=["--no-sandbox", "--disable-setuid-sandbox"]
    )

def test_page(page):

    page.goto("https://www.saucedemo.com/")

    page.screenshot(path="test_results/test_login/screenshot_login_page.png")

    buttonLocator = page.get_by_role("button", name="Login")
    page.get_by_placeholder("Password").fill("12345")
    buttonLocator.click()
    expect(page.get_by_text("Epic sadface")).to_be_visible()

    login_credentials = page.locator(".login_credentials")

    expect(login_credentials).to_contain_text("standard_user")
    expect(login_credentials).to_contain_text("locked_out_user")
    expect(login_credentials).to_contain_text("problem_user")
    expect(login_credentials).to_contain_text("performance_glitch_user")
    expect(login_credentials).to_contain_text("error_user")
    expect(login_credentials).to_contain_text("visual_user")

    expect(page.get_by_role("heading", name="Password for all users:")).to_be_visible()

    expect(page.get_by_placeholder("Username")).to_be_visible()
    expect(page.get_by_placeholder("Password")).to_be_visible()

    # Positive test case

    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")

    buttonLocator.hover()
    buttonLocator.click()

    page.screenshot(path="test_results/test_login/screenshot_login_success.png")
