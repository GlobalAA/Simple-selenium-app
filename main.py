from time import sleep
from uuid import uuid4

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import config

options = webdriver.FirefoxOptions()
options.add_argument("--headless")

driver = webdriver.Firefox(options)
driver.delete_all_cookies()

try:
	driver.get("https://github.com/login")

	username: WebElement = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'login_field')))
	password: WebElement = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'password')))

	username.clear()
	password.clear()

	username.send_keys(config.GITHUB_USER_USERNAME)
	password.send_keys(config.GITHUB_USER_PASSWORD.get_secret_value())

	password.send_keys(Keys.ENTER)
	sleep(0.5)
	driver.get("https://github.com/settings/tokens")

	WebDriverWait(driver, 3).until(
		EC.presence_of_element_located((By.XPATH, '//details[starts-with(@id, \'details\')]'))
	).click()

	WebDriverWait(driver, 3).until(
		EC.presence_of_element_located((By.XPATH, '//a[@href=\'/settings/tokens/new\']'))
	).click()

	token_name: WebElement = WebDriverWait(driver, 3).until(
		EC.presence_of_element_located((By.ID, 'oauth_access_description'))
	)
	token_name.clear()
	token_name.send_keys(str(uuid4()))

	WebDriverWait(driver, 3).until(
		EC.presence_of_element_located((By.XPATH, '//input[@value=\'repo\']'))
	).click()

	WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.ID, 'new_oauth_access'))).submit()

	token: WebElement = WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.ID, 'new-oauth-token')))

	print(f"GitHub token: {token.text}")

except TimeoutException:
	print("Timed out waiting for page to load")

except Exception as e:
	print(e)

finally:
	driver.close()
	driver.quit()