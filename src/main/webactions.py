import calendar
import os
import time

from configparser import NoOptionError, ConfigParser

from random import randint
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


config = ConfigParser()
project_root = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(project_root, "config")
config.read(config_path)
env = os.getenv("TARGET_ENV", "test")
gcw_new_desktop_url = config.get(env, "gcw_new_desk_url")
gcw_new_mobile_url = config.get(env, "gcw_new_mob_url")
user_name = config.get(env, "username")
passowrd = config.get(env, "password")

eastern_time = pytz.timezone("US/Eastern")


class BasePage:
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

    def wait_for_element_to_display(self, locator):
        """
        This method will wait for element to be visible
        """
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(locator),
                "Timed out waiting for alert to appear",
            )
            return True
        except TimeoutException:
            return False

    def wait_for_element_to_clickable(self, locator):
        """
        This method will wait for element to be visible
        """
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(locator),
                "Timed out waiting for alert to appear",
            )
            return True
        except TimeoutException:
            return False

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
    def get_day_of_week():
        my_date = date.today()
        day = calendar.day_name[my_date.weekday()]
        return day

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

    def navigate_to_url(self, url):
        """
        This method is used to open given URL in the same tab
        """
        self.driver.get(url)

    def enter_the_text_using_javascript(self, locator, value):
        """
        This method is used to enter the txt usting javascript
        """
        element = self.find_element(locator)
        value_to_type = "arguments[0].value='{}'".format(value)
        self.driver.execute_script(value_to_type, element)
