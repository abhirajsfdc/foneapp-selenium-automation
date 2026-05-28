"""
Single-use OTP page discovery script.
Logs in ONCE, waits for the OTP screen, prints all elements + HTML, quits.

Usage:
  python discover_otp.py
"""
import time
from selenium.webdriver.common.by import By
from utils.driver_factory import get_driver
from utils.helpers import discover_page_inputs, take_screenshot
from pages.login_page import LoginPage
import config


def main():
    driver = get_driver()
    try:
        print("Logging in (one OTP will be sent)...")
        page = LoginPage(driver)
        page.open_login()
        page.login()

        print("Waiting 5 seconds for OTP screen to render...")
        time.sleep(5)
        print(f"Current URL: {driver.current_url}\n")

        discover_page_inputs(driver)
        take_screenshot(driver, "otp_screen")

        # Dump HTML of the whole page body (focus on form/OTP areas)
        html = driver.execute_script("""
            var candidates = document.querySelectorAll(
                'form, main, [class*=otp i], [class*=verify i], [class*=code i], [class*=auth i]'
            );
            return Array.from(candidates).map(el => el.outerHTML).join('\\n---\\n');
        """)
        print("=== Relevant page HTML (first 4000 chars) ===")
        print((html or "No matching elements found")[:4000])

        # Also dump full body as fallback
        body_html = driver.execute_script("return document.body.innerHTML;")
        print("\n=== Full body HTML (first 2000 chars) ===")
        print((body_html or "")[:2000])

        print("\nDone. Check screenshots/otp_screen_*.png for a visual.")

    finally:
        time.sleep(2)
        driver.quit()


if __name__ == "__main__":
    main()
