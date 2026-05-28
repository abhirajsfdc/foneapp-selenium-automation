"""
Two-Factor Authentication tests for https://admin.foneapp.com

HOW TO RUN:
  pytest tests/test_2fa.py -v -m "live" -s

  The -s flag is REQUIRED — it lets the terminal show the OTP prompt
  and the countdown timer so you can type the code from your phone.

  Without -s the input prompt is hidden and the test will hang.

Test cases:
  TC09 — After valid login, OTP page appears
  TC10 — Valid OTP grants access to dashboard    (pauses for manual input)
  TC11 — Wrong OTP shows error message
  TC12 — Empty OTP field shows validation
  TC13 — Full flow: login → OTP → dashboard     (pauses for manual input)
"""
import pytest
import config
from pages.login_page import LoginPage
from pages.twofa_page import TwoFAPage
from pages.dashboard_page import DashboardPage


CREDS_MISSING = (
    not config.LOGIN_PHONE
    or not config.LOGIN_PASSWORD
    or config.LOGIN_PASSWORD == "your_password_here"
)

skip_no_creds = pytest.mark.skipif(
    CREDS_MISSING,
    reason="Set LOGIN_PHONE and LOGIN_PASSWORD in .env to run 2FA tests",
)


# ---------------------------------------------------------------------------
# Shared fixture: logs in and returns the TwoFAPage object
# ---------------------------------------------------------------------------
@pytest.fixture
def after_login(driver):
    login = LoginPage(driver)
    login.open_login()
    login.login()
    return TwoFAPage(driver), driver


# ── TC09 ─────────────────────────────────────────────────────────────────────
@pytest.mark.live
@skip_no_creds
def test_otp_screen_appears_after_login(after_login):
    """TC09: OTP input screen appears after submitting valid credentials."""
    otp_page, driver = after_login
    assert otp_page.is_otp_page(), (
        f"OTP page did not appear. Current URL: {driver.current_url}\n"
        "If login itself failed, check credentials in .env.\n"
        "If login succeeded but OTP field not found, run discover_otp.py\n"
        "and update _L.OTP_SINGLE in pages/twofa_page.py."
    )


# ── TC10 ─────────────────────────────────────────────────────────────────────
@pytest.mark.live
@skip_no_creds
def test_valid_otp_grants_dashboard_access(after_login):
    """
    TC10: User enters the OTP received on their phone → dashboard loads.

    IMPORTANT: Run with -s flag so the terminal prompt is visible:
      pytest tests/test_2fa.py::test_valid_otp_grants_dashboard_access -v -s
    """
    otp_page, driver = after_login

    # Pauses here — countdown shown — you type the OTP from your phone
    otp_page.submit_otp_manual(expiry_seconds=300)

    dashboard = DashboardPage(driver)
    assert dashboard.is_loaded(), (
        f"Dashboard did not load after OTP. URL: {driver.current_url}\n"
        "Check if OTP was typed correctly, or update _L.DASHBOARD "
        "in pages/dashboard_page.py."
    )
    dashboard.screenshot("10_dashboard_loaded")
    print(f"\nDashboard loaded. Page title: {driver.title}")


# ── TC11 ─────────────────────────────────────────────────────────────────────
@pytest.mark.live
@skip_no_creds
def test_wrong_otp_shows_error(after_login):
    """TC11: Entering an incorrect OTP shows an error message."""
    otp_page, driver = after_login
    otp_page.submit_otp_code("000000")   # deliberately wrong
    error = otp_page.get_error_message()
    assert error is not None, (
        "Expected an error for wrong OTP but none appeared.\n"
        "Update _L.ERROR_MSG in pages/twofa_page.py."
    )
    print(f"Error shown: {error!r}")


# ── TC12 ─────────────────────────────────────────────────────────────────────
@pytest.mark.live
@skip_no_creds
def test_empty_otp_shows_validation(after_login):
    """TC12: Submitting without entering OTP should not proceed."""
    from selenium.webdriver.common.by import By
    otp_page, driver = after_login
    try:
        otp_page.click(By.CSS_SELECTOR, "button[type='submit']")
    except Exception:
        pass
    still_on_otp = otp_page.is_otp_page(timeout=3)
    error = otp_page.get_error_message()
    assert still_on_otp or error is not None, (
        "Empty OTP was accepted — no validation triggered."
    )


# ── TC13 ─────────────────────────────────────────────────────────────────────
@pytest.mark.live
@skip_no_creds
def test_full_login_otp_flow(driver):
    """
    TC13: End-to-end flow — login → OTP → dashboard.

    IMPORTANT: Run with -s flag:
      pytest tests/test_2fa.py::test_full_login_otp_flow -v -s
    """
    # Step 1: Login
    login = LoginPage(driver)
    login.open_login()
    login.login()

    # Step 2: OTP — pauses for manual input
    otp_page = TwoFAPage(driver)
    assert otp_page.is_otp_page(), "OTP screen did not appear after login."
    otp_page.submit_otp_manual(expiry_seconds=300)

    # Step 3: Verify dashboard
    dashboard = DashboardPage(driver)
    assert dashboard.is_loaded(), (
        f"Dashboard not loaded after full flow. URL: {driver.current_url}"
    )
    dashboard.screenshot("13_end_to_end_success")
    print(f"\nFull flow complete. Dashboard title: {driver.title}")
