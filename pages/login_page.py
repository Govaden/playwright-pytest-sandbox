from playwright.async_api import Page


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("#password")
        self.login_button = page.get_by_role("button", name="Login")
        self.error_message = page.locator("xpath=//h3[@data-test='error']")
        self.username_placeholder = page.get_by_placeholder("Username")
        self.password_placeholder = page.get_by_placeholder("Password")
        self.accepted_usernames_heading = page.get_by_role("heading", name="Accepted usernames are:")
        self.password_for_all_users_heading = page.get_by_role("heading", name="Password for all users:")

    def login(self, username: str, password: str):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()