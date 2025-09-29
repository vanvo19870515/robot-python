"""
Page Object Model for Cookie Clicker game.

This module implements the Page Object pattern for better test maintainability
and separation of concerns.

Author: Test Automation Team
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time


class CookieClickerPage:
    """
    Page Object class for Cookie Clicker game interactions.

    Encapsulates all page-specific logic and element interactions.
    """

    def __init__(self, driver):
        """
        Initialize the page object with WebDriver instance.

        Args:
            driver: Selenium WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

        # Page elements (locators)
        self._cookie_button = (By.ID, "bigCookie")
        self._score_display = (By.ID, "cookies")
        self._cursor_upgrade = (By.ID, "product0")
        self._grandma_upgrade = (By.ID, "product1")
        self._farm_upgrade = (By.ID, "product2")
        self._mine_upgrade = (By.ID, "product3")
        self._factory_upgrade = (By.ID, "product4")
        self._bank_upgrade = (By.ID, "product5")
        self._temple_upgrade = (By.ID, "product6")
        self._wizard_tower_upgrade = (By.ID, "product7")
        self._shipment_upgrade = (By.ID, "product8")
        self._alchemy_lab_upgrade = (By.ID, "product9")
        self._portal_upgrade = (By.ID, "product10")
        self._time_machine_upgrade = (By.ID, "product11")
        self._antimatter_condenser_upgrade = (By.ID, "product12")
        self._prism_upgrade = (By.ID, "product13")
        self._chancemaker_upgrade = (By.ID, "product14")
        self._fractal_engine_upgrade = (By.ID, "product15")

        # Game state elements
        self._game_title = (By.CSS_SELECTOR, "title")
        self._main_content = (By.ID, "game")
        self._upgrade_section = (By.ID, "products")

    def wait_for_page_load(self, timeout=30):
        """
        Wait for the Cookie Clicker page to fully load.

        Args:
            timeout (int): Maximum time to wait in seconds

        Returns:
            bool: True if page loaded successfully

        Raises:
            TimeoutException: If page doesn't load within timeout
        """
        try:
            self.wait.until(
                EC.presence_of_element_located(self._cookie_button)
            )
            print("✅ Cookie Clicker page loaded successfully")
            return True
        except TimeoutException:
            print("❌ Cookie Clicker page failed to load")
            raise

    def click_cookie(self, times=1, delay=0.1):
        """
        Click the big cookie multiple times.

        Args:
            times (int): Number of times to click
            delay (float): Delay between clicks in seconds
        """
        cookie_element = self.wait.until(
            EC.element_to_be_clickable(self._cookie_button)
        )

        print(f"🍪 Clicking cookie {times} times with {delay}s delay")

        for i in range(times):
            try:
                cookie_element.click()
                time.sleep(delay)
                if (i + 1) % 10 == 0:  # Log every 10 clicks
                    print(f"   Clicked {i + 1}/{times} times")
            except Exception as e:
                print(f"⚠️  Error clicking cookie on attempt {i + 1}: {e}")
                break

    def get_current_score(self):
        """
        Get the current cookie count.

        Returns:
            int: Current cookie count
        """
        try:
            score_element = self.driver.find_element(*self._score_display)
            score_text = score_element.text.replace(",", "")
            # Extract number from text like "123 cookies"
            import re
            numbers = re.findall(r'\d+', score_text)
            return int(numbers[0]) if numbers else 0
        except (NoSuchElementException, ValueError, IndexError):
            print("⚠️  Could not read current score")
            return 0

    def wait_for_score_increase(self, target_score, timeout=10):
        """
        Wait for score to reach or exceed target value.

        Args:
            target_score (int): Target score to wait for
            timeout (int): Maximum wait time in seconds

        Returns:
            bool: True if target reached, False if timeout
        """
        print(f"⏳ Waiting for score to reach {target_score}")

        start_time = time.time()
        while time.time() - start_time < timeout:
            current_score = self.get_current_score()
            if current_score >= target_score:
                print(f"✅ Score reached {current_score} >= {target_score}")
                return True
            time.sleep(0.5)

        print(f"❌ Timeout waiting for score. Current: {self.get_current_score()}")
        return False

    def purchase_upgrade(self, upgrade_name):
        """
        Purchase a specific upgrade if available and affordable.

        Args:
            upgrade_name (str): Name of upgrade to purchase

        Returns:
            bool: True if purchase successful
        """
        upgrade_map = {
            "cursor": self._cursor_upgrade,
            "grandma": self._grandma_upgrade,
            "farm": self._farm_upgrade,
            "mine": self._mine_upgrade,
            "factory": self._factory_upgrade,
            "bank": self._bank_upgrade,
            "temple": self._temple_upgrade,
            "wizard_tower": self._wizard_tower_upgrade,
            "shipment": self._shipment_upgrade,
            "alchemy_lab": self._alchemy_lab_upgrade,
            "portal": self._portal_upgrade,
            "time_machine": self._time_machine_upgrade,
            "antimatter_condenser": self._antimatter_condenser_upgrade,
            "prism": self._prism_upgrade,
            "chancemaker": self._chancemaker_upgrade,
            "fractal_engine": self._fractal_engine_upgrade,
        }

        if upgrade_name not in upgrade_map:
            print(f"❌ Unknown upgrade: {upgrade_name}")
            return False

        try:
            upgrade_element = self.wait.until(
                EC.element_to_be_clickable(upgrade_map[upgrade_name])
            )
            upgrade_element.click()
            print(f"✅ Successfully purchased: {upgrade_name}")
            return True
        except TimeoutException:
            print(f"❌ Upgrade not available or too expensive: {upgrade_name}")
            return False
        except Exception as e:
            print(f"❌ Error purchasing upgrade {upgrade_name}: {e}")
            return False

    def is_upgrade_enabled(self, upgrade_name):
        """
        Check if an upgrade is enabled/available for purchase.

        Args:
            upgrade_name (str): Name of upgrade to check

        Returns:
            bool: True if upgrade is enabled
        """
        upgrade_map = {
            "cursor": self._cursor_upgrade,
            "grandma": self._grandma_upgrade,
            "farm": self._farm_upgrade,
            "mine": self._mine_upgrade,
            "factory": self._factory_upgrade,
        }

        if upgrade_name not in upgrade_map:
            return False

        try:
            upgrade_element = self.driver.find_element(*upgrade_map[upgrade_name])
            return upgrade_element.is_enabled()
        except NoSuchElementException:
            return False

    def get_game_statistics(self):
        """
        Get comprehensive game statistics.

        Returns:
            dict: Dictionary containing various game stats
        """
        stats = {}

        try:
            # Get current score
            stats['current_score'] = self.get_current_score()

            # Get upgrade counts (simplified)
            stats['upgrades_owned'] = len([
                upgrade for name, locator in [
                    ("cursor", self._cursor_upgrade),
                    ("grandma", self._grandma_upgrade),
                    ("farm", self._farm_upgrade),
                ] if self._is_upgrade_owned(locator)
            ])

            # Get game title
            try:
                title_element = self.driver.find_element(*self._game_title)
                stats['page_title'] = title_element.get_attribute('text')
            except:
                stats['page_title'] = "Unknown"

        except Exception as e:
            print(f"⚠️  Error getting game statistics: {e}")
            stats['error'] = str(e)

        return stats

    def _is_upgrade_owned(self, locator):
        """Helper method to check if upgrade is owned."""
        try:
            element = self.driver.find_element(*locator)
            # Check if element has any indication of being owned
            return "owned" in element.get_attribute("class").lower()
        except:
            return False

    def take_screenshot(self, filename="cookie_clicker_screenshot.png"):
        """
        Take a screenshot of the current page state.

        Args:
            filename (str): Name for the screenshot file
        """
        try:
            screenshot_path = f"/Users/vanvo/Documents/robot-python/reports/{filename}"
            self.driver.save_screenshot(screenshot_path)
            print(f"📸 Screenshot saved: {screenshot_path}")
            return screenshot_path
        except Exception as e:
            print(f"❌ Error taking screenshot: {e}")
            return None

    def get_page_performance_metrics(self):
        """
        Get page performance metrics.

        Returns:
            dict: Performance metrics
        """
        try:
            # Execute JavaScript to get performance metrics
            metrics = self.driver.execute_script("""
                const navigation = performance.getEntriesByType('navigation')[0];
                const paint = performance.getEntriesByType('paint');

                return {
                    dom_content_loaded: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
                    load_complete: navigation.loadEventEnd - navigation.loadEventStart,
                    first_paint: paint.find(p => p.name === 'first-paint')?.startTime || 0,
                    first_contentful_paint: paint.find(p => p.name === 'first-contentful-paint')?.startTime || 0
                };
            """)

            print("📊 Performance metrics collected"            print(f"   DOM Content Loaded: {metrics.get('dom_content_loaded', 0):.2f}ms")
            print(f"   Load Complete: {metrics.get('load_complete', 0)".2f"}ms")
            print(f"   First Paint: {metrics.get('first_paint', 0)".2f"}ms")
            print(f"   First Contentful Paint: {metrics.get('first_contentful_paint', 0)".2f"}ms")

            return metrics
        except Exception as e:
            print(f"⚠️  Error getting performance metrics: {e}")
            return {}
