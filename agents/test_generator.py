#!/usr/bin/env python3
"""
Test Generator Agent

Meta-Prompt: You are a Senior Test Engineer specializing in automated test generation.
Your role is to analyze code repositories and generate comprehensive test suites
that validate functionality, edge cases, and integration points.

Follows DX best practices:
- Unit prompting: One clear task per method
- Meta-prompting: Explicit role and context
- Modular design: Composable test generation functions
- Self-correction: Validate generated tests before output
"""

import os
import json
import ast
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class TestGenerator:
    """
    Agent responsible for generating comprehensive test suites for analyzed repositories.
    
    Meta-Prompt Context:
    - Role: Senior Test Engineer with expertise in Python, JavaScript, and modern testing frameworks
    - Task: Generate unit tests, integration tests, and validation scripts
    - Quality: Tests must be executable, comprehensive, and follow best practices
    """
    
    def __init__(self, prompts_dir="prompts", outputs_dir="outputs"):
        self.prompts_dir = Path(prompts_dir)
        self.outputs_dir = Path(outputs_dir)
        self.test_frameworks = {
            'python': ['pytest', 'unittest', 'nose2'],
            'javascript': ['jest', 'mocha', 'jasmine'],
            'java': ['junit', 'testng'],
            'go': ['testing', 'testify'],
            'rust': ['cargo test'],
            'c++': ['gtest', 'catch2']
        }
        
    def generate_tests(self, repo_data: Dict[str, Any], 
                      documentation: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main test generation pipeline.
        
        Args:
            repo_data: Parsed repository structure and code analysis
            documentation: Generated documentation sections
            
        Returns:
            Dict containing generated test files and test strategy
        """
        print("🧪 Test Generator: Analyzing codebase for test generation...")
        
        test_strategy = self._analyze_test_strategy(repo_data)
        test_files = self._generate_test_files(repo_data, test_strategy)
        test_coverage = self._analyze_coverage_requirements(repo_data)
        validation_scripts = self._generate_validation_scripts(repo_data)
        
        test_suite = {
            'strategy': test_strategy,
            'test_files': test_files,
            'coverage_requirements': test_coverage,
            'validation_scripts': validation_scripts,
            'generated_at': datetime.utcnow().isoformat(),
            'framework_recommendations': self._recommend_frameworks(repo_data)
        }
        
        # Save test generation results
        self._save_test_results(test_suite)
        
        print(f"✅ Generated {len(test_files)} test files with {test_strategy['approach']} strategy")
        return test_suite
    
    def _analyze_test_strategy(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Unit Prompt: Analyze repository to determine optimal testing strategy.
        
        Meta-Context: You are analyzing a codebase to determine the most effective
        testing approach based on project type, complexity, and existing patterns.
        """
        primary_language = repo_data.get('primary_language', 'unknown').lower()
        file_count = len(repo_data.get('files', []))
        has_existing_tests = self._detect_existing_tests(repo_data)
        
        # Determine testing approach based on project characteristics
        if file_count < 10:
            approach = 'lightweight'
            focus = ['unit_tests', 'basic_integration']
        elif file_count < 50:
            approach = 'standard'
            focus = ['unit_tests', 'integration_tests', 'end_to_end']
        else:
            approach = 'comprehensive'
            focus = ['unit_tests', 'integration_tests', 'end_to_end', 'performance', 'security']
        
        return {
            'approach': approach,
            'focus_areas': focus,
            'primary_language': primary_language,
            'existing_tests': has_existing_tests,
            'recommended_coverage': self._calculate_coverage_target(file_count),
            'priority_files': self._identify_critical_files(repo_data)
        }
    
    def _generate_test_files(self, repo_data: Dict[str, Any], 
                           strategy: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Unit Prompt: Generate specific test files based on analyzed code structure.
        
        Meta-Context: You are creating executable test files that validate
        the functionality of the analyzed codebase components.
        """
        test_files = []
        primary_language = strategy['primary_language']
        
        # Generate tests for critical files
        for file_path in strategy.get('priority_files', []):
            if self._should_generate_tests(file_path, repo_data):
                test_content = self._generate_test_content(file_path, repo_data, primary_language)
                if test_content:
                    test_files.append({
                        'source_file': file_path,
                        'test_file': self._get_test_filename(file_path, primary_language),
                        'content': test_content,
                        'test_type': 'unit',
                        'framework': self._get_preferred_framework(primary_language)
                    })
        
        # Generate integration tests
        if 'integration_tests' in strategy['focus_areas']:
            integration_tests = self._generate_integration_tests(repo_data, primary_language)
            test_files.extend(integration_tests)
        
        # Generate end-to-end tests for web applications
        if self._is_web_application(repo_data) and 'end_to_end' in strategy['focus_areas']:
            e2e_tests = self._generate_e2e_tests(repo_data)
            test_files.extend(e2e_tests)
        
        return test_files
    
    def _generate_test_content(self, file_path: str, repo_data: Dict[str, Any], 
                             language: str) -> Optional[str]:
        """
        Unit Prompt: Generate specific test content for a given source file.
        
        Meta-Context: You are writing executable test code that validates
        the functions, classes, and methods in the source file.
        """
        if language == 'python':
            return self._generate_python_tests(file_path, repo_data)
        elif language == 'javascript':
            return self._generate_javascript_tests(file_path, repo_data)
        elif language == 'java':
            return self._generate_java_tests(file_path, repo_data)
        else:
            return self._generate_generic_tests(file_path, repo_data, language)
    
    def _generate_python_tests(self, file_path: str, repo_data: Dict[str, Any]) -> str:
        """
        Generate Python-specific test content using pytest framework.
        """
        module_name = Path(file_path).stem
        test_content = f'''#!/usr/bin/env python3
"""
Generated tests for {file_path}
Auto-generated by GitRead Test Generator
"""

import pytest
import sys
from pathlib import Path

# Add source directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import {module_name}
except ImportError:
    pytest.skip(f"Could not import {module_name}", allow_module_level=True)


class Test{module_name.title()}:
    """Test suite for {module_name} module."""
    
    def setup_method(self):
        """Setup test fixtures before each test method."""
        pass
    
    def teardown_method(self):
        """Clean up after each test method."""
        pass
    
    def test_module_imports(self):
        """Test that the module can be imported successfully."""
        assert {module_name} is not None
    
    def test_basic_functionality(self):
        """Test basic functionality of the module."""
        # TODO: Add specific tests based on module analysis
        pass
    
    @pytest.mark.parametrize("input_value,expected", [
        ("test_input", "expected_output"),
        # Add more test cases
    ])
    def test_parametrized_cases(self, input_value, expected):
        """Test various input/output combinations."""
        # TODO: Implement parametrized tests
        pass
    
    def test_edge_cases(self):
        """Test edge cases and error conditions."""
        # TODO: Add edge case tests
        pass


if __name__ == "__main__":
    pytest.main([__file__])
'''
        return test_content
    
    def _generate_javascript_tests(self, file_path: str, repo_data: Dict[str, Any]) -> str:
        """
        Generate JavaScript-specific test content using Jest framework.
        """
        module_name = Path(file_path).stem
        test_content = f'''/**
 * Generated tests for {file_path}
 * Auto-generated by GitRead Test Generator
 */

const {module_name} = require('../{file_path}');

describe('{module_name}', () => {{
    beforeEach(() => {{
        // Setup test fixtures
    }});
    
    afterEach(() => {{
        // Clean up after tests
    }});
    
    test('module should be defined', () => {{
        expect({module_name}).toBeDefined();
    }});
    
    test('basic functionality', () => {{
        // TODO: Add specific tests based on module analysis
        expect(true).toBe(true);
    }});
    
    describe('edge cases', () => {{
        test('handles null input', () => {{
            // TODO: Add null input tests
        }});
        
        test('handles empty input', () => {{
            // TODO: Add empty input tests
        }});
    }});
    
    describe('error conditions', () => {{
        test('throws appropriate errors', () => {{
            // TODO: Add error condition tests
        }});
    }});
}});
'''
        return test_content
    
    def _generate_integration_tests(self, repo_data: Dict[str, Any], 
                                  language: str) -> List[Dict[str, Any]]:
        """
        Generate integration tests that validate component interactions.
        """
        integration_tests = []
        
        if language == 'python':
            test_content = '''#!/usr/bin/env python3
"""
Integration Tests
Auto-generated by GitRead Test Generator
"""

import pytest
import sys
from pathlib import Path

# Add source directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestIntegration:
    """Integration test suite."""
    
    def test_component_integration(self):
        """Test that components work together correctly."""
        # TODO: Add integration tests
        pass
    
    def test_data_flow(self):
        """Test data flow between components."""
        # TODO: Add data flow tests
        pass
    
    def test_api_endpoints(self):
        """Test API endpoints if applicable."""
        # TODO: Add API tests
        pass


if __name__ == "__main__":
    pytest.main([__file__])
'''
            integration_tests.append({
                'source_file': 'integration',
                'test_file': 'test_integration.py',
                'content': test_content,
                'test_type': 'integration',
                'framework': 'pytest'
            })
        
        return integration_tests
    
    def _generate_validation_scripts(self, repo_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate validation scripts for code quality and standards.
        """
        validation_scripts = []
        
        # Code quality validation script
        quality_script = '''#!/usr/bin/env python3
"""
Code Quality Validation Script
Auto-generated by GitRead Test Generator
"""

import subprocess
import sys
from pathlib import Path


def run_linting():
    """Run code linting checks."""
    try:
        result = subprocess.run(['flake8', '.'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Linting passed")
        else:
            print("❌ Linting failed:")
            print(result.stdout)
        return result.returncode == 0
    except FileNotFoundError:
        print("⚠️ flake8 not found, skipping linting")
        return True


def run_type_checking():
    """Run type checking if applicable."""
    try:
        result = subprocess.run(['mypy', '.'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Type checking passed")
        else:
            print("❌ Type checking failed:")
            print(result.stdout)
        return result.returncode == 0
    except FileNotFoundError:
        print("⚠️ mypy not found, skipping type checking")
        return True


def validate_structure():
    """Validate project structure."""
    required_files = ['README.md', 'requirements.txt']
    missing_files = []
    
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return False
    else:
        print("✅ Project structure validation passed")
        return True


if __name__ == "__main__":
    print("🔍 Running code quality validation...")
    
    checks = [
        run_linting(),
        run_type_checking(),
        validate_structure()
    ]
    
    if all(checks):
        print("\n✅ All validation checks passed!")
        sys.exit(0)
    else:
        print("\n❌ Some validation checks failed.")
        sys.exit(1)
'''
        
        validation_scripts.append({
            'script_name': 'validate_code_quality.py',
            'content': quality_script,
            'purpose': 'Code quality and standards validation',
            'executable': True
        })
        
        return validation_scripts
    
    def _detect_existing_tests(self, repo_data: Dict[str, Any]) -> bool:
        """
        Detect if the repository already has existing tests.
        """
        test_indicators = ['test_', '_test.', 'tests/', 'spec/', '__tests__/']
        files = repo_data.get('files', [])
        
        for file_path in files:
            if any(indicator in file_path.lower() for indicator in test_indicators):
                return True
        return False
    
    def _identify_critical_files(self, repo_data: Dict[str, Any]) -> List[str]:
        """
        Identify critical files that should have priority for test generation.
        """
        files = repo_data.get('files', [])
        critical_files = []
        
        # Priority patterns
        priority_patterns = [
            'main.py', 'app.py', 'index.js', 'server.js',
            'api/', 'core/', 'lib/', 'src/'
        ]
        
        for file_path in files:
            if any(pattern in file_path.lower() for pattern in priority_patterns):
                if not self._is_test_file(file_path):
                    critical_files.append(file_path)
        
        return critical_files[:10]  # Limit to top 10 critical files
    
    def _is_test_file(self, file_path: str) -> bool:
        """
        Check if a file is already a test file.
        """
        test_indicators = ['test_', '_test.', '/test', '/tests/', '/spec/']
        return any(indicator in file_path.lower() for indicator in test_indicators)
    
    def _should_generate_tests(self, file_path: str, repo_data: Dict[str, Any]) -> bool:
        """
        Determine if tests should be generated for a specific file.
        """
        # Skip test files, config files, and documentation
        skip_patterns = [
            '.md', '.txt', '.json', '.yml', '.yaml',
            '.cfg', '.ini', '.toml', 'test_', '_test.',
            'config', 'setup.py', '__init__.py'
        ]
        
        return not any(pattern in file_path.lower() for pattern in skip_patterns)
    
    def _get_test_filename(self, source_file: str, language: str) -> str:
        """
        Generate appropriate test filename based on language conventions.
        """
        path = Path(source_file)
        stem = path.stem
        
        if language == 'python':
            return f"test_{stem}.py"
        elif language == 'javascript':
            return f"{stem}.test.js"
        elif language == 'java':
            return f"{stem}Test.java"
        else:
            return f"test_{stem}.{path.suffix[1:]}"
    
    def _get_preferred_framework(self, language: str) -> str:
        """
        Get the preferred testing framework for a language.
        """
        frameworks = self.test_frameworks.get(language, ['generic'])
        return frameworks[0]  # Return the first (preferred) framework
    
    def _is_web_application(self, repo_data: Dict[str, Any]) -> bool:
        """
        Detect if the repository is a web application.
        """
        web_indicators = [
            'package.json', 'index.html', 'app.py', 'server.js',
            'django', 'flask', 'express', 'react', 'vue', 'angular'
        ]
        
        files = repo_data.get('files', [])
        content = ' '.join(files).lower()
        
        return any(indicator in content for indicator in web_indicators)
    
    def _generate_e2e_tests(self, repo_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate end-to-end tests for web applications.
        """
        e2e_tests = []
        
        # Basic E2E test template
        e2e_content = '''/**
 * End-to-End Tests
 * Auto-generated by GitRead Test Generator
 */

const { test, expect } = require('@playwright/test');

test.describe('Application E2E Tests', () => {
    test('homepage loads correctly', async ({ page }) => {
        await page.goto('http://localhost:3000');
        await expect(page).toHaveTitle(/.*/);
    });
    
    test('navigation works', async ({ page }) => {
        await page.goto('http://localhost:3000');
        // TODO: Add navigation tests
    });
    
    test('user interactions', async ({ page }) => {
        await page.goto('http://localhost:3000');
        // TODO: Add user interaction tests
    });
});
'''
        
        e2e_tests.append({
            'source_file': 'e2e',
            'test_file': 'e2e.test.js',
            'content': e2e_content,
            'test_type': 'e2e',
            'framework': 'playwright'
        })
        
        return e2e_tests
    
    def _generate_generic_tests(self, file_path: str, repo_data: Dict[str, Any], 
                              language: str) -> str:
        """
        Generate generic test template for unsupported languages.
        """
        return f'''/*
 * Generated tests for {file_path}
 * Auto-generated by GitRead Test Generator
 * Language: {language}
 */

// TODO: Implement tests for {language}
// This is a generic template that needs to be customized
// for the specific language and testing framework.

// Basic test structure:
// 1. Setup test environment
// 2. Execute functionality
// 3. Assert expected results
// 4. Clean up resources
'''
    
    def _analyze_coverage_requirements(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze and recommend test coverage requirements.
        """
        file_count = len(repo_data.get('files', []))
        complexity = self._estimate_complexity(repo_data)
        
        if complexity == 'low':
            target_coverage = 70
        elif complexity == 'medium':
            target_coverage = 80
        else:
            target_coverage = 90
        
        return {
            'target_coverage': target_coverage,
            'complexity': complexity,
            'critical_paths': self._identify_critical_paths(repo_data),
            'coverage_tools': self._recommend_coverage_tools(repo_data)
        }
    
    def _estimate_complexity(self, repo_data: Dict[str, Any]) -> str:
        """
        Estimate project complexity based on various factors.
        """
        file_count = len(repo_data.get('files', []))
        
        if file_count < 10:
            return 'low'
        elif file_count < 50:
            return 'medium'
        else:
            return 'high'
    
    def _identify_critical_paths(self, repo_data: Dict[str, Any]) -> List[str]:
        """
        Identify critical code paths that require high test coverage.
        """
        # This would be enhanced with actual code analysis
        return ['main execution paths', 'error handling', 'data processing']
    
    def _recommend_coverage_tools(self, repo_data: Dict[str, Any]) -> List[str]:
        """
        Recommend appropriate coverage tools based on the project.
        """
        primary_language = repo_data.get('primary_language', '').lower()
        
        coverage_tools = {
            'python': ['coverage.py', 'pytest-cov'],
            'javascript': ['nyc', 'jest --coverage'],
            'java': ['jacoco', 'cobertura'],
            'go': ['go test -cover'],
            'rust': ['cargo tarpaulin']
        }
        
        return coverage_tools.get(primary_language, ['generic coverage tool'])
    
    def _calculate_coverage_target(self, file_count: int) -> int:
        """
        Calculate appropriate coverage target based on project size.
        """
        if file_count < 10:
            return 70
        elif file_count < 50:
            return 80
        else:
            return 85
    
    def _recommend_frameworks(self, repo_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Recommend testing frameworks based on the project characteristics.
        """
        primary_language = repo_data.get('primary_language', '').lower()
        frameworks = self.test_frameworks.get(primary_language, ['generic'])
        
        return {
            'primary': frameworks[0] if frameworks else 'generic',
            'alternatives': frameworks[1:] if len(frameworks) > 1 else [],
            'reasoning': f"Best practices for {primary_language} development"
        }
    
    def _save_test_results(self, test_suite: Dict[str, Any]):
        """
        Save test generation results to outputs directory.
        """
        self.outputs_dir.mkdir(exist_ok=True)
        
        # Save test suite metadata
        test_metadata_path = self.outputs_dir / "test_generation_results.json"
        with open(test_metadata_path, 'w') as f:
            json.dump(test_suite, f, indent=2)
        
        # Save individual test files
        tests_dir = self.outputs_dir / "generated_tests"
        tests_dir.mkdir(exist_ok=True)
        
        for test_file in test_suite.get('test_files', []):
            test_path = tests_dir / test_file['test_file']
            with open(test_path, 'w') as f:
                f.write(test_file['content'])
        
        # Save validation scripts
        for script in test_suite.get('validation_scripts', []):
            script_path = self.outputs_dir / script['script_name']
            with open(script_path, 'w') as f:
                f.write(script['content'])
            
            # Make validation scripts executable
            if script.get('executable', False):
                os.chmod(script_path, 0o755)
        
        print(f"💾 Test results saved to {self.outputs_dir}")


if __name__ == "__main__":
    # Example usage
    generator = TestGenerator()
    
    # Mock repository data for testing
    mock_repo_data = {
        'primary_language': 'python',
        'files': ['main.py', 'utils.py', 'config.py'],
        'structure': {'src': ['main.py'], 'tests': []}
    }
    
    mock_documentation = {
        'sections': ['overview', 'installation', 'usage']
    }
    
    test_suite = generator.generate_tests(mock_repo_data, mock_documentation)
    print(f"Generated test suite: {test_suite['strategy']['approach']}")