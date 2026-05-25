# Selenium-Task
performing - Part 1:  Automation Test for Login Functionality (Pytest + Selenium) and Part 2:  Automation Test for Shopping Cart (Pytest + Selenium)

# SauceDemo Automation Framework

## Project Overview

This project contains an automated test suite developed using Python, Selenium WebDriver, and PyTest for testing the functionality of the SauceDemo website:

https://www.saucedemo.com/

The framework is designed using the Page Object Model (POM) design pattern to improve maintainability, reusability, and scalability of the automation code.

The automation suite covers:

- Login functionality testing
- Shopping cart functionality testing
- Checkout process validation
- Positive and negative test scenarios
- Validation of UI elements and error messages

---

# Tech Stack

- Python
- Selenium WebDriver
- PyTest
- WebDriver Manager
- PyTest HTML Report

---

# Framework Design

The framework follows the Page Object Model (POM) architecture.

## Project Structure

```text
saucedemo_automation/
│
├── pages/
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py
│
├── tests/
│   ├── test_login.py
│   └── test_cart.py
│
├── utils/
│   └── driver_factory.py
│
├── reports/
│
├── requirements.txt
├── pytest.ini
└── README.md