"""
Part 1 – Automation Test for Login Functionality
Covers: positive login, negative login (wrong password, locked user, empty fields).
"""
import pytest
from utils.driver_factory import driver  # noqa: F401  (re-export fixture)
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

VALID_USER = "standard_user"
VALID_PASS = "secret_sauce"
LOCKED_USER = "locked_out_user"
WRONG_PASS = "wrong_password"


class TestLogin:

    def test_successful_login(self, driver):
        """Standard user logs in and lands on the inventory page."""
        login = LoginPage(driver).open()
        login.login(VALID_USER, VALID_PASS)
        inventory = InventoryPage(driver)
        assert inventory.is_loaded(), "Expected to land on inventory page after valid login."

    def test_inventory_title_after_login(self, driver):
        """Verify the inventory page title reads 'Products'."""
        LoginPage(driver).open().login(VALID_USER, VALID_PASS)
        assert InventoryPage(driver).get_page_title() == "Products"

    def test_wrong_password_shows_error(self, driver):
        """Login with wrong password must show an error message."""
        login = LoginPage(driver).open()
        login.login(VALID_USER, WRONG_PASS)
        assert login.is_error_displayed(), "Expected an error for wrong password."

    def test_wrong_password_error_text(self, driver):
        """Error text must mention username/password mismatch."""
        login = LoginPage(driver).open()
        login.login(VALID_USER, WRONG_PASS)
        error = login.get_error_message()
        assert "Username and password do not match" in error, f"Unexpected error: {error}"

    def test_locked_user_shows_error(self, driver):
        """Locked-out user must see a locked error message."""
        login = LoginPage(driver).open()
        login.login(LOCKED_USER, VALID_PASS)
        error = login.get_error_message()
        assert "locked out" in error.lower(), f"Unexpected error: {error}"

    def test_empty_username_shows_error(self, driver):
        """Submitting with empty username must show a validation error."""
        login = LoginPage(driver).open()
        login.login("", VALID_PASS)
        assert login.is_error_displayed(), "Expected error for empty username."

    def test_empty_password_shows_error(self, driver):
        """Submitting with empty password must show a validation error."""
        login = LoginPage(driver).open()
        login.login(VALID_USER, "")
        assert login.is_error_displayed(), "Expected error for empty password."

    def test_both_fields_empty_shows_error(self, driver):
        """Submitting with all fields empty must show a validation error."""
        login = LoginPage(driver).open()
        login.click_login()
        assert login.is_error_displayed(), "Expected error when both fields are empty."
