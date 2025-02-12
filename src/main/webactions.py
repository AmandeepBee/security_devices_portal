import calendar
import csv
import os
import platform
import time
import unittest

import requests
import json
from configparser import NoOptionError, ConfigParser

from astroid import arguments
from selenium.webdriver.support.color import Color
from random import randint
import numpy as np
import pytz
import string
import random

from selenium.common import exceptions
from selenium.common.exceptions import (
    StaleElementReferenceException,
    ElementClickInterceptedException,
    TimeoutException,
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime, timedelta, date

from src.main.locators.message_center_menu import MessageCenterLocators

config = ConfigParser()
project_root = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(project_root, "config")
config.read(config_path)
system = platform.system()
if system == "Windows":
    env_path = os.path.join(project_root, "..\env")
else:
    env_path = os.path.join(project_root, "../env")
config.read(config_path)
file1 = open(env_path, "r")
file_values = file1.readlines()
file1.close()
env = file_values[0].split("\n")[0]
target_execution = file_values[1].split("\n")[0]
path = os.getcwd()
env = os.getenv("TARGET_ENV", env)
employee_username = config.get(env, "employee_username")
employee_password = config.get(env, "employee_password")
onpatient_url = config.get(env, "onpatient_url")
outlook_username = config.get(env, "outlook_username")
outlook_password = config.get(env, "outlook_password")

eastern_time = pytz.timezone("US/Eastern")


class BasePage(unittest.TestCase):
    """
    This is base web action class
    """

    def __init__(self, driver):
        """
        constructor of class
        @param self : this is refer to instance of object
        """
        self.driver = driver
        self.timeout = 50
        self.explicit_wait = WebDriverWait(
            self.driver, timeout=self.timeout, poll_frequency=1, ignored_exceptions=None
        )
        self.env_timeout = 1
        self.timeout_multiplier = 1
        super().__init__()
        try:
            self.env_timeout = 1
        except NoOptionError:
            self.env_timeout = 0
        try:
            self.env_timeout_multiplier = 1
        except NoOptionError:
            self.env_timeout_multiplier = 1
        self.env_timeout_total = self.env_timeout * self.timeout_multiplier
        self.driver = driver

    def find_element(self, locator, element=None, explicit_wait=True):
        if element is not None:
            return element.find_element(locator)
        elif explicit_wait:
            return self.explicit_wait.until(EC.visibility_of_element_located(locator))
        else:
            return self.driver.find_element(locator)

    def find_elements(self, locator, element=None):
        if element is not None:
            return element.find_elements(locator)
        else:
            return self.explicit_wait.until(
                EC.visibility_of_all_elements_located(locator)
            )

    def find_clickable_element(self, locator, element=None):
        if element is not None:
            found_element = element.find_element(locator)
            return found_element
        else:
            return self.explicit_wait.until(EC.element_to_be_clickable(locator))

    def find_clickable_ele(self, locator, element=None):
        if element is not None:
            found_element = element.find_element(locator)
            return found_element
        else:
            return self.explicit_wait.until(EC.element_to_be_clickable(locator))

    def find_visibility_of_element(self, locator, element=None):
        if element is not None:
            found_element = element.find_element(locator)
            return found_element
        else:
            return self.explicit_wait.until(EC.visibility_of_element_located(locator))

    def is_enabled(self, locator):
        """This method check element is enabled or not"""

        element = self.find_element(locator)
        state = element.is_enabled()
        return state

    def click(self, locator):
        """
        This method is used to click the element
        :@param driver :get locator from locators module
        """
        try:
            element = self.find_clickable_element(locator)
            ActionChains(self.driver).move_to_element(
                self.find_element(locator)
            ).perform()
            element_visible = self.is_displayed(locator)
            if not element_visible:
                self.driver.execute_script(
                    "arguments[0].scrollIntoView();",
                    self.find_clickable_element(locator),
                )
            time.sleep(1)
            element.click()
        except ElementClickInterceptedException:
            self.click_via_script(locator)
        except StaleElementReferenceException:
            return False

    def click_open_in_new_tab(self, locator):
        """
        This method is used to click open the element in new tab
        """
        self.find_clickable_element(locator)
        element = self.find_element(locator)
        element.send_keys(Keys.CONTROL + Keys.ENTER)

    def click_via_actionchains_offset(self, locator, x=100, y=100):
        """
        This method is used to click the element by actionchain
        :@param locator :get locator from locators module
        """
        element = self.find_clickable_element(locator)
        ActionChains(self.driver).move_to_element_with_offset(
            element, x, y
        ).click().perform()

    def click_via_actionchains_tab(self, locator):
        """
        This method is used to click the element by actionchain
        :@param locator :get locator from locators module
        """
        element = self.find_clickable_element(locator)
        ActionChains(self.driver).move_to_element(element).click(element).send_keys(
            Keys.TAB
        ).perform()

    def click_via_actionchains_enter(self, locator):
        """
        This method is used to click the element by actionchain
        :@param locator :get locator from locators module
        """
        element = self.find_clickable_element(locator)
        ActionChains(self.driver).move_to_element(element).click(element).send_keys(
            Keys.ENTER
        ).perform()

    def click_via_actionchains(self, locator):
        """
        This method is used to click the element by actionchain
        :@param locator :get locator from locators module
        """

        element = self.find_element(locator)
        hover = ActionChains(self.driver).move_to_element(element).click()
        hover.perform()

    def mouse_hover_and_click_element(self, locator, sub_locator, x=0, y=0):
        """
        This method is used to click the element by actionchain
        :@param locator :get locator from locators module
        """
        if x > 0 or y > 0:
            element = self.find_element(locator)
            hover = ActionChains(self.driver).move_to_element(element)
            hover.perform()
            sub_menu = self.find_clickable_element(sub_locator)
            ActionChains(self.driver).move_to_element(sub_menu).move_by_offset(
                x, y
            ).click().perform()
        else:
            element = self.find_element(locator)
            hover = ActionChains(self.driver).move_to_element(element)
            hover.perform()
            sub_menu = self.find_clickable_element(sub_locator)
            ActionChains(self.driver).move_to_element(sub_menu).click().perform()

    def click_via_script(self, locator):
        """
        This method is used to click the element by script
        :@param locator :get locator from locators module
        """
        try:
            element = self.find_clickable_element(locator)
            self.driver.execute_script("arguments[0].click();", element)
        except Exception as e:
            print("Exception Message: ", repr(e))
            return False

    def type(self, value, locator):
        """
        This method is used to enter the value
        :@param driver :get locator from locators module
        """
        self.wait_explicit()
        element = self.clear(locator)
        time.sleep(0.5)
        element.send_keys(value)

    def clear(self, locator):
        """
        This method is used to enter the value
        :@param driver :get locator from locators module
        """
        element = self.find_clickable_element(locator)
        element.clear()
        return element

    def clear_by_backspace(self, locator):
        """
        This method is used to clear the value by backspace key
        :@param driver :get locator from locators module
        """
        element = self.find_clickable_element(locator)
        text = element.get_attribute("value")
        while text != "":
            element.click()
            time.sleep(0.5)
            element.send_keys(Keys.END)
            element.send_keys(Keys.BACKSPACE)
            text = element.get_attribute("value")
        return element

    def closetab(self):
        self.driver.close()
        self.switch_to_window(0)
        time.sleep(2)

    def closetab_move_to_index(self, move_to_index):
        self.driver.close()
        self.switch_to_window(move_to_index)

    def selectby_visibletext(self, text_to_select, locator):
        """
        This method is used to Select the VisibleText
        :@param driver :get locator from locators module
        """
        select_element = Select(self.find_clickable_element(locator))
        select_element.select_by_visible_text(text_to_select)

    def selectby_index(self, index, locator):
        """
        This method is used to Select the VisibleText
        :@param driver :get locator from locators module
        """
        select_element = Select(self.find_clickable_element(locator))
        select_element.select_by_index(index)

    def selectby_value(self, value, locator):
        """
        This method is used to Select the VisibleText
        :@param driver :get locator from locators module
        """
        select_element = Select(self.find_clickable_element(locator))
        select_element.select_by_value(value)

    def get_first_selected_value(self, locator):
        """
        This method returns the first selected value in a dropdown
        :param locator:
        :return:
        """
        select_element = Select(self.find_clickable_element(locator))
        return select_element.first_selected_option.text

    def hover(self, locator):
        """
        This method is used to hover the element
        :@param driver :get locator from locators module
        """
        element = self.find_element(locator)
        hover = ActionChains(self.driver).move_to_element(element)
        hover.perform()

    def hover_click(self, locator):
        """
        This method is used to hover the element
        :@param driver :get locator from locators module
        """
        element = self.find_element(locator)
        hover = ActionChains(self.driver).move_to_element(element).click()
        hover.perform()

    def drag_source_and_drop_in_target(self, source, target, x=0, y=0):
        """
        This method is used to drag the source element in the target area
        :@param source, target :get source and target locators
        """
        drag = (
            ActionChains(self.driver)
            .click_and_hold(source)
            .move_to_element(target)
            .pause(1)
            .move_by_offset(x, y)
        )
        drag.release().perform()

    def drag_and_drop(self, source, target):
        """
        This method is used to drag the source element in the target area
        :@param source, target :get source and target locators
        """
        drag = (
            ActionChains(self.driver)
            .click_and_hold(source)
            .move_to_element(target)
            .pause(2)
            .move_by_offset(0, 0)
        )
        drag.drag_and_drop(source, target).release().perform()

    def get_text(self, locator):
        """
        This method is used the get text from text box
        :@param driver :get locator from locators module
        """
        element = self.find_element(locator)
        value = element.text
        return value

    def get_tag_name(self, locator):
        """
        This method is used the get tag name of any locators
        """
        element = self.find_element(locator)
        value = element.tag_name
        return value

    def is_selected(self, locators):
        """
        This method is used the is_selected
        :@param driver :get locator from locators module
        """
        element = self.find_element(locators)
        element.is_selected()
        self.find_element(locators).click()
        return element

    def set_checkbox_status(self, locator, status):
        """
        This method is used to set specified status for the checkbox/radio button
        :@param driver :get locator from locators module
        """
        current_status = self.is_checked(locator)
        element = self.find_element(locator)
        if status.lower() == "checked":
            if not current_status:
                self.driver.execute_script("arguments[0].click();", element)
        else:
            if current_status:
                self.driver.execute_script("arguments[0].click();", element)

    def scroll(self, locators):
        """
        This method is used the scroll the element
        :@param driver :get locator from locators module
        """
        element = self.find_element(locators)
        scroll_element = self.driver.execute_script(
            "return arguments[0].scrollIntoView();", element
        )
        return scroll_element

    def is_alert_present(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.alert_is_present(), "Timed out waiting for alert to appear"
            )
            return True
        except TimeoutException:
            return False

    def handle_alert(self, handle="accept"):
        """
        This method is used the handle alert
        :@param driver :get locator from locators module
        """
        if self.is_alert_present():
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            if handle == "accept":
                alert.accept()
                time.sleep(2)
                return alert_text
            else:
                alert.dismiss()
                return alert_text

    def if_alert_present(self):
        try:
            WebDriverWait(self.driver, 3).until(
                EC.alert_is_present(), "Timed out waiting for alert to appear"
            )
            return True
        except TimeoutException:
            return False

    def handle_an_alert(self, handle="accept"):
        """
        This method is used the handle alert
        :@param driver :get locator from locators module
        """
        if self.if_alert_present():
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            if handle == "accept":
                alert.accept()
                time.sleep(2)
                return alert_text
            else:
                alert.dismiss()
                return alert_text

    def handle_alert_1(self, handle="accept"):
        if self.is_alert_present():
            alert = self.driver.switch_to.alert
            if handle == "accept":
                alert.accept()
                time.sleep(2)
            else:
                return True

    def get_attribute(self, locator, attribute_name, element=None):
        """
        This method is used to get the specified attribute value
        :@param locator :get locator from locators module
        :@param attribute_name :name of the attribute e. value / text / innerText / etc.
        """
        if element is not None:
            return element.get_attribute(attribute_name)
        else:
            return self.find_element(locator).get_attribute(attribute_name)

    def get_attribute_without_visibility(self, locator, attribute_name):
        """
        This method is used to get the specified locator attribute value without checking for element visibility
        Note: Only Xpath values are allowed
        """
        if type(locator) == tuple:
            locator = locator[1]
        attribute = self.driver.find_element(By.XPATH, locator).get_attribute(
            attribute_name
        )
        return attribute

    def get_text_without_visibility(self, locator):
        """
        This method is used to get the specified locator text value without checking for element visibility
        Note: Only Xpath values are allowed
        """
        if type(locator) == tuple:
            locator = locator[1]
        text = self.driver.find_element(By.XPATH, locator).text
        return text

    def get_tag_name_without_visibility(self, locator):
        """
        This method is used to get the specified locator text value without checking for element visibility
        Note: Only Xpath values are allowed
        """
        tag_name = self.driver.find_element(By.XPATH, locator).tag_name
        return tag_name

    def get_attribute_value(self, locators):
        """
        This method is used the get the attribute value
        :@param driver :get locator from locators module
        """
        value = self.find_element(locators).get_attribute("value")
        return value

    def switch_to_window(self, window):
        """
        This method is used for switching to new tab by providing index
        :@param window : index values
        """
        self.driver.switch_to.window(self.driver.window_handles[window])
        time.sleep(6)

    def close_second_tab_and_switch_to_main_window(self, switch=True):
        """
        Method is to close second tab and switch to first/main tab
        """
        total_windows = len(self.driver.window_handles)
        if total_windows > 1:
            if switch:
                self.switch_to_window(0)
            self.driver.close()
            self.switch_to_window(0)
            time.sleep(1)

    def switch_to_iframe(self, locator):
        iframe = self.find_element(locator)
        self.driver.switch_to.frame(iframe)

    def switch_to_defaultcontent(self):
        self.driver.switch_to.default_content()

    def is_displayed(self, locator, explicit_wait=True):
        """
        This method is used to the get is_displayed value of an element
        :@param locator :get locator from locators module
        """
        try:
            self.in_visibility_element(
                locator=locator, explicit_wait=explicit_wait
            ).is_displayed()
            return True
        except TimeoutException:
            return False

    def if_displayed(self, locator, explicit_wait=True):
        """
        This method is used the get is_displayed value of an element in 3 seconds, this is a modified is_displayed just
        to check if the element is not available
        :@param locator :get locator from locators module
        """
        try:
            self.in_visibility_of_element(
                locator=locator, explicit_wait=explicit_wait
            ).is_displayed()
            return True
        except TimeoutException:
            return False

    def is_checked(self, locator):
        """
        This method is used to get checked status of a checkbox / radio button
        :@param locator :get locator from locators module
        """
        element = self.find_element(locator)
        checked = self.driver.execute_script("return arguments[0].checked;", element)
        return checked

    def get_page_title(self):
        """
        This method returns current browser window title
        """
        return self.driver.title

    def execute_script(self, java_script):
        """
        This method is used to execute any java script against the current browser window
        """
        self.driver.execute_script(java_script)

    def javascript_send_keys(self, data, locator):
        """
        This method is used as java script send keys by passing ID value
        """
        self.driver.execute_script(
            "document.getElementById({}).value='{}'".format(locator, data)
        )

    def handle_reload_site_alert(self):
        """
        This is as a java script method to stop Reload Site alert
        """
        self.driver.execute_script("window.onbeforeunload = function() {};")

    def get_current_url(self):
        """
        This method is used to get the current url of the browser window
        """
        return self.driver.current_url

    @staticmethod
    def get_string_params(locator):
        """
        This method is used the get params
        :@param driver :get locator from locators module
        """
        params = []
        for param in locator:
            params.append(param)
        return params[0], params[1]

    def enter_text(self, value, locator):
        """
        This method is used to enter the value
        :@param driver :get locator from locators module
        """
        element = self.find_element(locator)
        element.send_keys(value)

    def assert_loader_is_not_present(self):
        """
        Improvement  When no changes are made, this assertions adds dead time
        :return:
        """
        loader_appearance_wait = WebDriverWait(
            self.driver,
            timeout=10 * self.timeout_multiplier,
            poll_frequency=1,
            ignored_exceptions={
                exceptions.NoSuchElementException,
                exceptions.ElementNotVisibleException,
                exceptions.StaleElementReferenceException,
                exceptions.TimeoutException,
                exceptions.WebDriverException,
            },
        )
        time.sleep(3)
        loader_disappearance_wait = WebDriverWait(
            self.driver, timeout=10 * self.timeout_multiplier, poll_frequency=1
        )
        return loader_appearance_wait, loader_disappearance_wait

    def implicitywait(self):
        self.driver.implicitly_wait(70)

    def element_is_present(self, locator):
        try:
            self.find_element(locator=locator).is_present()
            return True
        except TimeoutException:
            return False

    def in_visibility_element(self, locator, element=None, explicit_wait=True):
        if element is not None:
            return element.find_element(locator)
        elif explicit_wait:
            return WebDriverWait(self.driver, 10).until(
                (EC.visibility_of_element_located(locator))
            )
        else:
            return self.driver.find_element(locator)

    def in_visibility_of_element(self, locator, element=None, explicit_wait=True):
        if element is not None:
            return element.find_element(locator)
        elif explicit_wait:
            return WebDriverWait(self.driver, 3).until(
                (EC.visibility_of_element_located(locator))
            )
        else:
            return self.driver.find_element(locator)

    def scroll_to_top(self):
        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.HOME)

    def scroll_to_bottom(self):
        """
        This method will scroll page to bottom
        """
        last_height = self.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            self.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def page_load(self, locator):
        sync_notification_appeared = False
        delay = 10
        try:
            myElem = WebDriverWait(self.driver, delay).until(
                EC.presence_of_element_located(locator)
            )
            return myElem
        except (
            exceptions.NoSuchElementException,
            exceptions.StaleElementReferenceException,
            exceptions.TimeoutException,
        ):
            return sync_notification_appeared

    def calculate_implicit_wait_time(self, locator, wait_value=5):
        if wait_value:
            self.driver.implicitly_wait(wait_value)
        try:
            myelement = self.find_element(locator)
            return myelement
        except (
            exceptions.NoSuchElementException,
            exceptions.StaleElementReferenceException,
            exceptions.TimeoutException,
        ):
            return wait_value

    @staticmethod
    def current_date_time():
        """
        This method is used to get current date
        """
        date = datetime.now()
        new_date = date.strftime("%m/%d/%Y %H:%M")
        return new_date

    @staticmethod
    def past_date_time(day):
        """
        This method is used to get past date
        """
        current_date = datetime.now()
        date = current_date - timedelta(days=day)
        return date

    @staticmethod
    def future_date_time(day):
        """
        This method is used to get future date
        """
        current_date = datetime.now()
        date = current_date + timedelta(days=day)
        return date

    def wait_implicit(self):
        self.driver.implicitly_wait(10)

    def wait_explicit(self):
        """
        Commented Code does nothing
        :return: Nothing
        """
        # WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'a')))
        # WebDriverWait(self.driver, 10).until(
        #     EC.presence_of_element_located((By.TAG_NAME, "div"))
        # )

    def wait_explicit_invisibility_of_loading(self):
        # WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'a')))
        LOADING_ICON = (By.XPATH, "(//i[@class='icon-spinner icon-spin'])[6]")
        WebDriverWait(self.driver, 30).until(
            EC.invisibility_of_element_located((LOADING_ICON))
        )

    def get_length(self, locator):
        """
        This method is used to get length
        :return:
        """
        try:
            element = self.find_elements(locator)
            length_count = len(element)
            return length_count
        except Exception as e:
            return 0

    def page_refresh(self):
        """
        This method is used to perform page refresh
        """
        self.handle_reload_site_alert()
        self.driver.refresh()
        self.wait_for_spinner_load_to_disappear()

    def hard_page_refresh(self):
        """
        This method is used to perform hard page refresh
        """
        self.driver.execute_script("location.reload(true);")
        time.sleep(2)

    def navigate_back(self):
        """
        This method is used to perform navigation back to page
        """
        self.driver.back()
        time.sleep(2)

    def switch_to_popup(self):
        for x in self.driver.window_handles:
            if x != self.driver.current_window_handle:
                child = x
                self.driver.switch_to.window(child)
        self.wait_implicit()

    def switchback_to_main(self):
        for x in self.driver.window_handles:
            if x != self.driver.current_window_handle:
                main = x
                self.driver.switch_to.window(main)
        self.wait_implicit()

    def open_new_browser_with_url(self, url):
        windows = self.driver.window_handles
        windows_count = len(windows)
        if windows_count > 0:
            self.driver.get(url)
        else:
            self.driver.execute_script("""window.open("{}","_blank");""".format(url))
            time.sleep(1)
            self.switch_to_window(1)

    def open_new_browser_with_given_url(self, url, window=1):
        self.driver.execute_script("""window.open("{}","_blank");""".format(url))
        time.sleep(1)
        self.switch_to_window(window)

    def open_new_blank_tab(self, window=1):
        time.sleep(5)
        self.driver.execute_script("window.open('', '_blank');")
        time.sleep(1)
        self.switch_to_window(window)

    def find_elements_by_xpath(self, locator):
        total_elements = len(self.driver.find_elements(By.XPATH, locator))
        return total_elements

    def get_all_options(self, locator):
        """
        This method returns the all option values in a dropdown
        :param locator:
        :return: list of all values
        """
        values = []
        try:
            select_element = Select(self.find_clickable_element(locator))
            options = select_element.options
            for option in options:
                value = option.text
                values.append(value)
            return values

        except Exception as e:
            return values

    """
    DrChrono web application specific functions
    """

    def get_provider_name(self):
        """
        This method is used to Provider Name of the specified account
        """
        provider_name_xpath = (By.XPATH, "//a[@id='switch-button']/span[1]")
        self.if_displayed(provider_name_xpath)
        provider_name = self.get_text_without_visibility(provider_name_xpath)
        return provider_name

    def get_account_user_name(self):
        """
        This method is used to logged in user at top right near logout
        """
        user_name_xpath = (By.XPATH, "//a[@id='switch-button']/../../..//strong")
        self.if_displayed(user_name_xpath)
        user_details = str(self.get_text_without_visibility(user_name_xpath)).split(
            " ("
        )
        user_name = user_details[0]
        return user_name

    def get_current_logged_in_user_detail(self):
        """
        This method is used to get Current User Name of the specified account
        """
        user_name = ""
        user_xpath = (By.XPATH, "//div[@id='toprightnav']/ul//strong")
        self.if_displayed(user_xpath)
        text = self.get_text(user_xpath)
        user_details = text.split("(")
        name = user_details[0].strip()
        doctor_id = user_details[1]
        user_id = doctor_id.split(")")[0]
        if "Dr." in name:
            user_name = name.split(".")[1].strip()
        return user_name, user_id, name

    @staticmethod
    def get_onpatient_url():
        """
        This method is used to get OnPatient portal URL from config file
        """
        return onpatient_url

    @staticmethod
    def get_target_environment():
        """
        This method is used to get the environment i.e. Staging or Prod
        """
        return env

    @staticmethod
    def employee_account_passcode():
        """
        This method is used to return another Markw employee account password
        """
        return employee_password

    @staticmethod
    def get_target_execution_environment():
        """
        This method is used to return if the target environment is Local or Remote
        """
        return target_execution

    @staticmethod
    def employee_account_username():
        """
        This method is used to return another Markw employee account username
        """
        return employee_username

    def DrChrono_app_login(self):
        """
        This method is used to login into DrChrono web application
        """
        login_username = (By.ID, "username")
        login_password = (By.ID, "password")
        login_button = (By.ID, "login")
        continue_btn = (By.ID, "id_login_continue_button")
        username = self.employee_account_username()
        password = self.employee_account_passcode()
        self.type(username, login_username)
        self.click(continue_btn)
        self.type(password, login_password)
        self.click(login_button)

    def click_logout(self):
        """
        This method is used to click log out
        """
        click_logout = (By.XPATH, "//i[@class='icon-power-off']")
        self.click(click_logout)

    def click_logout_and_login_code_block(self, username, password):
        """
        This method is used to log out and login into specified account
        """
        retry_count = 0
        self.click_logout()
        user_name = (By.ID, "username")
        pass_word = (By.ID, "password")
        login_btn = (By.ID, "login")
        continue_btn = (By.ID, "id_login_continue_button")
        self.type(username, user_name)
        self.click(continue_btn)
        self.type(password, pass_word)
        self.click(login_btn)
        time.sleep(1)
        # This method will come into picture when concurrent user login get permission denied error
        # This method will retry login and raise error if not able to login with 10 retries
        label = self.if_displayed(MessageCenterLocators.PERMISSION_DENIED_LABEL)
        if label:
            login_xpath = (By.XPATH, "//a[normalize-space()='Log In']")
            self.click(login_xpath)
            self.click_logout_and_login_code_block(username, password)
            retry_count += 1
            if retry_count > 10:
                raise AssertionError(
                    "Getting permission denied error, tried {0} times".format(
                        retry_count
                    )
                )

    def click_logout_and_login_into_another_account(self, verify=True):
        """
        This method is used to logout and Login into specified account
        """
        username = employee_username
        password = self.employee_account_passcode()
        user_xpath = (
            By.XPATH,
            "//small[normalize-space()='({})']".format(username.lower()),
        )
        user = self.if_displayed(user_xpath)
        if user is False:
            self.click_logout_and_login_code_block(username, password)
        if verify:
            self.login_to_current_provider_if_different()

    def click_logout_MarkW_and_login_into_Mark23_account(self):
        """
        This method is used to logout from MarkW and Login into Mark23
        """
        username = config.get(env, "username")
        password = config.get(env, "password")
        user_xpath = (
            By.XPATH,
            "//small[normalize-space()='({})']".format(username.lower()),
        )
        user = self.if_displayed(user_xpath)
        if user is False:
            self.click_logout_and_login_code_block(username, password)
        self.login_to_current_provider_if_different()

    def click_logout_and_login_into_staff_account(self):
        """
        This method is used to logout from MarkW and Login into Mark23
        """
        username = config.get(env, "staff_username")
        password = config.get(env, "staff_password")
        user_xpath = (
            By.XPATH,
            "//small[normalize-space()='({})']".format(username.lower()),
        )
        user = self.if_displayed(user_xpath)
        if user is False:
            self.click_logout_and_login_code_block(username, password)

    def click_logout_and_login_into_another_account_for_permission(
        self, username, password
    ):
        """
        This method is used to logout and Login into specified account for permission check
        """
        user_xpath = (
            By.XPATH,
            "//small[normalize-space()='({})']".format(username.lower()),
        )
        user = self.is_displayed(user_xpath)
        if user is False:
            self.click_logout_and_login_code_block(username, password)
        self.login_to_current_provider_if_different()

    def check_and_close_popup_notification(self):
        """
        Method is used to close the popup notification if displayed
        """
        time.sleep(1)
        popup_notification = (By.XPATH, "//div[@id='jGrowl']")
        flag = self.is_displayed(popup_notification)
        if flag:
            popup_notification_close = (By.XPATH, "//button[@class='jGrowl-close']")
            try:
                self.click(popup_notification_close)
                time.sleep(1)
            except Exception:
                pass

    @staticmethod
    def get_nth_day_document_management(nth_day):
        """
        Method used to return date i.e past nth day in MM-DATE-YEAR format
        Ex: 01-31-2023
        """
        any_date = datetime.now() + timedelta(days=int(nth_day))
        eastern_day = any_date.strftime("%m-%d-%Y")
        print(eastern_day)
        return eastern_day

    @staticmethod
    def eastern_timezone():
        today = datetime.now(eastern_time).strftime("%m/%d/%Y")
        return today

    @staticmethod
    def get_today_date(date_format):
        today = datetime.now(eastern_time).strftime(date_format)
        return today

    @staticmethod
    def get_nth_day(nth_day, format="%m/%d/%Y"):
        any_date = datetime.now() + timedelta(days=int(nth_day))
        eastern_day = any_date.strftime(format)
        return eastern_day

    @staticmethod
    def eastern_timezone_time_stamp():
        time_stamp = datetime.now(eastern_time).strftime("%m_%d_%Y_%H_%M_%S")
        return time_stamp

    @staticmethod
    def eastern_timezone_today_stamp():
        today_stamp = datetime.now(eastern_time).strftime("%m_%d_%Y_%S")
        return today_stamp

    @staticmethod
    def month_stamp():
        month = int(datetime.now(eastern_time).strftime("%m"))
        return month

    @staticmethod
    def hour_24_stamp():
        hour = int(datetime.now(eastern_time).strftime("%H"))
        return hour

    @staticmethod
    def hour_12_stamp():
        hour = int(datetime.now(eastern_time).strftime("%I"))
        return hour

    @staticmethod
    def day_stamp():
        day = int(datetime.now(eastern_time).strftime("%d"))
        return day

    @staticmethod
    def minute_second_stamp():
        minute_second = datetime.now(eastern_time).strftime("%M%S")
        return minute_second

    @staticmethod
    def check_month_and_return_date_time_stamp():
        """
        Method used to check which month and return date accordingly;
        Ex: March 10, 2022, 8:37 a.m. or Dec. 18, 2022, 7:27 p.m.
        """
        month = len(datetime.now().strftime("%B"))
        meridian = datetime.now(eastern_time).strftime("%p")
        hour = BasePage.hour_12_stamp()
        if meridian == "AM":
            meridian = "a.m."
        else:
            meridian = "p.m."
        if month > 5:
            month_name = datetime.now().strftime("%B")
            if month_name == "September":
                today_date = datetime.now(eastern_time).strftime(
                    "Sept. %d, %Y, {}:%M {}".format(hour, meridian)
                )
            else:
                today_date = datetime.now(eastern_time).strftime(
                    "%b. %d, %Y, {}:%M {}".format(hour, meridian)
                )
        else:
            today_date = datetime.now(eastern_time).strftime(
                "%B %d, %Y, {}:%M {}".format(hour, meridian)
            )
        if ":00" in today_date:
            stamp = today_date.split(":00")
            today_stamp = stamp[0] + stamp[1]
            return today_stamp
        else:
            return today_date

    @staticmethod
    def return_date_format_as_per_message_center_entry():
        """
        Method used to return date i.e Ex: July 3, 2023
        """
        today_date = ""
        day = BasePage.day_stamp()
        month = len(datetime.now().strftime("%B"))
        if month > 5:
            month_name = datetime.now().strftime("%B")
            if month_name == "September":
                today_date += datetime.now(eastern_time).strftime(
                    "Sept. {}, %Y".format(day)
                )
            else:
                today_date += datetime.now(eastern_time).strftime(
                    "%b. {}, %Y".format(day)
                )
        else:
            today_date += datetime.now(eastern_time).strftime("%B {}, %Y".format(day))
        return today_date

    @staticmethod
    def date_stamp(trim_month=False):
        """
        If trim_month is true then return date will be of format Dec 18, 2022
        Else
        Method used to check which month and return date accordingly;
        Ex: March 10, 2022 or Dec. 18, 2022.
        """
        operating_system = platform.system()
        if operating_system == "Windows":
            if trim_month:
                today_date = datetime.now(eastern_time).strftime("%b %#d, %Y")
            else:
                month = len(datetime.now().strftime("%B"))
                if month > 5:
                    month_name = datetime.now().strftime("%B")
                    if month_name == "September":
                        today_date = datetime.now(eastern_time).strftime("Sept %#d, %Y")
                    else:
                        today_date = datetime.now(eastern_time).strftime("%b %#d, %Y")
                else:
                    today_date = datetime.now(eastern_time).strftime("%B %#d, %Y")
        else:
            if trim_month:
                today_date = datetime.now(eastern_time).strftime("%b %-d, %Y")
            else:
                month = len(datetime.now().strftime("%B"))
                if month > 5:
                    month_name = datetime.now().strftime("%B")
                    if month_name == "September":
                        today_date = datetime.now(eastern_time).strftime("Sept %-d, %Y")
                    else:
                        today_date = datetime.now(eastern_time).strftime("%b %-d, %Y")
                else:
                    today_date = datetime.now(eastern_time).strftime("%B %-d, %Y")
        return today_date

    @staticmethod
    def get_day_of_week():
        my_date = date.today()
        day = calendar.day_name[my_date.weekday()]
        return day

    def verify_appointment(
        self,
        appointment_time,
        patient_name,
        appointment_id=None,
        save=False,
        video=False,
    ):
        """
        This method is used to verify Appointment
        """
        time.sleep(5)
        if len(appointment_time) == 6:
            am_pm = str(appointment_time[4:]).lower()
            appointment_time = appointment_time[0:4]
        else:
            am_pm = str(appointment_time[5:]).lower()
            if appointment_time[0] == "0":
                appointment_time = appointment_time[1:5]
            else:
                appointment_time = appointment_time[0:5]
        if appointment_time == "11:30":
            am_pm = "pm"
        if appointment_id:
            pat_appt_details_xpath = (
                "//div[@data-id='{}']//dl//span[contains(text(),'{}')][contains(text(),'{}')]"
                "/../..//dd".format(appointment_id, appointment_time, am_pm)
            )
            pat_appointment_details_xpath = (
                "//div[@data-id='{}']//dl//span[contains(text(),'{}')][contains(text(),'{}')]"
                "/../..//dd".format(appointment_id, appointment_time, am_pm)
            )
            print(pat_appointment_details_xpath)
        else:
            pat_appt_details_xpath = (
                "//div[@id='gridcontainer']//dl//span[contains(text(),'{}')][contains(text(),"
                "'{}')]/parent::dt/following-sibling::dd/span[contains(text(),'{}')]".format(
                    appointment_time, am_pm, patient_name
                )
            )
            pat_appointment_details_xpath = (
                "//div[@id='gridcontainer']//dl//span[contains(text(),'{}')][contains"
                "(text(),'{}')]/parent::dt/following-sibling::dd/span[contains(text(),"
                "'{}')]".format(appointment_time, am_pm, patient_name)
            )
            print(pat_appointment_details_xpath)
        pat_appointment_details = (By.XPATH, pat_appointment_details_xpath)
        for week in range(1, 6):
            pat_appointment_flag = self.is_displayed(pat_appointment_details)
            if pat_appointment_flag:
                self.scroll(pat_appointment_details)
                self.click_via_script(pat_appointment_details)
                time.sleep(5)
                schedule_appointment_modal = (
                    By.XPATH,
                    "//span[text()='Schedule Appointment']",
                )
                self.if_displayed(schedule_appointment_modal)
                allow_overlap_xpath = (
                    By.XPATH,
                    "//input[@id='id_appt-allow_overlapping']",
                )
                allow_overlap_flag = self.is_checked(allow_overlap_xpath)
                if allow_overlap_flag is False:
                    self.click(allow_overlap_xpath)
                if video:
                    video_inactive_xpath = (
                        By.XPATH,
                        "//span[@id='telemedicine-inactive-msg-container']//i[@class='icon-info-sign']",
                    )
                    video_inactive_flag = self.if_displayed(video_inactive_xpath)
                    if video_inactive_flag is False:
                        start_video = (
                            By.XPATH,
                            "//a[normalize-space()='Start Video Visit']",
                        )
                        self.click(start_video)
                        time.sleep(2)
                        tabs = self.get_windows_count()
                        self.switch_to_window(tabs - 1)
                        time.sleep(2)
                        join_call_option = (
                            By.XPATH,
                            "//button[normalize-space()='Join Call']",
                        )
                        join_call = self.if_displayed(join_call_option)
                        self.assertTrue(
                            join_call,
                            "It seems Join Call option from Start Video Visit is missing, verify!",
                        )
                        self.driver.close()
                        self.switch_to_window(0)
                time.sleep(1.5)
                appt_flag = len(
                    self.driver.find_elements(By.XPATH, pat_appt_details_xpath)
                )
                if save:
                    self.click((By.XPATH, "//button[@id='save_appointment']"))
                else:
                    self.click((By.XPATH, "//button[@id='save_and_close']"))
                time.sleep(3)
                if appt_flag == 0:
                    return False
                else:
                    return True
            else:
                WEEK_NEXT_BTN = (By.XPATH, "//button[@id='sfnextbtn']/i")
                self.click(WEEK_NEXT_BTN)
                time.sleep(2)
                if week == 5:
                    raise AssertionError(
                        "It seems the appointment is not displayed even after searching for 5 weeks of time, "
                        "so verify what went wrong exactly!"
                    )

    def verify_created_appointment(self, appointment_time, patient_name, appt_id=None):
        """
        This method is used to verify Appointment
        """
        time.sleep(3)
        try:
            if len(appointment_time) == 6:
                am_pm = str(appointment_time[4:]).lower()
                appointment_time = appointment_time[0:4]
            else:
                am_pm = str(appointment_time[5:]).lower()
                if appointment_time[0] == "0":
                    appointment_time = appointment_time[1:5]
                else:
                    appointment_time = appointment_time[0:5]
            if appt_id is not None:
                pat_appt_details_xpath = (
                    "//div[@id='gridcontainer']//div[@data-id='{}']//dl//span[contains(text(),'{}')][contains(text(),'{}')]/parent::dt/"
                    "following-sibling::dd/span[contains(text(),'{}')]".format(
                        appt_id, appointment_time, am_pm, patient_name
                    )
                )
                self.is_displayed((By.XPATH, pat_appt_details_xpath))
            else:
                pat_appt_details_xpath = (
                    "//div[@id='gridcontainer']//dl//span[contains(text(),'{}')][contains(text(),'{}')]/parent::dt/"
                    "following-sibling::dd/span[contains(text(),'{}')]".format(
                        appointment_time, am_pm, patient_name
                    )
                )
            time.sleep(1.5)
            appt_flag = len(self.driver.find_elements(By.XPATH, pat_appt_details_xpath))
            if appt_flag == 0:
                return False
            else:
                return True

        except Exception as e:
            print("Exception Message: ", repr(e))
            return False

    @staticmethod
    def drag_and_drop_file(drop_target, path):
        drop_file = """
            var target = arguments[0],
                offsetX = arguments[1],
                offsetY = arguments[2],
                document = target.ownerDocument || document,
                window = document.defaultView || window;
    
            var input = document.createElement('INPUT');
            input.type = 'file';
            input.onchange = function () {
              var rect = target.getBoundingClientRect(),
                  x = rect.left + (offsetX || (rect.width >> 1)),
                  y = rect.top + (offsetY || (rect.height >> 1)),
                  dataTransfer = { files: this.files };
    
              ['dragenter', 'dragover', 'drop'].forEach(function (name) {
                var evt = document.createEvent('MouseEvent');
                evt.initMouseEvent(name, !0, !0, window, 0, 0, 0, x, y, !1, !1, !1, !1, 0, null);
                evt.dataTransfer = dataTransfer;
                target.dispatchEvent(evt);
              });
    
              setTimeout(function () { document.body.removeChild(input); }, 25);
            };
            document.body.appendChild(input);
            return input;
        """
        driver = drop_target.parent
        file_input = driver.execute_script(drop_file, drop_target, 0, 0)
        file_input.send_keys(path)

    def upload_a_document(self, xpath_value):
        """
        Method is used to upload PDF document providing xpath <input type='file'> locator value
        """
        root_path = os.path.dirname(os.path.abspath("src/resources/DrChrono.pdf"))
        pdf_path = root_path + "/DrChrono.pdf"
        self.driver.find_element(By.XPATH, xpath_value).send_keys(pdf_path)

    def upload_a_file(self, file_path, file_name, xpath_value):
        """
        Method is used to upload any document providing if xpath <input type='file'> locator value
        """
        root_path = os.path.dirname(os.path.abspath(file_path))
        pdf_path = root_path + file_name
        self.driver.find_element(By.XPATH, xpath_value).send_keys(pdf_path)

    def click_download_pdf_using_key_actions(self, patient_name):
        """
        Method is click on Clinical Note download option using Keyboard actions and download the PDF locally
        """
        import pyautogui

        browser = str(self.driver)
        if "chrome" in browser:
            clicks = 8
        elif "firefox" in browser:
            clicks = 11
        else:
            raise Exception(
                "Manually check how many clicks required to click on the Print option for the new browser and edit this function!"
            )

        for click in range(0, clicks):
            pyautogui.hotkey("tab")
        pyautogui.hotkey("enter")
        time.sleep(15)
        pyautogui.typewrite(patient_name)
        time.sleep(2)
        pyautogui.hotkey("enter")
        time.sleep(5)

    def wait_for_loading_data(self):
        LOADING_ALERT_INFO = (By.XPATH, "//div[@class='waiting alert alert-info']")
        loading_flag = self.is_displayed(LOADING_ALERT_INFO)
        while loading_flag:
            loading_flag = self.if_displayed(LOADING_ALERT_INFO)
            time.sleep(1)

    def click_preview_note_and_click_on_alert_info(self):
        """
        Method is used to click on Preview Note and click on alert info text
        """
        PREVIEW_OR_VIEW_NOTE = (
            By.XPATH,
            "//a[@id='id_clinical_note_view_complete_note']",
        )
        preview_flag = self.is_displayed(PREVIEW_OR_VIEW_NOTE)
        self.assertTrue(
            preview_flag,
            "It seems Preview Note or View Note is missing or invalid xpath",
        )
        self.click_via_script(PREVIEW_OR_VIEW_NOTE)
        jgrowl_alert_notification = (By.XPATH, "//div[@id='jGrowl']/div[2]")
        saving_alert_notification = (By.XPATH, "//div[@class='jGrowl-message']")
        alert_flag = self.if_displayed(jgrowl_alert_notification)
        saving_flag = self.if_displayed(saving_alert_notification)
        if alert_flag or saving_flag:
            time.sleep(10)
            self.click(PREVIEW_OR_VIEW_NOTE)
            time.sleep(5)
        self.wait_for_loading_data()
        ALERT_INFO = (By.XPATH, "//div[@class='alert alert-info']")
        self.click(ALERT_INFO)
        time.sleep(30)

    def view_note_and_download_pdf(self, patient_name, preview=True):
        """
        Method is used to click on Preview Note and download, extract PDF data
        """
        target = self.get_target_execution_environment()
        if target == "localmachine":
            time.sleep(2)
            if preview:
                self.click_preview_note_and_click_on_alert_info()
            self.click_download_pdf_using_key_actions(patient_name)
            file_path = self.downloaded_pdf_file_path(patient_name)
            pdf_content = self.extract_pdf_content(file_path)
            pdf_data_as_string = ""
            for items in pdf_content:
                pdf_data_as_string = pdf_data_as_string + items + " "
            return pdf_data_as_string
        else:
            self.view_note_pdf()
            # note_iframe = (By.XPATH, "//iframe[@id='view_complete_note_object']")
            # self.switch_to_iframe(note_iframe)
            self.verify_if_embed_pdf_is_displayed(switch=False)
            # self.switch_to_defaultcontent()
            return False

    def view_note_pdf(self, preview=True):
        """
        Method is used to click on Preview Note
        """
        time.sleep(5)
        if preview:
            self.click_preview_note_and_click_on_alert_info()

    @staticmethod
    def get_random_appointment_time():
        time_slots = [
            "04:05PM",
            "04:20PM",
            "04:35PM",
            "04:50PM",
            "05:05PM",
            "05:20PM",
            "05:35PM",
            "05:50PM",
            "03:05PM",
            "03:20PM",
            "03:35PM",
            "03:50PM",
            "03:55PM",
            "01:05PM",
            "01:20PM",
            "01:35PM",
            "01:50PM",
            "01:55PM",
            "02:05PM",
            "02:20PM",
            "02:35PM",
            "02:50PM",
            "02:55PM",
        ]
        appointment_time = random.choice(time_slots)
        return appointment_time

    def downloaded_pdf_file_path(self, patient_name):
        from pathlib import Path

        downloads_path = ""
        target_exe_env = self.get_target_execution_environment()
        if "remote" in target_exe_env:
            downloads_path = (
                str("file:///C:/Users/ltuser/Downloads") + "/" + patient_name + ".pdf"
            )
        else:
            downloads_path = (
                str(Path.home() / "Downloads") + "/" + patient_name + ".pdf"
            )
        return downloads_path

    def downloaded_csv_file_path(self, patient_name):
        from pathlib import Path

        downloads_path = ""
        target_exe_env = self.get_target_execution_environment()
        print("Target env is {}".format(target_exe_env))
        if "remote" in target_exe_env:
            downloads_path = (
                str("file:///C:/Users/ltuser/Downloads") + "/" + patient_name + ".csv"
            )
        else:
            downloads_path = (
                str(Path.home() / "Downloads") + "/" + patient_name + ".csv"
            )
        return downloads_path

    def downloaded_zip_file_path(self, patient_name):
        from pathlib import Path

        downloads_path = ""
        target_exe_env = self.get_target_execution_environment()
        if "remote" in target_exe_env:
            downloads_path = (
                str("file:///C:/Users/ltuser/Downloads") + "/" + patient_name + ".zip"
            )
        else:
            downloads_path = (
                str(Path.home() / "Downloads") + "/" + patient_name + ".zip"
            )
        return downloads_path

    def downloaded_xml_file_path(self, patient_name):
        from pathlib import Path

        downloads_path = ""
        target_exe_env = self.get_target_execution_environment()
        if "remote" in target_exe_env:
            downloads_path = (
                str("file:///C:/Users/ltuser/Downloads") + "/" + patient_name + ".xml"
            )
        else:
            downloads_path = (
                str(Path.home() / "Downloads") + "/" + patient_name + ".xml"
            )
        return downloads_path

    @staticmethod
    def download_pdf_content(patient_name, url):
        """
        Method is used to download fax PDF
        """
        directory = os.getcwd()
        filename = directory + "/" + patient_name + ".pdf"
        response = requests.get(url)
        with open(filename, mode="wb") as f:
            f.write(response.content)

    @staticmethod
    def extract_the_pdf_content(patient_name):
        """
        Method is used to extract content from PDF by passing Patient Name
        """
        from io import StringIO

        from pdfminer.converter import TextConverter
        from pdfminer.layout import LAParams
        from pdfminer.pdfdocument import PDFDocument
        from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
        from pdfminer.pdfpage import PDFPage
        from pdfminer.pdfparser import PDFParser

        filename = os.getcwd() + "/" + patient_name + ".pdf"
        output_string = StringIO()
        with open(filename, "rb") as in_file:
            parser = PDFParser(in_file)
            doc = PDFDocument(parser)
            resource_mgr = PDFResourceManager()
            device = TextConverter(resource_mgr, output_string, laparams=LAParams())
            interpreter = PDFPageInterpreter(resource_mgr, device)
            for page in PDFPage.create_pages(doc):
                interpreter.process_page(page)
        values = output_string.getvalue().split("\n")
        data = []
        for items in values:
            item = items.strip()
            data.append(item)
        os.remove(filename)
        return data

    def verify_if_embed_pdf_is_displayed(self, switch=True, window=1):
        """
        Method is used to verify if Embed PDF is displayed/generated or not
        """
        if switch:
            self.switch_to_window(window)
        time.sleep(15)
        embed_pdf_xpath = (By.XPATH, "//embed[@type='application/pdf']")
        embed_pdf = self.if_displayed(embed_pdf_xpath)
        if embed_pdf is False:
            time.sleep(10)
        embed_pdf = self.is_displayed(embed_pdf_xpath)
        self.assertTrue(
            embed_pdf,
            "It seems the Embed PDF is either not generated or something went wrong, verify!",
        )
        if switch:
            self.closetab()

    @staticmethod
    def extract_pdf_content(file_path):
        """
        Method is used to extract content from PDF by passing File path
        """
        from io import StringIO

        from pdfminer.converter import TextConverter
        from pdfminer.layout import LAParams
        from pdfminer.pdfdocument import PDFDocument
        from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
        from pdfminer.pdfpage import PDFPage
        from pdfminer.pdfparser import PDFParser

        output_string = StringIO()
        with open(file_path, "rb") as in_file:
            parser = PDFParser(in_file)
            doc = PDFDocument(parser)
            resource_mgr = PDFResourceManager()
            device = TextConverter(resource_mgr, output_string, laparams=LAParams())
            interpreter = PDFPageInterpreter(resource_mgr, device)
            for page in PDFPage.create_pages(doc):
                interpreter.process_page(page)
        values = output_string.getvalue().split("\n")
        data = []
        for items in values:
            item = items.strip()
            data.append(item)
        os.remove(file_path)
        return data

    def upload_an_image(self, locator):
        """
        Method is used to upload an Image.
        @:param: locator - //input[@type='file']
        """
        root_path = os.path.dirname(os.path.abspath("src/resources/download.jpg"))
        img_path = root_path + "/download.jpg"
        self.driver.find_element(By.XPATH, locator).send_keys(img_path)
        time.sleep(1)

    def upload_any_image(self, image_name, locator):
        """
        Method is used to upload any Image.
        @:param: image_name.format - placed in 'driver' folder
        @:param: locator - //input[@type='file']
        """
        root_path = os.path.dirname(
            os.path.abspath("src/resources/{}".format(image_name))
        )
        img_path = root_path + "/{}".format(image_name)
        self.driver.find_element(By.XPATH, locator).send_keys(img_path)
        time.sleep(1)

    @staticmethod
    def create_random_string(chars):
        """
        Method is used to return a random text in lower case for mentioned character length
        @:param: chars
        """
        result = str("".join(random.choices(string.ascii_lowercase, k=chars)))
        return result

    @staticmethod
    def create_random_alpha_numeric_string(chars):
        """
        Method is used to return a random alpha numeric string in upper case for mentioned character length
        @:param: chars
        """
        result = str(
            "".join(random.choices(string.ascii_uppercase + string.digits, k=chars))
        )
        return result

    @staticmethod
    def create_random_numeric_string(chars):
        """
        Method is used to return a random numeric string for mentioned character length
        @:param: chars
        """
        result = str("".join(random.choices(string.digits, k=chars)))
        return result

    @staticmethod
    def create_random_alpha_numeric_special_string(chars):
        """
        Method is used to return a random alpha numeric string in upper case for mentioned character length
        @:param: chars
        """
        result = str(
            "".join(
                random.choices(
                    string.ascii_uppercase
                    + string.ascii_lowercase
                    + string.punctuation
                    + string.digits,
                    k=chars,
                )
            )
        )
        return result

    """PDF actions"""

    def close_pdf_window(self, num):
        """
        This method is used to close the given opened window
        """
        self.driver.close()
        self.switch_to_window(num)

    def is_export_notification_displayed(self):
        """
        This method will wait for notification 'Exporting.. ' and return true when displayed
        :return: boolean
        """
        export_notification_appeared = False
        exporting_div = (
            By.XPATH,
            "//div[@class='jGrowl-notification']//div[@class='jGrowl-message']",
        )
        try:
            export_notification_appeared = self.is_displayed(exporting_div, True)
        except (
            exceptions.NoSuchElementException,
            exceptions.StaleElementReferenceException,
            exceptions.TimeoutException,
        ):
            pass
        return export_notification_appeared

    def error_message_displayed(self):
        """
        This method will wait for error message to displayed
        :return: boolean
        """
        export_notification_appeared = False
        exporting_div = (By.XPATH, "//div[@id ='jGrowl']")

        try:
            export_notification_appeared = self.is_displayed(exporting_div)
        except (
            exceptions.NoSuchElementException,
            exceptions.StaleElementReferenceException,
            exceptions.TimeoutException,
        ):
            pass
        return export_notification_appeared

    def duplicate_error_message_displayed(self):
        """
        This method will wait for error message to displayed
        :return: boolean
        """
        list_messages = []
        export_notification_appeared = False
        exporting_div = (By.XPATH, "//div[@id ='jGrowl']")
        exporting_div_message = (
            By.XPATH,
            "//div[@id ='jGrowl']//div[@class='jGrowl-message']",
        )
        message = self.get_text(exporting_div_message)
        list_messages.append(message.strip())
        try:
            export_notification_appeared = self.is_displayed(exporting_div, True)
        except (
            exceptions.NoSuchElementException,
            exceptions.StaleElementReferenceException,
            exceptions.TimeoutException,
        ):
            pass
        list_messages.append(export_notification_appeared)
        return list_messages

    def success_message_displayed(self):
        """
        This method will wait for success message to displayed and then return it
        :return: message
        """
        exporting_div_message = (
            By.XPATH,
            "//div[@id ='jGrowl']//div[@class='jGrowl-message']",
        )
        message = self.get_text(exporting_div_message)
        try:
            export_notification_appeared = self.is_displayed(
                exporting_div_message, True
            )
        except (
            exceptions.NoSuchElementException,
            exceptions.StaleElementReferenceException,
            exceptions.TimeoutException,
        ):
            pass
        return message

    # def success_exporting_audit_log_message(self):
    #     """
    #     This method will wait for success message to displayed and then return it
    #     :return: message
    #     """
    #
    #     exporting_div = (By.XPATH, "//div[@id ='jGrowl']")
    #     exporting_div_message = (By.XPATH, "//div[@id ='jGrowl']//div[@class='jGrowl-message']")
    #     message = self.get_text(exporting_div_message)
    #     try:
    #         export_notification_appeared = self.is_displayed(exporting_div, True)
    #     except (
    #             exceptions.NoSuchElementException,
    #             exceptions.StaleElementReferenceException,
    #             exceptions.TimeoutException,
    #     ):
    #         pass
    #     return message

    def check_exporting_toast_notification(self):
        """
        This method is used to verify the Exporting Toast message notification
        """
        export_notification_appeared = False
        try:
            element = (
                By.XPATH,
                "//div[@class='jGrowl-message']"
                "[text()='Exporting... When complete, you will see exported data in Message Center.']",
            )
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(element)
            )
        except (
            exceptions.NoSuchElementException,
            exceptions.StaleElementReferenceException,
            exceptions.TimeoutException,
        ):
            pass
        return export_notification_appeared

    # Generating statements... When complete, you will see generated PDF in the Message Center.

    def check_denied_toast_notification_for_billing_profile_change(self):
        """
        This method is used to verify the Toast message notification when billing profile changed and denied
        """
        billing_notification_appeared = False
        try:
            element = (
                By.XPATH,
                "//div[@class='jGrowl-message'][text()='Line items cannot be modified by billing "
                "profile because there are posted transactions.']",
            )
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(element)
            )
            billing_notification_appeared = True
        except (
            exceptions.NoSuchElementException,
            exceptions.StaleElementReferenceException,
            exceptions.TimeoutException,
        ):
            pass
        return billing_notification_appeared

    def check_successful_drchrono_payment_toast_notification_visible(self):
        """
        This method is used to verify the Toast message notification when billing profile changed and denied
        """
        drchrono_payment_notification = False
        try:
            element = (
                By.XPATH,
                "//div[@class='jGrowl-message'][text()='DrChrono Payments payment successful.']",
            )
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(element)
            )
            drchrono_payment_notification = True
        except (
            exceptions.NoSuchElementException,
            exceptions.StaleElementReferenceException,
            exceptions.TimeoutException,
        ):
            pass
        return drchrono_payment_notification

    def check_successful_drchrono_payment_refund_toast_notification_visible(self):
        """
        This method is used to verify the Toast message notification when billing profile changed and denied
        """
        drchrono_payment_refund_notification = False
        try:
            element = (
                By.XPATH,
                "//div[@class='jGrowl-message'][text()='DrChrono Payments refund successful.']",
            )
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(element)
            )
            drchrono_payment_refund_notification = True
        except (
            exceptions.NoSuchElementException,
            exceptions.StaleElementReferenceException,
            exceptions.TimeoutException,
        ):
            pass
        return drchrono_payment_refund_notification

    def check_successful_drchrono_payment_profile_update_notification_visible(self):
        """
        This method is used to verify the Toast message notification when billing profile changed and denied
        """
        drchrono_profile_update_notification = False
        try:
            element = (
                By.XPATH,
                "//div[@class='jGrowl-message'][text()='Profile updated.']",
            )
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(element)
            )
            drchrono_profile_update_notification = True
        except (
            exceptions.NoSuchElementException,
            exceptions.StaleElementReferenceException,
            exceptions.TimeoutException,
        ):
            pass
        return drchrono_profile_update_notification

    def check_requesting_eligibilities_toast_notification_visible(self):
        """
        This method is used to verify the Toast message notification when eligibilities check are run
        """
        eligibility_run_notification = False
        try:
            element = (
                By.XPATH,
                "//div[@class='jGrowl-message'][text()='Requesting eligibilities...please check back in a few minutes.']",
            )
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(element)
            )
            eligibility_run_notification = True
        except (
            exceptions.NoSuchElementException,
            exceptions.StaleElementReferenceException,
            exceptions.TimeoutException,
        ):
            pass
        return eligibility_run_notification

    def check_duplicate_eob_toast_notification(self, trace, payer):
        """
        This method is used to verify the Exporting Toast message notification
        """
        notification_appeared = False
        try:
            element = (
                By.XPATH,
                "//div[@class='jGrowl-message']"
                "[text()='The EOB with trace number {0} & payer id {1} already exist']".format(
                    trace, payer
                ),
            )
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(element)
            )
            notification_appeared = True
        except (
            exceptions.NoSuchElementException,
            exceptions.StaleElementReferenceException,
            exceptions.TimeoutException,
        ):
            pass
        return notification_appeared

    @staticmethod
    def check_if_list_is_sorted_ascending(my_list):
        """
        This method is used to verify whether the given list is sorted in ascending order
        """
        status_ascending_order = False
        x = np.array(my_list)
        if all(x[:-1] <= x[1:]):
            status_ascending_order = True
        return status_ascending_order

    @staticmethod
    def check_if_list_is_sorted_descending(my_list):
        """
        This method is used to verify whether the given list is sorted in descending order
        """
        status_descending_order = False
        x = np.array(my_list)
        if all(x[:-1] >= x[1:]):
            status_descending_order = True
        return status_descending_order

    def is_clickable(self, locator):
        """
        This method is used the get bool value if element is clickable or not
        :@param locator :get locator from locators module
        """
        try:
            self.find_clickable_element(locator=locator)
            return True
        except TimeoutException:
            return False

    def select_date(self, custom_date):
        """
        This method is used the select custom date
        :@param custom_date :get custom_date from test module
        """
        date = custom_date.split("/")
        expected_date_month = int(date[0])
        expected_date_day = int(date[1])
        expected_date_year = int(date[2])

        default_calender_locator = (
            "//div[contains(@class,'xdsoft_datetimepicker') and contains(@style,'display: "
            "block')]"
        )
        time_locator = (
            By.XPATH,
            default_calender_locator
            + "//div[@class='xdsoft_time xdsoft_current']//following-sibling::div",
        )
        try:
            # Date selection
            current_date_locator = (
                By.XPATH,
                default_calender_locator
                + "//tbody//td[contains(@class,'xdsoft_current')]",
            )
            current_date_text_locator = (
                By.XPATH,
                default_calender_locator
                + "//tbody//td[contains(@class,'xdsoft_today')]",
            )

            # self.click(current_date_locator)
            current_date_value = self.get_attribute(
                current_date_text_locator, "data-date"
            )
            if expected_date_day != current_date_value:
                date_to_select = self.driver.find_elements(
                    By.XPATH,
                    default_calender_locator + "//tbody//td[contains("
                    "@class,'xdsoft_date') "
                    "and not(contains("
                    "@class, "
                    "'xdsoft_other_month'))]/div",
                )
                for date in date_to_select:
                    date_select = int(date.text)
                    if date_select == expected_date_day:
                        date.click()
                        break

            # Year element
            current_year_locator = (
                By.XPATH,
                default_calender_locator + "//div[contains(@class,'xdsoft_label "
                "xdsoft_year')]",
            )
            current_year_text_locator = (
                By.XPATH,
                default_calender_locator + "//div[contains(@class,"
                "'xdsoft_yearselect')]//div[contains("
                "@class,'xdsoft_current')]",
            )

            self.click(current_year_locator)
            get_year = int(self.get_text(current_year_text_locator))
            if expected_date_year != get_year:
                years_to_select = self.driver.find_elements(
                    By.XPATH,
                    default_calender_locator + "//div[contains(@class,"
                    "'xdsoft_yearselect')]//div[contains(@class,"
                    "'xdsoft_option')]",
                )
                for year in years_to_select:
                    text = year.get_attribute("data-value")
                    if int(text.strip()) == expected_date_year:
                        year.click()
                        break

            # Month element
            current_month_locator = (
                By.XPATH,
                default_calender_locator
                + "//div[contains(@class,'xdsoft_label xdsoft_month')]",
            )
            current_month_text_locator = (
                By.XPATH,
                default_calender_locator + "//div[contains(@class,"
                "'xdsoft_monthselect')]//div[contains("
                "@class,'xdsoft_current')]",
            )
            self.click(current_month_locator)
            current_month = self.get_text(current_month_text_locator)
            # Month mapping method used to map month in integer to string
            month_need_to_select = self.month_mapping(expected_date_month)
            if month_need_to_select is not current_month:
                month_to_select = self.driver.find_elements(
                    By.XPATH,
                    default_calender_locator + "//div[contains(@class,"
                    "'xdsoft_monthselect')]//div[contains(@class, "
                    "'xdsoft_option')]",
                )
                for month in month_to_select:
                    text = int(month.get_attribute("data-value"))
                    # Month mapping attribute method used to map month in data value to string
                    month_needed = self.month_mapping_attribute(text)
                    if month_needed is month_need_to_select:
                        element = self.find_element(
                            (
                                By.XPATH,
                                default_calender_locator
                                + "//div[contains(@class,'xdsoft_monthselect')]//div["
                                "contains(@class, 'xdsoft_scroller')]",
                            )
                        )
                        self.driver.execute_script(
                            "arguments[0].setAttribute('style', 'display: block; height: "
                            "86px; margin-top: 72px;');",
                            element,
                        )
                        self.driver.execute_script(
                            "arguments[0].setAttribute('style', 'display: block; height: "
                            "86px; margin-top: 0px;');",
                            element,
                        )
                        ActionChains(self.driver).move_to_element(
                            month
                        ).click().perform()
                        break
            else:
                pass
            self.click_via_actionchains_tab(current_date_locator)

        except Exception as e:
            print("Exception Message: ", repr(e))
            return False

    @staticmethod
    def month_mapping(month):
        """
        This method is used to map and return month in string w.r.t. month in integer
        :@param month :get month from test module
        """
        switcher = {
            1: "January",
            2: "February",
            3: "March",
            4: "April",
            5: "May",
            6: "June",
            7: "July",
            8: "August",
            9: "September",
            10: "October",
            11: "November",
            12: "December",
        }
        return switcher.get(month)

    @staticmethod
    def month_mapping_attribute(value):
        """
        This method is used to map and return month in string w.r.t data-value
        :@param value :get value from module
        """
        switcher = {
            0: "January",
            1: "February",
            2: "March",
            3: "April",
            4: "May",
            5: "June",
            6: "July",
            7: "August",
            8: "September",
            9: "October",
            10: "November",
            11: "December",
        }
        return switcher.get(value)

    def login_to_current_provider_if_different(self):
        """
        This method is used to select current provide if it's different.
        """
        provider = self.get_provider_name().strip()
        user, username, name = self.get_current_logged_in_user_detail()
        if provider != name:
            link_switch = (By.XPATH, "//a[@id='switch-button']")
            self.click(link_switch)
            link_doctorid = (
                By.XPATH,
                "//*[@id='updateDoctor']/li/a[contains(text(), '{}')]".format(user),
            )
            self.hover(link_doctorid)
            self.click(link_doctorid)
            time.sleep(2)
        url = self.get_current_url()
        self.assertTrue(username in url, "Failed to login account")

    def enable_feature_flag(
        self,
        feature_internal_name,
        provider="Dr. Mark Williams, Jr",
        override_name="mark23",
        doctor_disable=False,
    ):
        """
        This method is used to enable feature flag for provider Dr. Mark Williams, Jr from markw account, so make sure
        this provider exists in doctor override list
        """
        self.wait_for_spinner_load_to_disappear()
        self.is_displayed(
            (By.XPATH, "//div[@class='nav-collapse collapse']//a[contains(text(),'⚔')]")
        )
        self.hover(
            (By.XPATH, "//div[@class='nav-collapse collapse']//a[contains(text(),'⚔')]")
        )
        self.if_displayed(
            (By.XPATH, "(//a[normalize-space()='Feature Rollout Tool'])[1]")
        )
        self.click((By.XPATH, "(//a[normalize-space()='Feature Rollout Tool'])[1]"))
        self.if_displayed((By.XPATH, "//table/tbody//tr/td"))
        internal_name_textbox = (By.XPATH, "//input[@placeholder='Internal Name']")
        self.click(internal_name_textbox)
        self.type(feature_internal_name, internal_name_textbox)
        self.is_displayed(
            (
                By.XPATH,
                "//th[normalize-space()='Internal Name']/../../..//tbody//code[normalize-space("
                ")='{}']".format(feature_internal_name),
            )
        )
        self.click((By.XPATH, "//i[@title='Edit this document']"))
        time.sleep(15)
        if doctor_disable:
            doctors_expand_xpath = (By.XPATH, "//label[normalize-space()='Doctors']")
            self.click(doctors_expand_xpath)
            time.sleep(1)
            self.scroll(doctors_expand_xpath)
            time.sleep(1)
            is_present = self.get_length(
                (
                    By.XPATH,
                    "//label[normalize-space()='Doctors']/..//td[normalize-space()"
                    "='{}']".format(provider),
                )
            )
            provider_entry = (
                By.XPATH,
                "//label[normalize-space()='Doctors']/..//td[normalize-space()"
                "='{}']/..//td[5]".format(provider),
            )
            if is_present == 1:
                value = self.get_text(provider_entry)
                if value == "false":
                    print("Flag already disabled")
                else:
                    if value == "true":
                        doctors_provider_entry_xpath = (
                            "//label[normalize-space()='Doctors']/..//td[normalize-space()='{}']"
                            "/..".format(provider)
                        )
                        self.click(
                            (
                                By.XPATH,
                                doctors_provider_entry_xpath
                                + "//i[@class='fa fa-arrows-h']",
                            )
                        )
                        time.sleep(5)
                        success_alert = (
                            By.XPATH,
                            "//div[@class='alert alert-dismissible ng-scope ng-binding alert-success']",
                        )
                        # self.if_displayed(success_alert)
                        updated_value = self.get_text(
                            (By.XPATH, doctors_provider_entry_xpath + "//td[5]")
                        )
                        if updated_value == "true":
                            raise AssertionError(
                                "Seems feature flag {} has not been updated after click.".format(
                                    feature_internal_name
                                )
                            )
        else:
            doctors_expand_xpath = (By.XPATH, "//label[normalize-space()='Doctors']")
            self.click(doctors_expand_xpath)
            time.sleep(1)
            self.scroll(doctors_expand_xpath)
            time.sleep(1)
            provider_entry = (
                By.XPATH,
                "//td[normalize-space()='{}']/..//td[5]".format(provider),
            )
            is_present = self.get_length(
                (
                    By.XPATH,
                    "//label[normalize-space()='Doctors']/..//td[normalize-space()"
                    "='{}']".format(provider),
                )
            )
            if is_present == 0:
                override_textbox = (
                    By.XPATH,
                    "//input[@id='overrides_doctors']/..//input[@placeholder='Add new override']",
                )
                self.scroll(override_textbox)
                self.click(override_textbox)
                name = override_name.lower()
                self.type(name, override_textbox)
                time.sleep(3)
                result_xpath = (
                    By.XPATH,
                    "(//a[contains(text(),'{}')])[1]".format(name),
                )
                result_flag = self.is_displayed(result_xpath)
                self.assertTrue(
                    result_flag,
                    "It seems the selected Provider result was not displayed, verify!",
                )
                self.click(result_xpath)
                self.click(
                    (
                        By.XPATH,
                        "//input[@id='overrides_doctors']/..//i[contains(@class,'fa-plus-square-o')]",
                    )
                )
                time.sleep(2)
                self.page_refresh()
                time.sleep(5)
                self.click(doctors_expand_xpath)
                time.sleep(2)
                provider_entry_flag = self.if_displayed(provider_entry)
                self.assertTrue(
                    provider_entry_flag,
                    "It seems the Provider entry is not displayed after selecting from "
                    "override search result!",
                )
                value = self.get_text(provider_entry)
                if value == "false":
                    doctors_provider_entry_xpath = (
                        "//label[normalize-space()='Doctors']/..//td[normalize-space()='{}']"
                        "/..".format(provider)
                    )
                    self.click(
                        (
                            By.XPATH,
                            doctors_provider_entry_xpath
                            + "//i[@class='fa fa-arrows-h']",
                        )
                    )
                    time.sleep(5)
                    success_alert = (
                        By.XPATH,
                        "//div[@class='alert alert-dismissible ng-scope ng-binding alert-success']",
                    )
                    # self.if_displayed(success_alert)
                    updated_value = self.get_text(
                        (By.XPATH, doctors_provider_entry_xpath + "//td[5]")
                    )
                    if updated_value == "false":
                        raise AssertionError(
                            "Seems feature flag {} has not been updated after click.".format(
                                feature_internal_name
                            )
                        )
            else:
                value = self.get_text(provider_entry)
                if value == "false":
                    doctors_provider_entry_xpath = (
                        "//label[normalize-space()='Doctors']/..//td[normalize-space()='{}']"
                        "/..".format(provider)
                    )
                    self.click(
                        (
                            By.XPATH,
                            doctors_provider_entry_xpath
                            + "//i[@class='fa fa-arrows-h']",
                        )
                    )
                    time.sleep(3)
                    success_alert = (
                        By.XPATH,
                        "//div[@class='alert alert-dismissible ng-scope ng-binding alert-success']",
                    )
                    # self.if_displayed(success_alert)
                    updated_value = self.get_text(
                        (By.XPATH, doctors_provider_entry_xpath + "//td[5]")
                    )
                    if updated_value == "false":
                        raise AssertionError(
                            "Seems feature flag {} has not been enabled after click.".format(
                                feature_internal_name
                            )
                        )

    def disable_feature_flag(
        self,
        feature_internal_name,
        provider="Dr. Mark Williams, Jr",
        override_name="mark23",
    ):
        """
        This method is used to disable feature flag for provider Dr. Mark Williams, Jr from markw account, so make sure
        this provider exists in doctor override list
        """
        self.enable_feature_flag(
            feature_internal_name,
            provider,
            override_name,
            doctor_disable=True,
        )

    def enable_feature_flag_user(
        self,
        feature_internal_name,
        provider="Dr. Mark Williams, Jr",
        override_name="mark23",
        user_disable=False,
    ):
        """
        This method is used to enable feature flag for provider Dr. Mark Williams, Jr from markw account, so make sure
        this provider exists in doctor override list
        """
        self.wait_for_spinner_load_to_disappear()
        self.is_displayed(
            (By.XPATH, "//div[@class='nav-collapse collapse']//a[contains(text(),'⚔')]")
        )
        self.hover(
            (By.XPATH, "//div[@class='nav-collapse collapse']//a[contains(text(),'⚔')]")
        )
        self.if_displayed(
            (By.XPATH, "(//a[normalize-space()='Feature Rollout Tool'])[1]")
        )
        self.click((By.XPATH, "(//a[normalize-space()='Feature Rollout Tool'])[1]"))
        self.if_displayed((By.XPATH, "//table/tbody//tr/td"))
        internal_name_textbox = (By.XPATH, "//input[@placeholder='Internal Name']")
        self.click(internal_name_textbox)
        self.type(feature_internal_name, internal_name_textbox)
        self.is_displayed(
            (
                By.XPATH,
                "//th[normalize-space()='Internal Name']/../../..//tbody//code[normalize-space("
                ")='{}']".format(feature_internal_name),
            )
        )
        self.click((By.XPATH, "//i[@title='Edit this document']"))
        time.sleep(15)
        if user_disable:
            user_expand_xpath = (By.XPATH, "//label[normalize-space()='User']")
            self.click(user_expand_xpath)
            time.sleep(1)
            self.scroll(user_expand_xpath)
            time.sleep(1)
            is_present = self.get_length(
                (
                    By.XPATH,
                    "//label[normalize-space()='User']/..//td[normalize-space()"
                    "='{}']".format(provider),
                )
            )
            provider_entry = (
                By.XPATH,
                "//label[normalize-space()='User']/..//td[normalize-space()"
                "='{}']/..//td[3]".format(provider),
            )
            if is_present == 1:
                value = self.get_text(provider_entry)
                if value == "false":
                    print("Flag already disabled")
                else:
                    if value == "true":
                        doctors_provider_entry_xpath = (
                            "//label[normalize-space()='User']/..//td[normalize-space()='{}']"
                            "/..".format(provider)
                        )
                        self.click(
                            (
                                By.XPATH,
                                doctors_provider_entry_xpath
                                + "//i[@class='fa fa-arrows-h']",
                            )
                        )
                        time.sleep(5)
                        success_alert = (
                            By.XPATH,
                            "//div[@class='alert alert-dismissible ng-scope ng-binding alert-success']",
                        )
                        # self.if_displayed(success_alert)
                        updated_value = self.get_text(
                            (By.XPATH, doctors_provider_entry_xpath + "//td[3]")
                        )
                        if updated_value == "true":
                            raise AssertionError(
                                "Seems feature flag {} has not been updated after click.".format(
                                    feature_internal_name
                                )
                            )
        else:
            doctors_expand_xpath = (By.XPATH, "//label[normalize-space()='User']")
            self.click(doctors_expand_xpath)
            time.sleep(1)
            self.scroll(doctors_expand_xpath)
            time.sleep(1)
            provider_entry = (
                By.XPATH,
                "//td[normalize-space()='{}']/..//td[3]".format(provider),
            )
            is_present = self.get_length(
                (
                    By.XPATH,
                    "//label[normalize-space()='User']/..//td[normalize-space()"
                    "='{}']".format(provider),
                )
            )
            if is_present == 0:
                override_textbox = (
                    By.XPATH,
                    "//input[@id='overrides_user']/..//input[@placeholder='Add new override']",
                )
                self.scroll(override_textbox)
                self.click(override_textbox)
                name = override_name.lower()
                self.type(name, override_textbox)
                time.sleep(10)
                result_xpath = (
                    By.XPATH,
                    "(//a[contains(text(),'{}')])[1]".format(provider),
                )
                print(result_xpath)
                result_flag = self.is_displayed(result_xpath)
                self.assertTrue(
                    result_flag,
                    "It seems the selected Provider result was not displayed, verify!",
                )
                self.click(result_xpath)
                self.click(
                    (
                        By.XPATH,
                        "//input[@id='overrides_user']/..//i[contains(@class,'fa-plus-square-o')]",
                    )
                )
                time.sleep(2)
                self.page_refresh()
                time.sleep(5)
                self.click(doctors_expand_xpath)
                time.sleep(2)
                provider_entry_flag = self.if_displayed(provider_entry)
                self.assertTrue(
                    provider_entry_flag,
                    "It seems the Provider entry is not displayed after selecting from "
                    "override search result!",
                )
                value = self.get_text(provider_entry)
                if value == "false":
                    doctors_provider_entry_xpath = (
                        "//label[normalize-space()='User']/..//td[normalize-space()='{}']"
                        "/..".format(provider)
                    )
                    self.click(
                        (
                            By.XPATH,
                            doctors_provider_entry_xpath
                            + "//i[@class='fa fa-arrows-h']",
                        )
                    )
                    time.sleep(5)
                    success_alert = (
                        By.XPATH,
                        "//div[@class='alert alert-dismissible ng-scope ng-binding alert-success']",
                    )
                    # self.if_displayed(success_alert)
                    updated_value = self.get_text(
                        (By.XPATH, doctors_provider_entry_xpath + "//td[3]")
                    )
                    if updated_value == "false":
                        raise AssertionError(
                            "Seems feature flag {} has not been updated after click.".format(
                                feature_internal_name
                            )
                        )
            else:
                value = self.get_text(provider_entry)
                if value == "false":
                    doctors_provider_entry_xpath = (
                        "//label[normalize-space()='User']/..//td[normalize-space()='{}']"
                        "/..".format(provider)
                    )
                    self.click(
                        (
                            By.XPATH,
                            doctors_provider_entry_xpath
                            + "//i[@class='fa fa-arrows-h']",
                        )
                    )
                    time.sleep(3)
                    success_alert = (
                        By.XPATH,
                        "//div[@class='alert alert-dismissible ng-scope ng-binding alert-success']",
                    )
                    # self.if_displayed(success_alert)
                    updated_value = self.get_text(
                        (By.XPATH, doctors_provider_entry_xpath + "//td[3]")
                    )
                    if updated_value == "false":
                        raise AssertionError(
                            "Seems feature flag {} has not been enabled after click.".format(
                                feature_internal_name
                            )
                        )

    def disable_feature_flag_user(
        self,
        feature_internal_name,
        provider="Dr. Mark Williams, Jr",
        override_name="mark23",
    ):
        """
        This method is used to disable feature flag for provider Dr. Mark Williams, Jr from markw account, so make sure
        this provider exists in doctor override list
        """
        self.enable_feature_flag_user(
            feature_internal_name,
            provider,
            override_name,
            user_disable=True,
        )

    def cut_text(self):
        """
        This method is used to enter the value
        :@param driver :get locator from locators module
        """
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys("a").key_up(
            Keys.CONTROL
        ).perform()
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys("x").key_up(
            Keys.CONTROL
        ).perform()

    def paste_text(self):
        """
        This method is used to enter the value
        :@param driver :get locator from locators module
        """
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys("v").key_up(
            Keys.CONTROL
        ).perform()

    def get_windows_count(self):
        """
        This method is used to get window handles count in integer
        """
        windows = self.driver.window_handles
        return len(windows)

    def check_support_option_and_close_popup(self):
        """
        Method is used to check whether Support option is displayed and close Walk-through pop-up if displayed
        """
        support_option_iframe = (By.XPATH, "//iframe[@id='launcher']")
        self.is_displayed(support_option_iframe)
        time.sleep(2)

    def normal_click(self, locator):
        """
        This method is used to click the element
        :@param driver :get locator from locators module
        """
        try:
            self.wait_explicit()
            element = self.find_clickable_element(locator)
            element.click()
        except ElementClickInterceptedException:
            self.click_via_script(locator)
        except StaleElementReferenceException:
            return False

    @staticmethod
    def read_data_from_csv(file_name):
        """
        This method is used to read the data from csv file
        """
        my_list = []
        with open(file_name) as file:
            data = csv.reader(file, delimiter=",")
            next(data)  # To skip the header
            for row in data:
                my_list.append(row)
        return my_list

    def compare_title(self, page_title):
        """
        This method is used to compare the title with flags
        """
        get_title = self.get_page_title()
        self.assertEqual(get_title, page_title)

    def compare_title_with_no_page_error(self, page_title):
        """
        This method is used to compare the title with no page error
        """
        get_title = self.get_page_title()
        self.assertEqual(get_title, page_title)

    def double_click(self, locator):
        """
        This method is used to double click the element
        :@param driver :get locator from locators module
        """
        try:
            self.wait_explicit()
            ActionChains(self.driver).double_click(self.find_element(locator)).perform()
        except ElementClickInterceptedException:
            self.click_via_script(locator)
        except StaleElementReferenceException:
            return False

    def wait_for_invisibility_of_element(self, element):
        """
        This method is used to wait for the web-element to disappear.
        """
        WebDriverWait(self.driver, 10).until(
            (EC.invisibility_of_element_located((By.XPATH, element)))
        )

    def wait_for_visibility_of_element(self, locator):
        """
        This method is used to wait for the web-element to appear.
        """
        self.explicit_wait.until(EC.visibility_of_element_located(locator))

    def wait_explicitly_for_invisibility_of_element(self, locator):
        """
        This method is used to wait for the web-element to appear.
        """
        self.explicit_wait.until(EC.invisibility_of_element_located(locator))

    @staticmethod
    def get_onpatient_signup_link_from_email():
        """
        This method is used to get signup link from given email address from the first email entry available
        """
        import imaplib
        import email
        import re

        # account credentials
        username = outlook_username
        password = outlook_password

        imap_server = "outlook.office365.com"
        # create an IMAP4 class with SSL
        imap = imaplib.IMAP4_SSL(imap_server)
        # authenticate
        imap.login(username, password)

        status, messages = imap.select("Inbox")

        result, data = imap.uid("search", "UNSEEN")  # search all email and return uids
        links_list = []
        if result == "OK":
            for num in data[0].split():
                result, data = imap.uid("fetch", num, "(RFC822)")
                if result == "OK":
                    email_message = email.message_from_bytes(
                        data[0][1]
                    )  # raw email text including headers
                    subject = email_message["Subject"]
                    if "Connect with " in subject:
                        for link in re.findall(
                            "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|%[0-9a-fA-F][0-9a-fA-F])+",
                            email_message.as_string(),
                        ):
                            links_list.append(link)

        imap.close()
        imap.logout()
        signup_link = links_list[0]
        print(signup_link)
        return signup_link

    def wait_for_in_visibility_of_element(self, element, waiting_time):
        """
        This method is used to wait for the web-element to disappear and waiting time given by user
        """
        WebDriverWait(self.driver, waiting_time).until(
            (EC.invisibility_of_element_located((By.XPATH, element)))
        )

    def find_element_by_css_selector(self, element):
        """
        This method is used to find the element using css selector
        """
        return self.driver.find_element(By.CSS_SELECTOR, element)

    @staticmethod
    def get_public_ip_address():
        """
        This method is used to get public IP address of the current machine
        """
        ip_json_endpoint = "https://api.ipify.org?format=json"

        response = requests.get(ip_json_endpoint)
        return json.loads(response.text)["ip"]

    def get_month_number(self, month_name):
        """
        This method is used to find the month number
        """
        from datetime import datetime

        month_name = month_name.lower()
        if len(month_name) == 3:
            month_num = datetime.strptime(month_name, "%b").month
        else:
            month_num = datetime.strptime(month_name, "%B").month
        return month_num

    def get_month_name(self, month_num):
        """
        This method is used to get month name from month number
        """
        import calendar

        if len(month_num) == 2:
            if month_num[0] == "0":
                month_num = int(month_num[1])
            else:
                month_num = int(month_num)
        else:
            month_num = int(month_num)

        return calendar.month_abbr[month_num]

    def get_border_color(self, locator):
        """
        This method is used to get border color
        """
        element = self.driver.find_element(By.XPATH, locator)
        color = element.value_of_css_property("border-color")
        hex_number = Color.from_string(color).hex
        return hex_number

    def type_text(self, value, locator):
        """
        This method is used to clear the value by backspace key
        :@param driver :get locator from locators module
        """
        element = self.find_clickable_element(locator)
        count = len(value)
        for item in range(0, count):
            element.send_keys(value[item])
            time.sleep(0.8)

    @staticmethod
    def time_stamp_without_seconds():
        time_stamp = datetime.now(eastern_time).strftime("%m_%d_%Y_%H_%M")
        return time_stamp

    def PressKey(self, key):
        """
        This method will help to perform key press action
        """
        action = ActionChains(self.driver)
        if self.GetKey(key) is not "":
            action.send_keys(self.GetKey(key)).perform()
        else:
            action.send_keys(key).perform()

    def PressKeys(self, keys):
        """
        This method will press keyboard keys given as list. Keys Shift, Control and Alt use key down event.
        """
        sequence = ActionChains(self.driver)
        keys = [x.lower() for x in keys]

        if "shift" in keys:
            sequence = sequence.key_down(Keys.SHIFT)
        if "control" in keys:
            sequence = sequence.key_down(Keys.CONTROL)
        if "alt" in keys:
            sequence = sequence.key_down(Keys.ALT)
        if len(keys) > 0:
            for k in keys:
                if self.GetKey(k) is not "":
                    sequence = sequence.send_keys(self.GetKey(k))
                else:
                    sequence = sequence.send_keys(k)

        if "shift" in keys:
            sequence = sequence.key_up(Keys.SHIFT)
        if "control" in keys:
            sequence = sequence.key_up(Keys.CONTROL)
        if "alt" in keys:
            sequence = sequence.key_up(Keys.ALT)
        sequence.perform()

    def PressKeyDown(self, key):
        sequence = ActionChains(self.driver)
        if "shift" in key:
            sequence = sequence.key_down(Keys.SHIFT)
        if "control" in key:
            sequence = sequence.key_down(Keys.CONTROL)
        if "alt" in key:
            sequence = sequence.key_down(Keys.ALT)
        sequence.perform()

    def PressKeyUp(self, key):
        sequence = ActionChains(self.driver)
        if "shift" in key:
            sequence = sequence.key_up(Keys.SHIFT)
        if "control" in key:
            sequence = sequence.key_up(Keys.CONTROL)
        if "alt" in key:
            sequence = sequence.key_up(Keys.ALT)
        sequence.perform()

    def SendText(self, text):
        self.switch_to_window(1)
        action = ActionChains(self.driver)
        action.send_keys(text).build().perform()

    def GetKey(self, key):
        """
        This method will return key stroke based upon key enter
        """
        key = key.lower()
        switcher = {
            "enter": Keys.ENTER,
            "tab": Keys.TAB,
            "shift": Keys.SHIFT,
            "control": Keys.CONTROL,
            "alt": Keys.ALT,
            "space": Keys.SPACE,
            "arrowup": Keys.ARROW_UP,
            "arrowdown": Keys.ARROW_DOWN,
            "arrowleft": Keys.ARROW_LEFT,
            "arrowright": Keys.ARROW_RIGHT,
            "delete": Keys.DELETE,
            "backspace": Keys.BACKSPACE,
            "home": Keys.HOME,
            "end": Keys.END,
        }
        return switcher.get(key)

    @staticmethod
    def generate_random_with_n_digits(num_of_digits):
        """
        This method will generate numbers based on number of digits provided
        """
        range_start = 10 ** (num_of_digits - 1)
        range_end = (10**num_of_digits) - 1
        return randint(range_start, range_end)

    @staticmethod
    def get_days_between_two_dates(date_1, date_2):
        """
        This method is used to get the days between the two dates
        """
        d1 = datetime.strptime(date_1, "%m/%d/%Y")
        d2 = datetime.strptime(date_2, "%m/%d/%Y")
        delta = d2 - d1
        return delta.days

    def zoom_out_screen_resolution(self):
        """
        This method will zoom out screen resolution
        """
        self.driver.set_window_size(1920, 1080)
        # self.execute_script("document.body.style.zoom = '80%';")

    def compare_page_title(self, page_title):
        """
        This method is used to compare the title
        """
        get_title = self.get_page_title()
        self.assertEqual(get_title, page_title)

    def handle_alert_text(self, user_text, handle="OK"):
        if self.if_alert_present():
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            self.assertIn(user_text, alert_text, "alert text not matched")
            if handle == "OK":
                alert.accept()
                time.sleep(2)
                return alert_text
            else:
                alert.dismiss()
                return alert_text

    def verify_pdf_content(self):
        """
        This method is used to verify pdf content
        """
        time.sleep(4)
        preview_pdf_xpath = (By.XPATH, "//embed[@type='application/pdf']")
        preview_pdf = self.is_displayed(preview_pdf_xpath)
        self.assertTrue(
            preview_pdf, "It seems the PDF was not generated, kindly verify!"
        )
        time.sleep(3)
        self.closetab()
        time.sleep(1.5)

    def wait_for_invisibility_of_element(self, element):
        """
        This method is used to wait for the web-element to disappear.
        """
        WebDriverWait(self.driver, 10).until(
            (EC.invisibility_of_element_located((By.XPATH, element)))
        )

    def get_popup_notification_text(self):
        """
        This method is used to get popup notification text.
        """
        popup_notification = (By.XPATH, "//div[@id='jGrowl']")
        flag = self.is_displayed(popup_notification)
        if flag:
            popup_notification_text = (By.XPATH, "//div[@class='jGrowl-message']")
            get_popup_text = self.get_text(popup_notification_text)
            return get_popup_text

    def get_page_source(self):
        """
        This method is used to get page source
        """
        src = self.driver.page_source
        return src

    def return_checkbox_status(self, locators):
        """
        This method is used to check if checkbox is checked or not.
        """
        element = self.find_element(locators)
        status = element.is_selected()
        return status

    @staticmethod
    def future_day_stamp(day):
        day = int(datetime.now(eastern_time).strftime("%d")) + int(
            str(timedelta(days=day))[0]
        )
        return day

    def wait_for_spinner_load_to_disappear(self):
        """
        This method will wait for spinner load to disappear
        """
        retry_count = 0
        loader_flag_xpath = (By.XPATH, "//div[@class ='loading_cover']")
        loader_flag = self.if_displayed(loader_flag_xpath)
        while loader_flag:
            time.sleep(5)
            loader_flag_xpath = (By.XPATH, "//div[@class ='loading_cover']")
            loader_flag = self.if_displayed(loader_flag_xpath)
            retry_count += 1
            if retry_count > 15:
                print("Seems there is an issue with page loading")
                break

    @staticmethod
    def get_number_of_days_in_month(custom_date):
        """
        This method is used to get number of days in a month
        """
        date_list = custom_date.split("/")
        year = int(date_list[2])
        if len(date_list[0]) == 2:
            if (date_list[0])[0] == "0":
                month = int((date_list[0])[1])
            else:
                month = int(date_list[0])
        else:
            month = int(date_list[0])
        if (
            month == 1
            or month == 3
            or month == 5
            or month == 7
            or month == 8
            or month == 10
            or month == 12
        ):
            max_day_value = 31
        elif month == 4 or month == 6 or month == 9 or month == 11:
            max_day_value = 30
        elif year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
            max_day_value = 29
        else:
            max_day_value = 28
        return max_day_value

    def check_flag_popup(self):
        """
        This method will close flag pop up on adding patient in appointment.
        """
        FLAG_ALERT_MODAL = (By.XPATH, "(//h3[contains(text(),'Flag Alert')])[1]")
        FLAG_ALERT_OKAY_BTN = (By.XPATH, "(//button[@id='close-flag-alert-modal'])[1]")
        alert_flag = self.if_displayed(FLAG_ALERT_MODAL)
        if alert_flag:
            self.click(FLAG_ALERT_OKAY_BTN)
            time.sleep(2)

    def get_nth_day_with_format(self, nth_day, format):
        any_date = datetime.now() + timedelta(days=int(nth_day))
        eastern_day = any_date.strftime(format)
        return eastern_day

    def remove_readonly_attribute_from_html(self, element):
        """
        This method is used to remove the readonly attribute from html tag
        """
        self.driver.execute_script("arguments[0].removeAttribute('readonly')", element)

    def navigate_to_url(self, url):
        """
        This method is used to open given URL in the same tab
        """
        self.driver.get(url)

    def enable_feature_flag_for_practice_group(
        self,
        feature_internal_name,
        practice_group,
        pg_override_name,
        pg_disable=False,
    ):
        """
        This method is used to enable feature flag for provider Dr. Mark Williams, Jr from markw account, so make sure
        this provider exists in doctor override list
        """
        self.wait_for_spinner_load_to_disappear()
        self.is_displayed(
            (By.XPATH, "//div[@class='nav-collapse collapse']//a[contains(text(),'⚔')]")
        )
        self.hover(
            (By.XPATH, "//div[@class='nav-collapse collapse']//a[contains(text(),'⚔')]")
        )
        self.if_displayed(
            (By.XPATH, "(//a[normalize-space()='Feature Rollout Tool'])[1]")
        )
        self.click((By.XPATH, "(//a[normalize-space()='Feature Rollout Tool'])[1]"))
        self.if_displayed((By.XPATH, "//table/tbody//tr/td"))
        internal_name_textbox = (By.XPATH, "//input[@placeholder='Internal Name']")
        self.click(internal_name_textbox)
        self.type(feature_internal_name, internal_name_textbox)
        self.is_displayed(
            (
                By.XPATH,
                "//th[normalize-space()='Internal Name']/../../..//tbody//code[normalize-space("
                ")='{}']".format(feature_internal_name),
            )
        )
        self.click((By.XPATH, "//i[@title='Edit this document']"))
        time.sleep(15)
        if pg_disable:
            user_expand_xpath = (
                By.XPATH,
                "//label[normalize-space()='Practice Groups']",
            )
            self.click(user_expand_xpath)
            time.sleep(1)
            self.scroll(user_expand_xpath)
            time.sleep(1)
            is_present = self.get_length(
                (
                    By.XPATH,
                    "//label[normalize-space()='Practice Groups']/..//td[normalize-space()"
                    "='{}']".format(practice_group),
                )
            )
            provider_entry = (
                By.XPATH,
                "//label[normalize-space()='Practice Groups']/..//td[normalize-space()"
                "='{}']/..//td[4]".format(practice_group),
            )
            if is_present == 1:
                value = self.get_text(provider_entry)
                if value == "false":
                    print("Flag already disabled")
                else:
                    if value == "true":
                        doctors_provider_entry_xpath = (
                            "//label[normalize-space()='Practice Groups']/..//td[normalize-space()='{}']"
                            "/..".format(practice_group)
                        )
                        self.click(
                            (
                                By.XPATH,
                                doctors_provider_entry_xpath
                                + "//i[@class='fa fa-arrows-h']",
                            )
                        )
                        time.sleep(5)
                        success_alert = (
                            By.XPATH,
                            "//div[@class='alert alert-dismissible ng-scope ng-binding alert-success']",
                        )
                        # self.if_displayed(success_alert)
                        updated_value = self.get_text(
                            (By.XPATH, doctors_provider_entry_xpath + "//td[3]")
                        )
                        if updated_value == "true":
                            raise AssertionError(
                                "Seems feature flag {} has not been updated after click.".format(
                                    feature_internal_name
                                )
                            )
        else:
            doctors_expand_xpath = (
                By.XPATH,
                "//label[normalize-space()='Practice Groups']",
            )
            self.click(doctors_expand_xpath)
            time.sleep(1)
            self.scroll(doctors_expand_xpath)
            time.sleep(1)
            provider_entry = (
                By.XPATH,
                "//td[normalize-space()='{}']/..//td[4]".format(practice_group),
            )
            is_present = self.get_length(
                (
                    By.XPATH,
                    "//label[normalize-space()='Practice Groups']/..//td[normalize-space()"
                    "='{}']".format(practice_group),
                )
            )
            if is_present == 0:
                override_textbox = (
                    By.XPATH,
                    "//input[@id='overrides_groups']/..//input[@placeholder='Add new override']",
                )
                self.scroll(override_textbox)
                self.click(override_textbox)
                name = pg_override_name.lower()
                self.type(name, override_textbox)
                time.sleep(10)
                result_xpath = (
                    By.XPATH,
                    "(//a[contains(text(),'{}')])[2]".format(practice_group),
                )
                print(result_xpath)
                time.sleep(5)
                result_flag = self.is_displayed(result_xpath)
                self.assertTrue(
                    result_flag,
                    "It seems the selected Provider result was not displayed, verify!",
                )
                self.click(result_xpath)
                self.click(
                    (
                        By.XPATH,
                        "//input[@id='overrides_groups']/..//i[contains(@class,'fa-plus-square-o')]",
                    )
                )
                time.sleep(2)
                self.page_refresh()
                time.sleep(5)
                self.click(doctors_expand_xpath)
                time.sleep(2)
                provider_entry_flag = self.if_displayed(provider_entry)
                self.assertTrue(
                    provider_entry_flag,
                    "It seems the Provider entry is not displayed after selecting from "
                    "override search result!",
                )
                value = self.get_text(provider_entry)
                if value == "false":
                    doctors_provider_entry_xpath = (
                        "//label[normalize-space()='Practice Groups']/..//td[normalize-space()='{}']"
                        "/..".format(practice_group)
                    )
                    self.click(
                        (
                            By.XPATH,
                            doctors_provider_entry_xpath
                            + "//i[@class='fa fa-arrows-h']",
                        )
                    )
                    time.sleep(5)
                    success_alert = (
                        By.XPATH,
                        "//div[@class='alert alert-dismissible ng-scope ng-binding alert-success']",
                    )
                    # self.if_displayed(success_alert)
                    updated_value = self.get_text(
                        (By.XPATH, doctors_provider_entry_xpath + "//td[4]")
                    )
                    if updated_value == "false":
                        raise AssertionError(
                            "Seems feature flag {} has not been updated after click.".format(
                                feature_internal_name
                            )
                        )
            else:
                value = self.get_text(provider_entry)
                if value == "false":
                    doctors_provider_entry_xpath = (
                        "//label[normalize-space()='Practice Groups']/..//td[normalize-space()='{}']"
                        "/..".format(practice_group)
                    )
                    self.click(
                        (
                            By.XPATH,
                            doctors_provider_entry_xpath
                            + "//i[@class='fa fa-arrows-h']",
                        )
                    )
                    time.sleep(3)
                    success_alert = (
                        By.XPATH,
                        "//div[@class='alert alert-dismissible ng-scope ng-binding alert-success']",
                    )
                    # self.if_displayed(success_alert)
                    updated_value = self.get_text(
                        (By.XPATH, doctors_provider_entry_xpath + "//td[4]")
                    )
                    if updated_value == "false":
                        raise AssertionError(
                            "Seems feature flag {} has not been enabled after click.".format(
                                feature_internal_name
                            )
                        )

    def disable_feature_flag_for_practice_group(
        self,
        feature_internal_name,
        practice_group_name,
        pg_override_name,
    ):
        """
        This method is used to disable feature flag for practice groups, make to pass name of feature flag and
        practice group.
        """
        self.enable_feature_flag_for_practice_group(
            feature_internal_name,
            practice_group_name,
            pg_override_name,
            pg_disable=True,
        )

    def convert_into_24_hour_format(self, time):
        """
        This method is used to convert time into 24 hour format
        """
        hour = int(time[:2]) % 12
        minutes = int(time[3:5])
        if time[5] == "p":
            hour += 12
        return "{:02}:{:02}".format(hour, minutes)

    @staticmethod
    def get_day_name_of_date(required_date):
        """
        This method is used to get the name of that particular day
        :@param pass the date in the format dd/mm/YYYY
        """
        import datetime

        required_date_list = required_date.split("/")
        particular_date = required_date_list[1]
        particular_month = required_date_list[0]
        if len(particular_date) == 2:
            if particular_date[0] == 0:
                particular_date = particular_date[1]
            else:
                particular_date = particular_date
        else:
            particular_date = particular_date
        if len(particular_month) == 2:
            if particular_month[0] == 0:
                particular_month = particular_month[1]
            else:
                particular_month = particular_month
        else:
            particular_date = particular_month
        d = datetime.date(
            int(required_date_list[2]), int(particular_month), int(particular_date)
        )
        return calendar.day_name[d.weekday()]

    def get_next_hour_time(self):
        """
        This method is used to get current hour
        """
        date = datetime.now()
        new_date = date.strftime("%I:00%p")
        new_date = new_date.replace("AM", "am").replace("PM", "pm")
        return new_date

    @staticmethod
    def get_appointment_id_from_patient_chart(href_url):
        """
        Method is used to get Appointment ID from Clinical Note link
        """
        appointment_id = href_url.split("/")
        print(appointment_id)
        if appointment_id[-1] != "":
            return appointment_id[-1]
        else:
            return appointment_id[-2]

    def verify_feature_flag(
        self,
        feature_internal_name,
    ):
        """
        This method is used to verify feature flag for provider Dr. Mark Williams, Jr from markw account.
        """
        self.wait_for_spinner_load_to_disappear()
        self.is_displayed(
            (By.XPATH, "//div[@class='nav-collapse collapse']//a[contains(text(),'⚔')]")
        )
        self.hover(
            (By.XPATH, "//div[@class='nav-collapse collapse']//a[contains(text(),'⚔')]")
        )
        self.if_displayed(
            (By.XPATH, "(//a[normalize-space()='Feature Rollout Tool'])[1]")
        )
        self.click((By.XPATH, "(//a[normalize-space()='Feature Rollout Tool'])[1]"))
        self.if_displayed((By.XPATH, "//table/tbody//tr/td"))
        internal_name_textbox = (By.XPATH, "//input[@placeholder='Internal Name']")
        self.click(internal_name_textbox)
        self.type(feature_internal_name, internal_name_textbox)
        ff_check = self.is_displayed(
            (
                By.XPATH,
                "//th[normalize-space()='Internal Name']/../../..//tbody//code[normalize-space("
                ")='{}']".format(feature_internal_name),
            )
        )
        self.assertTrue(ff_check, "Unable to verify feature flag, please verify!!!")

    def enter_the_text_using_javascript(self, locator, value):
        """
        This method is used to enter the txt usting javascript
        """
        element = self.find_element(locator)
        value_to_type = "arguments[0].value='{}'".format(value)
        self.driver.execute_script(value_to_type, element)

    def get_start_date_end_date_given_start_date_by_adding_days(
        self, start_date, days_to_add
    ):
        """
        This method will return start date, end date after adding days to start date
        """
        # Define the start date
        start = datetime.strptime(start_date, "%m/%d/%Y")

        # Add days
        end_date = start + timedelta(days=days_to_add)
        end_date = end_date.strftime("%m/%d/%Y")
        return start_date, end_date

    @staticmethod
    def compare_two_dates(date_1, date_2):
        """
        This method is used to compare the dates
        @ returning true if second date is greater, else False
        """
        d1 = datetime.strptime(date_1, "%m/%d/%Y")
        d2 = datetime.strptime(date_2, "%m/%d/%Y")
        return d2 > d1

    @staticmethod
    def check_whether_string_is_date_format(test_str, format):
        """
        This method is used to validate if given string is date format
        """
        date_format = True
        try:
            date_format = bool(datetime.strptime(test_str, format))
        except ValueError:
            date_format = False
        return date_format

    def wait_for_calendar_toast_updating(self):
        """
        This method is used to validate if given string is date format
        """
        retry_count = 0
        updating_calendar_toast = (
            By.XPATH,
            "//div[@id='sync-notification']//span[normalize-space()='Updating calendar...']",
        )
        try:
            alert_flag = self.if_displayed(updating_calendar_toast)
            while alert_flag:
                time.sleep(5)
                alert_flag = self.if_displayed(updating_calendar_toast)
                retry_count += 1
                if retry_count > 8:
                    print("Seems there is an issue with page loading")
                    break
        except Exception:
            pass
