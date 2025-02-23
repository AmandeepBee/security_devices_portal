import pytest

from src.main.pages.login_actions import LoginPageActions


class TestGcwNewLogin:

    @pytest.mark.smoke
    @pytest.mark.c1
    def test_c1_login_to_new_gcw_desktop_portal(self, driver):
        """
        This test will login to new desktop portal of GCW
        """
        self.driver = driver
        try:
            self.tc_id = "TS_c1"
            self.tc_desc = "Verify user is able login to new GCW desktop portal"

            login = LoginPageActions(self.driver)

            self.tc_step = "Login to GCW desktop portal"
            login.login_to_new_desktop_portal()

            self.tc_step = "Logout from GCW desktop portal"
            login.logout_from_portal()

        except Exception as e:
            print(e)
            self.fail("Test case failed at {0}".format(self.tc_step))
