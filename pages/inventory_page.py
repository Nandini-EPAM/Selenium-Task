from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class InventoryPage:
    URL = "https://www.saucedemo.com/inventory.html"

    # Locators
    _TITLE = (By.CLASS_NAME, "title")
    _ITEMS = (By.CLASS_NAME, "inventory_item")
    _ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    _ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "button[data-test^='add-to-cart']")
    _CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    _CART_LINK = (By.CLASS_NAME, "shopping_cart_link")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def is_loaded(self) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located(self._TITLE))
            return "inventory" in self.driver.current_url
        except Exception:
            return False

    def get_page_title(self) -> str:
        return self.wait.until(EC.visibility_of_element_located(self._TITLE)).text

    def get_item_count(self) -> int:
        items = self.wait.until(EC.presence_of_all_elements_located(self._ITEMS))
        return len(items)

    def add_item_to_cart_by_index(self, index: int = 0):
        """Add one item to the cart by its position in the list (0-based)."""
        buttons = self.wait.until(EC.presence_of_all_elements_located(self._ADD_TO_CART_BUTTONS))
        buttons[index].click()
        return self

    def add_all_items_to_cart(self):
        buttons = self.wait.until(EC.presence_of_all_elements_located(self._ADD_TO_CART_BUTTONS))
        for btn in buttons:
            btn.click()
        return self

    def get_cart_badge_count(self) -> int:
        try:
            badge = self.wait.until(EC.visibility_of_element_located(self._CART_BADGE))
            return int(badge.text)
        except Exception:
            return 0

    def go_to_cart(self):
        self.wait.until(EC.element_to_be_clickable(self._CART_LINK)).click()
