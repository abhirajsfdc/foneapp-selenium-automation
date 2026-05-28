"""
Run this script FIRST to discover all input fields and buttons on the login
and 2FA pages. Use the output to update locators in pages/login_page.py
and pages/twofa_page.py.

Usage:
  python discover.py
"""
import time
from selenium.webdriver.common.by import By
from utils.driver_factory import get_driver
from utils.helpers import discover_page_inputs, take_screenshot
import config


def inspect_page(driver, url, label):
    print(f"\n{'='*60}")
    print(f"Inspecting: {label}")
    print(f"URL: {url}")
    print(f"{'='*60}")
    driver.get(url)
    time.sleep(3)   # wait for JS to render
    discover_page_inputs(driver)
    take_screenshot(driver, f"discover_{label.lower().replace(' ', '_')}")


def main():
    driver = get_driver()
    try:
        # 1. Inspect login page
        inspect_page(driver, config.BASE_URL, "Login Page")

        # 2. If you have credentials, log in and inspect 2FA page
        if config.LOGIN_PHONE and config.LOGIN_PHONE != "4155550142":
            email_field = driver.find_element(By.ID, "login-phone")
            pwd_field   = driver.find_element(By.ID, "login-password")
            email_field.send_keys(config.LOGIN_PHONE)
            pwd_field.send_keys(config.LOGIN_PASSWORD)

            submit = driver.find_element(
                By.CSS_SELECTOR,
                "button[type='submit'], input[type='submit']"
            )
            submit.click()
            time.sleep(3)

            inspect_page(driver, driver.current_url, "After Login (2FA or Dashboard)")
        else:
            print("\nSkipping post-login inspection.")
            print("Set LOGIN_PHONE and LOGIN_PASSWORD in .env, then re-run.")

    finally:
        driver.quit()
    print("\nDone. Check the screenshots/ folder for visual reference.")


if __name__ == "__main__":
    main()
