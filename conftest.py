import os
import pytest
from utils.driver_factory import get_driver
from utils.helpers import take_screenshot
import config as app_config


def pytest_configure(config):
    os.makedirs(app_config.SCREENSHOT_DIR, exist_ok=True)
    os.makedirs(app_config.REPORT_DIR, exist_ok=True)


@pytest.fixture(scope="function")
def driver():
    """Provides a fresh browser for each test; quits after."""
    d = get_driver()
    yield d
    d.quit()


@pytest.fixture(scope="session")
def driver_session():
    """Shared browser for the whole test session (use carefully)."""
    d = get_driver()
    yield d
    d.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Auto-screenshot on test failure."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver") or item.funcargs.get("driver_session")
        if driver:
            test_name = item.name.replace("/", "_").replace(" ", "_")
            take_screenshot(driver, f"FAIL_{test_name}")
