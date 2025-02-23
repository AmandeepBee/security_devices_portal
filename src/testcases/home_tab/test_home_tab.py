import pytest

from src.main.pages.home_tab_actions import HomePageActions
from src.main.pages.login_actions import LoginPageActions
from src.main.pages.navigation_actions import NavigationActions


class TestHomeTab:

    @pytest.mark.smoke
    @pytest.mark.c2
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

            self.tc_step = "Navigate to home tab and verify"
            nav.click_home_tab()

            self.tc_step = "Logout from GCW desktop portal"
            login.logout_from_portal()

        except Exception as e:
            print(e)
            pytest.fail("Test case failed at {0}".format(self.tc_step))

    @pytest.mark.smoke
    @pytest.mark.c3
    @pytest.mark.parametrize(
        "root_device, device", [("Gold Coast Water", "Canowindra Reservoir")]
    )
    def test_c3_verify_default_device_settings_home_tab(
        self, driver, root_device, device
    ):
        """
        This test will navigate home tab and verify default device setting for 1 device selected.
        1. Login to Portal
        2. Navigate to home tab
        3. Uncheck all devices
        4. Select 1 device.
        5. Verify default alert settings selected and shown on map drop.
        """
        self.driver = driver
        try:
            self.tc_id = "TS_c3"
            self.tc_desc = "This test will navigate home tab and verify default device setting for 1 device selected."

            login = LoginPageActions(self.driver)
            nav = NavigationActions(self.driver)
            home_tab = HomePageActions(self.driver)

            self.tc_step = "Login to GCW desktop portal"
            login.login_to_new_desktop_portal()

            self.tc_step = "Navigate to home tab and verify"
            nav.click_home_tab()

            self.tc_step = "Uncheck root device"
            home_tab.uncheck_root_device(root_device)

            self.tc_step = "Select 1 device"
            home_tab.check_device(device)
            default_alerts = home_tab.get_count_of_selected_alerts()

            self.tc_step = "Click map drop and verify details"
            count_of_alerts_on_dialog = (
                home_tab.click_map_drop_verify_and_return_count_of_items(device)
            )

            self.tc_step = "Verify alert count of default selected and on map drop"
            assert (
                default_alerts == count_of_alerts_on_dialog
            ), "Seems there is mis match of alerts selected by default and alerts shown on dialog"

            self.tc_step = "Logout from GCW desktop portal"
            login.logout_from_portal()

        except Exception as e:
            print(e)
            pytest.fail("Test case failed at {0}".format(self.tc_step))

    @pytest.mark.smoke
    @pytest.mark.c4
    @pytest.mark.parametrize(
        "root_device, device, alert_name",
        [("Gold Coast Water", "Canowindra Reservoir", "Salinity")],
    )
    def test_c4_verify_alert_selected_deselected_device_settings_home_tab(
        self, driver, root_device, device, alert_name
    ):
        """
        This test will navigate home tab and verify default device setting for 1 device selected.
        1. Login to Portal
        2. Navigate to home tab
        3. Uncheck all devices
        4. Select 1 device.
        5. Add 1 alert and verfify on home page and map drop dialog.
        """
        self.driver = driver
        try:
            self.tc_id = "TS_c3"
            self.tc_desc = "This test will navigate home tab and verify default device setting for 1 device selected."

            login = LoginPageActions(self.driver)
            nav = NavigationActions(self.driver)
            home_tab = HomePageActions(self.driver)

            self.tc_step = "Login to GCW desktop portal"
            login.login_to_new_desktop_portal()

            self.tc_step = "Navigate to home tab and verify"
            nav.click_home_tab()

            self.tc_step = "Uncheck root device"
            home_tab.uncheck_root_device(root_device)

            self.tc_step = "Select 1 device"
            home_tab.check_device(device)
            default_items = home_tab.get_count_of_selected_alerts()

            self.tc_step = "Add alert on home tab and verify details"
            home_tab.select_alert_on_home_tab(alert_name)
            items_count_after_alert_selected = home_tab.get_count_of_selected_alerts()
            assert (
                default_items + 1 == items_count_after_alert_selected
            ), "Alert count is not as expected"

            self.tc_step = "Click map drop, get alert count and verify details"
            count_of_items_on_dialog = (
                home_tab.click_map_drop_verify_and_return_count_of_items(device)
            )
            assert (
                items_count_after_alert_selected == count_of_items_on_dialog
            ), "Seems there is mis match of items selected by default and items shown on dialog"

            self.tc_step = "Remove alert on home tab and verify details"
            home_tab.deselect_alert_on_home_tab(alert_name)
            items_count_after_alert_deselected = home_tab.get_count_of_selected_alerts()
            assert (
                default_items == items_count_after_alert_deselected
            ), "Alert count is not as expected"

            self.tc_step = "Logout from GCW desktop portal"
            login.logout_from_portal()

        except Exception as e:
            print(e)
            pytest.fail("Test case failed at {0}".format(self.tc_step))
