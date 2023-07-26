from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType
from pyquery import PyQuery

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem

from scraper.market.util import save_file
from time import sleep
import logging
import traceback
import config as c

fh = logging.FileHandler(c.LOGGER_CONFIG['file'])
fh.setFormatter(c.LOGGER_CONFIG['formatter'])


class Request:
    selenium_retries = 0

    def __init__(self, url, domain):
        self.url = url
        self.domain = domain
        self.log = logging.getLogger('selenium_request')
        self.log.addHandler(fh)
        self.log.setLevel(c.LOGGER_CONFIG['level'])
        
        self.latitude = c.DEFAULT_LATITUDE
        self.longitude = c.DEFAULT_LONGITUDE
        self.accuracy = c.LOCATION_ACCURACY

    def get_selenium_res(self, class_name):
        try:
            self.log.info(f'starting to get html {self.url}')

            browser = webdriver.Chrome(options=Request.get_options())
            browser.get(self.url)
            
            time_to_wait = 15
            
            try:
                WebDriverWait(browser, time_to_wait).until(
                    EC.presence_of_element_located((By.CLASS_NAME, class_name)))
            finally:
                browser.maximize_window()
                
                browser.execute_cdp_cmd("Emulation.setGeolocationOverride", {
                    "latitude": self.latitude,
                    "longitude": self.longitude,
                    "accuracy": self.accuracy
                })
                
                html_page = browser.page_source

        
                save_file(f'1_{self.domain}', 'html', html_page, 'success')

                if Request.make_captcha(html_page) and 'yandex' in self.domain:
                    self.log.info('Pass captcha required in yandex')
                    browser.find_element(
                        By.CLASS_NAME, 'CheckboxCaptcha-Button').click()

                    try:
                        WebDriverWait(browser, time_to_wait).until(
                            EC.presence_of_element_located((By.CLASS_NAME, class_name)))
                    finally:
                        browser.maximize_window()
                        html_page = browser.page_source
                        html_page = self.get_html(browser)
                        save_file(f'2_{self.domain}', 'html', html_page, 'success')

                self.log.info(f'html page by {self.url} successfully got')
                browser.close()

                return html_page

        except (TimeoutError, WebDriverException):
            self.log.error(traceback.format_exc())
            sleep(6)
            self.selenium_retries += 1
            self.log.info('Selenium retry #: ' + str(self.selenium_retries))

            return self.get_selenium_res(class_name)

    def get_html(self, browser):
        time_to_wait = 15
        try:
            WebDriverWait(browser, time_to_wait).until(
                EC.presence_of_element_located((By.CLASS_NAME, class_name)))
        finally:
            browser.maximize_window()
            page_html = browser.page_source

            return page_html

    @staticmethod
    def get_options():
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1420, 1080')
        options.add_argument('--disable-gpu')
        options.add_argument(f'--user-agent={Request.get_user_agent()}')

        return options

    @staticmethod
    def get_user_agent():
        software_names = [SoftwareName.CHROME.value]
        operating_systems = [OperatingSystem.WINDOWS.value,
                             OperatingSystem.LINUX.value]

        user_agent_rotator = UserAgent(software_names=software_names,
                                       operating_systems=operating_systems,
                                       limit=100)

        user_agent = user_agent_rotator.get_random_user_agent()

        return user_agent

    @staticmethod
    def make_captcha(html: str) -> bool:
        '''
            Returns True if need to pass captcha
            Otherwise - False
        '''
        pq = PyQuery(html)

        return len(pq('input.CheckboxCaptcha-Button')) > 0
