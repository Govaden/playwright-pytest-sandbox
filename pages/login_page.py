from playwright.async_api import Locator, Page


class LoginPage:

    URL = "https://www.saucedemo.com/"

    def __init__(self, page: Page): 
        self.page = page

    # Locators

    def username_input(self) -> Locator:
        return self.page.locator("#user-name")
    
    def password_input(self) -> Locator:
        return self.page.locator("#password")
    
    def login_button(self) -> Locator:
        return self.page.get_by_role("button", name="Login")

    def error_message(self, text: str) -> Locator:
        """Return a locator matching the visible error message by its full text."""
        return self.page.get_by_text(text)
    
    def accepted_usernames_heading(self) -> Locator:
        return self.page.get_by_role("heading", name="Accepted usernames are:")
    
    def password_for_all_users_heading(self) -> Locator:
        return self.page.get_by_role("heading", name="Password for all users:")
    
    # Actions

    def open(self) -> None:
        self.page.goto(self.URL)
 
    def fill_username(self, username: str) -> None:
        self.username_input.fill(username)
 
    def fill_password(self, password: str) -> None:
        self.password_input.fill(password)

    def submit(self) -> None:
        self.login_button.click()

    def login(self, username: str, password: str) -> None:
        """Fill credentials and click Login. Skips empty fields."""
        if username:
            self.fill_username(username)
        if password:
            self.fill_password(password)
        self.submit()