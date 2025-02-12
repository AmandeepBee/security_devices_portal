import os

import pytest

from ddt import ddt, data, unpack
from src.main.environmentsetup import TestBase

from datetime import datetime


@ddt
class LoginTest(TestBase):

    @pytest.mark.c304
    @pytest.mark.production_smoke
    @data(())
    @unpack
    def test_ts_login(self):
        """
        """
        try:
            self.tc_id = "TS_c304"
            self.tc_desc = (
                "Verify user is able to Edit Clinical Notes from Patient's chart"
            )
            self.test_fail = False

            self.tc_step = (
                "Goto Patient's chart and check if appointments are available"
            )

        except Exception as e:
            print(e)
            self.test_fail = True