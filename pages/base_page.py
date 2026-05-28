from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.helpers import take_screenshot


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def open(self, url):
        self.driver.get(url)

    def find(self, by, locator):
        return self.wait.until(EC.presence_of_element_located((by, locator)))

    def click(self, by, locator):
        el = self.wait.until(EC.element_to_be_clickable((by, locator)))
        el.click()
        return el

    def type_text(self, by, locator, text, clear=True):
        el = self.wait.until(EC.visibility_of_element_located((by, locator)))
        if clear:
            el.clear()
        el.send_keys(text)
        return el

    def get_text(self, by, locator):
        return self.find(by, locator).text.strip()

    def is_visible(self, by, locator, timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, locator))
            )
            return True
        except Exception:
            return False

    def wait_for_url(self, partial_url, timeout=15):
        WebDriverWait(self.driver, timeout).until(EC.url_contains(partial_url))

    def wait_for_invisible(self, by, locator, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located((by, locator))
            )
        except Exception:
            pass

    def js_click(self, by, locator):
        el = self.find(by, locator)
        self.driver.execute_script("arguments[0].click();", el)
        return el

    def screenshot(self, name):
        return take_screenshot(self.driver, name)

    @property
    def current_url(self):
        return self.driver.current_url

    @property
    def title(self):
        return self.driver.title
