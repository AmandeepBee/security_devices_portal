from selenium.webdriver.common.by import By


class NavigationTabLocators(object):
    """
    This method is for navigation tab locators.
    """

    HOME_TAB_NAV_XPATH = (By.XPATH, '//a[@href="/home"]')
    FREE_CHLORINE_XPATH = (By.XPATH, '//a[text()="Free Chlorine"]')

    CLARITY_TAB_NAV_XPATH = (By.XPATH, '//a[@href="/clarity"]')
    REAL_TIME_STATUS_LABEL_XPATH = (By.XPATH, '//div[text()="Real-Time Status"]')

    SUMMARY_TAB_NAV_XPATH = (By.XPATH, '//a[@href="/summary"]')
    ACTUAL_VALUE_XPATH = (By.XPATH, '//a[text()="Actual Values"]')

    OVERVIEW_TAB_NAV_XPATH = (By.XPATH, '//a[@href="/overview"]')

    CHARTS_TAB_NAV_XPATH = (By.XPATH, '//a[@href="/charts"]')
    MEASUREMENTS_VALUE_XPATH = (By.XPATH, '//a[text()="Measurements"]')

    REPORT_TAB_NAV_XPATH = (By.XPATH, '//a[@href="/report"]')
    SUN_XPATH = (By.XPATH, '//button[text()="Sun"]')

    REPORT_DOWNLOAD_TAB_NAV_XPATH = (By.XPATH, '//a[@href="/reportdownload"]')
    CALLIBRATION_REPORT_LABEL_XPATH = '//a[text()="Calibration Reports"]'

    DATA_DOWNLOAD_TAB_NAV_XPATH = (By.XPATH, '//a[@href="/datadownload"]')
    SELECT_INSTALLATION_LABEL_XPATH = (
        By.XPATH,
        '//h3[text()="Please select an installation"]',
    )

    MAINTENANCE_TAB_NAV_XPATH = (By.XPATH, '//a[@href="/maintenance"]')
    SELECT_UNIT_LABEL_XPATH = (By.XPATH, '//h3[text()="Please Select a Unit"]')
    MONITORING_LABEL_XPATH = (By.XPATH, '//a[text()="Monitoring"]')

    SETTINGS_TAB_NAV_XPATH = (By.XPATH, '//a[@href="/settings"]')
    FLOW_STATUS_XPATH = (By.XPATH, '//a[text()="Flow Status"]')

    USER_MANUAL_TAB_NAV_XPATH = (By.XPATH, '//a[@href="/usermanual"]')
    USER_MNGMT_PANEL_XPATH = (By.XPATH, '//div[text()="User Management Panel"]')

    ACTIVE_DATA_TAB_NAV_XPATH = (By.XPATH, '//a[@href="/activedata"]')
    INSTALLATION_TAB_NAV_XPATH = (By.XPATH, '//a[@href="/installtions"]')
    ADD_NEW_INSTALLATION_BTN_XPATH = (
        By.XPATH,
        '//button[text()=" Add a New Installation "]',
    )
