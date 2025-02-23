import logging
import time
from src.main.locators.home_tab_locators import HomeTabLocators
from src.main.webactions import BasePage
from selenium.webdriver.common.by import By


class HomePageActions(BasePage):
    """
    This class is used for home page action
    """

    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    def uncheck_root_device(self, root_device):
        """
        This method wiill uncheck root device
        """
        self.wait_for_element_to_clickable(HomeTabLocators.ROOT_ITEM_XPATH)
        time.sleep(5)
        root_device_xpath = (
            By.XPATH,
            '(//div[@class="wrapper_1"]/app-tree//li/a[text()="{0}"]/i)[1]'.format(
                root_device
            ),
        )
        self.click(root_device_xpath)

    def check_device(self, device):
        """
        This method will click on device mentioned as argument
        """
        device_xpath = (By.XPATH, '(//app-tree//a[text()="{0}"]/i)[1]'.format(device))
        self.click(device_xpath)
        time.sleep(3)

    def get_count_of_selected_alerts(self):
        """
        This method will get count of selected alerts on home tab.
        """
        count = self.get_count_of_elements(HomeTabLocators.MAP_DROP_BTN_XPATH)
        count = int(count)
        item_name = []
        if count is not 1:
            raise AssertionError(
                "More than 1 device selected, though selected only one in the test, please check."
            )
        items_xpath = (By.XPATH, '//div[@class="wrapper_2"]/app-sensors//li')
        count_of_item_default = self.get_count_of_elements(items_xpath)
        for i in range(1, count_of_item_default + 1):
            item_selected_xpath = (
                By.XPATH,
                '(//div[@class="wrapper_2"]/app-sensors//li/input)[{0}]'.format(i),
            )
            selected = self.is_selected(item_selected_xpath)
            if selected:
                item_text_xpath = (
                    By.XPATH,
                    '(//div[@class="wrapper_2"]/app-sensors//li/a)[{0}]'.format(i),
                )
                get_text = self.get_text(item_text_xpath)
                item_name.append(get_text)
        count = len(item_name)
        return count

    def click_map_drop_verify_and_return_count_of_items(self, device):
        """
        This method will click on map drop and verify the same.
        """
        time.sleep(2)
        self.click_via_script(HomeTabLocators.MAP_DROP_BTN_XPATH)
        dialog_pop_up_xpath = (By.XPATH, '//span[text()="{0}"]'.format(device))
        self.wait_for_element_to_clickable(dialog_pop_up_xpath)
        items_on_dlg_xpath = (By.XPATH, "//table/tr/td[1]")
        count_of_items_displayed = self.get_count_of_elements(items_on_dlg_xpath)
        self.click_via_script(HomeTabLocators.CLOSE_MAP_DIALOG_XPATH)
        return count_of_items_displayed

    def select_alert_on_home_tab(self, alert_name):
        """
        This method will select alert on home tab.
        """
        item_selected_xpath = (
            By.XPATH,
            '//div[@class="wrapper_2"]/app-sensors//li/a[text()="{0}"]/preceding-sibling::input'.format(
                alert_name
            ),
        )
        selected = self.is_selected(item_selected_xpath)
        if not selected:
            self.click(item_selected_xpath)
        else:
            logging.log("Item already selected")

    def deselect_alert_on_home_tab(self, alert_name):
        """
        This method will de-select alert on home tab.
        """
        item_selected_xpath = (
            By.XPATH,
            '//div[@class="wrapper_2"]/app-sensors//li/a[text()="{0}"]/preceding-sibling::input'.format(
                alert_name
            ),
        )
        selected = self.is_selected(item_selected_xpath)
        if selected:
            self.click(item_selected_xpath)
        else:
            logging.log("Item already de selected")
