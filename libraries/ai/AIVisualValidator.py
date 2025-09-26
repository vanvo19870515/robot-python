"""
AIVisualValidator - AI-Powered Visual Testing
Uses AI and computer vision for visual validation and testing
"""

import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from robot.api import logger
from robot.api.deco import keyword, library
import yaml

@library
class AIVisualValidator:
    """AI-powered visual validation for web applications"""

    def __init__(self):
        self.config = self._load_config()
        self.screenshot_counter = 0

    def _load_config(self):
        """Load configuration from yaml file"""
        try:
            with open('config/robot.yaml', 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            logger.warn(f"Could not load config: {e}")
            return {}

    @keyword("Capture Page Screenshot")
    def capture_page_screenshot(self, filename_prefix="screenshot"):
        """Capture full page screenshot"""
        try:
            screenshot_dir = self.config.get('data', {}).get('screenshot_dir', 'screenshots')
            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{filename_prefix}_{timestamp}.png"
            filepath = os.path.join(screenshot_dir, filename)

            # Get full page height
            total_height = self.driver.execute_script("""
                return Math.max(
                    document.body.scrollHeight,
                    document.body.offsetHeight,
                    document.documentElement.clientHeight,
                    document.documentElement.scrollHeight,
                    document.documentElement.offsetHeight
                );
            """)

            # Set window size to full page height
            viewport_height = self.driver.execute_script("return window.innerHeight")
            self.driver.set_window_size(1920, total_height)

            # Scroll to top and capture
            self.driver.execute_script("window.scrollTo(0, 0);")
            self.driver.save_screenshot(filepath)

            # Reset window size
            self.driver.set_window_size(1920, 1080)

            logger.info(f"Screenshot captured: {filepath}")
            return filepath

        except Exception as e:
            logger.error(f"Failed to capture screenshot: {e}")
            return None

    @keyword("Compare Visual Elements")
    def compare_visual_elements(self, baseline_image, current_image, threshold=0.9):
        """
        Compare two images for visual differences
        Args:
            baseline_image: Path to baseline image
            current_image: Path to current image
            threshold: Similarity threshold (0-1)
        Returns:
            Comparison result and difference percentage
        """
        try:
            # Load images
            baseline = cv2.imread(baseline_image)
            current = cv2.imread(current_image)

            if baseline is None or current is None:
                logger.error("Could not load one or both images")
                return False, 0

            # Convert to grayscale
            baseline_gray = cv2.cvtColor(baseline, cv2.COLOR_BGR2GRAY)
            current_gray = cv2.cvtColor(current, cv2.COLOR_BGR2GRAY)

            # Compute structural similarity
            similarity = self._calculate_ssim(baseline_gray, current_gray)

            is_similar = similarity >= threshold

            logger.info(f"Visual similarity: {similarity:.2%} (threshold: {threshold:.2%})")
            logger.info(f"Visual match: {'PASS' if is_similar else 'FAIL'}")

            return is_similar, similarity

        except Exception as e:
            logger.error(f"Failed to compare images: {e}")
            return False, 0

    def _calculate_ssim(self, img1, img2):
        """Calculate Structural Similarity Index"""
        try:
            from skimage.metrics import structural_similarity as ssim
            score, _ = ssim(img1, img2, full=True)
            return score
        except ImportError:
            # Fallback to simple pixel comparison
            logger.warn("SSIM not available, using pixel comparison")
            return self._simple_similarity(img1, img2)

    def _simple_similarity(self, img1, img2):
        """Simple pixel-by-pixel similarity calculation"""
        if img1.shape != img2.shape:
            return 0.0

        # Calculate mean squared error
        mse = np.mean((img1.astype(float) - img2.astype(float)) ** 2)

        if mse == 0:
            return 1.0

        # Calculate PSNR-based similarity
        psnr = 20 * np.log10(255.0 / np.sqrt(mse))
        similarity = 1.0 / (1.0 + np.exp(-psnr/10.0))  # Sigmoid normalization

        return similarity

    @keyword("Highlight Element On Screenshot")
    def highlight_element_on_screenshot(self, screenshot_path, locator, color="red"):
        """
        Highlight an element on a screenshot
        Args:
            screenshot_path: Path to screenshot
            locator: Element locator (xpath)
            color: Highlight color (red, blue, green, yellow)
        Returns:
            Path to modified screenshot
        """
        try:
            # Load screenshot
            image = Image.open(screenshot_path)
            draw = ImageDraw.Draw(image)

            # Find element coordinates
            element = self.driver.find_element(By.XPATH, locator)
            location = element.location
            size = element.size

            # Convert coordinates
            x1, y1 = int(location['x']), int(location['y'])
            x2, y2 = x1 + int(size['width']), y1 + int(size['height'])

            # Define colors
            colors = {
                'red': (255, 0, 0, 128),
                'blue': (0, 0, 255, 128),
                'green': (0, 255, 0, 128),
                'yellow': (255, 255, 0, 128)
            }

            color_rgba = colors.get(color, colors['red'])

            # Draw highlight rectangle
            draw.rectangle([x1, y1, x2, y2], outline=color_rgba[:3], width=3, fill=color_rgba)

            # Save modified image
            timestamp = datetime.now().strftime("%H%M%S")
            filename = f"highlighted_{timestamp}.png"
            output_path = os.path.join(os.path.dirname(screenshot_path), filename)
            image.save(output_path)

            logger.info(f"Highlighted screenshot saved: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Failed to highlight element: {e}")
            return None

    @keyword("Validate Image Quality")
    def validate_image_quality(self, image_path):
        """
        Validate image quality metrics
        Args:
            image_path: Path to image to validate
        Returns:
            Quality metrics dictionary
        """
        try:
            image = cv2.imread(image_path)
            if image is None:
                return {"error": "Could not load image"}

            # Calculate basic metrics
            height, width = image.shape[:2]

            # Brightness (average pixel value)
            brightness = np.mean(image)

            # Contrast (standard deviation)
            contrast = np.std(image)

            # Sharpness (using Laplacian variance)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()

            # Colorfulness
            colorfulness = self._calculate_colorfulness(image)

            metrics = {
                "dimensions": f"{width}x{height}",
                "brightness": round(brightness, 2),
                "contrast": round(contrast, 2),
                "sharpness": round(sharpness, 2),
                "colorfulness": round(colorfulness, 2),
                "quality_score": self._calculate_overall_quality(brightness, contrast, sharpness, colorfulness)
            }

            logger.info(f"Image quality metrics: {metrics}")
            return metrics

        except Exception as e:
            logger.error(f"Failed to validate image quality: {e}")
            return {"error": str(e)}

    def _calculate_colorfulness(self, image):
        """Calculate colorfulness metric"""
        try:
            # Convert to float
            image = image.astype(float)

            # Split channels
            B, G, R = image[:,:,0], image[:,:,1], image[:,:,2]

            # Compute RG and YB differences
            RG = R - G
            YB = 0.5 * (R + G) - B

            # Compute mean and std
            RG_mean, RG_std = np.mean(RG), np.std(RG)
            YB_mean, YB_std = np.mean(YB), np.std(YB)

            # Calculate colorfulness
            colorfulness = np.sqrt(RG_std**2 + YB_std**2) + 0.3 * np.sqrt(RG_mean**2 + YB_mean**2)

            return colorfulness

        except Exception:
            return 0

    def _calculate_overall_quality(self, brightness, contrast, sharpness, colorfulness):
        """Calculate overall image quality score"""
        try:
            # Normalize metrics (ideal ranges)
            brightness_score = 1.0 if 100 <= brightness <= 150 else max(0, 1 - abs(brightness - 125) / 125)
            contrast_score = min(1.0, contrast / 50.0)  # Ideal contrast around 50
            sharpness_score = min(1.0, sharpness / 100.0)  # Ideal sharpness varies
            colorfulness_score = min(1.0, colorfulness / 30.0)  # Ideal colorfulness around 30

            # Weighted average
            overall_score = (
                brightness_score * 0.25 +
                contrast_score * 0.25 +
                sharpness_score * 0.25 +
                colorfulness_score * 0.25
            )

            return round(overall_score * 100, 1)

        except Exception:
            return 0

    @keyword("Detect UI Elements")
    def detect_ui_elements(self, screenshot_path):
        """
        Use computer vision to detect UI elements
        Args:
            screenshot_path: Path to screenshot
        Returns:
            Detected elements information
        """
        try:
            image = cv2.imread(screenshot_path)
            if image is None:
                return {"error": "Could not load image"}

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Apply edge detection
            edges = cv2.Canny(gray, 50, 150)

            # Find contours
            contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            elements = []
            for i, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if area > 100:  # Filter small noise
                    x, y, w, h = cv2.boundingRect(contour)
                    elements.append({
                        "id": i,
                        "position": f"({x}, {y})",
                        "size": f"{w}x{h}",
                        "area": int(area),
                        "type": self._classify_element(w, h, area)
                    })

            # Sort by area (larger elements first)
            elements.sort(key=lambda x: x['area'], reverse=True)

            logger.info(f"Detected {len(elements)} UI elements")

            return {
                "total_elements": len(elements),
                "elements": elements[:10],  # Return top 10 largest elements
                "image_info": self.validate_image_quality(screenshot_path)
            }

        except Exception as e:
            logger.error(f"Failed to detect UI elements: {e}")
            return {"error": str(e)}

    def _classify_element(self, width, height, area):
        """Classify UI element type based on dimensions and area"""
        aspect_ratio = width / height if height > 0 else 0

        if aspect_ratio > 3:
            return "Text/Button"  # Likely text or narrow button
        elif aspect_ratio < 0.3:
            return "Tall Element"  # Likely sidebar or tall component
        elif area > 50000:
            return "Large Container"  # Likely main content area
        elif 10000 < area <= 50000:
            return "Medium Container"  # Likely card or section
        elif 1000 < area <= 10000:
            return "Small Container"  # Likely button or input
        else:
            return "Small Element"  # Likely icon or small component

    @keyword("Validate Visual Consistency")
    def validate_visual_consistency(self, baseline_screenshot, current_screenshot, tolerance=5):
        """
        Validate visual consistency between baseline and current
        Args:
            baseline_screenshot: Path to baseline screenshot
            current_screenshot: Path to current screenshot
            tolerance: Tolerance percentage for differences
        Returns:
            Consistency validation result
        """
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
