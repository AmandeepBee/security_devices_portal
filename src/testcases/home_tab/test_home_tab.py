import pytest

from src.main.pages.login_actions import LoginPageActions
from src.main.pages.navigation_actions import NavigationActions


class TestHomeTab:

    @pytest.mark.smoke
    def test_c2_login_to_new_gcw_desktop_portal_home_tab(self, driver):
        """
        This test will login to new desktop portal of GCW and test home tab
        1. Login to Portal
        2. Navigate to home tab
        3. Verify home tab
        """
        self.driver = driver
        try:
            self.tc_id = "TS_c2"
            self.tc_desc = "Verify user is able login to new GCW desktop portal"

            login = LoginPageActions(self.driver)
            nav = NavigationActions(self.driver)

            self.tc_step = "Login to GCW desktop portal"
            login.login_to_new_desktop_portal()

            self.tc_step = "Navigate to home tab"
            nav.click_home_tab()

            self.tc_step = "Logout from GCW desktop portal"
            login.logout_from_portal()

        except Exception as e:
            print(e)
            self.fail("Test case failed at {0}".format(self.tc_step))
