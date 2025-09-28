#!/usr/bin/env python3
"""
Advanced Test Runner for Robot Framework with Allure, Applitools, and Telegram integration

Features:
- Web testing with Selenium (Chrome)
- Mobile testing with Appium (Android)
- Visual validation with Applitools Eyes
- Allure reporting
- Telegram notifications
- Environment setup and validation
"""

import os
import sys
import subprocess
import argparse
import time
from datetime import datetime


class TestRunner:
    """
    Advanced test runner with comprehensive features for web and mobile testing.
    """

    def __init__(self):
        """Initialize the test runner."""
        self.project_root = os.getcwd()
        self.tests_dir = os.path.join(self.project_root, "tests", "suites")
        self.reports_dir = os.path.join(self.project_root, "reports")
        self.allure_results_dir = os.path.join(self.project_root, "allure-results")

    def setup_environment(self):
        """Setup and validate test environment"""
        print("🔧 Setting up test environment...")

        # Ensure required directories exist
        os.makedirs(self.reports_dir, exist_ok=True)
        os.makedirs(self.allure_results_dir, exist_ok=True)

        # Check if dependencies are installed
        try:
            import robot
            print("✅ Robot Framework is installed")
        except ImportError:
            print("❌ Robot Framework not found. Installing...")
            self.install_dependencies()

        # Validate environment variables
        self.validate_environment_variables()

    def validate_environment_variables(self):
        """Validate required environment variables"""
        required_vars = ['APPLITOOLS_API_KEY']
        missing_vars = []

        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)

        if missing_vars:
            print(f"⚠️  Missing environment variables: {', '.join(missing_vars)}")
            print("   Some features may not work correctly.")
        else:
            print("✅ All required environment variables are set")

    def install_dependencies(self):
        """Install Python dependencies"""
        try:
            print("📦 Installing Python dependencies...")
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r",
                os.path.join(self.project_root, "requirements.txt")
            ], check=True)
            print("✅ Dependencies installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            sys.exit(1)

    def run_cookie_clicker_tests(self):
        """Run Cookie Clicker web tests"""
        print("🍪 Running Cookie Clicker Tests...")
        test_file = os.path.join(self.tests_dir, "cookie_clicker_test.robot")
        return self.run_robot_tests(test_file, "Cookie Clicker tests completed successfully")

    def run_apidemos_tests(self):
        """Run ApiDemos mobile tests"""
        print("📱 Running ApiDemos Mobile Tests...")
        test_file = os.path.join(self.tests_dir, "apidemos_test.robot")
        return self.run_robot_tests(test_file, "ApiDemos tests completed successfully")

    def run_all_tests(self):
        """Run all available tests"""
        print("🏃 Running All Tests...")

        # Run web tests first
        web_success = self.run_cookie_clicker_tests()

        # Run mobile tests
        mobile_success = self.run_apidemos_tests()

        return all([web_success, mobile_success])

    def run_robot_tests(self, test_file, success_message):
        """Execute Robot Framework tests with enhanced features"""
        try:
            # Build Robot command with Allure integration
            cmd = [
                "robot",
                "--outputdir", self.reports_dir,
                "--loglevel", "INFO",
                "--variable", f"APPLITOOLS_API_KEY:{os.getenv('APPLITOOLS_API_KEY', '')}",
                "--pythonpath", os.path.join(self.project_root, "libraries"),
                test_file
            ]

            print(f"🤖 Executing Robot Framework tests: {os.path.basename(test_file)}")

            # Execute tests
            start_time = time.time()
            result = subprocess.run(cmd, cwd=self.project_root, capture_output=True, text=True)
            duration = time.time() - start_time

            # Parse results
            if result.returncode == 0:
                print(f"✅ {success_message}")
                self.generate_allure_report()
                return True
            else:
                print(f"❌ Tests failed with return code: {result.returncode}")
                print("STDOUT:", result.stdout)
                if result.stderr:
                    print("STDERR:", result.stderr)
                return False

        except FileNotFoundError:
            print("❌ Robot Framework not found. Please install dependencies first.")
            return False
        except Exception as e:
            print(f"❌ Error running tests: {e}")
            return False

    def generate_allure_report(self):
        """Generate Allure report from test results"""
        try:
            print("🎨 Generating Allure report...")

            # Check if allure command is available
            allure_cmd = "allure"
            try:
                subprocess.run([allure_cmd, "--version"], capture_output=True, check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                print("⚠️  Allure CLI not found. Install with: npm install -g allure-commandline")
                return

            # Generate report
            cmd = [
                allure_cmd, "generate",
                self.allure_results_dir,
                "--output", os.path.join(self.project_root, "allure-report"),
                "--clean"
            ]

            subprocess.run(cmd, check=True)
            print("✅ Allure report generated successfully")
            print(f"📊 Report available at: {os.path.join(self.project_root, 'allure-report', 'index.html')}")

        except subprocess.CalledProcessError as e:
            print(f"⚠️  Failed to generate Allure report: {e}")
        except Exception as e:
            print(f"⚠️  Error generating Allure report: {e}")


def send_telegram_message(message):
    """Send a message to Telegram (helper function)"""
    try:
        import requests

        bot_token = "8387676250:AAH1VNxOofEKA04ilK90zPA0zoZ1tFjXuzk"
        chat_id = "6225001877"

        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML"
        }

        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print("✅ Telegram notification sent successfully")
        else:
            print(f"⚠️  Failed to send Telegram notification: {response.status_code}")

    except ImportError:
        print("⚠️  Requests library not available for Telegram notifications")
    except Exception as e:
        print(f"⚠️  Error sending Telegram notification: {e}")


def main():
    """Main execution block"""
    parser = argparse.ArgumentParser(
        description="Advanced Test Runner with Allure, Applitools, and Telegram",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_tests.py --web          # Run Cookie Clicker web tests
  python run_tests.py --mobile       # Run ApiDemos mobile tests
  python run_tests.py --all          # Run all tests
  python run_tests.py --setup        # Setup environment only
        """
    )

    parser.add_argument("--web", action="store_true", help="Run Cookie Clicker web tests")
    parser.add_argument("--mobile", action="store_true", help="Run ApiDemos mobile tests")
    parser.add_argument("--all", action="store_true", help="Run all test suites")
    parser.add_argument("--setup", action="store_true", help="Setup environment only")

    args = parser.parse_args()

    runner = TestRunner()
    runner.setup_environment()

    if args.setup:
        print("✅ Environment setup completed")
        return

    success = False
    start_time = time.time()

    if args.web:
        success = runner.run_cookie_clicker_tests()
    elif args.mobile:
        success = runner.run_apidemos_tests()
    elif args.all:
        success = runner.run_all_tests()
    else:
        parser.print_help()
        return

    duration = time.time() - start_time

    # Send final notification
    if success:
        message = "🎉 <b>Test execution completed successfully!</b>\n\n"
        message += f"Duration: {duration:.1f}s\n"
        message += f"Report: {os.path.join(runner.project_root, 'allure-report', 'index.html')}"
        send_telegram_message(message)
    else:
        message = "❌ <b>Test execution completed with failures.</b>\n\n"
        message += f"Duration: {duration:.1f}s\n"
        message += "Check console output and log files for details."
        send_telegram_message(message)


if __name__ == "__main__":
    main()