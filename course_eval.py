from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import secret

# Opening the website in the chrome browser.
driver = webdriver.Chrome()
driver.get("https://moodle.cu.edu.ng/mod/feedback/complete.php?id=25712&courseid")

# Logging in to the website.
username = driver.find_element(By.ID, "username")
password = driver.find_element(By.ID, "password")
username.clear()
username.send_keys(secret.username)
password.clear()
password.send_keys(secret.password)
driver.find_element(By.ID, "kc-login").click()

elements = [
"id_multichoice_117453", 
"id_multichoice_117454", 
"id_multichoice_117456", 
"id_multichoice_117457", 
"id_multichoice_117459", 
"id_multichoice_117460", 
"id_multichoice_117461", 
"id_multichoice_117462", 
"id_multichoice_117464", 
"id_multichoice_117465", 
"id_multichoice_117466", 
"id_multichoice_117467", 
"id_multichoice_117469", 
"id_multichoice_117470", 
"id_multichoice_117471", 
"id_multichoice_117473", 
"id_multichoice_117474", 
"id_multichoice_117475", 
"id_multichoice_117477", 
"id_multichoice_117478", 
"id_multichoice_117480", 
"id_multichoice_117481", 
"id_multichoice_117482", 
"id_multichoice_117484", 
"id_multichoice_117485", 
"id_multichoice_117487", 
"id_multichoice_117488", 
"id_multichoice_117490", 
"id_multichoice_117491", 
]
for element in elements:
    Select(driver.find_element(By.ID, element)).select_by_visible_text("Agree")

rate_element = Select(driver.find_element(By.ID, "id_multichoice_117494")).select_by_visible_text("Good")
lecturer_element = driver.find_element(By.ID, "id_textfield_117493")
lecturer_element.clear()
lecturer_element.send_keys("Dr. ")

all_options = [option.text for option in element.options]

time.sleep(3)
# driver.quit()