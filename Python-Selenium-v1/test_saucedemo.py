import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from faker import Faker
fake = Faker('id_ID')

@pytest.fixture
def driver():
    # Inisialisasi WebDriver
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get('https://saucedemo.com/')
    yield driver
    driver.quit()

def login(driver, username, password):
    driver.find_element(By.CSS_SELECTOR, '[id="user-name"]').send_keys(username)
    driver.find_element(By.CSS_SELECTOR, '[id="password"]').send_keys(password)
    driver.find_element(By.CSS_SELECTOR, '[id="login-button"]').click()

def test_login_with_valid_credential(driver):
    login(driver, 'standard_user', 'secret_sauce')
    assert driver.find_element(By.ID, 'react-burger-menu-btn').is_displayed()
    driver.save_screenshot('1.login valid credential.png')

def test_login_with_invalid_credential(driver):
    login(driver, 'invalid_user', 'invalid_password')
    assert driver.find_element(By.CSS_SELECTOR, '[data-test="error"]').text == "Epic sadface: Username and password do not match any user in this service"
    driver.save_screenshot('2.login invalid credential.png')

def test_logout(driver):
    login(driver, 'standard_user', 'secret_sauce')
    driver.find_element(By.ID, 'react-burger-menu-btn').click()
    time.sleep(1)
    driver.find_element(By.ID, 'logout_sidebar_link').click()
    assert driver.find_element(By.CSS_SELECTOR, '[id="login-button"]').is_displayed()
    driver.save_screenshot('3.logout.png')

def test_login_with_empty_username_and_password(driver):
    driver.find_element(By.CSS_SELECTOR, '[id="login-button"]').click()
    assert driver.find_element(By.CSS_SELECTOR, '[data-test="error"]').text == "Epic sadface: Username is required"
    driver.save_screenshot('4.login with empty credential.png')

def test_login_with_empty_username(driver):
    login(driver,'','secret_sauce')
    assert driver.find_element(By.CSS_SELECTOR, '[data-test="error"]').text == "Epic sadface: Username is required"
    driver.save_screenshot('5.login with empty username.png')

def test_login_with_empty_password(driver):
    login(driver,'standard_user','')
    assert driver.find_element(By.CSS_SELECTOR, '[data-test="error"]').text == "Epic sadface: Password is required"
    driver.save_screenshot('6.login with empty password.png')

def test_add_item_to_cart(driver):
    login(driver,'standard_user','secret_sauce')
    driver.find_element(By.CSS_SELECTOR, '[data-test="add-to-cart-sauce-labs-backpack"]').click()
    assert driver.find_element(By.CSS_SELECTOR, '[class="shopping_cart_badge"]').text == "1"
    driver.save_screenshot('7.add item to cart.png')

def test_remove_item_from_cart(driver):
    login(driver, 'standard_user', 'secret_sauce')
    driver.find_element(By.CSS_SELECTOR, '[data-test="add-to-cart-sauce-labs-backpack"]').click()
    assert driver.find_element(By.CSS_SELECTOR, '[class="shopping_cart_badge"]').text == "1"
    driver.save_screenshot('8.add item to cart.png')

    driver.find_element(By.CSS_SELECTOR, '[data-test="remove-sauce-labs-backpack"]').click()
    assert driver.find_element(By.CSS_SELECTOR, '[data-test="inventory-item"]').is_displayed()
    driver.save_screenshot('9.remove item to cart.png')

def test_checkout(driver):
    first_name = fake.first_name()
    last_name = fake.last_name()
    postal_code = fake.postcode()

    login(driver, 'standard_user', 'secret_sauce')
    driver.find_element(By.CSS_SELECTOR, '[data-test="add-to-cart-sauce-labs-backpack"]').click()
    driver.find_element(By.CSS_SELECTOR, '[class="shopping_cart_link"]').click()
    driver.find_element(By.CSS_SELECTOR, '[data-test="checkout"]').click()
    driver.find_element(By.CSS_SELECTOR, '[data-test="firstName"]').send_keys(first_name)
    driver.find_element(By.CSS_SELECTOR, '[data-test="lastName"]').send_keys(last_name)
    driver.find_element(By.CSS_SELECTOR, '[data-test="postalCode"]').send_keys(postal_code)
    driver.save_screenshot('10.checkout data.png')
    driver.find_element(By.CSS_SELECTOR, '[data-test="continue"]').click()
    driver.find_element(By.CSS_SELECTOR, '[data-test="finish"]').click()
    driver.save_screenshot('11.checkout.png')
