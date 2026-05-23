from playwright.sync_api import Locator, Page

class InventoryPage:

    URL = "https://www.saucedemo.com/inventory.html"

    def __init__(self, page: Page):
        self.page = page

    # Locators

    @property
    def inventory_list(self) -> Locator:
        return self.page.locator(".inventory_list")
    
    @property
    def sort_dropdown(self) -> Locator:
        return self.page.locator(".product_sort_container")
    
    @property
    def page_title(self) -> Locator:
        return self.page.locator("xpath=//span[@class='title']")
    
    @property
    def menu_button(self) -> Locator:
        return self.page.get_by_role("button", name="Open Menu")
    
    @property
    def menu_wrapper(self) -> Locator:
        return self.page.locator(".bm-menu-wrap")
    
    @property
    def logout_sidebar_link(self) -> Locator:
        return self.page.locator("#logout_sidebar_link")
    
    @property
    def logout_link(self) -> Locator:
        return self.page.get_by_role("link", name="Logout")
    
    @property
    def item_details_name(self) -> Locator:
        return self.page.locator(".inventory_details_name")

    # Actions

    def get_product_item(self, product_name: str) -> Locator:
        """Return a locator matching the inventory item by its name."""
        return self.page.locator(".inventory_item").filter(has_text=product_name)

    def add_product_to_cart(self, product_name: str) -> None:
        self.get_product_item(product_name).get_by_role("button", name="Add to cart").click()

    def open_product(self, product_name: str) -> None:
        self.page.locator(".inventory_item_name", has_text=product_name).click()

    def sort_products(self, sort_value: str) -> None:
        """Select a sorting option by its value attribute."""
        self.sort_dropdown.select_option(sort_value)

    def open_menu(self) -> None:
        self.menu_button.click()

    def logout(self) -> None:
        self.logout_link.hover()
        self.logout_link.press("Enter")