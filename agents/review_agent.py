#!/usr/bin/env python3
"""
Review Agent

Meta-Prompt: You are a Senior Technical Writer and Code Review Specialist.
Your role is to critically evaluate generated documentation, identify gaps,
ensure quality standards, and manage regeneration feedback loops.

Follows DX best practices:
- Meta-prompting: Explicit reviewer role and quality criteria
- Self-correction: Iterative improvement through feedback loops
- Modular design: Composable review functions for different content types
- Regeneration blocks: Structured handoff for continuous improvement
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime


class ReviewAgent:
    """
    Agent responsible for reviewing, critiquing, and improving generated documentation.
    
    Meta-Prompt Context:
    - Role: Senior Technical Writer with expertise in documentation standards
    - Task: Review documentation quality, completeness, and accuracy
    - Quality: Provide actionable feedback and regeneration recommendations
    - Standards: Follow technical writing best practices and accessibility guidelines
    """
    
    def __init__(self, prompts_dir="prompts", outputs_dir="outputs"):
        self.prompts_dir = Path(prompts_dir)
        self.outputs_dir = Path(outputs_dir)
        self.quality_criteria = {
            'completeness': {
                'weight': 0.3,
                'checks': ['all_sections_present', 'adequate_detail', 'examples_included']
            },
            'accuracy': {
                'weight': 0.25,
                'checks': ['technical_correctness', 'up_to_date_info', 'valid_links']
            },
            'clarity': {
                'weight': 0.25,
                'checks': ['clear_language', 'logical_structure', 'consistent_terminology']
            },
            'usability': {
                'weight': 0.2,
                'checks': ['actionable_instructions', 'proper_formatting', 'accessibility']
            }
        }
        
    def review_documentation(self, documentation: Dict[str, Any], 
                           repo_data: Dict[str, Any],
                           test_results: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Main documentation review pipeline.
        
        Args:
            documentation: Generated documentation to review
            repo_data: Original repository data for context
            test_results: Test generation results for validation
            
        Returns:
            Dict containing review results, scores, and improvement recommendations
        """
        print("📋 Review Agent: Analyzing documentation quality...")
        
        # Perform comprehensive review
        quality_scores = self._assess_quality(documentation, repo_data)
        content_gaps = self._identify_content_gaps(documentation, repo_data)
        technical_issues = self._check_technical_accuracy(documentation, repo_data)
        usability_feedback = self._evaluate_usability(documentation)
        
        # Generate improvement recommendations
        recommendations = self._generate_recommendations(
            quality_scores, content_gaps, technical_issues, usability_feedback
        )
        
        # Create regeneration block for next iteration
        regeneration_block = self._create_regeneration_block(
            documentation, quality_scores, recommendations, test_results
        )
        
        review_results = {
            'review_timestamp': datetime.utcnow().isoformat(),
            'overall_score': self._calculate_overall_score(quality_scores),
            'quality_scores': quality_scores,
            'content_gaps': content_gaps,
            'technical_issues': technical_issues,
            'usability_feedback': usability_feedback,
            'recommendations': recommendations,
            'regeneration_block': regeneration_block,
            'approval_status': self._determine_approval_status(quality_scores)
        }
        
        # Save review results
        self._save_review_results(review_results)
        
        # Update regeneration block file
        self._update_regeneration_block(regeneration_block)
        
        print(f"✅ Review complete. Overall score: {review_results['overall_score']:.1f}/100")
        return review_results
    
    def _assess_quality(self, documentation: Dict[str, Any], 
                       repo_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Unit Prompt: Assess documentation quality across multiple dimensions.
        
        Meta-Context: You are evaluating documentation against professional
        technical writing standards and user experience best practices.
        """
        scores = {}
        
        # Assess completeness
        scores['completeness'] = self._assess_completeness(documentation, repo_data)
        
        # Assess accuracy
        scores['accuracy'] = self._assess_accuracy(documentation, repo_data)
        
        # Assess clarity
        scores['clarity'] = self._assess_clarity(documentation)
        
        # Assess usability
        scores['usability'] = self._assess_usability(documentation)
        
        return scores
    
    def _assess_completeness(self, documentation: Dict[str, Any], 
                           repo_data: Dict[str, Any]) -> float:
        """
        Assess how complete the documentation is relative to the codebase.
        """
        score = 0.0
        max_score = 100.0
        
        # Check for essential sections
        essential_sections = [
            'overview', 'installation', 'usage', 'api', 'examples',
            'contributing', 'license', 'changelog'
        ]
        
        doc_content = str(documentation).lower()
        sections_present = sum(1 for section in essential_sections 
                             if section in doc_content)
        score += (sections_present / len(essential_sections)) * 40
        
        # Check for code examples
        if '```' in str(documentation) or 'example' in doc_content:
            score += 20
        
        # Check for adequate detail (length as proxy)
        total_length = sum(len(str(section)) for section in documentation.values() 
                          if isinstance(section, str))
        if total_length > 1000:
            score += 20
        elif total_length > 500:
            score += 10
        
        # Check for project-specific content
        primary_language = repo_data.get('primary_language', '').lower()
        if primary_language and primary_language in doc_content:
            score += 20
        
        return min(score, max_score)
    
    def _assess_accuracy(self, documentation: Dict[str, Any], 
                        repo_data: Dict[str, Any]) -> float:
        """
        Assess technical accuracy of the documentation.
        """
        score = 80.0  # Start with high score, deduct for issues
        
        # Check for common accuracy issues
        doc_text = str(documentation).lower()
        
        # Check for placeholder text that wasn't replaced
        placeholders = ['todo', 'placeholder', 'example.com', 'your_', 'replace_this']
        placeholder_count = sum(1 for placeholder in placeholders if placeholder in doc_text)
        score -= placeholder_count * 10
        
        # Check for broken markdown syntax
        markdown_issues = self._check_markdown_syntax(str(documentation))
        score -= len(markdown_issues) * 5
        
        # Check for inconsistent terminology
        inconsistencies = self._check_terminology_consistency(documentation)
        score -= len(inconsistencies) * 3
        
        return max(score, 0.0)
    
    def _assess_clarity(self, documentation: Dict[str, Any]) -> float:
        """
        Assess clarity and readability of the documentation.
        """
        score = 0.0
        doc_text = str(documentation)
        
        # Check for clear structure (headers)
        header_count = doc_text.count('#')
        if header_count >= 3:
            score += 25
        elif header_count >= 1:
            score += 15
        
        # Check for proper formatting
        if '```' in doc_text:  # Code blocks
            score += 20
        if '- ' in doc_text or '* ' in doc_text:  # Lists
            score += 15
        if '[' in doc_text and '](' in doc_text:  # Links
            score += 10
        
        # Check for clear language (avoid overly complex sentences)
        sentences = doc_text.split('.')
        avg_sentence_length = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
        if avg_sentence_length < 20:
            score += 20
        elif avg_sentence_length < 30:
            score += 10
        
        # Check for consistent tone
        if self._has_consistent_tone(doc_text):
            score += 10
        
        return min(score, 100.0)
    
    def _assess_usability(self, documentation: Dict[str, Any]) -> float:
        """
        Assess how usable and actionable the documentation is.
        """
        score = 0.0
        doc_text = str(documentation)
        
        # Check for actionable instructions
        action_words = ['install', 'run', 'execute', 'configure', 'setup', 'create']
        action_count = sum(1 for word in action_words if word in doc_text.lower())
        score += min(action_count * 10, 30)
        
        # Check for step-by-step instructions
        if any(pattern in doc_text for pattern in ['1.', '2.', 'step', 'first', 'then']):
            score += 25
        
        # Check for troubleshooting section
        if any(term in doc_text.lower() for term in ['troubleshoot', 'common issues', 'faq']):
            score += 20
        
        # Check for contact/support information
        if any(term in doc_text.lower() for term in ['contact', 'support', 'help', 'issue']):
            score += 15
        
        # Check for accessibility features
        if self._check_accessibility_features(doc_text):
            score += 10
        
        return min(score, 100.0)
    
    def _identify_content_gaps(self, documentation: Dict[str, Any], 
                             repo_data: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Unit Prompt: Identify missing or insufficient content areas.
        
        Meta-Context: You are analyzing documentation completeness against
        industry standards and user needs for this type of project.
        """
        gaps = []
        doc_content = str(documentation).lower()
        
        # Check for missing essential sections
        essential_sections = {
            'installation': ['install', 'setup', 'requirements'],
            'usage': ['usage', 'how to', 'getting started'],
            'api_documentation': ['api', 'methods', 'functions'],
            'examples': ['example', 'demo', 'sample'],
            'contributing': ['contribut', 'development', 'pull request'],
            'license': ['license', 'copyright'],
            'changelog': ['changelog', 'version', 'release']
        }
        
        for section, keywords in essential_sections.items():
            if not any(keyword in doc_content for keyword in keywords):
                gaps.append({
                    'type': 'missing_section',
                    'section': section,
                    'severity': 'high' if section in ['installation', 'usage'] else 'medium',
                    'description': f"Missing {section.replace('_', ' ')} section"
                })
        
        # Check for language-specific gaps
        primary_language = repo_data.get('primary_language', '').lower()
        if primary_language:
            language_gaps = self._check_language_specific_gaps(doc_content, primary_language)
            gaps.extend(language_gaps)
        
        # Check for project-type specific gaps
        project_type = self._infer_project_type(repo_data)
        type_gaps = self._check_project_type_gaps(doc_content, project_type)
        gaps.extend(type_gaps)
        
        return gaps
    
    def _check_technical_accuracy(self, documentation: Dict[str, Any], 
                                repo_data: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Check for technical accuracy issues in the documentation.
        """
        issues = []
        doc_text = str(documentation)
        
        # Check for markdown syntax issues
        markdown_issues = self._check_markdown_syntax(doc_text)
        issues.extend(markdown_issues)
        
        # Check for broken or placeholder links
        link_issues = self._check_links(doc_text)
        issues.extend(link_issues)
        
        # Check for inconsistent code examples
        code_issues = self._check_code_examples(doc_text, repo_data)
        issues.extend(code_issues)
        
        return issues
    
    def _evaluate_usability(self, documentation: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate documentation from a user experience perspective.
        """
        doc_text = str(documentation)
        
        return {
            'navigation': self._assess_navigation(doc_text),
            'readability': self._assess_readability(doc_text),
            'actionability': self._assess_actionability(doc_text),
            'accessibility': self._assess_accessibility(doc_text)
        }
    
    def _generate_recommendations(self, quality_scores: Dict[str, float],
                                content_gaps: List[Dict[str, str]],
                                technical_issues: List[Dict[str, str]],
                                usability_feedback: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Unit Prompt: Generate specific, actionable improvement recommendations.
        
        Meta-Context: You are providing expert guidance to improve documentation
        quality based on identified issues and industry best practices.
        """
        recommendations = []
        
        # Recommendations based on quality scores
        for criterion, score in quality_scores.items():
            if score < 70:
                recommendations.append({
                    'category': 'quality_improvement',
                    'priority': 'high',
                    'criterion': criterion,
                    'recommendation': self._get_quality_recommendation(criterion, score),
                    'impact': 'Improves overall documentation quality'
                })
        
        # Recommendations based on content gaps
        for gap in content_gaps:
            if gap['severity'] == 'high':
                recommendations.append({
                    'category': 'content_addition',
                    'priority': 'high',
                    'section': gap['section'],
                    'recommendation': f"Add comprehensive {gap['section'].replace('_', ' ')} section",
                    'impact': 'Essential for user onboarding and adoption'
                })
        
        # Recommendations based on technical issues
        if technical_issues:
            recommendations.append({
                'category': 'technical_fixes',
                'priority': 'medium',
                'recommendation': f"Fix {len(technical_issues)} technical issues including markdown syntax and links",
                'impact': 'Improves documentation reliability and professionalism'
            })
        
        # Recommendations based on usability feedback
        for aspect, feedback in usability_feedback.items():
            if isinstance(feedback, dict) and feedback.get('score', 100) < 70:
                recommendations.append({
                    'category': 'usability_improvement',
                    'priority': 'medium',
                    'aspect': aspect,
                    'recommendation': feedback.get('recommendation', f"Improve {aspect}"),
                    'impact': 'Enhances user experience and adoption'
                })
        
        return recommendations
    
    def _create_regeneration_block(self, documentation: Dict[str, Any],
                                 quality_scores: Dict[str, float],
                                 recommendations: List[Dict[str, str]],
                                 test_results: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Unit Prompt: Create structured regeneration block for next iteration.
        
        Meta-Context: You are creating a handoff document that enables
        continuous improvement and tracks progress across iterations.
        """
        overall_score = self._calculate_overall_score(quality_scores)
        
        regeneration_block = {
            'phase': 'GitRead v2 - Documentation Review Complete',
            'timestamp': datetime.utcnow().isoformat(),
            'overall_quality_score': overall_score,
            'changes_this_pass': [
                'Comprehensive documentation review completed',
                'Quality assessment across 4 dimensions performed',
                'Content gaps and technical issues identified',
                'Actionable improvement recommendations generated'
            ],
            'quality_breakdown': quality_scores,
            'critical_issues': [
                rec['recommendation'] for rec in recommendations 
                if rec.get('priority') == 'high'
            ],
            'errors_or_todos': [
                'Address high-priority content gaps',
                'Fix technical accuracy issues',
                'Implement usability improvements'
            ],
            'recommended_next_steps': [
                'Implement high-priority recommendations',
                'Re-run documentation generation with improvements',
                'Conduct user testing of documentation',
                'Set up automated quality checks'
            ],
            'inputs_used': [
                'Generated documentation',
                'Repository analysis data',
                'Quality assessment criteria',
                'Technical writing best practices'
            ],
            'outputs_generated': [
                'Quality scores and breakdown',
                'Content gap analysis',
                'Technical issue report',
                'Improvement recommendations',
                'Regeneration block for next iteration'
            ],
            'metrics': {
                'total_recommendations': len(recommendations),
                'high_priority_issues': len([r for r in recommendations if r.get('priority') == 'high']),
                'review_completion_time': datetime.utcnow().isoformat()
            }
        }
        
        # Add test results if available
        if test_results:
            regeneration_block['test_integration'] = {
                'tests_generated': len(test_results.get('test_files', [])),
                'test_strategy': test_results.get('strategy', {}).get('approach', 'unknown'),
                'coverage_target': test_results.get('coverage_requirements', {}).get('target_coverage', 'unknown')
            }
        
        return regeneration_block
    
    def _calculate_overall_score(self, quality_scores: Dict[str, float]) -> float:
        """
        Calculate weighted overall quality score.
        """
        total_score = 0.0
        total_weight = 0.0
        
        for criterion, score in quality_scores.items():
            weight = self.quality_criteria.get(criterion, {}).get('weight', 0.25)
            total_score += score * weight
            total_weight += weight
        
        return total_score / total_weight if total_weight > 0 else 0.0
    
    def _determine_approval_status(self, quality_scores: Dict[str, float]) -> str:
        """
        Determine if documentation meets approval criteria.
        """
        overall_score = self._calculate_overall_score(quality_scores)
        
        if overall_score >= 85:
            return 'approved'
        elif overall_score >= 70:
            return 'approved_with_recommendations'
        else:
            return 'requires_revision'
    
    # Helper methods for specific checks
    
    def _check_markdown_syntax(self, text: str) -> List[Dict[str, str]]:
        """Check for common markdown syntax issues."""
        issues = []
        
        # Check for unmatched code blocks
        code_block_count = text.count('```')
        if code_block_count % 2 != 0:
            issues.append({
                'type': 'markdown_syntax',
                'severity': 'medium',
                'description': 'Unmatched code block markers (```)',
                'recommendation': 'Ensure all code blocks are properly closed'
            })
        
        # Check for malformed links
        import re
        malformed_links = re.findall(r'\[([^\]]+)\]\([^\)]*\s[^\)]*\)', text)
        if malformed_links:
            issues.append({
                'type': 'markdown_syntax',
                'severity': 'low',
                'description': f'Found {len(malformed_links)} potentially malformed links',
                'recommendation': 'Check link syntax for spaces in URLs'
            })
        
        return issues
    
    def _check_links(self, text: str) -> List[Dict[str, str]]:
        """Check for broken or placeholder links."""
        issues = []
        
        # Check for placeholder links
        placeholder_patterns = ['example.com', 'your-repo', 'your-username', 'placeholder']
        for pattern in placeholder_patterns:
            if pattern in text.lower():
                issues.append({
                    'type': 'placeholder_link',
                    'severity': 'high',
                    'description': f'Found placeholder link containing "{pattern}"',
                    'recommendation': 'Replace placeholder links with actual URLs'
                })
        
        return issues
    
    def _check_code_examples(self, text: str, repo_data: Dict[str, Any]) -> List[Dict[str, str]]:
        """Check code examples for consistency and accuracy."""
        issues = []
        
        # Check if code examples match the primary language
        primary_language = repo_data.get('primary_language', '').lower()
        if primary_language and '```' in text:
            # This is a simplified check - could be enhanced with actual parsing
            if f'```{primary_language}' not in text and primary_language != 'unknown':
                issues.append({
                    'type': 'code_example',
                    'severity': 'medium',
                    'description': f'Code examples may not match primary language ({primary_language})',
                    'recommendation': f'Ensure code examples are in {primary_language} or specify language'
                })
        
        return issues
    
    def _check_terminology_consistency(self, documentation: Dict[str, Any]) -> List[str]:
        """Check for inconsistent terminology usage."""
        # This is a simplified implementation
        # In practice, this would use NLP techniques for better analysis
        return []  # Placeholder for now
    
    def _has_consistent_tone(self, text: str) -> bool:
        """Check if the documentation has a consistent tone."""
        # Simplified check for consistent tone
        # Look for mix of formal/informal language
        formal_indicators = ['utilize', 'implement', 'configure', 'execute']
        informal_indicators = ['use', 'do', 'setup', 'run']
        
        formal_count = sum(1 for word in formal_indicators if word in text.lower())
        informal_count = sum(1 for word in informal_indicators if word in text.lower())
        
        # If there's a significant imbalance, tone might be inconsistent
        total = formal_count + informal_count
        if total > 0:
            ratio = abs(formal_count - informal_count) / total
            return ratio < 0.8  # Allow some variation
        
        return True
    
    def _check_accessibility_features(self, text: str) -> bool:
        """Check for accessibility features in documentation."""
        accessibility_indicators = [
            'alt text', 'screen reader', 'accessibility', 'a11y',
            'keyboard navigation', 'contrast', 'aria-label'
        ]
        return any(indicator in text.lower() for indicator in accessibility_indicators)
    
    def _check_language_specific_gaps(self, doc_content: str, language: str) -> List[Dict[str, str]]:
        """Check for language-specific documentation gaps."""
        gaps = []
        
        language_requirements = {
            'python': ['requirements.txt', 'pip install', 'virtual environment'],
            'javascript': ['package.json', 'npm install', 'node_modules'],
            'java': ['maven', 'gradle', 'classpath'],
            'go': ['go mod', 'go get', 'go build'],
            'rust': ['cargo', 'crates.io', 'cargo.toml']
        }
        
        requirements = language_requirements.get(language, [])
        for requirement in requirements:
            if requirement not in doc_content:
                gaps.append({
                    'type': 'language_specific',
                    'section': f'{language}_requirements',
                    'severity': 'medium',
                    'description': f'Missing {language}-specific information about {requirement}'
                })
        
        return gaps
    
    def _infer_project_type(self, repo_data: Dict[str, Any]) -> str:
        """Infer project type from repository data."""
        files = repo_data.get('files', [])
        file_content = ' '.join(files).lower()
        
        if any(indicator in file_content for indicator in ['package.json', 'index.html', 'app.js']):
            return 'web_application'
        elif any(indicator in file_content for indicator in ['setup.py', '__init__.py', 'requirements.txt']):
            return 'python_library'
        elif any(indicator in file_content for indicator in ['pom.xml', 'build.gradle']):
            return 'java_application'
        elif 'cargo.toml' in file_content:
            return 'rust_project'
        else:
            return 'general'
    
    def _check_project_type_gaps(self, doc_content: str, project_type: str) -> List[Dict[str, str]]:
        """Check for project-type specific documentation gaps."""
        gaps = []
        
        type_requirements = {
            'web_application': ['deployment', 'environment variables', 'browser support'],
            'python_library': ['pypi', 'packaging', 'testing'],
            'java_application': ['build instructions', 'dependencies', 'jvm requirements'],
            'rust_project': ['cargo commands', 'rust version', 'compilation']
        }
        
        requirements = type_requirements.get(project_type, [])
        for requirement in requirements:
            if requirement not in doc_content:
                gaps.append({
                    'type': 'project_type_specific',
                    'section': f'{project_type}_{requirement}',
                    'severity': 'medium',
                    'description': f'Missing {project_type} information about {requirement}'
                })
        
        return gaps
    
    def _assess_navigation(self, text: str) -> Dict[str, Any]:
        """Assess navigation and structure of documentation."""
        header_count = text.count('#')
        toc_present = 'table of contents' in text.lower() or 'toc' in text.lower()
        
        score = 0
        if header_count >= 3:
            score += 50
        if toc_present:
            score += 30
        if '[' in text and '](' in text:  # Internal links
            score += 20
        
        return {
            'score': min(score, 100),
            'headers_count': header_count,
            'toc_present': toc_present,
            'recommendation': 'Add table of contents and more section headers' if score < 70 else 'Good navigation structure'
        }
    
    def _assess_readability(self, text: str) -> Dict[str, Any]:
        """Assess readability of the documentation."""
        sentences = text.split('.')
        words = text.split()
        
        avg_sentence_length = len(words) / max(len(sentences), 1)
        
        score = 100
        if avg_sentence_length > 25:
            score -= 30
        elif avg_sentence_length > 20:
            score -= 15
        
        return {
            'score': max(score, 0),
            'avg_sentence_length': avg_sentence_length,
            'recommendation': 'Break down long sentences for better readability' if score < 70 else 'Good readability'
        }
    
    def _assess_actionability(self, text: str) -> Dict[str, Any]:
        """Assess how actionable the documentation is."""
        action_words = ['install', 'run', 'execute', 'configure', 'setup', 'create', 'build']
        action_count = sum(1 for word in action_words if word in text.lower())
        
        score = min(action_count * 15, 100)
        
        return {
            'score': score,
            'action_words_count': action_count,
            'recommendation': 'Add more actionable instructions and commands' if score < 70 else 'Good actionability'
        }
    
    def _assess_accessibility(self, text: str) -> Dict[str, Any]:
        """Assess accessibility features of the documentation."""
        accessibility_features = self._check_accessibility_features(text)
        
        score = 80 if accessibility_features else 60  # Base score
        
        return {
            'score': score,
            'features_present': accessibility_features,
            'recommendation': 'Consider adding accessibility guidelines' if not accessibility_features else 'Accessibility considerations present'
        }
    
    def _get_quality_recommendation(self, criterion: str, score: float) -> str:
        """Get specific recommendation based on quality criterion and score."""
        recommendations = {
            'completeness': {
                'low': 'Add missing essential sections (installation, usage, examples)',
                'medium': 'Expand existing sections with more detail and examples',
                'high': 'Fine-tune content depth and add advanced topics'
            },
            'accuracy': {
                'low': 'Fix technical errors, broken links, and placeholder content',
                'medium': 'Review and update technical details for accuracy',
                'high': 'Verify all technical information is current and correct'
            },
            'clarity': {
                'low': 'Improve structure, add headers, and simplify language',
                'medium': 'Enhance formatting and logical flow',
                'high': 'Polish language and ensure consistent terminology'
            },
            'usability': {
                'low': 'Add step-by-step instructions and troubleshooting',
                'medium': 'Improve actionability and user guidance',
                'high': 'Enhance user experience with better organization'
            }
        }
        
        if score < 50:
            level = 'low'
        elif score < 75:
            level = 'medium'
        else:
            level = 'high'
        
        return recommendations.get(criterion, {}).get(level, f'Improve {criterion}')
    
    def _save_review_results(self, review_results: Dict[str, Any]):
        """Save review results to outputs directory."""
        self.outputs_dir.mkdir(exist_ok=True)
        
        review_path = self.outputs_dir / "documentation_review.json"
        with open(review_path, 'w') as f:
            json.dump(review_results, f, indent=2)
        
        print(f"💾 Review results saved to {review_path}")
    
    def _update_regeneration_block(self, regeneration_block: Dict[str, Any]):
        """Update the regeneration block file."""
        self.outputs_dir.mkdir(exist_ok=True)
        
        regen_path = self.outputs_dir / "regeneration_block.md"
        
        # Format regeneration block as markdown
        markdown_content = self._format_regeneration_block_markdown(regeneration_block)
        
        with open(regen_path, 'w') as f:
            f.write(markdown_content)
        
        print(f"📝 Regeneration block updated: {regen_path}")
    
    def _format_regeneration_block_markdown(self, block: Dict[str, Any]) -> str:
        """Format regeneration block as markdown."""
        markdown = f"""# GitRead Regeneration Block

**Phase:** {block['phase']}  
**Timestamp:** {block['timestamp']}  
**Overall Quality Score:** {block['overall_quality_score']:.1f}/100

## Changes This Pass

{chr(10).join(f'- {change}' for change in block['changes_this_pass'])}

## Quality Breakdown

{chr(10).join(f'- **{criterion.title()}:** {score:.1f}/100' for criterion, score in block['quality_breakdown'].items())}

## Critical Issues

{chr(10).join(f'- {issue}' for issue in block['critical_issues']) if block['critical_issues'] else '- No critical issues identified'}

## Errors or TODOs

{chr(10).join(f'- {todo}' for todo in block['errors_or_todos'])}

## Recommended Next Steps

{chr(10).join(f'1. {step}' for step in block['recommended_next_steps'])}

## Inputs Used

{chr(10).join(f'- {input_item}' for input_item in block['inputs_used'])}

## Outputs Generated

{chr(10).join(f'- {output}' for output in block['outputs_generated'])}

## Metrics

{chr(10).join(f'- **{metric.replace("_", " ").title()}:** {value}' for metric, value in block['metrics'].items())}
"""
        
        # Add test integration if available
        if 'test_integration' in block:
            test_info = block['test_integration']
            markdown += f"""\n## Test Integration

- **Tests Generated:** {test_info['tests_generated']}
- **Test Strategy:** {test_info['test_strategy']}
- **Coverage Target:** {test_info['coverage_target']}%
"""
        
        markdown += "\n---\n\n*Generated by GitRead Review Agent*\n"
        
        return markdown


if __name__ == "__main__":
    # Example usage
    reviewer = ReviewAgent()
    
    # Mock documentation for testing
    mock_documentation = {
        'overview': 'This is a sample project overview.',
        'installation': 'Run pip install to install dependencies.',
        'usage': 'Use the main.py script to run the application.'
    }
    
    mock_repo_data = {
        'primary_language': 'python',
        'files': ['main.py', 'requirements.txt', 'README.md']
    }
    
    review_results = reviewer.review_documentation(mock_documentation, mock_repo_data)
    print(f"Review completed with overall score: {review_results['overall_score']:.1f}")