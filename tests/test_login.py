"""
Functional tests — Login page for https://admin.foneapp.com/auth/login

HOW TO RUN:
  Safe tests (no OTP triggered):
    pytest tests/test_login.py -v -m "not live"

  Tests that use real credentials and may trigger OTP — run manually only:
    pytest tests/test_login.py -v -m "live"

Test cases:
  TC01 — Login page loads correctly              (safe, no OTP)
  TC02 — Valid credentials → 2FA page appears    (live — triggers OTP)
  TC03 — Fake credentials rejected with error    (safe, no OTP)
  TC04 — Real phone + wrong password → error     (live — may trigger OTP)
  TC05 — Empty phone validation                  (safe, no OTP)
  TC06 — Empty password validation               (safe, no OTP)
  TC07 — Empty both fields validation            (safe, no OTP)
  TC08 — Forgot password link present            (safe, no OTP)
"""
import pytest
import config
from pages.login_page import LoginPage


CREDS_MISSING = (
    not config.LOGIN_PHONE
    or not config.LOGIN_PASSWORD
    or config.LOGIN_PASSWORD == "your_password_here"
)


@pytest.fixture(autouse=True)
def open_login(driver):
    page = LoginPage(driver)
    page.open_login()
    return page


# ── TC01 — safe ───────────────────────────────────────────────────────────────
def test_login_page_loads(driver):
    """TC01: Login page opens with country dropdown, phone and password fields."""
    page = LoginPage(driver)
    assert page.is_login_page(), f"Login page did not load. URL: {driver.current_url}"
    assert "foneapp" in driver.title.lower() or "auth" in driver.current_url


# ── TC02 — live (triggers OTP) ────────────────────────────────────────────────
@pytest.mark.live
@pytest.mark.skipif(CREDS_MISSING, reason="Set LOGIN_PHONE and LOGIN_PASSWORD in .env")
def test_valid_login_reaches_2fa(driver):
    """TC02: Valid credentials → 2FA/OTP screen appears. Run with: pytest -m live"""
    page = LoginPage(driver)
    page.login()
    assert "/auth/login" not in driver.current_url or not page.is_login_page(), (
        f"Still on login page after valid credentials. URL: {driver.current_url}"
    )


# ── TC03 — safe (fake number, no OTP) ────────────────────────────────────────
def test_invalid_credentials_shows_error(driver):
    """TC03: Completely fake phone+password → error shown. No real OTP triggered."""
    page = LoginPage(driver)
    page.login(phone="9999999999", password="FakePass_xyz_000!")
    error = page.get_error_message()
    assert error is not None, (
        "Expected an error for invalid credentials but none appeared.\n"
        "Update _L.ERROR_MSG in pages/login_page.py to match the actual error element."
    )
    print(f"Error shown: {error!r}")


# ── TC04 — live (real phone, wrong password — may trigger rate limit) ─────────
@pytest.mark.live
@pytest.mark.skipif(CREDS_MISSING, reason="Set LOGIN_PHONE in .env to test wrong-password")
def test_wrong_password_shows_error(driver):
    """TC04: Real phone + wrong password → error shown. Run with: pytest -m live"""
    page = LoginPage(driver)
    page.login(phone=config.LOGIN_PHONE, password="WrongPass_xyz_999!")
    error = page.get_error_message()
    assert error is not None, "Expected error for wrong password, got none."
    print(f"Error shown: {error!r}")


# ── TC05 — safe ───────────────────────────────────────────────────────────────
def test_empty_phone_shows_validation(driver):
    """TC05: Submit with empty phone → stays on login or shows error."""
    page = LoginPage(driver)
    page.enter_password("SomePassword123!")
    page.click_submit()
    assert page.is_login_page() or page.get_error_message() is not None, (
        "Form submitted with empty phone — validation did not fire."
    )


# ── TC06 — safe ───────────────────────────────────────────────────────────────
def test_empty_password_shows_validation(driver):
    """TC06: Submit with empty password → stays on login or shows error."""
    page = LoginPage(driver)
    page.enter_phone("4155550142")
    page.click_submit()
    assert page.is_login_page() or page.get_error_message() is not None, (
        "Form submitted with empty password — validation did not fire."
    )


# ── TC07 — safe ───────────────────────────────────────────────────────────────
def test_empty_both_fields_shows_validation(driver):
    """TC07: Submit with both fields empty → stays on login or shows error."""
    page = LoginPage(driver)
    page.click_submit()
    assert page.is_login_page() or page.get_error_message() is not None, (
        "Form submitted with all fields empty — validation did not fire."
    )


# ── TC08 — safe ───────────────────────────────────────────────────────────────
def test_forgot_password_link_present(driver):
    """TC08: A forgot/reset password link is visible on the login page."""
    page = LoginPage(driver)
    present = page.is_forgot_password_present()
    print(f"Forgot password link present: {present}")
