from selenium.webdriver.common.by import By


class HomeTabLocators(object):
    """
    This section is for home tab locators.
    """

    ROOT_ITEM_XPATH = (By.XPATH, "(//app-tree//ul/li//a/i)[1]")
