"""
Centralized Configuration Management System.

This module provides a unified way to manage all application settings,
environment variables, and configuration parameters.

Author: Test Automation Team
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """
    Centralized configuration management for the test automation framework.

    Provides access to all configuration parameters with validation and defaults.
    """

    def __init__(self):
        """Initialize configuration with environment variables and defaults."""
        self._config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from multiple sources."""
        config = {}

        # Base configuration
        config.update(self._get_base_config())

        # Environment-specific configuration
        config.update(self._get_environment_config())

        # API configuration
        config.update(self._get_api_config())

        # Browser configuration
        config.update(self._get_browser_config())

        # Mobile configuration
        config.update(self._get_mobile_config())

        # Reporting configuration
        config.update(self._get_reporting_config())

        return config

    def _get_base_config(self) -> Dict[str, Any]:
        """Get base application configuration."""
        return {
            "project_name": "Robot Framework Test Automation",
            "version": "2.0.0",
            "author": "SDET Team",
            "base_url": "https://orteil.dashnet.org/cookieclicker/",
            "timeout": 30,
            "retry_attempts": 3,
            "screenshot_on_failure": True,
        }

    def _get_environment_config(self) -> Dict[str, Any]:
        """Get environment-specific configuration."""
        return {
            "environment": os.getenv("TEST_ENVIRONMENT", "development"),
            "debug_mode": os.getenv("DEBUG_MODE", "false").lower() == "true",
            "headless_mode": os.getenv("HEADLESS_MODE", "false").lower() == "true",
        }

    def _get_api_config(self) -> Dict[str, Any]:
        """Get API-related configuration."""
        return {
            "applitools": {
                "api_key": os.getenv("APPLITOOLS_API_KEY", ""),
                "server_url": "https://eyesapi.applitools.com",
                "app_name": "Cookie Clicker Test",
                "batch_name": "Cookie Clicker Batch",
            },
            "telegram": {
                "bot_token": os.getenv("TELEGRAM_BOT_TOKEN", "8387676250:AAH1VNxOofEKA04ilK90zPA0zoZ1tFjXuzk"),
                "chat_id": os.getenv("TELEGRAM_CHAT_ID", "6225001877"),
                "enabled": os.getenv("TELEGRAM_ENABLED", "true").lower() == "true",
            },
        }

    def _get_browser_config(self) -> Dict[str, Any]:
        """Get browser-specific configuration."""
        return {
            "browser": {
                "name": os.getenv("BROWSER", "chrome"),
                "headless": os.getenv("HEADLESS", "false").lower() == "true",
                "window_size": os.getenv("WINDOW_SIZE", "1920x1080"),
                "implicit_wait": int(os.getenv("IMPLICIT_WAIT", "10")),
                "page_load_timeout": int(os.getenv("PAGE_LOAD_TIMEOUT", "30")),
            }
        }

    def _get_mobile_config(self) -> Dict[str, Any]:
        """Get mobile testing configuration."""
        return {
            "mobile": {
                "platform": os.getenv("MOBILE_PLATFORM", "Android"),
                "device_name": os.getenv("DEVICE_NAME", "emulator-5554"),
                "automation_name": os.getenv("AUTOMATION_NAME", "UiAutomator2"),
                "appium_server": os.getenv("APPIUM_SERVER", "http://127.0.0.1:4723"),
                "app_path": os.getenv("APP_PATH", ""),
                "new_command_timeout": int(os.getenv("NEW_COMMAND_TIMEOUT", "300")),
            }
        }

    def _get_reporting_config(self) -> Dict[str, Any]:
        """Get reporting configuration."""
        return {
            "reporting": {
                "output_dir": os.getenv("OUTPUT_DIR", "reports"),
                "allure_enabled": os.getenv("ALLURE_ENABLED", "true").lower() == "true",
                "screenshot_dir": os.getenv("SCREENSHOT_DIR", "screenshots"),
                "log_level": os.getenv("LOG_LEVEL", "INFO"),
            }
        }

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key.

        Args:
            key (str): Configuration key (supports dot notation like 'browser.name')
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self._config

        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

    def set(self, key: str, value: Any):
        """
        Set configuration value.

        Args:
            key (str): Configuration key
            value: Value to set
        """
        keys = key.split('.')
        config = self._config

        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value

    def save_to_file(self, filepath: str = "config.json"):
        """Save current configuration to JSON file."""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2, ensure_ascii=False)
            print(f"✅ Configuration saved to {filepath}")
        except Exception as e:
            print(f"❌ Error saving configuration: {e}")

    def load_from_file(self, filepath: str = "config.json"):
        """Load configuration from JSON file."""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    file_config = json.load(f)
                    self._config.update(file_config)
                print(f"✅ Configuration loaded from {filepath}")
        except Exception as e:
            print(f"❌ Error loading configuration: {e}")

    def validate_config(self) -> bool:
        """Validate that all required configuration is present."""
        required_keys = [
            "browser.name",
            "mobile.platform",
        ]

        missing_keys = []
        for key in required_keys:
            if self.get(key) is None:
                missing_keys.append(key)

        if missing_keys:
            print(f"⚠️  Missing required configuration: {', '.join(missing_keys)}")
            return False

        print("✅ Configuration validation passed")
        return True

    def print_config_summary(self):
        """Print a summary of current configuration."""
        print("\n🔧 Configuration Summary:")
        print("=" * 50)

        # Browser config
        print("🌐 Browser Configuration:")
        browser = self.get("browser", {})
        for key, value in browser.items():
            print(f"   {key}: {value}")

        # Mobile config
        print("\n📱 Mobile Configuration:")
        mobile = self.get("mobile", {})
        for key, value in mobile.items():
            print(f"   {key}: {value}")

        # API config
        print("\n🔌 API Configuration:")
        applitools = self.get("applitools", {})
        for key, value in applitools.items():
            # Mask API key for security
            display_value = "****" + value[-4:] if key == "api_key" and value else value
            print(f"   {key}: {display_value}")

        telegram = self.get("telegram", {})
        for key, value in telegram.items():
            display_value = "****" + value[-4:] if key == "bot_token" and value else value
            print(f"   {key}: {display_value}")

        print("\n📊 Reporting Configuration:")
        reporting = self.get("reporting", {})
        for key, value in reporting.items():
            print(f"   {key}: {value}")

        print("=" * 50)


# Global configuration instance
config = Config()


def get_config() -> Config:
    """Get the global configuration instance."""
    return config


def reload_config():
    """Reload configuration from all sources."""
    global config
    config = Config()


# Example usage and validation
if __name__ == "__main__":
    # Print configuration summary
    config.print_config_summary()

    # Validate configuration
    config.validate_config()

    # Save configuration to file
    config.save_to_file()
