from distutils.log import error
import requests
from bs4 import BeautifulSoup
import re
import sys
from os.path import abspath, dirname
import os
from selenium import webdriver
import selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
# import chromedriver_autoinstaller
# chromedriver_autoinstaller.install()
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service


import time
import secret
import fill_eval
import moodle_login

# TODO : add "submit immediately parameter"
# TODO : download all driver extentions and add to path
# FIXME : Find how to know the user's browser build for the correct driver
# TODO : add browser parameter
# TODO : add error handling
# TODO : Allow multiple url
# TODO : Create virtual env for package installation
# TODO: Make a log.txt that includes current time and date, browser version and course eval status


def autoCourseEval(browser = "chrome", link = "https://moodle.cu.edu.ng/", select_values = [
    'A', 
    'D',
    'D', 
    'D', 
    'A', 
    'D',
    'D', 
    'D',
    'D',
    'A', 
    'A', 
    'D',
    'SS', 
    'SS', 
    'A', 
    'D', 
    'SS', 
    'A', 
    'A', 
    'D', 
    'A', 
    'D', 
    'D', 
    'A', 
    'D',
    'D',
    'D',
    'D',
    'A', 
    'Dr. ', 
    'G'
], submit = False):
     
   # A dictionary of browsers and their corresponding webdriver.
    browsers = {
        "chrome": [webdriver.Chrome, ChromeDriverManager().install(), "browserVersion"],
        "msedge": [webdriver.Edge, EdgeChromiumDriverManager().install(), "browserVersion"], 
        # "firefox": webdriver.Firefox(GeckoDriverManager()), 
        # "safari": webdriver.Safari(.GeckoDriverManager().install())
    }

    # Checking the version of the user's browser and then adding the driver file to the PATH
    # environment variable.
    driver_files = os.listdir(".\\drivers")
    # current version of the user's broswer
    driver = browsers[browser][0](service = Service(browsers[browser][1]))
    browser_version = driver.capabilities[browsers[browser][2]][0 : 13] + browser
    if browser == "chrome":
        browser_version = driver.capabilities[browsers[browser][2]][0 : 3] + browser
    for browsers[browser] in browsers:
        for driver_file in driver_files:
            if browser_version.startswith(driver_file[0: len(browser_version)]):
                print()
                print(driver_file)
                print()
                # Adding  the driver_file path to the PATH environment variable.
                os.environ["PATH"] = abspath(driver_file) + ";" + os.environ["PATH"]

                driver.get(link)

    # WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="page-wrapper"]/nav/ul[2]/li[2]/div/span/a'))).click()
    driver.find_element(By.XPATH, '//*[@id="page-wrapper"]/nav/ul[2]/li[2]/div/span/a').click()

    # Logging in to the website.
    # driver.find_element(By.XPATH, '//*[@id="page-wrapper"]/nav/ul[2]/li[2]/div/span/a').click()
    # time.sleep(5)
    
    moodle_login.moodle_login(driver=driver)

    # driver.find_element(By.XPATH, '//*[@id="page-wrapper"]/nav/div[1]/button/i').click()

    # //*[@id="nav-drawer"]/nav/ul/li[6]/a
    # //*[@id="nav-drawer"]/nav/ul/li[6]/a/div/div/span[2]

    # //*[@id="nav-drawer"]/nav/ul/li[7]/a

    # //*[@id="nav-drawer"]/nav/ul/li[15]/a/div/div/span[2]
    # //*[@id="course-info-container-9458-5"]/div/div[1]/a/span[3]
    # //*[@id="course-info-container-9461-5"]/div/div[1]/a/span[3]
    # //*[@id="course-info-container-9457-5"]/div/div[1]/a/span[3]
    course_id  = ['9472', '9435', '9454', '9456', '9457', '9458', '9460', '9461', '9462', '8803', '8644', '8606', '8607']
    try:
        wait = WebDriverWait(driver, 20)
        ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
        for i in range (len(course_id)):
            url = f'https://moodle.cu.edu.ng/course/view.php?id={course_id[i]}'
            driver.get(url)
            course_title = driver.title[8:14]
            if "ALPHA MID-SEMESTER COURSE EVALUATION FOR 2022/2023 FOR ALL STUDENTS IS NOW OPENED" in driver.page_source: 
                url = f'https://moodle.cu.edu.ng/mod/feedback/view.php?id=27536&courseid={course_id[i]}'
                driver.get(url)
                try:
                    assert "You've already completed this activity." not in driver.page_source
                    print(f'{course_title}: New Mid-Semester course evaluation found')
                    url = driver.find_element(By.LINK_TEXT, 'Answer the questions').get_attribute('href')
                    driver.find_element(By.LINK_TEXT, 'Answer the questions').click()

                    fill_eval.fill_eval(driver=driver, url=url, elements=select_values)

                    time.sleep(5)
                    driver.execute_script("window.history.go(-1)")
                    driver.execute_script("window.history.go(-1)")

                except AssertionError:
                    driver.execute_script("window.history.go(-1)")
                    print(f'{course_title}: Mid-Semester course evaluation already completed')

            try:
                if "ALPHA MID-SEMESTER COURSE EVALUATION FOR 2022/2023 FOR ALL STUDENTS IS NOW OPENED" in driver.page_source: 
                    main_eval = False
                if 'COURSE EVALUATION WEEK' in driver.page_source:
                    main_eval = True
                if main_eval:
                    print(f'{course_title} contains course evaluation')
                    annoucement = driver.find_element(By.XPATH, '//*[starts-with(@id,"module-")]/div/div/div[2]/div[1]/a/span')
                    annoucement.click()
                    if 'Jump to...' in driver.page_source:
                        navigate = Select(driver.find_element(By.ID, "jump-to-activity"))
                        navigate_options = navigate.options
                        navigate_options_value = [option_value.text for option_value in navigate_options]
                        course_eval_filtered = [option for option in navigate_options_value if option.find('EVALUATION') != -1]
                        print(navigate_options_value)
                        print()
                        # print(course_eval_filtered)
                        for i in range(len(navigate_options_value)):
                            # navigate = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "jump-to-activity"))))
                            # WebDriverWait(driver, 10).until(EC.presence_of_element_located(navigate.select_by_visible_text(item)))
                            # print("Option loaded")
                            # navigate = WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions).until(EC.presence_(driver.find_element(By.ID, "jump-to-activity")))
                            if navigate_options_value[i] in course_eval_filtered:
                                navigate = Select(driver.find_element(By.ID, "jump-to-activity"))
                                navigate_options = navigate.options
                                navigate.select_by_visible_text(navigate_options_value[i])
                                driver.find_element(By.ID, "jump-to-activity").send_keys(Keys.ENTER)
                                if "ALPHA MID-SEMESTER COURSE EVALUATION FOR 2022/2023 FOR ALL STUDENTS IS NOW OPENED" in driver.page_source: 
                                    main_eval = False
                                    if 'course evaluation' in driver.page_source:
                                        main_eval = True
                                        if main_eval:
                                            try:
                                                assert "You've already completed this activity." not in driver.page_source
                                                print(f'{navigate_options_value[i]}: New course evaluation found')
                                                url = driver.find_element(By.LINK_TEXT, 'Answer the questions').get_attribute('href')
                                                driver.find_element(By.LINK_TEXT, 'Answer the questions').click()
                                                fill_eval.fill_eval(driver=driver, url=url, elements=select_values)

                                            except AssertionError:
                                                print(f'{navigate_options_value[i]}: Course evaluation already completed')
                            else: 
                                print(f'{navigate_options_value[i]}: No course eval here')
                else: print(f'{course_title} does not contain weekly course evaluation')
                print()

            except AssertionError:
                print('Page contains no course evaluation.')

        # print(course_elems)
        # elems = wait.until(lambda driver: driver.find_elements(By.XPATH, "//span[contains(., 'multiline')]")) #.click()
        elems = []
        for elem in elems:
            # print("id:", elem.get_attribute('id')) 
            print("href:", elem.get_attribute('href'))
            print("href:", type(elem.get_attribute('href')))
            print("outerHTML:", elem.get_attribute('outerHTML'))
            print("innerHTML:", elem.get_attribute('innerHTML'))
            print("Class Name:", elem.get_attribute('class'))
        
    except selenium.common.exceptions.NoSuchElementException:
        print('Element not found')

 
    # try:
    # 
    # elems = driver.find_elements(By.XPATH, f'/html/body/div[3]/div[3]/div/div/section[1]/div/aside/section/div/div/div[1]/div[2]/div/div/div[1]/div/div/div[1]/div/div/div[1]/a[*]/span[3]')
    # print(elems)
        # for elem in elems:
    #         print("id:", elem.get_attribute('id'))
    #         print("href:", elem.get_attribute('href'))
    #         print("outerHTML:", elem.get_attribute('outerHTML'))
    # except selenium.common.exceptions.NoSuchElementException:
    #     pass
    # cookies = driver.get_cookies()[1]
    # print(type(driver.get_cookies()))

    # req = requests.get('https://moodle.cu.edu.ng/course/view.php?id=9454')
    # print(req.text)

    # elements = {
    # "id_multichoice_117453": {
    #     "section": "A",
    #     "name": "multichoice_117453",
    #     "fieldtype": "select", 
    #     "value": select_values[0]
    # }, 
    # "id_multichoice_117454": {
    #     "section": "A",
    #     "name": "multichoice_117454",
    #     "fieldtype": "select", 
    #     "value": select_values[1]
    # }, 
    # "id_multichoice_117456": {
    #     "section": "B",
    #     "name": "multichoice_117456",
    #     "fieldtype": "select", 
    #     "value": select_values[2]
    # }, 
    # "id_multichoice_117457": {
    #     "section": "B",
    #     "name": "multichoice_117457", 
    #     "fieldtype": "select",
    #     "value": select_values[3]
    # }, 
    # "id_multichoice_117459": {
    #     "section": "C",
    #     "name": "multichoice_117459", 
    #     "fieldtype": "select",
    #     "value": select_values[4]
    # }, 
    # "id_multichoice_117460": {
    #     "section": "C",
    #     "name": "multichoice_117460", 
    #     "fieldtype": "select",
    #     "value": select_values[5]
    # }, 
    # "id_multichoice_117461": {
    #     "section": "C",
    #     "name": "multichoice_117461", 
    #     "fieldtype": "select",
    #     "value": select_values[6]
    # }, 
    # "id_multichoice_117462": {
    #     "section": "C",
    #     "name": "multichoice_117462", 
    #     "fieldtype": "select",
    #     "value": select_values[7]
    # }, 
    # "id_multichoice_117464": {
    #     "section": "D",
    #     "name": "multichoice_117464", 
    #     "fieldtype": "select",
    #     "value": select_values[8]
    # }, 
    # "id_multichoice_117465": {
    #     "section": "D",
    #     "name": "multichoice_117465", 
    #     "fieldtype": "select",
    #     "value": select_values[9]
    # }, 
    # "id_multichoice_117466": {
    #     "section": "D",
    #     "name": "multichoice_117466", 
    #     "fieldtype": "select",
    #     "value": select_values[10]
    # }, 
    # "id_multichoice_117467": {
    #     "section": "D",
    #     "name": "multichoice_117467", 
    #     "fieldtype": "select",
    #     "value": select_values[11]
    # }, 
    # "id_multichoice_117469": {
    #     "section": "E",
    #     "name": "multichoice_117469", 
    #     "fieldtype": "select",
    #     "value": select_values[12]
    # }, 
    # "id_multichoice_117470": {
    #     "section": "E",
    #     "name": "multichoice_117470", 
    #     "fieldtype": "select",
    #     "value": select_values[13]
    # }, 
    # "id_multichoice_117471": {
    #     "section": "E",
    #     "name": "multichoice_117471", 
    #     "fieldtype": "select",
    #     "value": select_values[14]
    # }, 
    # "id_multichoice_117473": {
    #     "section": "F",
    #     "name": "multichoice_117473", 
    #     "fieldtype": "select",
    #     "value": select_values[15]
    # }, 
    # "id_multichoice_117474": {
    #     "section": "F",
    #     "name": "multichoice_117474", 
    #     "fieldtype": "select",
    #     "value": select_values[16]
    # }, 
    # "id_multichoice_117475": {
    #     "section": "F",
    #     "name": "multichoice_117475", 
    #     "fieldtype": "select",
    #     "value": select_values[17]
    # }, 
    # "id_multichoice_117477": {
    #     "section": "G",
    #     "name": "multichoice_117477", 
    #     "fieldtype": "select",
    #     "value": select_values[18]
    # }, 
    # "id_multichoice_117478": {
    #     "section": "G",
    #     "name": "multichoice_117478", 
    #     "fieldtype": "select",
    #     "value": select_values[19]
    # }, 
    # "id_multichoice_117480": {
    #     "section": "H",
    #     "name": "multichoice_117480", 
    #     "fieldtype": "select",
    #     "value": select_values[20]
    # }, 
    # "id_multichoice_117481": {
    #     "section": "H",
    #     "name": "multichoice_117481", 
    #     "fieldtype": "select",
    #     "value": select_values[21]
    # }, 
    # "id_multichoice_117482": {
    #     "section": "H",
    #     "name": "multichoice_117482", 
    #     "fieldtype": "select",
    #     "value": select_values[22]
    # }, 
    # "id_multichoice_117484": {
    #     "section": "I",
    #     "name": "multichoice_117484", 
    #     "fieldtype": "select",
    #     "value": select_values[23]
    # }, 
    # "id_multichoice_117485": {
    #     "section": "I",
    #     "name": "multichoice_117485", 
    #     "fieldtype": "select",
    #     "value": select_values[24]
    # }, 
    # "id_multichoice_117487": {
    #     "section": "J",
    #     "name": "multichoice_117487", 
    #     "fieldtype": "select",
    #     "value": select_values[25]
    # }, 
    # "id_multichoice_117488": {
    #     "section": "J",
    #     "name": "multichoice_117488", 
    #     "fieldtype": "select",
    #     "value": select_values[26]
    # }, 
    # "id_multichoice_117490": {
    #     "section": "K",
    #     "name": "multichoice_117490", 
    #     "fieldtype": "select",
    #     "value": select_values[27]
    # }, 
    # "id_multichoice_117491": {
    #     "section": "K",
    #     "name": "multichoice_117491", 
    #     "fieldtype": "select",
    #     "value": select_values[28]
    # }, 
    # "id_multichoice_117494": {
    #     "section": "none",
    #     "name": "multichoice_117494", 
    #     "fieldtype": "select",
    #     "value": select_values[29]   
    # }
    # }

    # # TODO : Assert "Already completed" not in page

    # courseEvalRegex = re.compile(r"\w*\s*COURSE EVALUATION|course evaluation\s*\w*")
    # # courseEvalRegex.findall()
    # print()
    # # driver.find_elements(By.LINK_TEXT, r"\w*\s*COURSE EVALUATION|course evaluation\s*\w*")
    # # print(driver.find_elements(By.LINK_TEXT, ))
    # print()

    # # lecturer_element = driver.find_element(By.ID, "")
    # # lecturer_element.clear()
    # # lecturer_element.send_keys("Dr. ")
    # # if submit:
    # #     time.sleep(3)
    #     # driver.find_element(By.LINK_TEXT, "Submit your answers").click()

    # time.sleep(5)


    # # all_options = [option.text for option in element.options]

    # # time.sleep(3)
    driver.close()
    driver.quit()


autoCourseEval()