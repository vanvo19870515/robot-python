"""
AITestGenerator - AI-Powered Test Case Generation
Uses AI to generate test scenarios, assertions, and edge cases
"""

import os
import yaml
from openai import OpenAI
from anthropic import Anthropic
from robot.api import logger
from robot.api.deco import keyword, library

@library
class AITestGenerator:
    """AI-powered test case and scenario generation"""

    def __init__(self):
        self.config = self._load_config()
        self.ai_provider = self.config.get('ai', {}).get('provider', 'openai')
        self.model = self.config.get('ai', {}).get('model', 'gpt-4')
        self.client = self._initialize_ai_client()

    def _load_config(self):
        """Load configuration from yaml file"""
        try:
            with open('config/robot.yaml', 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            logger.warn(f"Could not load config: {e}")
            return {}

    def _initialize_ai_client(self):
        """Initialize AI client based on provider"""
        try:
            if self.ai_provider == 'openai':
                return OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            elif self.ai_provider == 'anthropic':
                return Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
            else:
                logger.warn(f"Unsupported AI provider: {self.ai_provider}")
                return None
        except Exception as e:
            logger.error(f"Failed to initialize AI client: {e}")
            return None

    @keyword("Generate Test Scenario")
    def generate_test_scenario(self, application_type, feature_description):
        """
        Generate test scenario using AI
        Args:
            application_type: Type of application (web, mobile, api)
            feature_description: Description of the feature to test
        Returns:
            Generated test scenario as string
        """
        if not self.client:
            return "AI client not initialized"

        prompt = f"""
        Generate a comprehensive test scenario for the following:

        Application Type: {application_type}
        Feature Description: {feature_description}

        Please provide:
        1. Test scenario name
        2. Preconditions
        3. Test steps (detailed)
        4. Expected results
        5. Potential edge cases
        6. Data requirements

        Format the response as a structured test case.
        """

        try:
            if self.ai_provider == 'openai':
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=self.config.get('ai', {}).get('max_tokens', 2000),
                    temperature=self.config.get('ai', {}).get('temperature', 0.7)
                )
                return response.choices[0].message.content

            elif self.ai_provider == 'anthropic':
                response = self.client.messages.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=self.config.get('ai', {}).get('max_tokens', 2000),
                    temperature=self.config.get('ai', {}).get('temperature', 0.7)
                )
                return response.content[0].text

        except Exception as e:
            logger.error(f"Failed to generate test scenario: {e}")
            return f"Error generating test scenario: {str(e)}"

    @keyword("Generate Test Assertions")
    def generate_test_assertions(self, page_content, element_type):
        """
        Generate appropriate assertions for given content
        Args:
            page_content: Description of page content
            element_type: Type of element (button, form, list, etc.)
        Returns:
            Generated assertions as string
        """
        if not self.client:
            return "AI client not initialized"

        prompt = f"""
        Generate appropriate test assertions for:

        Page Content: {page_content}
        Element Type: {element_type}

        Please provide Robot Framework style assertions including:
        1. Element visibility assertions
        2. Content validation assertions
        3. State validation assertions
        4. Error condition assertions
        5. Accessibility assertions

        Format as executable Robot Framework keywords.
        """

        try:
            if self.ai_provider == 'openai':
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1500,
                    temperature=0.5
                )
                return response.choices[0].message.content

            elif self.ai_provider == 'anthropic':
                response = self.client.messages.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1500,
                    temperature=0.5
                )
                return response.content[0].text

        except Exception as e:
            logger.error(f"Failed to generate assertions: {e}")
            return f"Error generating assertions: {str(e)}"

    @keyword("Generate Edge Cases")
    def generate_edge_cases(self, feature_description):
        """
        Generate edge cases and negative scenarios
        Args:
            feature_description: Description of the feature
        Returns:
            Generated edge cases as string
        """
        if not self.client:
            return "AI client not initialized"

        prompt = f"""
        Generate comprehensive edge cases and negative test scenarios for:

        Feature Description: {feature_description}

        Please provide:
        1. Boundary value scenarios
        2. Invalid input scenarios
        3. Error condition scenarios
        4. Performance stress scenarios
        5. Security test scenarios
        6. Accessibility scenarios

        Format each scenario with:
        - Scenario name
        - Test steps
        - Expected behavior
        - Priority level
        """

        try:
            if self.ai_provider == 'openai':
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=2000,
                    temperature=0.8
                )
                return response.choices[0].message.content

            elif self.ai_provider == 'anthropic':
                response = self.client.messages.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=2000,
                    temperature=0.8
                )
                return response.content[0].text

        except Exception as e:
            logger.error(f"Failed to generate edge cases: {e}")
            return f"Error generating edge cases: {str(e)}"

    @keyword("Generate Test Data")
    def generate_test_data(self, data_type, count=10):
        """
        Generate test data using AI
        Args:
            data_type: Type of data needed (user, product, address, etc.)
            count: Number of data sets to generate
        Returns:
            Generated test data as JSON string
        """
        if not self.client:
            return '{"error": "AI client not initialized"}'

        prompt = f"""
        Generate {count} sets of realistic test data for: {data_type}

        Please provide the data in JSON format with appropriate fields for {data_type}.
        Include variations in the data to cover different scenarios.

        Example format for user data:
        [
            {{
                "name": "John Doe",
                "email": "john.doe@example.com",
                "age": 25,
                "active": true
            }}
        ]

        Ensure the data is realistic and covers edge cases.
        """

        try:
            if self.ai_provider == 'openai':
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=2000,
                    temperature=0.9
                )
                return response.choices[0].message.content

            elif self.ai_provider == 'anthropic':
                response = self.client.messages.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=2000,
                    temperature=0.9
                )
                return response.content[0].text

        except Exception as e:
            logger.error(f"Failed to generate test data: {e}")
            return f'{{"error": "Failed to generate test data: {str(e)}"}}'

    @keyword("Analyze Test Coverage")
    def analyze_test_coverage(self, existing_tests, application_features):
        """
        Analyze test coverage gaps using AI
        Args:
            existing_tests: Description of existing tests
            application_features: Description of application features
        Returns:
            Coverage analysis and recommendations
        """
        if not self.client:
            return "AI client not initialized"

        prompt = f"""
        Analyze test coverage for the following:

        Existing Tests: {existing_tests}
        Application Features: {application_features}

        Please provide:
        1. Coverage gaps identified
        2. Missing test scenarios
        3. Risk areas not covered
        4. Recommendations for additional tests
        5. Priority levels for new tests

        Format as a structured analysis report.
        """

        try:
            if self.ai_provider == 'openai':
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=2000,
                    temperature=0.6
                )
                return response.choices[0].message.content

            elif self.ai_provider == 'anthropic':
                response = self.client.messages.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=2000,
                    temperature=0.6
                )
                return response.content[0].text

        except Exception as e:
            logger.error(f"Failed to analyze test coverage: {e}")
            return f"Error analyzing test coverage: {str(e)}"

    @keyword("Generate Performance Test")
    def generate_performance_test(self, feature_description):
        """
        Generate performance test scenarios
        Args:
            feature_description: Description of the feature to test
        Returns:
            Performance test scenario
        """
        if not self.client:
            return "AI client not initialized"

        prompt = f"""
        Generate performance test scenarios for:

        Feature Description: {feature_description}

        Please provide:
        1. Load testing scenarios
        2. Stress testing scenarios
        3. Volume testing scenarios
        4. Performance metrics to measure
        5. Success criteria

        Format as executable test scenarios.
        """

        try:
            if self.ai_provider == 'openai':
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=2000,
                    temperature=0.7
                )
                return response.choices[0].message.content

            elif self.ai_provider == 'anthropic':
                response = self.client.messages.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=2000,
                    temperature=0.7
                )
                return response.content[0].text

        except Exception as e:
            logger.error(f"Failed to generate performance test: {e}")
            return f"Error generating performance test: {str(e)}"

    @keyword("Generate Security Test")
    def generate_security_test(self, feature_description):
        """
        Generate security test scenarios
        Args:
            feature_description: Description of the feature to test
        Returns:
            Security test scenario
        """
        if not self.client:
            return "AI client not initialized"

        prompt = f"""
        Generate security test scenarios for:

        Feature Description: {feature_description}

        Please provide:
        1. Authentication and authorization tests
        2. Input validation tests
        3. SQL injection tests
        4. XSS vulnerability tests
        5. CSRF protection tests
        6. Data encryption tests

        Format as security test scenarios with steps and assertions.
        """

        try:
            if self.ai_provider == 'openai':
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=2000,
                    temperature=0.8
                )
                return response.choices[0].message.content

            elif self.ai_provider == 'anthropic':
                response = self.client.messages.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=2000,
                    temperature=0.8
                )
                return response.content[0].text

        except Exception as e:
            logger.error(f"Failed to generate security test: {e}")
            return f"Error generating security test: {str(e)}"
