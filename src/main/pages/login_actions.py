from configparser import ConfigParser
import os
import time

import pytz
from src.main.locators.login_locators import LoginLocators
from src.main.webactions import BasePage


class LoginPage(BasePage):
    """
    This class is used for loing verification
    """

    config = ConfigParser()
    project_root = os.path.dirname(os.path.dirname(__file__))
    config_path = os.path.join(project_root, "config")
    config.read(config_path)
    env = os.getenv("TARGET_ENV", "test")
    gcw_new_desktop_url = config.get(env, "gcw_new_desk_url")
    gcw_new_mobile_url = config.get(env, "gcw_new_mob_url")
    user_name = config.get(env, "username")
    passowrd = config.get(env, "password")

    eastern_time = pytz.timezone("US/Eastern")

    def get_gcw_new_portal_desktop_url(self):
        """
        This method will get new portal desktop url
        """
        self.driver.get(self.gcw_new_desktop_url)

    def login_to_new_desktop_portal(self):
        """
        This method will login to new desktop portal of gcw
        """
        self.get_gcw_new_portal_desktop_url()
        time.sleep(1)
        login_displayed = self.is_displayed(LoginLocators.USER_NAME_TEXT_BOX_XPATH)
        if not login_displayed:
            raise AssertionError("There is problem with login page load, please check")
        self.type(self.user_name, LoginLocators.USER_NAME_TEXT_BOX_XPATH)
        self.type(self.passowrd, LoginLocators.USER_PASSWORD_TEXT_BOX_XPATH)
        self.click(LoginLocators.SUBMIT_BTN_XPATH)

        home_tab_displayed = self.is_displayed(LoginLocators.HOME_PAGE_TAB_XPATH)
        if not home_tab_displayed:
            raise AssertionError("Seems login page not loading, please check")

    def logout_from_portal(self):
        """
        This method will logout from portal
        """
        self.click(LoginLocators.LOGOUT_BTN_XPATH)
        time.sleep(10)
        login_displayed = self.is_displayed(LoginLocators.USER_NAME_TEXT_BOX_XPATH)
        if not login_displayed:
            raise AssertionError("There is problem with logout, please check")
