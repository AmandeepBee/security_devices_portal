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


@pytest.fixture(scope='session', autouse=True)
def driver():
    """
    Pytest fixture to initialize and close the WebDriver.
    """
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()
        yield driver

    except WebDriverException as e:
        logger.error(f"WebDriverException: {e}")
        pytest.fail(f"WebDriverException: {e}")
    except Exception as e:
        logger.error(f"Unexpected Exception: {e}")
        pytest.fail(f"Unexpected Exception: {e}")
    finally:
        driver.quit()
