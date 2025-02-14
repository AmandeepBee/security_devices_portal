import logging
import os
import platform
import subprocess
import time
import unittest
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote.remote_connection import RemoteConnection
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

time_stamp = datetime.now().strftime("%m/%d/%Y")
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestBase(unittest.TestCase):
    """
    Initialization and closure of driver for each class - Globally
    """

    driver = None

    def setUp(self):
        super(TestBase, self).setUp()
        try:
            chrome_options = Options()
            chrome_options.add_argument("--start-maximized")
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.maximize_window()
            return self.driver
        except WebDriverException as e:
            print(e)
        except Exception as e:
            raise Exception(e)
        self.screenshot_counter = 0

    def tearDownClass(self):
        super(TestBase, self).tearDownClass()
        # obj_login = LoginPage(self.driver)
        # obj_login.page_refresh()
        # obj_login.click_logout()
        self.driver.quit()
