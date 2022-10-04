from lib2to3.pgen2.driver import Driver
import sys
from os.path import abspath, dirname
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
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
# TODO : add "submit immediately parameter"
# TODO : download all driver extentions and add to path
# FIXME : Find how to know the user's browser build for the correct driver
# TODO : add browser parameter
# TODO : add error handling
# TODO : Allow multiple url

def autoCourseEval(browser = "msedge", select_values = [
        "Agree", 
        "Disagree", 
        "Disagree", 
        "Disagree", 
        "Agree", 
        "Disagree", 
        "Disagree", 
        "Disagree", 
        "Disagree", 
        "Agree", 
        "Agree", 
        "Disagree", 
        "Strongly Disagree", 
        "Strongly Disagree", 
        "Agree", 
        "Disagree", 
        "Strongly Disagree", 
        "Agree", 
        "Agree", 
        "Disagree", 
        "Agree", 
        "Disagree", 
        "Disagree", 
        "Agree", 
        "Disagree", 
        "Disagree", 
        "Disagree", 
        "Disagree", 
        "Agree", 
        "Good"
    ], submit = False):
    cwd = os.getcwd()
    # Adding the path to the chromedriver.exe to the PATH environment variable.
    # os.environ["PATH"] += ";" + abspath(r"drivers\msedgedriver.exe")   
    # sys.path.insert(0, abspath("msedgedriver.exe"))
     
   # A dictionary of browsers and their corresponding webdriver.
    browsers = {
        "chrome": [webdriver.Chrome, ChromeDriverManager().install(), "browserVersion"],
        "msedge": [webdriver.Edge, EdgeChromiumDriverManager().install(), "browserVersion"], 
        # "firefox": webdriver.Firefox(GeckoDriverManager()), 
        # "safari": webdriver.Safari(.GeckoDriverManager().install())
    }

    # Checking if the browser version is the same as the driver version.
    driver_files = os.listdir(".\\drivers")
    driver = browsers[browser][0](service = Service(browsers[browser][1]))
    # current version of the user's broswer
   

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

                driver.get("https://moodle.cu.edu.ng/mod/feedback/complete.php?id=25712&courseid")

    # Logging in to the website.
    username = driver.find_element(By.ID, "username")
    password = driver.find_element(By.ID, "password")
    username.clear()
    username.send_keys(secret.username)
    password.clear()
    password.send_keys(secret.password)
    driver.find_element(By.ID, "kc-login").click()

    # TODO : Assert "Already completed" not in page
    elements = {
    "id_multichoice_117453": {
        "section": "A",
        "name": "multichoice_117453",
        "fieldtype": "select", 
        "value": select_values[0]
    }, 
    "id_multichoice_117454": {
        "section": "A",
        "name": "multichoice_117454",
        "fieldtype": "select", 
        "value": select_values[1]
    }, 
    "id_multichoice_117456": {
        "section": "B",
        "name": "multichoice_117456",
        "fieldtype": "select", 
        "value": select_values[2]
    }, 
    "id_multichoice_117457": {
        "section": "B",
        "name": "multichoice_117457", 
        "fieldtype": "select",
        "value": select_values[3]
    }, 
    "id_multichoice_117459": {
        "section": "C",
        "name": "multichoice_117459", 
        "fieldtype": "select",
        "value": select_values[4]
    }, 
    "id_multichoice_117460": {
        "section": "C",
        "name": "multichoice_117460", 
        "fieldtype": "select",
        "value": select_values[5]
    }, 
    "id_multichoice_117461": {
        "section": "C",
        "name": "multichoice_117461", 
        "fieldtype": "select",
        "value": select_values[6]
    }, 
    "id_multichoice_117462": {
        "section": "C",
        "name": "multichoice_117462", 
        "fieldtype": "select",
        "value": select_values[7]
    }, 
    "id_multichoice_117464": {
        "section": "D",
        "name": "multichoice_117464", 
        "fieldtype": "select",
        "value": select_values[8]
    }, 
    "id_multichoice_117465": {
        "section": "D",
        "name": "multichoice_117465", 
        "fieldtype": "select",
        "value": select_values[9]
    }, 
    "id_multichoice_117466": {
        "section": "D",
        "name": "multichoice_117466", 
        "fieldtype": "select",
        "value": select_values[10]
    }, 
    "id_multichoice_117467": {
        "section": "D",
        "name": "multichoice_117467", 
        "fieldtype": "select",
        "value": select_values[11]
    }, 
    "id_multichoice_117469": {
        "section": "E",
        "name": "multichoice_117469", 
        "fieldtype": "select",
        "value": select_values[12]
    }, 
    "id_multichoice_117470": {
        "section": "E",
        "name": "multichoice_117470", 
        "fieldtype": "select",
        "value": select_values[13]
    }, 
    "id_multichoice_117471": {
        "section": "E",
        "name": "multichoice_117471", 
        "fieldtype": "select",
        "value": select_values[14]
    }, 
    "id_multichoice_117473": {
        "section": "F",
        "name": "multichoice_117473", 
        "fieldtype": "select",
        "value": select_values[15]
    }, 
    "id_multichoice_117474": {
        "section": "F",
        "name": "multichoice_117474", 
        "fieldtype": "select",
        "value": select_values[16]
    }, 
    "id_multichoice_117475": {
        "section": "F",
        "name": "multichoice_117475", 
        "fieldtype": "select",
        "value": select_values[17]
    }, 
    "id_multichoice_117477": {
        "section": "G",
        "name": "multichoice_117477", 
        "fieldtype": "select",
        "value": select_values[18]
    }, 
    "id_multichoice_117478": {
        "section": "G",
        "name": "multichoice_117478", 
        "fieldtype": "select",
        "value": select_values[19]
    }, 
    "id_multichoice_117480": {
        "section": "H",
        "name": "multichoice_117480", 
        "fieldtype": "select",
        "value": select_values[20]
    }, 
    "id_multichoice_117481": {
        "section": "H",
        "name": "multichoice_117481", 
        "fieldtype": "select",
        "value": select_values[21]
    }, 
    "id_multichoice_117482": {
        "section": "H",
        "name": "multichoice_117482", 
        "fieldtype": "select",
        "value": select_values[22]
    }, 
    "id_multichoice_117484": {
        "section": "I",
        "name": "multichoice_117484", 
        "fieldtype": "select",
        "value": select_values[23]
    }, 
    "id_multichoice_117485": {
        "section": "I",
        "name": "multichoice_117485", 
        "fieldtype": "select",
        "value": select_values[24]
    }, 
    "id_multichoice_117487": {
        "section": "J",
        "name": "multichoice_117487", 
        "fieldtype": "select",
        "value": select_values[25]
    }, 
    "id_multichoice_117488": {
        "section": "J",
        "name": "multichoice_117488", 
        "fieldtype": "select",
        "value": select_values[26]
    }, 
    "id_multichoice_117490": {
        "section": "K",
        "name": "multichoice_117490", 
        "fieldtype": "select",
        "value": select_values[27]
    }, 
    "id_multichoice_117491": {
        "section": "K",
        "name": "multichoice_117491", 
        "fieldtype": "select",
        "value": select_values[28]
    }, 
    "id_multichoice_117494": {
        "section": "none",
        "name": "multichoice_117494", 
        "fieldtype": "select",
        "value": select_values[29]   
    }
    }

    for element in elements:
        Select(driver.find_element(By.ID, element)).select_by_visible_text(elements[element]["value"])

    lecturer_element = driver.find_element(By.ID, "id_textfield_117493")
    lecturer_element.clear()
    lecturer_element.send_keys("Dr. ")
    if submit:
        time.sleep(3)
        driver.find_element(By.LINK_TEXT, "Submit your answers").click()

    time.sleep(5)


    # all_options = [option.text for option in element.options]

    # time.sleep(3)
    # driver.quit()



autoCourseEval()