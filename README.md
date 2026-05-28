# FoneApp Admin Portal — Selenium Automation

Automated functional test suite for the FoneApp admin web portal.  
Built with **Python + Selenium + Pytest** using the **Page Object Model (POM)** pattern.

## Test Coverage

| # | Module | Test Case | Type |
|---|---|---|---|
| TC01 | Login | Page loads with all fields visible | Safe |
| TC02 | Login | Valid credentials accepted | Live |
| TC03 | Login | Invalid credentials rejected with error | Safe |
| TC04 | Login | Wrong password shows error | Live |
| TC05 | Login | Empty phone field validation | Safe |
| TC06 | Login | Empty password field validation | Safe |
| TC07 | Login | Both fields empty validation | Safe |
| TC08 | Login | Forgot password link present | Safe |
| TC09 | 2FA | OTP screen appears after login | Live |
| TC10 | 2FA | Valid OTP grants dashboard access | Live |
| TC11 | 2FA | Wrong OTP shows error | Live |
| TC12 | 2FA | Empty OTP field validation | Live |
| TC13 | 2FA | End-to-end login → OTP → dashboard | Live |

## Project Structure

```
├── pages/
│   ├── base_page.py        # Shared Selenium helpers
│   ├── login_page.py       # Login page interactions
│   ├── twofa_page.py       # OTP/2FA page interactions
│   └── dashboard_page.py   # Post-login dashboard
├── tests/
│   ├── test_login.py       # TC01–TC08
│   └── test_2fa.py         # TC09–TC13
├── utils/
│   ├── driver_factory.py   # Chrome/Firefox setup
│   ├── helpers.py          # Waits, screenshots
│   └── otp_input.py        # Manual OTP entry with countdown
├── conftest.py             # Pytest fixtures
├── config.py               # Settings loader
├── requirements.txt        # Dependencies
└── .env.example            # Credential template
```

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/abhirajsfdc/foneapp-selenium-automation.git
cd foneapp-selenium-automation

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your credentials
copy .env.example .env
# Edit .env with your login details
```

## Running Tests

```bash
# Safe tests — no OTP triggered, run anytime
pytest tests/test_login.py -v -m "not live"

# Full 2FA flow — have your phone ready, type OTP when prompted
pytest tests/test_2fa.py::test_full_login_otp_flow -v -s

# All tests
pytest -v
```

## Tech Stack

- **Language:** Python 3.12
- **Automation:** Selenium WebDriver 4.x
- **Test Runner:** Pytest
- **Pattern:** Page Object Model (POM)
- **Browser:** Chrome (via WebDriver Manager — no manual driver setup)
- **Reporting:** pytest-html
