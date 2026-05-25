from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    URL = "https://www.saucedemo.com/"

    # Locators
    _USERNAME = (By.ID, "user-name")
    _PASSWORD = (By.ID, "password")
    _LOGIN_BTN = (By.ID, "login-button")
    _ERROR_MSG = (By.CSS_SELECTOR, "[data-test='error']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def open(self):
        self.driver.get(self.URL)
        return self

    def enter_username(self, username: str):
        field = self.wait.until(EC.visibility_of_element_located(self._USERNAME))
        field.clear()
        field.send_keys(username)
        return self

    def enter_password(self, password: str):
        field = self.wait.until(EC.visibility_of_element_located(self._PASSWORD))
        field.clear()
        field.send_keys(password)
        return self

    def click_login(self):
        self.wait.until(EC.element_to_be_clickable(self._LOGIN_BTN)).click()
        return self

    def login(self, username: str, password: str):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        return self

    def get_error_message(self) -> str:
        return self.wait.until(EC.visibility_of_element_located(self._ERROR_MSG)).text

    def is_error_displayed(self) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located(self._ERROR_MSG))
            return True
        except Exception:
            return False
