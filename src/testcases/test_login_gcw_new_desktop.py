import pytest

from ddt import ddt, data, unpack
from src.main.environmentsetup import TestBase

from src.main.pages.login_actions import LoginPage


@ddt
class GcwNewLoginTest(TestBase):

    @pytest.mark.c1
    @data(())
    @unpack
    def test_ts_login_to_new_gcw_desktop_portal(self):
        """
        This test will login to new desktop portal of GCW
        """
        try:
            self.tc_id = "TS_c1"
            self.tc_desc = "Verify user is able login to new GCW desktop portal"

            login = LoginPage(self.driver)

            self.tc_step = "Login to GCW desktop portal"
            login.login_to_new_desktop_portal()

            self.tc_step = "Logout for desktop portal"
            login.logout_from_portal()

        except Exception as e:
            print(e)
            self.test_fail = True
