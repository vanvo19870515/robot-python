"""
MobileUtils - Custom Library for Mobile App Automation
Provides enhanced mobile testing capabilities using Appium
"""

import os
import time
import yaml
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.common.multi_action import MultiAction
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from robot.api import logger
from robot.api.deco import keyword, library

@library
class MobileUtils:
    """Enhanced mobile automation utilities using Appium"""

    def __init__(self):
        self.config = self._load_config()
        self.screenshot_counter = 0

    def _load_config(self):
        """Load configuration from yaml file"""
        try:
            with open('config/appium.yaml', 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            logger.warn(f"Could not load mobile config: {e}")
            return {}

    @keyword("Start Appium Server")
    def start_appium_server(self):
        """Start Appium server"""
        try:
            import subprocess
            cmd = [
                "appium",
                "--address", self.config.get('appium', {}).get('server', {}).get('host', '127.0.0.1'),
                "--port", str(self.config.get('appium', {}).get('server', {}).get('port', 4723)),
                "--log-level", self.config.get('appium', {}).get('server', {}).get('log_level', 'info')
            ]

            # Start Appium server in background
            self.appium_process = subprocess.Popen(cmd)
            logger.info("Appium server started successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to start Appium server: {e}")
            return False

    @keyword("Stop Appium Server")
    def stop_appium_server(self):
        """Stop Appium server"""
        try:
            if hasattr(self, 'appium_process'):
                self.appium_process.terminate()
                self.appium_process.wait()
                logger.info("Appium server stopped successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to stop Appium server: {e}")
            return False

    @keyword("Swipe Up")
    def swipe_up(self, duration=1000):
        """Swipe up on mobile screen"""
        try:
            size = self.driver.get_window_size()
            start_x = size['width'] // 2
            start_y = size['height'] * 3 // 4
            end_y = size['height'] // 4

            self.driver.swipe(start_x, start_y, start_x, end_y, duration)
            logger.info("Swiped up successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to swipe up: {e}")
            return False

    @keyword("Swipe Down")
    def swipe_down(self, duration=1000):
        """Swipe down on mobile screen"""
        try:
            size = self.driver.get_window_size()
            start_x = size['width'] // 2
            start_y = size['height'] // 4
            end_y = size['height'] * 3 // 4

            self.driver.swipe(start_x, start_y, start_x, end_y, duration)
            logger.info("Swiped down successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to swipe down: {e}")
            return False

    @keyword("Swipe Left")
    def swipe_left(self, duration=1000):
        """Swipe left on mobile screen"""
        try:
            size = self.driver.get_window_size()
            start_y = size['height'] // 2
            start_x = size['width'] * 3 // 4
            end_x = size['width'] // 4

            self.driver.swipe(start_x, start_y, end_x, start_y, duration)
            logger.info("Swiped left successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to swipe left: {e}")
            return False

    @keyword("Swipe Right")
    def swipe_right(self, duration=1000):
        """Swipe right on mobile screen"""
        try:
            size = self.driver.get_window_size()
            start_y = size['height'] // 2
            start_x = size['width'] // 4
            end_x = size['width'] * 3 // 4

            self.driver.swipe(start_x, start_y, end_x, start_y, duration)
            logger.info("Swiped right successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to swipe right: {e}")
            return False

    @keyword("Tap Element")
    def tap_element(self, locator):
        """Tap on mobile element"""
        try:
            element = self.driver.find_element(AppiumBy.XPATH, locator)
            # Use TouchAction for precise tapping
            touch_action = TouchAction(self.driver)
            touch_action.tap(element).perform()
            logger.info(f"Tapped element: {locator}")
            return True
        except NoSuchElementException:
            logger.error(f"Element not found for tapping: {locator}")
            return False

    @keyword("Long Press Element")
    def long_press_element(self, locator, duration=2000):
        """Long press on mobile element"""
        try:
            element = self.driver.find_element(AppiumBy.XPATH, locator)
            # Use TouchAction for long press
            touch_action = TouchAction(self.driver)
            touch_action.long_press(element, duration=duration).release().perform()
            logger.info(f"Long pressed element: {locator} for {duration}ms")
            return True
        except NoSuchElementException:
            logger.error(f"Element not found for long press: {locator}")
            return False

    @keyword("Scroll To Element Mobile")
    def scroll_to_element_mobile(self, locator, direction="down", max_swipes=10):
        """Scroll to find mobile element"""
        try:
            for _ in range(max_swipes):
                try:
                    element = self.driver.find_element(AppiumBy.XPATH, locator)
                    logger.info(f"Found element after scrolling: {locator}")
                    return True
                except NoSuchElementException:
                    if direction == "down":
                        self.swipe_up()
                    else:
                        self.swipe_down()

            logger.error(f"Element not found after {max_swipes} swipes: {locator}")
            return False

        except Exception as e:
            logger.error(f"Failed to scroll to element: {e}")
            return False

    @keyword("Get Device Info")
    def get_device_info(self):
        """Get mobile device information"""
        try:
            info = {
                "platform": self.driver.capabilities.get('platformName', 'Unknown'),
                "version": self.driver.capabilities.get('platformVersion', 'Unknown'),
                "device": self.driver.capabilities.get('deviceName', 'Unknown'),
                "orientation": self.driver.orientation,
                "battery": self._get_battery_level(),
                "network": self._get_network_type()
            }
            logger.info(f"Device info: {info}")
            return info
        except Exception as e:
            logger.error(f"Failed to get device info: {e}")
            return {}

    def _get_battery_level(self):
        """Get battery level"""
        try:
            return self.driver.execute_script("mobile: shell", {
                "command": "dumpsys battery | grep level"
            })
        except:
            return "Unknown"

    def _get_network_type(self):
        """Get network type"""
        try:
            return self.driver.execute_script("mobile: shell", {
                "command": "getprop gsm.network.type"
            })
        except:
            return "Unknown"

    @keyword("Take Mobile Screenshot")
    def take_mobile_screenshot(self, filename_prefix="mobile"):
        """Take mobile screenshot"""
        try:
            screenshot_dir = self.config.get('mobile_reporting', {}).get('screenshots_dir', 'screenshots/mobile')
            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)

            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"{filename_prefix}_{timestamp}.png"
            filepath = os.path.join(screenshot_dir, filename)

            self.driver.save_screenshot(filepath)
            logger.info(f"Mobile screenshot saved: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Failed to take mobile screenshot: {e}")
            return None

    @keyword("Hide Keyboard")
    def hide_keyboard(self):
        """Hide mobile keyboard"""
        try:
            self.driver.hide_keyboard()
            logger.info("Keyboard hidden successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to hide keyboard: {e}")
            return False

    @keyword("Press Key Code")
    def press_key_code(self, key_code):
        """Press hardware key by code"""
        try:
            self.driver.press_keycode(key_code)
            logger.info(f"Pressed key code: {key_code}")
            return True
        except Exception as e:
            logger.error(f"Failed to press key code: {e}")
            return False

    @keyword("Rotate Device")
    def rotate_device(self, orientation="LANDSCAPE"):
        """Rotate device orientation"""
        try:
            self.driver.orientation = orientation
            logger.info(f"Device rotated to: {orientation}")
            return True
        except Exception as e:
            logger.error(f"Failed to rotate device: {e}")
            return False

    @keyword("Send SMS")
    def send_sms(self, phone_number, message):
        """Send SMS (Android only)"""
        try:
            self.driver.execute_script("mobile: shell", {
                "command": f"am start -a android.intent.action.SENDTO -d sms:{phone_number} --es sms_body '{message}'"
            })
            logger.info(f"SMS sent to {phone_number}: {message}")
            return True
        except Exception as e:
            logger.error(f"Failed to send SMS: {e}")
            return False

    @keyword("Make Call")
    def make_call(self, phone_number):
        """Make phone call (Android only)"""
        try:
            self.driver.execute_script("mobile: shell", {
                "command": f"am start -a android.intent.action.CALL -d tel:{phone_number}"
            })
            logger.info(f"Call initiated to: {phone_number}")
            return True
        except Exception as e:
            logger.error(f"Failed to make call: {e}")
            return False

    @keyword("Check App State")
    def check_app_state(self, app_package):
        """Check if app is running in foreground/background"""
        try:
            state = self.driver.execute_script("mobile: shell", {
                "command": f"dumpsys window windows | grep -E 'mCurrentFocus|mFocusedApp'"
            })
            logger.info(f"App state for {app_package}: {state}")
            return state
        except Exception as e:
            logger.error(f"Failed to check app state: {e}")
            return None

    @keyword("Reset App")
    def reset_app(self):
        """Reset mobile app"""
        try:
            self.driver.reset()
            logger.info("App reset successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to reset app: {e}")
            return False

    @keyword("Background App")
    def background_app(self, seconds=5):
        """Put app in background for specified seconds"""
        try:
            self.driver.background_app(seconds)
            logger.info(f"App backgrounded for {seconds} seconds")
            return True
        except Exception as e:
            logger.error(f"Failed to background app: {e}")
            return False

    @keyword("Activate App")
    def activate_app(self, app_package):
        """Activate mobile app"""
        try:
            self.driver.activate_app(app_package)
            logger.info(f"App activated: {app_package}")
            return True
        except Exception as e:
            logger.error(f"Failed to activate app: {e}")
            return False

    @keyword("Get Performance Data")
    def get_performance_data(self, data_type="cpuinfo"):
        """Get mobile performance data"""
        try:
            data = self.driver.execute_script("mobile: shell", {
                "command": f"dumpsys {data_type}"
            })
            logger.info(f"Performance data ({data_type}): retrieved")
            return data
        except Exception as e:
            logger.error(f"Failed to get performance data: {e}")
            return None
