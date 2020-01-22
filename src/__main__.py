import selenium
from selenium import webdriver
import sys
import logging as log

import src.crawler as crawler
from src.constant import *
import src.utils as utils


def main():
    utils.create_logging()
    table = utils.connect_to_table()

    try:
        options = webdriver.ChromeOptions()
        # options.add_argument('--proxy-server=http://81.163.113.232:8080')
        # options.add_argument('--headless')
        options.add_argument('--disable-extensions')
        options.add_argument('--profile-directory=Default')
        options.add_argument("--incognito")
        options.add_argument("--disable-plugins-discovery")
        driver = webdriver.Chrome(options=options)
        driver.delete_all_cookies()
    except Exception as e:
        log.error('Chromedriver problem: ' + str(e))
        sys.exit()

    for i in range(ACCOUNTS):
        profile = crawler.generate_identity(driver)

        try:
            crawler.sign_up_to_fb(driver, profile)
        except selenium.common.exceptions.TimeoutException:
            log.info('Could not create profile for {} {}, id {}'.format(profile.first_name, profile.last_name, profile.pid))
            continue

        table.append_row([profile.pid, profile.first_name, profile.last_name, profile.email, profile.password])

    driver.close()



if __name__ == '__main__':
    main()