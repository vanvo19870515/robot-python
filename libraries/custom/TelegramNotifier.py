"""
Custom Robot Framework library for Telegram notifications.

This library provides keywords for:
- Sending text messages to Telegram
- Sending test results and reports
- Handling different message formats

Author: Test Automation Team
"""

import os
import requests
from robot.api import logger
from robot.api.deco import keyword


class TelegramNotifier:
    """
    Robot Framework library for sending Telegram notifications.

    This library handles sending messages to Telegram chat via bot API.
    """

    def __init__(self):
        """Initialize the Telegram notifier."""
        self._bot_token = None
        self._chat_id = None
        self._base_url = "https://api.telegram.org/bot"

    @keyword("Configure Telegram")
    def configure_telegram(self, bot_token, chat_id):
        """
        Configure Telegram bot credentials.

        Args:
            bot_token (str): Telegram bot token
            chat_id (str): Telegram chat ID

        Example:
        | Configure Telegram | 8387676250:AAH1VNxOofEKA04ilK90zPA0zoZ1tFjXuzk | 6225001877 |
        """
        self._bot_token = bot_token
        self._chat_id = chat_id
        logger.info("Telegram notifier configured successfully")

    @keyword("Send Telegram Message")
    def send_telegram_message(self, message, parse_mode="HTML"):
        """
        Send a text message to the configured Telegram chat.

        Args:
            message (str): Message content to send
            parse_mode (str): Parse mode for message formatting ('HTML' or 'Markdown')

        Returns:
            bool: True if message was sent successfully

        Example:
        | Send Telegram Message | <b>Test completed!</b>\n✅ All tests passed | parse_mode=HTML |
        """
        if not self._bot_token or not self._chat_id:
            logger.error("Telegram not configured. Call 'Configure Telegram' first.")
            return False

        try:
            url = f"{self._base_url}{self._bot_token}/sendMessage"
            payload = {
                "chat_id": self._chat_id,
                "text": message,
                "parse_mode": parse_mode,
                "disable_web_page_preview": True
            }

            response = requests.post(url, json=payload, timeout=10)

            if response.status_code == 200:
                result = response.json()
                if result.get("ok"):
                    logger.info("✅ Telegram message sent successfully")
                    return True
                else:
                    logger.error(f"Telegram API error: {result.get('description', 'Unknown error')}")
            else:
                logger.error(f"HTTP error {response.status_code}: {response.text}")

        except requests.exceptions.RequestException as e:
            logger.error(f"Network error sending Telegram message: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error sending Telegram message: {str(e)}")

        return False

    @keyword("Send Test Result")
    def send_test_result(self, test_name, status, duration=None, details=None):
        """
        Send a formatted test result message to Telegram.

        Args:
            test_name (str): Name of the test
            status (str): Test status ('PASSED', 'FAILED', 'ERROR')
            duration (str): Test duration (optional)
            details (str): Additional details (optional)

        Example:
        | Send Test Result | Cookie Clicker Test | PASSED | 2m 30s | All assertions passed |
        """
        if status.upper() == "PASSED":
            emoji = "✅"
            status_text = "PASSED"
        elif status.upper() == "FAILED":
            emoji = "❌"
            status_text = "FAILED"
        else:
            emoji = "⚠️"
            status_text = "ERROR"

        message = f"<b>Test Result</b>\n\n"
        message += f"<b>Test:</b> {test_name}\n"
        message += f"<b>Status:</b> {emoji} {status_text}\n"

        if duration:
            message += f"<b>Duration:</b> {duration}\n"

        if details:
            message += f"\n<b>Details:</b>\n{details}"

        return self.send_telegram_message(message)

    @keyword("Send Test Summary")
    def send_test_summary(self, total_tests, passed, failed, duration):
        """
        Send a test execution summary to Telegram.

        Args:
            total_tests (int): Total number of tests
            passed (int): Number of passed tests
            failed (int): Number of failed tests
            duration (str): Total execution duration

        Example:
        | Send Test Summary | 5 | 4 | 1 | 3m 45s |
        """
        success_rate = (passed / total_tests * 100) if total_tests > 0 else 0

        message = "<b>🧪 Test Execution Summary</b>\n\n"
        message += f"<b>Total Tests:</b> {total_tests}\n"
        message += f"<b>✅ Passed:</b> {passed}\n"
        message += f"<b>❌ Failed:</b> {failed}\n"
        message += f"<b>📊 Success Rate:</b> {success_rate:.1f}%\n"
        message += f"<b>⏱️ Duration:</b> {duration}\n"

        if success_rate == 100:
            message += "\n🎉 All tests passed successfully!"
        elif failed > 0:
            message += "\n🔧 Some tests failed. Check logs for details."

        return self.send_telegram_message(message)
