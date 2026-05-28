import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL           = os.getenv("BASE_URL", "https://admin.foneapp.com")
LOGIN_COUNTRY      = os.getenv("LOGIN_COUNTRY", "IN")   # 2-letter country code
LOGIN_PHONE        = os.getenv("LOGIN_PHONE", "")       # digits only, no country prefix
LOGIN_PASSWORD     = os.getenv("LOGIN_PASSWORD", "")

# Maps 2-letter country code → the visible text in the dropdown
COUNTRY_DROPDOWN_MAP = {
    "FR": "+33 FR",
    "DE": "+49 DE",
    "IN": "+91 IN",
    "JP": "+81 JP",
    "GB": "+44 GB",
    "US": "+1 US",
}
TOTP_SECRET        = os.getenv("TOTP_SECRET", "")
HEADLESS           = os.getenv("HEADLESS", "false").lower() == "true"
BROWSER            = os.getenv("BROWSER", "chrome").lower()
IMPLICIT_WAIT      = int(os.getenv("IMPLICIT_WAIT", 10))
PAGE_LOAD_TIMEOUT  = int(os.getenv("PAGE_LOAD_TIMEOUT", 30))
SCREENSHOT_DIR     = os.path.join(os.path.dirname(__file__), "screenshots")
REPORT_DIR         = os.path.join(os.path.dirname(__file__), "reports")
