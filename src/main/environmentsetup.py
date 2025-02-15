import logging
from datetime import datetime
import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options

time_stamp = datetime.now().strftime("%m/%d/%Y")
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestBase:
    """
    Initialization and closure of driver for each class - Globally
    """

    driver = None

    @pytest.fixture(scope="function")
    def driver_request(request):
        """
        Pytest fixture to initialize and close the WebDriver.
        """
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.maximize_window()
            request.driver = driver
            yield driver

        except WebDriverException as e:
            logger.error(f"WebDriverException: {e}")
            pytest.fail(f"WebDriverException: {e}")
        except Exception as e:
            logger.error(f"Unexpected Exception: {e}")
            pytest.fail(f"Unexpected Exception: {e}")
        finally:
            driver.quit()
