"""
Login Page Object for https://admin.foneapp.com/auth/login

Page structure (confirmed via JS inspection 2026-05-29):
  Country dropdown : <select aria-label="Country code"> — options like "+91 IN"
  Phone input      : id="login-phone"  (digits only, no country prefix)
  Password input   : id="login-password"
  Submit button    : button[type="submit"]  text="Sign in"
  Spinner overlay  : .spinner  (Angular loading overlay — must disappear before clicking)
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage
import config


class _L:
    COUNTRY_SELECT = (By.CSS_SELECTOR, "select[aria-label='Country code']")
    PHONE_INPUT    = (By.ID, "login-phone")
    PASSWORD_INPUT = (By.ID, "login-password")
    SUBMIT_BTN     = (By.CSS_SELECTOR, "button[type='submit']")
    SPINNER        = (By.CSS_SELECTOR, ".spinner")
    ERROR_MSG      = (By.CSS_SELECTOR, ".error, .alert-danger, [class*='error' i], [role='alert'], .toast-error")
    FORGOT_LINK    = (By.CSS_SELECTOR, "a[href*='forgot'], a[href*='reset'], a[href*='password']")


class LoginPage(BasePage):
    URL = f"{config.BASE_URL}/auth/login"

    def open_login(self):
        self.open(self.URL)
        self.wait_for_invisible(*_L.SPINNER)
        self.screenshot("01_login_page_opened")

    def select_country(self, country_code=None):
        country_code = country_code or config.LOGIN_COUNTRY
        visible_text = config.COUNTRY_DROPDOWN_MAP.get(country_code.upper())
        if not visible_text:
            raise ValueError(
                f"Country code '{country_code}' not in COUNTRY_DROPDOWN_MAP. "
                f"Supported: {list(config.COUNTRY_DROPDOWN_MAP.keys())}"
            )
        select_el = self.find(*_L.COUNTRY_SELECT)
        Select(select_el).select_by_visible_text(visible_text)

    def enter_phone(self, phone):
        # Strip any accidental spaces, +, or country code the user may have typed
        digits_only = "".join(filter(str.isdigit, str(phone)))
        self.type_text(*_L.PHONE_INPUT, digits_only)

    def enter_password(self, password):
        self.type_text(*_L.PASSWORD_INPUT, password)

    def click_submit(self):
        self.wait_for_invisible(*_L.SPINNER)
        try:
            self.click(*_L.SUBMIT_BTN)
        except Exception:
            self.js_click(*_L.SUBMIT_BTN)

    def login(self, country=None, phone=None, password=None):
        self.select_country(country or config.LOGIN_COUNTRY)
        self.enter_phone(phone or config.LOGIN_PHONE)
        self.enter_password(password or config.LOGIN_PASSWORD)
        self.screenshot("02_credentials_entered")
        self.click_submit()
        self.wait_for_invisible(*_L.SPINNER)
        self.screenshot("03_after_submit")

    def get_error_message(self):
        if self.is_visible(*_L.ERROR_MSG, timeout=6):
            return self.get_text(*_L.ERROR_MSG)
        return None

    def is_login_page(self):
        return self.is_visible(*_L.PHONE_INPUT, timeout=8)

    def is_forgot_password_present(self):
        return self.is_visible(*_L.FORGOT_LINK, timeout=5)
