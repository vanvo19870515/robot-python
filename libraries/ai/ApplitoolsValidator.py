"""
ApplitoolsValidator - Applitools Eyes Integration for Visual Testing
Provides enhanced visual validation with screenshot comparison and Allure integration
"""

import os
import time
from datetime import datetime
from PIL import Image, ImageDraw
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from robot.api import logger
from robot.api.deco import keyword, library
import yaml

try:
    from applitools.selenium import Eyes, Target, VisualGridRunner, Configuration
    APPLITOOLS_AVAILABLE = True
except ImportError:
    APPLITOOLS_AVAILABLE = False
    logger.warn("Applitools Eyes not available. Install with: pip install applitools-eyes")

@library
class ApplitoolsValidator:
    """Applitools Eyes integration for advanced visual testing"""

    def __init__(self):
        self.config = self._load_config()
        self.eyes = None
        self.runner = None
        self.screenshot_counter = 0

    def _load_config(self):
        """Load configuration from yaml file"""
        try:
            with open('config/robot.yaml', 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            logger.warn(f"Could not load config: {e}")
            return {}

    def _initialize_eyes(self):
        """Initialize Applitools Eyes"""
        if not APPLITOOLS_AVAILABLE:
            logger.error("Applitools Eyes not available. Please install the package.")
            return False

        try:
            # Use Visual Grid Runner for enhanced performance
            self.runner = VisualGridRunner(10)  # Concurrency of 10

            self.eyes = Eyes(self.runner)
            self.eyes.api_key = os.getenv('APPLITOOLS_API_KEY', '')

            if not self.eyes.api_key:
                logger.warn("APPLITOOLS_API_KEY not set. Visual testing will be limited.")

            # Configure Eyes
            self.eyes.configure.batch_name = "SDET Technical Exercise"
            self.eyes.configure.app_name = "Robot Framework Demo"

            # Set match level to LAYOUT for better baseline matching
            self.eyes.configure.match_level = "LAYOUT"

            logger.info("Applitools Eyes initialized successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize Applitools Eyes: {e}")
            return False

    @keyword("Start Visual Test")
    def start_visual_test(self, test_name, viewport_size="1920x1080"):
        """Start a visual test session"""
        if not self._initialize_eyes():
            return False

        try:
            # Configure viewport
            if viewport_size:
                width, height = map(int, viewport_size.split('x'))
                self.eyes.configure.viewport_size = {"width": width, "height": height}

            # Start the test
            self.eyes.open(self.driver, "Robot Framework Demo", test_name)
            logger.info(f"Started visual test: {test_name}")
            return True

        except Exception as e:
            logger.error(f"Failed to start visual test: {e}")
            return False

    @keyword("Check Window")
    def check_window(self, tag=""):
        """Check the entire window for visual differences"""
        if not self.eyes:
            logger.error("Visual test not started. Call Start Visual Test first.")
            return False

        try:
            # Take screenshot and compare with baseline
            self.eyes.check_window(tag or f"Step {self.screenshot_counter}")
            self.screenshot_counter += 1
            logger.info(f"Window checked with tag: {tag}")
            return True

        except Exception as e:
            logger.error(f"Failed to check window: {e}")
            return False

    @keyword("Check Element")
    def check_element(self, locator, tag=""):
        """Check specific element for visual differences"""
        if not self.eyes:
            logger.error("Visual test not started. Call Start Visual Test first.")
            return False

        try:
            # Find element and check it
            element = self.driver.find_element(By.XPATH, locator)
            self.eyes.check_element(element, tag or f"Element {self.screenshot_counter}")
            self.screenshot_counter += 1
            logger.info(f"Element checked: {locator} with tag: {tag}")
            return True

        except Exception as e:
            logger.error(f"Failed to check element: {e}")
            return False

    @keyword("Check Region")
    def check_region(self, x, y, width, height, tag=""):
        """Check specific region for visual differences"""
        if not self.eyes:
            logger.error("Visual test not started. Call Start Visual Test first.")
            return False

        try:
            # Define region and check it
            region = {"x": int(x), "y": int(y), "width": int(width), "height": int(height)}
            self.eyes.check_region(region, tag or f"Region {self.screenshot_counter}")
            self.screenshot_counter += 1
            logger.info(f"Region checked: {region} with tag: {tag}")
            return True

        except Exception as e:
            logger.error(f"Failed to check region: {e}")
            return False

    @keyword("End Visual Test")
    def end_visual_test(self):
        """End the visual test session and get results"""
        if not self.eyes:
            logger.error("No visual test session active")
            return False

        try:
            # Close Eyes session
            results = self.eyes.close(False)  # Don't throw on failure

            if results:
                logger.info("Visual test completed successfully"                logger.info(f"  - Test: {results.name}")
                logger.info(f"  - Status: {results.status}")
                logger.info(f"  - URL: {results.url}")
                logger.info(f"  - Steps: {results.steps}")

                # Log mismatches if any
                if results.mismatches > 0:
                    logger.warn(f"  - Mismatches found: {results.mismatches}")

                return {
                    "name": results.name,
                    "status": results.status,
                    "mismatches": results.mismatches,
                    "steps": results.steps,
                    "url": results.url
                }
            else:
                logger.warn("No visual test results available")
                return None

        except Exception as e:
            logger.error(f"Failed to end visual test: {e}")
            return False
        finally:
            if self.eyes:
                self.eyes.abort()

    @keyword("Take Applitools Screenshot")
    def take_applitools_screenshot(self, filename_prefix="applitools"):
        """Take screenshot with Applitools integration"""
        try:
            screenshot_dir = "screenshots/applitools"
            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{filename_prefix}_{timestamp}.png"
            filepath = os.path.join(screenshot_dir, filename)

            # Take screenshot using Selenium
            self.driver.save_screenshot(filepath)

            # Also check with Applitools if session is active
            if self.eyes:
                self.check_window(f"Screenshot: {filename_prefix}")

            logger.info(f"Applitools screenshot saved: {filepath}")
            return filepath

        except Exception as e:
            logger.error(f"Failed to take Applitools screenshot: {e}")
            return None

    @keyword("Compare Baseline Images")
    def compare_baseline_images(self, baseline_path, current_path, threshold=0.95):
        """Compare baseline and current images using computer vision"""
        try:
            from skimage.metrics import structural_similarity as ssim
            import cv2

            # Load images
            baseline = cv2.imread(baseline_path)
            current = cv2.imread(current_path)

            if baseline is None or current is None:
                logger.error("Could not load one or both images")
                return False, 0

            # Convert to grayscale
            baseline_gray = cv2.cvtColor(baseline, cv2.COLOR_BGR2GRAY)
            current_gray = cv2.cvtColor(current, cv2.COLOR_BGR2GRAY)

            # Compute SSIM
            score, diff = ssim(baseline_gray, current_gray, full=True)

            is_similar = score >= threshold

            logger.info(f"Image similarity: {score:.2%} (threshold: {threshold:.2%})")
            logger.info(f"Images {'match' if is_similar else 'differ'}")

            # Save difference image if available
            if diff is not None:
                diff_path = current_path.replace('.png', '_diff.png')
                cv2.imwrite(diff_path, (diff * 255).astype('uint8'))
                logger.info(f"Difference image saved: {diff_path}")

            return is_similar, score

        except ImportError:
            logger.warn("scikit-image not available. Using simple comparison.")
            return self._simple_image_comparison(baseline_path, current_path, threshold)

    def _simple_image_comparison(self, baseline_path, current_path, threshold):
        """Simple image comparison when advanced libraries aren't available"""
        try:
            from PIL import Image

            baseline = Image.open(baseline_path)
            current = Image.open(current_path)

            if baseline.size != current.size:
                logger.error("Images have different dimensions")
                return False, 0

            # Simple pixel-by-pixel comparison
            pixels_diff = 0
            total_pixels = baseline.size[0] * baseline.size[1]

            for x in range(baseline.size[0]):
                for y in range(baseline.size[1]):
                    if baseline.getpixel((x, y)) != current.getpixel((x, y)):
                        pixels_diff += 1

            similarity = 1.0 - (pixels_diff / total_pixels)

            logger.info(f"Pixel similarity: {similarity:.2%} (threshold: {threshold:.2%})")
            return similarity >= threshold, similarity

        except Exception as e:
            logger.error(f"Failed to compare images: {e}")
            return False, 0

    @keyword("Generate Visual Report")
    def generate_visual_report(self, test_results):
        """Generate comprehensive visual report"""
        try:
            report_data = {
                "timestamp": datetime.now().isoformat(),
                "test_results": test_results,
                "summary": {
                    "total_tests": len(test_results),
                    "passed": sum(1 for r in test_results if r.get('status') == 'PASSED'),
                    "failed": sum(1 for r in test_results if r.get('status') == 'FAILED'),
                    "unresolved": sum(1 for r in test_results if r.get('status') == 'UNRESOLVED')
                },
                "recommendations": self._generate_recommendations(test_results)
            }

            # Save report
            report_path = f"reports/visual_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(report_path, 'w') as f:
                import json
                json.dump(report_data, f, indent=2)

            logger.info(f"Visual report generated: {report_path}")
            return report_path

        except Exception as e:
            logger.error(f"Failed to generate visual report: {e}")
            return None

    def _generate_recommendations(self, test_results):
        """Generate recommendations based on test results"""
        recommendations = []

        failed_tests = [r for r in test_results if r.get('status') == 'FAILED']

        if failed_tests:
            recommendations.append("Review failed visual tests and update baselines if changes are expected")
            recommendations.append("Check for UI layout changes or styling updates")

        unresolved_tests = [r for r in test_results if r.get('status') == 'UNRESOLVED']
        if unresolved_tests:
            recommendations.append("Resolve unresolved visual differences in Applitools dashboard")
            recommendations.append("Approve or reject baseline changes as needed")

        if len(recommendations) == 0:
            recommendations.append("All visual tests passed successfully")
            recommendations.append("Continue monitoring for visual regressions")

        return recommendations

    @keyword("Setup Visual Grid")
    def setup_visual_grid(self, concurrency=5):
        """Setup Visual Grid for cross-browser testing"""
        if not APPLITOOLS_AVAILABLE:
            logger.error("Applitools Eyes not available")
            return False

        try:
            # Configure Visual Grid
            self.runner = VisualGridRunner(concurrency)

            # Set up multiple browsers and viewports
            self.runner.configure.set_concurrency(concurrency)

            # Add different browsers and viewports
            browsers = [
                {"name": "chrome", "width": 1920, "height": 1080},
                {"name": "chrome", "width": 1366, "height": 768},
                {"name": "chrome", "width": 375, "height": 667},  # Mobile
                {"name": "firefox", "width": 1920, "height": 1080},
                {"name": "safari", "width": 1920, "height": 1080},
            ]

            for browser in browsers:
                self.runner.configure.add_browser(
                    browser["width"], browser["height"], browser["name"]
                )

            logger.info(f"Visual Grid configured with {concurrency} concurrency and {len(browsers)} browser configurations")
            return True

        except Exception as e:
            logger.error(f"Failed to setup Visual Grid: {e}")
            return False

    @keyword("Validate Visual Consistency")
    def validate_visual_consistency(self, baseline_screenshot, current_screenshot, tolerance=5):
        """Validate visual consistency with tolerance percentage"""
        try:
            # Get image quality metrics for both images
            baseline_metrics = self.validate_image_quality(baseline_screenshot)
            current_metrics = self.validate_image_quality(current_screenshot)

            if 'error' in baseline_metrics or 'error' in current_metrics:
                return {"error": "Could not analyze one or both images"}

            # Compare key metrics
            differences = {}
            for metric in ['brightness', 'contrast', 'sharpness', 'colorfulness']:
                if metric in baseline_metrics and metric in current_metrics:
                    baseline_val = baseline_metrics[metric]
                    current_val = current_metrics[metric]

                    if isinstance(baseline_val, (int, float)) and isinstance(current_val, (int, float)):
                        diff = abs(baseline_val - current_val)
                        diff_percent = (diff / max(baseline_val, 1)) * 100

                        differences[metric] = {
                            "baseline": baseline_val,
                            "current": current_val,
                            "difference": round(diff, 2),
                            "difference_percent": round(diff_percent, 1),
                            "within_tolerance": diff_percent <= tolerance
                        }

            # Overall consistency score
            consistent_metrics = sum(1 for d in differences.values() if d['within_tolerance'])
            total_metrics = len(differences)
            consistency_score = (consistent_metrics / total_metrics) * 100 if total_metrics > 0 else 0

            result = {
                "consistency_score": round(consistency_score, 1),
                "total_metrics": total_metrics,
                "consistent_metrics": consistent_metrics,
                "differences": differences,
                "is_consistent": consistency_score >= 80,  # 80% consistency threshold
                "tolerance_used": tolerance
            }

            logger.info(f"Visual consistency score: {consistency_score:.1f}%")
            return result

        except Exception as e:
            logger.error(f"Failed to validate visual consistency: {e}")
            return {"error": str(e)}
