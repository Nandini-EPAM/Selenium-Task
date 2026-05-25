from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CheckoutPage:
    STEP_ONE_URL = "https://www.saucedemo.com/checkout-step-one.html"
    STEP_TWO_URL = "https://www.saucedemo.com/checkout-step-two.html"
    COMPLETE_URL = "https://www.saucedemo.com/checkout-complete.html"

    # Step 1 locators
    _FIRST_NAME = (By.ID, "first-name")
    _LAST_NAME = (By.ID, "last-name")
    _POSTAL_CODE = (By.ID, "postal-code")
    _CONTINUE_BTN = (By.ID, "continue")
    _STEP1_ERROR = (By.CSS_SELECTOR, "[data-test='error']")

    # Step 2 locators
    _FINISH_BTN = (By.ID, "finish")
    _ITEM_TOTAL = (By.CLASS_NAME, "summary_subtotal_label")
    _TOTAL = (By.CLASS_NAME, "summary_total_label")

    # Complete locators
    _COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    _BACK_HOME_BTN = (By.ID, "back-to-products")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    # --- Step 1 ---
    def fill_info(self, first_name: str, last_name: str, postal_code: str):
        self.wait.until(EC.visibility_of_element_located(self._FIRST_NAME)).send_keys(first_name)
        self.driver.find_element(*self._LAST_NAME).send_keys(last_name)
        self.driver.find_element(*self._POSTAL_CODE).send_keys(postal_code)
        return self

    def click_continue(self):
        btn = self.wait.until(EC.element_to_be_clickable(self._CONTINUE_BTN))
        btn.click()
        # Wait for either navigation away (btn stale) or a validation error appearing.
        try:
            WebDriverWait(self.driver, 10).until(
                EC.any_of(
                    EC.staleness_of(btn),
                    EC.visibility_of_element_located(self._STEP1_ERROR),
                )
            )
        except Exception:
            pass
        return self

    def get_step1_error(self) -> str:
        return self.wait.until(EC.visibility_of_element_located(self._STEP1_ERROR)).text

    def is_step1_error_displayed(self) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located(self._STEP1_ERROR))
            return True
        except Exception:
            return False

    # --- Step 2 ---
    def get_item_total_text(self) -> str:
        return self.wait.until(EC.visibility_of_element_located(self._ITEM_TOTAL)).text

    def get_total_text(self) -> str:
        return self.wait.until(EC.visibility_of_element_located(self._TOTAL)).text

    def click_finish(self):
        self.wait.until(EC.element_to_be_clickable(self._FINISH_BTN)).click()
        return self

    # --- Complete ---
    def is_order_complete(self) -> bool:
        try:
            header = self.wait.until(EC.visibility_of_element_located(self._COMPLETE_HEADER))
            return "thank you" in header.text.lower()
        except Exception:
            return False

    def get_complete_header(self) -> str:
        return self.wait.until(EC.visibility_of_element_located(self._COMPLETE_HEADER)).text

    def back_to_home(self):
        self.wait.until(EC.element_to_be_clickable(self._BACK_HOME_BTN)).click()
