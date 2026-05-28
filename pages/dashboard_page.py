from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class _L:
    SIDEBAR     = (By.CSS_SELECTOR, "nav, aside, [class*='sidebar' i]")
    USER_AVATAR = (By.CSS_SELECTOR, "[class*='avatar' i], [class*='profile' i], [class*='user-menu' i]")
    LOGOUT_BTN  = (By.CSS_SELECTOR, "a[href*='logout'], button:contains('Logout'), a:contains('Sign out')")
    PAGE_HEADER = (By.CSS_SELECTOR, "h1, h2, .page-title, [class*='header' i]")


class DashboardPage(BasePage):

    def is_loaded(self):
        return self.is_visible(*_L.SIDEBAR, timeout=10)

    def get_page_header(self):
        if self.is_visible(*_L.PAGE_HEADER, timeout=5):
            return self.get_text(*_L.PAGE_HEADER)
        return None

    def logout(self):
        if self.is_visible(*_L.USER_AVATAR, timeout=5):
            self.click(*_L.USER_AVATAR)
        self.click(*_L.LOGOUT_BTN)
        self.screenshot("logout_clicked")
