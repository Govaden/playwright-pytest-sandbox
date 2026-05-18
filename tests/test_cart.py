from playwright.sync_api import Page, expect

def test_cart(page: Page):
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

    page.get_by_role("button", name="Remove").click()
    
    expect(page.get_by_text("Sauce Labs Backpack")).not_to_be_visible()