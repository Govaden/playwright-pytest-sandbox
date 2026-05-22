from playwright.sync_api import Page, expect
import pytest

@pytest.mark.parametrize("first_name, last_name, postal_code", [
    ("John", "Doe", "12345"),
    ("Jane", "Smith", "54321"),
    pytest.param("", "Doe", "12345", marks=pytest.mark.xfail(reason="First name is required")),
]) 

def test_checkout(page: Page, first_name: str, last_name: str, postal_code: str):
    page.goto("https://www.saucedemo.com/")

    username_input = page.locator("#user-name")
    password_input = page.locator("#password")
    login_button = page.get_by_role("button", name="Login")

    username_input.fill("standard_user")
    password_input.fill("secret_sauce")
    login_button.click()

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    expect(page.locator(".inventory_list")).to_be_visible()

    product = page.locator(".inventory_item").filter(
        has_text="Sauce Labs Backpack"
    )

    expect(product).to_be_visible()
    product.get_by_role("button", name="Add to cart").click()

    cart_badge = page.locator(".shopping_cart_badge")
    expect(cart_badge).to_have_text("1")

    page.locator(".shopping_cart_link").click()
    expect(page).to_have_url("https://www.saucedemo.com/cart.html")

    expect(page.get_by_text("Sauce Labs Backpack")).to_be_visible()

    page.get_by_role("button", name="Checkout").click()
    expect(page).to_have_url("https://www.saucedemo.com/checkout-step-one.html")

    first_name_input = page.locator("#first-name")
    last_name_input = page.locator("#last-name")
    postal_code_input = page.locator("#postal-code")

    first_name_input.fill(first_name)
    last_name_input.fill(last_name)
    postal_code_input.fill(postal_code)

    expect(first_name_input).to_have_value(first_name)
    expect(last_name_input).to_have_value(last_name)
    expect(postal_code_input).to_have_value(postal_code)

    page.get_by_role("button", name="Continue").click()

    expect(page).to_have_url("https://www.saucedemo.com/checkout-step-two.html")

    expect(page.get_by_text("Sauce Labs Backpack")).to_be_visible()
    expect(page.locator(".summary_total_label")).to_be_visible()

    page.get_by_role("button", name="Finish").click()
    expect(page).to_have_url("https://www.saucedemo.com/checkout-complete.html")

    expect(
        page.locator("xpath=//h2[@class='complete-header']")
    ).to_have_text("Thank you for your order!")

    page.screenshot(path="test_results/test_checkout/screenshot_checkout.png")