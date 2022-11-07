from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time

def fill_eval(driver, url, elements, submit = False, lecturer = False):
    """
    It takes a list of elements, and fills them into the evaluation form
    
    :param driver: The webdriver object
    :param url: The url of the evaluation page
    :param elements: A list of the answers to the questions
    :param submit: If True, the evaluation will be submitted, defaults to False (optional)
    :param lecturer: If you want to enter the lecturer for the week, set this to True, defaults to False
    (optional)
    """
    driver.get(url)
    

    for i in range(len(elements)):
        if lecturer:
            elements[-2] = input("Enter Course Lecturer for the week: ")
        driver.find_element(By.XPATH, '//*[starts-with(@id,"id_multichoice_")]').send_keys((Keys.TAB * i), elements[i])

    if submit:
        time.sleep(1)
        driver.find_element(By.LINK_TEXT, "Submit your answers").click()
        print("Evaluation Submitted.")