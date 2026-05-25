"""
Part 2 – Automation Test for Shopping Cart & Checkout
Covers: add item, cart count, remove item, full checkout flow, empty-info validation.
"""
import pytest
from utils.driver_factory import driver  # noqa: F401  (re-export fixture)
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

VALID_USER = "standard_user"
VALID_PASS = "secret_sauce"


def _logged_in_inventory(driver):
    """Helper: open the site, log in, return InventoryPage."""
    LoginPage(driver).open().login(VALID_USER, VALID_PASS)
    return InventoryPage(driver)


class TestShoppingCart:

    def test_add_one_item_updates_badge(self, driver):
        """Adding one item must set the cart badge to 1."""
        inv = _logged_in_inventory(driver)
        inv.add_item_to_cart_by_index(0)
        assert inv.get_cart_badge_count() == 1

    def test_add_multiple_items_updates_badge(self, driver):
        """Adding two items must set the cart badge to 2."""
        inv = _logged_in_inventory(driver)
        inv.add_item_to_cart_by_index(0)
        inv.add_item_to_cart_by_index(1)
        assert inv.get_cart_badge_count() == 2

    def test_cart_page_shows_added_item(self, driver):
        """After adding one item the cart page must list exactly one item."""
        inv = _logged_in_inventory(driver)
        inv.add_item_to_cart_by_index(0)
        inv.go_to_cart()
        cart = CartPage(driver)
        assert cart.is_loaded(), "Expected cart page to load."
        assert cart.get_cart_item_count() == 1

    def test_remove_item_from_cart(self, driver):
        """Removing the only item from the cart must leave cart empty."""
        inv = _logged_in_inventory(driver)
        inv.add_item_to_cart_by_index(0)
        inv.go_to_cart()
        cart = CartPage(driver)
        cart.remove_item_by_index(0)
        assert cart.get_cart_item_count() == 0

    def test_cart_preserves_item_names(self, driver):
        """Item names shown on the inventory page must match those in the cart."""
        inv = _logged_in_inventory(driver)
        # Capture name before adding
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        wait = WebDriverWait(driver, 15)
        item_name_els = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "inventory_item_name")))
        first_item_name = item_name_els[0].text
        inv.add_item_to_cart_by_index(0)
        inv.go_to_cart()
        cart = CartPage(driver)
        assert first_item_name in cart.get_item_names()


class TestCheckout:

    def _add_and_go_to_checkout(self, driver):
        inv = _logged_in_inventory(driver)
        inv.add_item_to_cart_by_index(0)
        inv.go_to_cart()
        CartPage(driver).proceed_to_checkout()
        return CheckoutPage(driver)

    def test_checkout_step1_renders(self, driver):
        """Checkout step-1 page loads after clicking Checkout."""
        checkout = self._add_and_go_to_checkout(driver)
        assert "checkout-step-one" in driver.current_url

    def test_checkout_empty_info_shows_error(self, driver):
        """Submitting checkout step-1 without filling info must show an error."""
        checkout = self._add_and_go_to_checkout(driver)
        checkout.click_continue()
        assert checkout.is_step1_error_displayed(), "Expected validation error for empty info."

    def test_full_checkout_flow(self, driver):
        """Complete a full checkout from adding item to the confirmation screen."""
        checkout = self._add_and_go_to_checkout(driver)
        checkout.fill_info("Jane", "Doe", "12345").click_continue()
        assert "checkout-step-two" in driver.current_url, "Expected to reach step 2."
        checkout.click_finish()
        assert checkout.is_order_complete(), "Expected order completion confirmation."

    def test_checkout_complete_header_text(self, driver):
        """Order complete screen must say 'Thank you for your order!'."""
        checkout = self._add_and_go_to_checkout(driver)
        checkout.fill_info("Jane", "Doe", "12345").click_continue()
        checkout.click_finish()
        header = checkout.get_complete_header()
        assert "Thank you" in header, f"Unexpected header: {header}"
