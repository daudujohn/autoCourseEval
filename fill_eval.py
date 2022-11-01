from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

import time

def fill_eval(driver, url, elements, submit = False, lecturer = False):
    driver.get(url)
    # driver.find_element(By.CLASS_NAME, "custom-select").send_keys(Keys.TAB)
    # select_options = select.options
    # select_options_value = [option_value.text for option_value in select_options]
    # print(select_options_value)
    # select.select_by_visible_text(select_options_value[i])
    # # driver.find_element(By.CLASS_NAME, """custom-select
                       
    # #                    """).send_keys(Keys.ENTER)

    for i in range(len(elements)):
        # driver.send_keys(Keys.TAB * 10)
        # select.select_by_visible_text(select_options_value[i])
        # //*[@id="id_multichoice_117496"]
        # //*[@id="id_multichoice_124707"]
        if lecturer:
            elements[-2] = input("Enter Course Lecturer for the week: ")
        driver.find_element(By.XPATH, '//*[starts-with(@id,"id_multichoice_")]').send_keys((Keys.TAB * i), elements[i])

        # driver.send_keys( '\ue004' )
    # lecturer_element = driver.find_element(By.CLASS_NAME, "form-control is-invalid")
    # print('lecturer')

    # lecturer_element.clear()
    # if lecturer:
    #     my_lecturer = input("Enter Course Lecturer for the week: ")
    #     lecturer_element.send_keys(my_lecturer)
    # else: lecturer_element.send_keys("Dr. ")
    if submit:
        time.sleep(3)
        driver.find_element(By.LINK_TEXT, "Submit your answers").click()

