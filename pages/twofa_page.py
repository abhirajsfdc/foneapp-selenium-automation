"""
OTP Verification Page Object for https://admin.foneapp.com/auth/otp

Confirmed page structure (discovered 2026-05-29):
  URL         : /auth/otp?returnUrl=...
  OTP inputs  : 6 × <input class="otp-input" maxlength="1" aria-label="Digit N of 6">
  Verify btn  : button[type="submit"]  — starts DISABLED, enabled after all 6 digits filled
  Sign again  : <button class="auth-link">Sign in again</button>
  Error       : .error-banner
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from utils.otp_input import prompt_for_otp


class _L:
    OTP_DIGIT_BOXES = (By.CSS_SELECTOR, "input.otp-input")
    VERIFY_BTN      = (By.CSS_SELECTOR, "button[type='submit'].btn-primary")
    SIGN_IN_AGAIN   = (By.CSS_SELECTOR, "button.auth-link")
    ERROR_MSG       = (By.CSS_SELECTOR, ".error-banner, [role='alert'], .alert-danger")
    SPINNER         = (By.CSS_SELECTOR, ".spinner")
    DASHBOARD       = (By.CSS_SELECTOR, "nav, aside, [class*='sidebar' i], [class*='dashboard' i]")
    OTP_URL_PART    = "/auth/otp"


class TwoFAPage(BasePage):

    # ------------------------------------------------------------------
    # Detection
    # ------------------------------------------------------------------
    def is_otp_page(self, timeout=10):
        """True if we're on the OTP screen."""
        if self.OTP_URL_PART in self.current_url:
            return True
        return self.is_visible(*_L.OTP_DIGIT_BOXES, timeout=timeout)

    def is_dashboard_visible(self, timeout=10):
        return self.is_visible(*_L.DASHBOARD, timeout=timeout)

    # ------------------------------------------------------------------
    # Manual entry — pauses test, user types OTP from their phone
    # ------------------------------------------------------------------
    def submit_otp_manual(self, expiry_seconds=300):
        """
        Pauses with a countdown timer, waits for the user to type the
        OTP received on their phone, then fills all 6 boxes and submits.

        MUST run pytest with -s flag so the terminal prompt is visible.
        """
        self.screenshot("04_otp_page_loaded")
        code = prompt_for_otp(expiry_seconds=expiry_seconds, label="SMS OTP")
        self._fill_and_submit(code)

    # ------------------------------------------------------------------
    # Direct entry — you already have the code as a string
    # ------------------------------------------------------------------
    def submit_otp_code(self, code: str):
        """Enter a known OTP code directly (e.g. for negative tests)."""
        self.screenshot("04_otp_page_loaded")
        self._fill_and_submit(code)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------
    def _fill_and_submit(self, code: str):
        self.wait_for_invisible(*_L.SPINNER)

        # Wait for the 6 digit boxes to be present
        self.wait.until(
            EC.presence_of_all_elements_located(_L.OTP_DIGIT_BOXES)
        )
        boxes = self.driver.find_elements(*_L.OTP_DIGIT_BOXES)

        if len(boxes) < 6:
            raise RuntimeError(
                f"Expected 6 OTP digit boxes, found {len(boxes)}. "
                "Run discover_otp.py to re-inspect the OTP page."
            )

        # Pad or truncate code to 6 digits
        code = code.strip()[:6].ljust(6, "0")

        for box, digit in zip(boxes, code):
            box.clear()
            box.send_keys(digit)

        # Wait for Verify button to become enabled (Angular enables it after all digits filled)
        self.wait.until(
            EC.element_to_be_clickable(_L.VERIFY_BTN)
        )
        self.screenshot("05_otp_entered")
        self.click(*_L.VERIFY_BTN)
        self.wait_for_invisible(*_L.SPINNER)
        self.screenshot("06_after_otp_submit")

    def get_error_message(self):
        if self.is_visible(*_L.ERROR_MSG, timeout=5):
            return self.get_text(*_L.ERROR_MSG)
        return None

    def click_sign_in_again(self):
        """Goes back to login page to request a fresh OTP."""
        self.click(*_L.SIGN_IN_AGAIN)
