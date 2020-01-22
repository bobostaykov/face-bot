import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
import logging as log
import random
import time

from datatype.gender import Gender
from datatype.profile import Profile
from src.constant import *
import src.utils as utils



def generate_new_email():
    while True:
        page = requests.get(DELETE_MAIL_URL)
        soup = BeautifulSoup(page.text, 'html.parser')
        email = soup.find('input', attrs={'id': 'mail'}).get('value')
        if 'daymailonline.com' in email:
            return email



def generate_new_email2(driver):
    driver.get('https://www.fakemailgenerator.net/')
    driver.find_element_by_xpath('//a[@href = "javascript:changeMailbox()"]').click()
    driver.find_element_by_xpath('//span[text() = "More"]/..').click()
    driver.find_element_by_xpath('//a[text() = "@iffymedia.com"]').click()
    email = driver.find_element_by_xpath('//input[@title = "Click to copy"]').get_attribute('data-clipboard-text')
    return email




def generate_identity(driver):
    driver.get(FAKE_IDENTITY_URL)

    pid = utils.get_new_id()

    name = WebDriverWait(driver, WINDOW_WAIT).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'name'))).text
    first_name = name.split()[0]
    last_name = name.split()[len(name.split()) - 1]

    pass_xpath = '//a[text() = "Password Generator"]/..'
    password = WebDriverWait(driver, WINDOW_WAIT).until(expected_conditions.presence_of_element_located((By.XPATH, pass_xpath)))
    password = password.text.split('\n')[0]

    info_table = WebDriverWait(driver, WINDOW_WAIT).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'basic-face')))
    gender = info_table.find_element_by_xpath('./div[2]/p/b')
    if gender == 'male':
        gender = Gender.M
    else:
        gender = Gender.F

    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    email = generate_new_email2(driver)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    return Profile(pid, first_name, last_name, email, password, gender)




def get_fb_code(driver, email):
    driver.get(CHANGE_MAIL_URL)

    login = WebDriverWait(driver, WINDOW_WAIT).until(expected_conditions.presence_of_element_located((By.XPATH, '//input[@placeholder = "Login"]')))
    domain = Select(driver.find_element_by_id('domain'))
    save = driver.find_element_by_id('postbut')

    login.send_keys(email.split('@')[0])
    domain.select_by_visible_text('@' + email.split('@')[1])
    save.click()

    driver.get(REFRESH_MAIL_URL)

    subject = WebDriverWait(driver, FB_CODE_WAIT).until(expected_conditions.presence_of_element_located
                                                       ((By.XPATH, '//a[contains(@title, "Facebook")]'))).get_attribute('title')
    fb_code = subject.split()[0]
    return fb_code




def get_fb_code2(driver, email):
    driver.get('https://www.fakemailgenerator.net/')
    driver.find_element_by_xpath('//a[@data-original-title = "Customize mailbox"]').click()

    username = driver.find_element_by_id('user_mailbox')
    domain = Select(driver.find_element_by_id('user_mailhost'))
    save = driver.find_element_by_id('user_set')

    username.clear()
    username.send_keys(email.split('@')[0])
    domain.select_by_visible_text('@' + email.split('@')[1])
    save.click()

    driver.find_element_by_xpath('//a[@href = "javascript:manualRefresh()"]').click()

    subject = WebDriverWait(driver, FB_CODE_WAIT).until(expected_conditions.presence_of_element_located
                                                        ((By.XPATH, '//a[contains(text(), "Facebook ")]')))
    print(subject.text)
    fb_code = subject.text.split()[0]
    return fb_code




def sign_up_to_fb(driver, profile):
    driver.get(FB_HOME_URL)

    if profile.gender == Gender.M:
        gend = 2
    else:
        gend = 1

    first_name = driver.find_element_by_name('firstname')
    first_name.send_keys(profile.first_name)

    last_name = driver.find_element_by_name('lastname')
    last_name.send_keys(profile.last_name)

    email = driver.find_element_by_name('reg_email__')
    email.send_keys(profile.email)

    re_email = driver.find_element_by_name('reg_email_confirmation__')
    re_email.send_keys(profile.email)

    password = driver.find_element_by_name('reg_passwd__')
    password.send_keys(profile.password)

    birth_day = Select(driver.find_element_by_id('day'))
    birth_day.select_by_value(str(random.randint(1, 28)))
    birth_month = Select(driver.find_element_by_id('month'))
    birth_month.select_by_value(str(random.randint(1, 12)))
    birth_year = Select(driver.find_element_by_id('year'))
    birth_year.select_by_value(str(random.randint(1950, 2001)))

    gender = driver.find_element_by_xpath('//input[@name = "sex" and @value = "{}"]'.format(gend))
    gender.click()

    signup = driver.find_element_by_name('websubmit')
    signup.click()

    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    fb_code = get_fb_code2(driver, profile.email)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    # WebDriverWait(driver, WINDOW_WAIT).until(expected_conditions.presence_of_element_located((By.ID, 'checkpointSubmitButton'))).click()
    # WebDriverWait(driver, WINDOW_WAIT).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'recaptcha-checkbox-border'))).click()

    code_input = WebDriverWait(driver, WINDOW_WAIT).until(expected_conditions.presence_of_element_located((By.ID, 'code_in_cliff')))
    code_input.send_keys(fb_code)

    driver.find_element_by_name('confirm').click()

    log.info('Profile for {} {}, id {} created'.format(profile.first_name, profile.last_name, profile.pid))

    time.sleep(10)




def login(driver):
    driver.get(FB_HOME_URL)
    email = driver.find_element_by_name('email')
    password = driver.find_element_by_name('pass')

    email.send_keys('fetuzacef@cryptonet.top')
    password.send_keys('Vihrogon1000')

    driver.find_element_by_xpath('//input[@value = "Log In"]').click()

    time.sleep(10)