"""
WebUtils - Custom Library for Enhanced Web Automation
Provides advanced web interaction utilities for Robot Framework
"""

import time
import os
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from robot.api import logger
from robot.api.deco import keyword, library
import yaml

@library
class WebUtils:
    """Enhanced web automation utilities"""

    def __init__(self):
        self.screenshot_counter = 0
        self.config = self._load_config()

    def _load_config(self):
        """Load configuration from yaml file"""
        try:
            with open('config/robot.yaml', 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            logger.warn(f"Could not load config: {e}")
            return {}

    @keyword("Wait And Click Element")
    def wait_and_click_element(self, locator, timeout=10):
        """Wait for element to be clickable and click it"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, locator))
            )
            element.click()
            logger.info(f"Clicked element: {locator}")
            return True
        except TimeoutException:
            logger.error(f"Element not clickable within {timeout}s: {locator}")
            return False

    @keyword("Wait For Element To Be Visible")
    def wait_for_element_visible(self, locator, timeout=10):
        """Wait for element to be visible"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((By.XPATH, locator))
            )
            logger.info(f"Element visible: {locator}")
            return True
        except TimeoutException:
            logger.error(f"Element not visible within {timeout}s: {locator}")
            return False

    @keyword("Take Screenshot On Failure")
    def take_screenshot_on_failure(self, test_name):
        """Take screenshot when test fails"""
        try:
            if not os.path.exists(self.config.get('data', {}).get('screenshot_dir', 'screenshots')):
                os.makedirs(self.config.get('data', {}).get('screenshot_dir', 'screenshots'))

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{test_name}_{timestamp}_FAILED.png"
            filepath = os.path.join(self.config.get('data', {}).get('screenshot_dir', 'screenshots'), filename)

            self.driver.save_screenshot(filepath)
            logger.info(f"Screenshot saved: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")
            return None

    @keyword("Scroll To Element")
    def scroll_to_element(self, locator):
        """Scroll to specific element"""
        try:
            element = self.driver.find_element(By.XPATH, locator)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(1)  # Wait for scroll to complete
            logger.info(f"Scrolled to element: {locator}")
            return True
        except NoSuchElementException:
            logger.error(f"Element not found for scrolling: {locator}")
            return False

    @keyword("Hover Over Element")
    def hover_over_element(self, locator):
        """Hover over element to trigger mouse events"""
        try:
            element = self.driver.find_element(By.XPATH, locator)
            ActionChains(self.driver).move_to_element(element).perform()
            logger.info(f"Hovered over element: {locator}")
            return True
        except NoSuchElementException:
            logger.error(f"Element not found for hover: {locator}")
            return False

    @keyword("Select Dropdown By Text")
    def select_dropdown_by_text(self, locator, text):
        """Select dropdown option by visible text"""
        try:
            select_element = Select(self.driver.find_element(By.XPATH, locator))
            select_element.select_by_visible_text(text)
            logger.info(f"Selected dropdown option: {text}")
            return True
        except Exception as e:
            logger.error(f"Failed to select dropdown option '{text}': {e}")
            return False

    @keyword("Get Element Text")
    def get_element_text(self, locator):
        """Get text content of element"""
        try:
            element = self.driver.find_element(By.XPATH, locator)
            text = element.text.strip()
            logger.info(f"Element text: {text}")
            return text
        except NoSuchElementException:
            logger.error(f"Element not found: {locator}")
            return None

    @keyword("Clear And Type Text")
    def clear_and_type_text(self, locator, text):
        """Clear field and type new text"""
        try:
            element = self.driver.find_element(By.XPATH, locator)
            element.clear()
            element.send_keys(text)
            logger.info(f"Typed text into element: {text}")
            return True
        except NoSuchElementException:
            logger.error(f"Element not found: {locator}")
            return False

    @keyword("Wait For Page Load")
    def wait_for_page_load(self, timeout=30):
        """Wait for page to load completely"""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            logger.info("Page loaded completely")
            return True
        except TimeoutException:
            logger.warn(f"Page did not load within {timeout}s")
            return False

    @keyword("Switch To Frame")
    def switch_to_frame(self, frame_locator):
        """Switch to iframe"""
        try:
            frame = self.driver.find_element(By.XPATH, frame_locator)
            self.driver.switch_to.frame(frame)
            logger.info(f"Switched to frame: {frame_locator}")
            return True
        except NoSuchElementException:
            logger.error(f"Frame not found: {frame_locator}")
            return False

    @keyword("Switch To Default Content")
    def switch_to_default_content(self):
        """Switch back to default content"""
        try:
            self.driver.switch_to.default_content()
            logger.info("Switched to default content")
            return True
        except Exception as e:
            logger.error(f"Failed to switch to default content: {e}")
            return False

    @keyword("Get Current URL")
    def get_current_url(self):
        """Get current page URL"""
        try:
            url = self.driver.current_url
            logger.info(f"Current URL: {url}")
            return url
        except Exception as e:
            logger.error(f"Failed to get current URL: {e}")
            return None

    @keyword("Verify Page Title")
    def verify_page_title(self, expected_title):
        """Verify page title matches expected"""
        try:
            actual_title = self.driver.title
            if actual_title == expected_title:
                logger.info(f"Page title verified: {actual_title}")
                return True
            else:
                logger.error(f"Page title mismatch. Expected: {expected_title}, Actual: {actual_title}")
                return False
        except Exception as e:
            logger.error(f"Failed to verify page title: {e}")
            return False

    @keyword("Count Elements")
    def count_elements(self, locator):
        """Count number of elements matching locator"""
        try:
            elements = self.driver.find_elements(By.XPATH, locator)
            count = len(elements)
            logger.info(f"Found {count} elements matching: {locator}")
            return count
        except Exception as e:
            logger.error(f"Failed to count elements: {e}")
            return 0

    @keyword("Element Should Be Enabled")
    def element_should_be_enabled(self, locator):
        """Verify element is enabled"""
        try:
            element = self.driver.find_element(By.XPATH, locator)
            if element.is_enabled():
                logger.info(f"Element is enabled: {locator}")
                return True
            else:
                logger.error(f"Element is disabled: {locator}")
                return False
        except NoSuchElementException:
            logger.error(f"Element not found: {locator}")
            return False

    @keyword("Element Should Be Disabled")
    def element_should_be_disabled(self, locator):
        """Verify element is disabled"""
        try:
            element = self.driver.find_element(By.XPATH, locator)
            if not element.is_enabled():
                logger.info(f"Element is disabled: {locator}")
                return True
            else:
                logger.error(f"Element is enabled (expected disabled): {locator}")
                return False
        except NoSuchElementException:
            logger.error(f"Element not found: {locator}")
            return False
