from selenium.webdriver.common.by import By


class LoginLocators(object):
    """
    This section if for login page locators.
    """

    USER_NAME_TEXT_BOX_XPATH = (
        By.XPATH,
        '(//div[@class="login_box_container"]//input)[1]',
    )
    USER_PASSWORD_TEXT_BOX_XPATH = (
        By.XPATH,
        '(//div[@class="login_box_container"]//input)[2]',
    )
    SUBMIT_BTN_XPATH = (By.XPATH, '//div[@class="login_box_container"]//button')

    HOME_PAGE_TAB_XPATH = (By.XPATH, '//a[@href="/home"]')

    LOGOUT_BTN_XPATH = (
        By.XPATH,
        '//i[contains(@class, "fa-sign-out-alt")]/ancestor::li',
    )
