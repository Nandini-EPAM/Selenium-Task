from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage:
    URL = "https://www.saucedemo.com/cart.html"

    # Locators
    _TITLE = (By.CLASS_NAME, "title")
    _CART_ITEMS = (By.CLASS_NAME, "cart_item")
    _ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    _CHECKOUT_BTN = (By.ID, "checkout")
    _CONTINUE_SHOPPING_BTN = (By.ID, "continue-shopping")
    _REMOVE_BUTTONS = (By.CSS_SELECTOR, "button[data-test^='remove']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def is_loaded(self) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located(self._TITLE))
            return "cart" in self.driver.current_url
        except Exception:
            return False

    def get_cart_item_count(self) -> int:
        try:
            items = self.wait.until(EC.presence_of_all_elements_located(self._CART_ITEMS))
            return len(items)
        except Exception:
            return 0

    def get_item_names(self) -> list:
        names = self.wait.until(EC.presence_of_all_elements_located(self._ITEM_NAMES))
        return [n.text for n in names]

    def remove_item_by_index(self, index: int = 0):
        buttons = self.wait.until(EC.presence_of_all_elements_located(self._REMOVE_BUTTONS))
        buttons[index].click()
        return self

    def proceed_to_checkout(self):
        self.wait.until(EC.element_to_be_clickable(self._CHECKOUT_BTN)).click()

    def continue_shopping(self):
        self.wait.until(EC.element_to_be_clickable(self._CONTINUE_SHOPPING_BTN)).click()
