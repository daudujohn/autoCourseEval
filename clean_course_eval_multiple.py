import os
from os.path import abspath
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
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service

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
# TODO: Write scripts to install requirements for different os


def autoCourseEval(browser = "chrome", link = "https://moodle.cu.edu.ng/login/index.php", select_values = [
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
    """
    It takes in a list of values and then uses those values to fill in a form on a webpage
    
    :param browser: The browser to use, defaults to chrome (optional)
    :param link: The link to the web page, defaults to https://moodle.cu.edu.ng/ (optional)
    :param select_values: A list of values to be selected in the course evaluation
    :param submit: If set to True, the script will submit the form. If set to False, the script will
    only fill the form, defaults to False (optional)
    """

   # A dictionary of browsers and their corresponding webdriver.
    browsers = {
        "chrome": [webdriver.Chrome, ChromeDriverManager().install(), "browserVersion"],
        "msedge": [webdriver.Edge, EdgeChromiumDriverManager().install(), "browserVersion"], 
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
                # Adding the driver_file path to the PATH environment variable.
                os.environ["PATH"] = abspath(driver_file) + ";" + os.environ["PATH"]

                driver.get(link)

    # driver.find_element(By.XPATH, '//*[@id="page-wrapper"]/nav/ul[2]/li[2]/div/span/a').click()

    moodle_login.moodle_login(driver=driver)

    course_id  = ['9472', '9435', '9454', '9456', '9457', '9458', '9460', '9461', '9462', '8803', '8644', '8606', '8607']

    try:
        for i in range (len(course_id)):
            url = f'https://moodle.cu.edu.ng/course/view.php?id={course_id[i]}'
            driver.get(url)
            try:
                WebDriverWait(driver, 2).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept()
                print("alert accepted")
            except (selenium.common.exceptions.NoAlertPresentException, selenium.common.exceptions.TimeoutException) as e:
                print(e)

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

                    driver.execute_script("window.history.go(-2)")

                    try:
                        alert = driver.switch_to.alert
                        alert.accept()
                        print("alert accepted")
                    except (selenium.common.exceptions.NoAlertPresentException, selenium.common.exceptions.TimeoutException) as e:
                        print(e)

                except AssertionError:
                    driver.execute_script("window.history.go(-1)")
                    print(f'{course_title}: Mid-Semester course evaluation already completed')

            try:
                if "ALPHA MID-SEMESTER COURSE EVALUATION FOR 2022/2023 FOR ALL STUDENTS IS NOW OPENED" in driver.page_source: 
                    main_eval = False
                if 'COURSE EVALUATION WEEK' in driver.page_source:
                    main_eval = True
                try:
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

                            for i in range(len(navigate_options_value)):
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
                except UnboundLocalError as e:
                    print("Confirm Username and Password were entered correctly")
                    print(e)
                else: print(f'{course_title} does not contain weekly course evaluation')
                print()

            except AssertionError:
                print('Page contains no course evaluation.')
        
    except selenium.common.exceptions.NoSuchElementException:
        print('Element not found')

 
    driver.close()
    driver.quit()


autoCourseEval()