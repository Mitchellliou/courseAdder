from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
import sys
import getpass


def wait_until_visible(search_by, element):
    switcher = {
        'id': __id_visible,
        'class': __class_name_visible
    }

    return switcher.get(search_by)(element)


def __id_visible(element):
    try:
        element_present = expected_conditions.visibility_of_element_located((By.ID, element))
        WebDriverWait(driver, 10).until(element_present)
        return True
    except TimeoutException:
        print("Timed out waiting for page to load")
        return False


def __class_name_visible(element):
    try:
        element_present = expected_conditions.visibility_of_element_located((By.CLASS_NAME, element))
        WebDriverWait(driver, 10).until(element_present)
        return True
    except TimeoutException:
        print("Timed out waiting for page to load")
        return False


if len(sys.argv) != 4:
    username = input("What is your username: ")
    password = getpass.getpass("What is your password: ")
    crn = input("Enter your CRN: ")
else:
    username = sys.argv[1]
    password = sys.argv[2]
    crn = sys.argv[3]

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1000")

chrome_path = os.getcwd() + "/chromedriver"

driver = webdriver.Chrome(executable_path=chrome_path)
driver.get("https://hokiespa.vt.edu")
driver.set_page_load_timeout(30)
driver.implicitly_wait(5)

driver.find_element_by_id("username").send_keys(username)
driver.find_element_by_id("password").send_keys(password)
driver.find_element_by_class_name("btn").click()
driver.implicitly_wait(10)

driver.switch_to.frame("duo_iframe")
wait_until_visible('id', 'passcode')
driver.find_element_by_id('passcode').click()
message = driver.find_element_by_class_name('message-text').text
passcodes = ["0956848", "1476887",  "2813603",  "3966008", "4062484",  "5822102",  "6054511",  "7523422",  "8557030",  "9734070"]
driver.find_element_by_class_name("passcode-input").send_keys(passcodes[int(message[-2])])
driver.find_element_by_id('passcode').click()

driver.quit()
