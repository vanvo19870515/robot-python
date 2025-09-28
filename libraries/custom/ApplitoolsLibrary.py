"""
Custom Robot Framework library for Applitools visual testing integration.

This library provides keywords for:
- Opening and closing Applitools Eyes sessions
- Performing visual checkpoints
- Configuring viewport sizes

Author: Test Automation Team
"""

import os
from robot.api import logger
from robot.api.deco import keyword
from applitools.selenium import Eyes, Target


class ApplitoolsLibrary:
    """
    Robot Framework library for Applitools Eyes integration.

    This library handles visual validation using Applitools Eyes service.
    """

    def __init__(self):
        """Initialize the Applitools library."""
        self._eyes = None
        self._driver = None

    @keyword("Open Applitools Session")
    def open_applitools_session(self, api_key, app_name, test_name, driver):
        """
        Open an Applitools Eyes session for visual testing.

        Args:
            api_key (str): Applitools API key
            app_name (str): Name of the application being tested
            test_name (str): Name of the test case
            driver: Selenium WebDriver instance

        Example:
        | Open Applitools Session | ${APPLITOOLS_API_KEY} | Cookie Clicker | Basic Gameplay | ${driver} |
        """
        try:
            self._eyes = Eyes()
            self._eyes.api_key = api_key
            self._driver = driver

            # Configure server URL for Applitools
            self._eyes.server_url = "https://eyesapi.applitools.com"

            # Open the Eyes session
            self._eyes.open(
                driver=driver,
                app_name=app_name,
                test_name=test_name,
                viewport_size=None  # Will use browser window size
            )

            logger.info(f"Opened Applitools session for test: {test_name}")
        except Exception as e:
            logger.error(f"Failed to open Applitools session: {str(e)}")
            raise

    @keyword("Perform Visual Checkpoint")
    def perform_visual_checkpoint(self, checkpoint_name, fully=True):
        """
        Perform a visual checkpoint using Applitools Eyes.

        Args:
            checkpoint_name (str): Name for this checkpoint
            fully (bool): Whether to capture the full page or viewport only

        Example:
        | Perform Visual Checkpoint | Cookie Clicker Main Screen | fully=True |
        """
        if not self._eyes:
            raise AssertionError("Applitools session not opened. Call 'Open Applitools Session' first.")

        try:
            if fully:
                self._eyes.check(checkpoint_name, Target.window().fully())
            else:
                self._eyes.check(checkpoint_name, Target.window())

            logger.info(f"Performed visual checkpoint: {checkpoint_name}")
        except Exception as e:
            logger.error(f"Failed to perform visual checkpoint '{checkpoint_name}': {str(e)}")
            raise

    @keyword("Close Applitools Session")
    def close_applitools_session(self):
        """
        Close the Applitools Eyes session and perform final validation.

        Example:
        | Close Applitools Session |
        """
        if not self._eyes:
            logger.warning("No Applitools session to close.")
            return

        try:
            # Close the session and get results
            results = self._eyes.close(False)  # Don't throw on diff

            if results:
                logger.info(f"Applitools session closed. Results: {results}")

                # Check if test passed
                if results.is_passed:
                    logger.info("✅ Visual validation PASSED")
                else:
                    logger.error("❌ Visual validation FAILED")
                    logger.error(f"Mismatches found: {results.mismatches}")

                    # Log detailed results
                    for step in results.steps:
                        if not step.is_passed:
                            logger.error(f"Step '{step.name}' failed: {step.mismatches} mismatches")
            else:
                logger.warning("No results returned from Applitools")

        except Exception as e:
            logger.error(f"Error closing Applitools session: {str(e)}")
            raise
        finally:
            # Always clean up
            if self._eyes:
                try:
                    self._eyes.abort()
                except:
                    pass
                self._eyes = None
                self._driver = None

    @keyword("Set Viewport Size")
    def set_viewport_size(self, width, height):
        """
        Set the viewport size for Applitools visual testing.

        Args:
            width (int): Viewport width in pixels
            height (int): Viewport height in pixels

        Example:
        | Set Viewport Size | 1920 | 1080 |
        """
        if not self._eyes:
            raise AssertionError("Applitools session not opened. Call 'Open Applitools Session' first.")

        try:
            from applitools.selenium import RectangleSize
            viewport_size = RectangleSize(width, height)
            self._eyes.configure.viewport_size = viewport_size
            logger.info(f"Set viewport size to {width}x{height}")
        except Exception as e:
            logger.error(f"Failed to set viewport size: {str(e)}")
            raise
