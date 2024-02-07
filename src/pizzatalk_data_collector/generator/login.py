import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def bypassing_cloudflare(driver):
    WebDriverWait(driver, 4).until(
        EC.presence_of_element_located((By.ID, "challenge-form"))
    )
    driver.find_element(By.ID, "challenge-form").click()


def login_openai(driver, email_address, password):
    wait = WebDriverWait(driver, 10)

    wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'button[data-testid="login-button"]')
        )
    ).click()

    wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'input[name="username"]')
        )
    ).send_keys(email_address)

    driver.find_element(By.CSS_SELECTOR, 'button[name="action"]').click()

    wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'input[name="password"]')
        )
    ).send_keys(password)

    driver.find_element(
        By.CSS_SELECTOR, 'button[data-action-button-primary="true"]'
    ).click()
