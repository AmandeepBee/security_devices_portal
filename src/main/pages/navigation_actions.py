from src.main.locators.navigation_locators import NavigationTabLocators
from src.main.webactions import BasePage
from selenium.webdriver.support import expected_conditions as EC


class NavigationActions(BasePage):
    """
    This class is used for navigation methods
    """

    def click_home_tab(self):
        """
        This method will click on Home tab on navigation page.
        """
        self.click(NavigationTabLocators.HOME_TAB_NAV_XPATH)
        self.wait_for_element_to_clickable(NavigationTabLocators.FREE_CHLORINE_XPATH)

    def click_clarity_tab(self):
        """
        This method will click on clarity tab on navigation page.
        """
        self.click(NavigationTabLocators.CLARITY_TAB_NAV_XPATH)
        self.wait_for_element_to_clickable(
            NavigationTabLocators.REAL_TIME_STATUS_LABEL_XPATH
        )

    def click_summary_tab(self):
        """
        This method will click on summary tab on navigation page.
        """
        self.click(NavigationTabLocators.SUMMARY_TAB_NAV_XPATH)
        self.wait_for_element_to_clickable(NavigationTabLocators.ACTUAL_VALUE_XPATH)

    def click_overview_tab(self):
        """
        This method will click on overview tab on navigation page.
        """
        self.click(NavigationTabLocators.OVERVIEW_TAB_NAV_XPATH)
        self.wait_for_element_to_clickable(NavigationTabLocators.ACTUAL_VALUE_XPATH)

    def click_charts_tab(self):
        """
        This method will click on charts tab on navigation page.
        """
        self.click(NavigationTabLocators.CHARTS_TAB_NAV_XPATH)
        self.wait_for_element_to_clickable(
            NavigationTabLocators.MEASUREMENTS_VALUE_XPATH
        )

    def click_report_tab(self):
        """
        This method will click on report tab on navigation page.
        """
        self.click(NavigationTabLocators.REPORT_TAB_NAV_XPATH)
        self.wait_for_element_to_clickable(NavigationTabLocators.SUN_XPATH)

    def click_report_download_tab(self):
        """
        This method will click on report download tab on navigation page.
        """
        self.click(NavigationTabLocators.REPORT_TAB_NAV_XPATH)
        self.wait_for_element_to_clickable(
            NavigationTabLocators.CALLIBRATION_REPORT_LABEL_XPATH
        )

    def click_data_download_tab(self):
        """
        This method will click on data download tab on navigation page.
        """
        self.click(NavigationTabLocators.DATA_DOWNLOAD_TAB_NAV_XPATH)
        self.wait_for_element_to_clickable(
            NavigationTabLocators.SELECT_INSTALLATION_LABEL_XPATH
        )

    def click_maintenance_tab(self):
        """
        This method will click on data download tab on navigation page.
        """
        self.click(NavigationTabLocators.MAINTENANCE_TAB_NAV_XPATH)
        self.wait_for_element_to_clickable(
            NavigationTabLocators.SELECT_UNIT_LABEL_XPATH
        )

    def click_settings_tab(self):
        """
        This method will click on settings tab on navigation page.
        """
        self.click(NavigationTabLocators.SETTINGS_TAB_NAV_XPATH)
        self.wait_for_element_to_clickable(NavigationTabLocators.FLOW_STATUS_XPATH)

    def click_user_manual_tab(self):
        """
        This method will click on user manual tab on navigation page.
        """
        self.click(NavigationTabLocators.USER_MANUAL_TAB_NAV_XPATH)
        self.wait_for_element_to_clickable(NavigationTabLocators.USER_MNGMT_PANEL_XPATH)

    def click_active_data_tab(self):
        """
        This method will click on active data tab on navigation page.
        """
        self.click(NavigationTabLocators.ACTIVE_DATA_TAB_NAV_XPATH)
        self.wait_for_element_to_clickable(NavigationTabLocators.FREE_CHLORINE_XPATH)

    def click_installation_tab(self):
        """
        This method will click on installation tab on navigation page.
        """
        self.click(NavigationTabLocators.INSTALLATION_TAB_NAV_XPATH)
        self.wait_for_element_to_clickable(
            NavigationTabLocators.ADD_NEW_INSTALLATION_BTN_XPATH
        )
