from selenium.webdriver.common.by import By
import os
from dotenv import load_dotenv

def moodle_login(driver):
    """
    It finds the username and password fields, clears them, enters the username and password, and clicks
    the login button
    
    :param driver: the webdriver object
    """
    load_dotenv()

    USERNAME = os.environ.get('user_name')
    PASSWORD = os.environ.get('pass_word')

    username = driver.find_element(By.ID, "username")
    password = driver.find_element(By.ID, "password")
    username.clear()
    username.send_keys(USERNAME)
    password.clear()
    password.send_keys(PASSWORD)
    driver.find_element(By.ID, "kc-login").click()
