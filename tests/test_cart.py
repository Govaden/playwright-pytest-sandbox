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

    products_to_add = [
        "Sauce Labs Backpack",
        "Sauce Labs Bike Light",
        "Sauce Labs Bolt T-Shirt"
    ]

    for product_name in products_to_add:
        page.locator(".inventory_item").filter(
            has_text=product_name
        ).get_by_role("button", name="Add to cart").click()

    expect(page.locator(".shopping_cart_badge")).to_have_text("3")

    page.locator(".shopping_cart_link").click()
    expect(page).to_have_url("https://www.saucedemo.com/cart.html")

    for product_name in products_to_add:
        expect(page.get_by_text(product_name)).to_be_visible()

    product_to_remove = "Sauce Labs Bike Light"

    page.locator(".cart_item").filter(
        has_text=product_to_remove
    ).get_by_role("button", name="Remove").click()

    expect(page.get_by_text(product_to_remove)).not_to_be_visible()
    expect(page.locator(".shopping_cart_badge")).to_have_text("2")
    remaining = [p for p in products_to_add if p != product_to_remove]
    for product_name in remaining:
        expect(page.get_by_text(product_name)).to_be_visible()

    page.screenshot(path="test_results/test_cart/screenshot_cart_remove.png")