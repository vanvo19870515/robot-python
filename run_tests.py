#!/usr/bin/env python3
"""
SDET Technical Exercise - Test Runner
Automated test execution and reporting for the Robot Framework project
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

class TestRunner:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.tests_dir = self.project_root / "tests"
        self.reports_dir = self.project_root / "reports"

    def setup_environment(self):
        """Setup test environment"""
        print("🔧 Setting up test environment...")

        # Create reports directory
        self.reports_dir.mkdir(exist_ok=True)

        # Check if dependencies are installed
        try:
            import robot
            print("✅ Robot Framework is installed")
        except ImportError:
            print("❌ Robot Framework not found. Installing...")
            self.install_dependencies()

    def install_dependencies(self):
        """Install Python dependencies"""
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r",
                str(self.project_root / "requirements.txt")
            ], check=True)
            print("✅ Dependencies installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            sys.exit(1)

    def run_demo_tests(self):
        """Run demo tests to showcase functionality"""
        print("🎬 Running Demo Tests...")
        return self.run_robot_tests("demo_tests.robot", "Demo tests completed successfully")

    def run_smoke_tests(self):
        """Run smoke tests for comprehensive validation"""
        print("🚀 Running Smoke Tests...")
        return self.run_robot_tests("smoke_tests.robot", "Smoke tests completed successfully")

    def run_all_tests(self):
        """Run all available tests"""
        print("🏃 Running All Tests...")
        return self.run_robot_tests("", "All tests completed successfully")

    def run_robot_tests(self, test_file, success_message):
        """Execute Robot Framework tests"""
        try:
            cmd = [
                "robot",
                "--outputdir", str(self.reports_dir),
                "--loglevel", "INFO",
                "--variable", f"PROJECT_ROOT:{self.project_root}",
                str(self.tests_dir / "suites" / test_file) if test_file else str(self.tests_dir / "suites")
            ]

            result = subprocess.run(cmd, cwd=self.project_root, capture_output=True, text=True)

            if result.returncode == 0:
                print(f"✅ {success_message}")
                self.show_results()
                return True
            else:
                print(f"❌ Tests failed with return code: {result.returncode}")
                print("STDOUT:", result.stdout)
                print("STDERR:", result.stderr)
                return False

        except FileNotFoundError:
            print("❌ Robot Framework not found. Please install dependencies first.")
            return False
        except Exception as e:
            print(f"❌ Error running tests: {e}")
            return False

    def show_results(self):
        """Display test results"""
        print("\n📊 Test Results:")
        print(f"   📁 Reports: {self.reports_dir}")
        print(f"   📄 Log: {self.reports_dir}/log.html")
        print(f"   📋 Report: {self.reports_dir}/report.html")
        print(f"   📊 Output: {self.reports_dir}/output.xml")

    def generate_test_report(self):
        """Generate additional test reports"""
        try:
            # Try to generate Allure report if available
            if os.system("allure --version") == 0:
                print("🎨 Generating Allure report...")
                os.system("allure generate allure-results --clean")
                print("   📊 Allure report: allure-report/index.html")
        except:
            pass

    def main(self):
        """Main execution method"""
        parser = argparse.ArgumentParser(description="SDET Technical Exercise Test Runner")
        parser.add_argument("--demo", action="store_true", help="Run demo tests")
        parser.add_argument("--smoke", action="store_true", help="Run smoke tests")
        parser.add_argument("--all", action="store_true", help="Run all tests")
        parser.add_argument("--setup", action="store_true", help="Setup environment only")

        args = parser.parse_args()

        # Setup environment
        self.setup_environment()

        if args.setup:
            print("✅ Environment setup completed")
            return

        # Run tests based on arguments
        success = False
        if args.demo or not any([args.demo, args.smoke, args.all]):
            success = self.run_demo_tests()
        elif args.smoke:
            success = self.run_smoke_tests()
        elif args.all:
            success = self.run_all_tests()

        # Generate additional reports
        self.generate_test_report()

        if success:
            print("\n🎉 Test execution completed successfully!")
            print("📋 Check the reports directory for detailed results.")
        else:
            print("\n❌ Test execution completed with failures.")
            print("🔍 Check the console output and log files for details.")
            sys.exit(1)

if __name__ == "__main__":
    runner = TestRunner()
    runner.main()
