from selenium.webdriver.common.by import By


class HomeTabLocators(object):
    """
    This section is for home tab locators.
    """

    ROOT_ITEM_XPATH = (By.XPATH, "(//app-tree//ul/li//a/i)[1]")
    MAP_DROP_BTN_XPATH = (By.XPATH, '//div[@role="button"]')
    CLOSE_MAP_DIALOG_XPATH = (
        By.XPATH,
        '(//span[text()="Canowindra Reservoir"]/../span)[2]',
    )
