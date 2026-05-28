import os
import time
import pyotp
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import config


def take_screenshot(driver, name="screenshot"):
    os.makedirs(config.SCREENSHOT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(config.SCREENSHOT_DIR, f"{name}_{timestamp}.png")
    driver.save_screenshot(path)
    print(f"Screenshot saved: {path}")
    return path


def wait_for_element(driver, by, locator, timeout=15):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, locator))
    )


def wait_for_clickable(driver, by, locator, timeout=15):
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, locator))
    )


def wait_for_visible(driver, by, locator, timeout=15):
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((by, locator))
    )


def wait_for_url_contains(driver, partial_url, timeout=15):
    return WebDriverWait(driver, timeout).until(
        EC.url_contains(partial_url)
    )


def wait_for_text_in_element(driver, by, locator, text, timeout=15):
    return WebDriverWait(driver, timeout).until(
        EC.text_to_be_present_in_element((by, locator), text)
    )


def get_totp_code(secret=None):
    secret = secret or config.TOTP_SECRET
    if not secret or secret == "YOUR_BASE32_TOTP_SECRET_HERE":
        raise ValueError(
            "TOTP_SECRET is not set in .env file. "
            "Get this from the QR code setup page or your authenticator app export."
        )
    totp = pyotp.TOTP(secret)
    return totp.now()


def discover_page_inputs(driver):
    """Debug helper — prints all input fields on the current page."""
    inputs = driver.find_elements(By.TAG_NAME, "input")
    print(f"\n--- Discovered {len(inputs)} input(s) on: {driver.current_url} ---")
    for i, el in enumerate(inputs):
        print(
            f"  [{i}] type={el.get_attribute('type')!r:12} "
            f"name={el.get_attribute('name')!r:20} "
            f"id={el.get_attribute('id')!r:20} "
            f"placeholder={el.get_attribute('placeholder')!r}"
        )
    buttons = driver.find_elements(By.TAG_NAME, "button")
    print(f"--- Discovered {len(buttons)} button(s) ---")
    for i, b in enumerate(buttons):
        print(f"  [{i}] text={b.text!r:20} type={b.get_attribute('type')!r}")
    print("---\n")
