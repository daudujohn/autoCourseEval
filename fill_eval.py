from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time

def fill_eval(driver, url, elements, submit = False, lecturer = False):
    driver.get(url)
    

    for i in range(len(elements)):
        if lecturer:
            elements[-2] = input("Enter Course Lecturer for the week: ")
        driver.find_element(By.XPATH, '//*[starts-with(@id,"id_multichoice_")]').send_keys((Keys.TAB * i), elements[i])

    if submit:
        time.sleep(3)
        driver.find_element(By.LINK_TEXT, "Submit your answers").click()

