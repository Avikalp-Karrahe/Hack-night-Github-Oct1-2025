#!/usr/bin/env python3
"""
Document Planner Agent

Generates structured outlines for project documentation using meta-prompting.
This is the first step in the prompt chaining process.
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional


class DocPlanner:
    """Agent responsible for generating documentation outlines."""
    
    def __init__(self, prompts_dir="prompts"):
        self.prompts_dir = Path(prompts_dir)
        self.prompts_dir.mkdir(exist_ok=True)
        
        # Standard documentation sections
        self.standard_sections = [
            "Project Overview",
            "Features",
            "Technology Stack",
            "Installation",
            "Configuration",
            "Usage",
            "API Documentation",
            "Project Structure",
            "Development",
            "Testing",
            "Deployment",
            "Contributing",
            "License"
        ]
        
        # Initialize prompt templates
        self._create_prompt_templates()
    
    def generate_outline(self, repo_data: Dict[str, Any], ai_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a structured outline for the project documentation.
        
        Args:
            repo_data (Dict[str, Any]): Parsed repository data
            ai_context (Dict[str, Any]): AI learning context and past docs
            
        Returns:
            Dict[str, Any]: Generated outline with sections and priorities
        """
        print("📋 Generating documentation outline...")
        
        # Analyze repository to determine relevant sections
        relevant_sections = self._analyze_relevant_sections(repo_data)
        
        # Create outline structure
        outline = {
            'project_name': repo_data.get('name', 'Unknown Project'),
            'sections': relevant_sections,
            'metadata': {
                'generated_from': repo_data.get('path'),
                'primary_language': self._get_primary_language(repo_data),
                'project_type': self._detect_project_type(repo_data),
                'complexity': self._assess_complexity(repo_data)
            },
            'prompts': self._generate_section_prompts(relevant_sections, repo_data, ai_context)
        }
        
        # Save outline for reference
        self._save_outline(outline)
        
        print(f"✅ Generated outline with {len(relevant_sections)} sections")
        return outline
    
    def _analyze_relevant_sections(self, repo_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Analyze repository data to determine which sections are relevant.
        
        Args:
            repo_data (Dict[str, Any]): Parsed repository data
            
        Returns:
            List[Dict[str, Any]]: List of relevant sections with metadata
        """
        sections = []
        
        # Always include basic sections with enhanced structure
        sections.append({
            'title': 'Project Summary & Goals',
            'priority': 'high',
            'required': True,
            'description': 'Comprehensive project overview including goals, target audience, and primary objectives',
            'subsections': ['Overview', 'Primary Goals', 'Target Audience', 'Success Metrics']
        })
        
        # Enhanced Features section
        sections.append({
            'title': 'Key Features & Use Cases',
            'priority': 'high',
            'required': True,
            'description': 'Detailed feature breakdown with use cases and examples',
            'subsections': ['Core Features', 'Use Cases', 'Feature Highlights', 'Capabilities Matrix']
        })
        
        # Enhanced Technology stack
        if repo_data.get('languages') or repo_data.get('dependencies'):
            sections.append({
                'title': 'Technology Stack',
                'priority': 'high',
                'required': True,
                'description': 'Comprehensive breakdown of technologies, frameworks, libraries, and tools',
                'subsections': ['Frontend Framework', '3D Graphics & Animation', 'Development Tools', 'File Breakdown', 'Architecture Overview']
            })
        
        # Enhanced Setup Instructions section
        sections.append({
            'title': 'Setup Instructions',
            'priority': 'high',
            'required': True,
            'description': 'Comprehensive installation and setup guide with prerequisites and troubleshooting',
            'subsections': ['Prerequisites', 'System Requirements', 'Step-by-Step Installation', 'Verification', 'Troubleshooting Installation']
        })
        
        # Enhanced Configuration section
        sections.append({
            'title': 'Configuration Required',
            'priority': 'high',
            'required': True,
            'description': 'Detailed configuration setup including environment variables and framework configurations',
            'subsections': ['Environment Variables', 'TypeScript Configuration', 'Build Configuration', 'Development Settings']
        })
        
        # Usage section
        sections.append({
            'title': 'Usage',
            'priority': 'high',
            'required': True,
            'description': 'How to use the project with examples'
        })
        
        # API Documentation for web services
        if self._is_api_project(repo_data):
            sections.append({
                'title': 'API Documentation',
                'priority': 'high',
                'required': True,
                'description': 'API endpoints, request/response formats'
            })
        
        # Enhanced Project Structure section
        sections.append({
            'title': 'Project Structure',
            'priority': 'high',
            'required': True,
            'description': 'Detailed directory structure with descriptions and file organization',
            'subsections': ['Directory Tree', 'Directory Descriptions', 'Key Files', 'Asset Organization']
        })
        
        # Major Components & Modules section
        sections.append({
            'title': 'Major Components & Modules',
            'priority': 'high',
            'required': True,
            'description': 'Detailed breakdown of core application components and their responsibilities',
            'subsections': ['Core Application Components', 'Data Management', 'Architecture Patterns', 'Module Dependencies']
        })
        
        # Execution Plan section
        sections.append({
            'title': 'Execution Plan',
            'priority': 'medium',
            'required': True,
            'description': 'Step-by-step execution workflow and operational procedures',
            'subsections': ['Development Workflow', 'Build Process', 'Testing Strategy', 'Deployment Pipeline']
        })
        
        # Enhanced Development section
        sections.append({
            'title': 'Development Workflow',
            'priority': 'medium',
            'required': True,
            'description': 'Comprehensive development guidelines and best practices',
            'subsections': ['Development Environment', 'Code Standards', 'Git Workflow', 'Review Process']
        })
        
        # Enhanced Testing section
        sections.append({
            'title': 'Testing Strategy',
            'priority': 'medium',
            'required': True,
            'description': 'Comprehensive testing approach including unit, integration, and end-to-end testing',
            'subsections': ['Testing Framework', 'Test Types', 'Running Tests', 'Coverage Reports', 'CI/CD Integration']
        })
        
        # Deployment Checklist section
        sections.append({
            'title': 'Deployment Checklist',
            'priority': 'medium',
            'required': True,
            'description': 'Complete deployment guide with pre-deployment checks and post-deployment verification',
            'subsections': ['Pre-deployment Checks', 'Deployment Steps', 'Environment Configuration', 'Monitoring Setup', 'Rollback Procedures']
        })
        
        # Troubleshooting & Tips section
        sections.append({
            'title': 'Troubleshooting & Tips',
            'priority': 'medium',
            'required': True,
            'description': 'Common issues, solutions, and best practices for development and deployment',
            'subsections': ['Common Issues', 'Development Tips', 'Performance Tips', 'Debugging Guide', 'FAQ']
        })
        
        # Performance Optimization section
        sections.append({
            'title': 'Performance Optimization',
            'priority': 'medium',
            'required': True,
            'description': 'Performance optimization strategies and monitoring techniques',
            'subsections': ['Optimization Strategies', 'Monitoring Tools', 'Benchmarking', 'Caching Strategies', 'Resource Management']
        })
        
        # Contributing Guidelines section
        sections.append({
            'title': 'Contributing Guidelines',
            'priority': 'low',
            'required': True,
            'description': 'Guidelines for contributing to the project including code standards and review process',
            'subsections': ['Getting Started', 'Code Standards', 'Pull Request Process', 'Issue Reporting', 'Community Guidelines']
        })
        
        # License section if license exists
        if repo_data.get('license'):
            sections.append({
                'title': 'License',
                'priority': 'low',
                'required': False,
                'description': 'License information and terms'
            })
        
        return sections
    
    def _has_features_info(self, repo_data: Dict[str, Any]) -> bool:
        """Check if repository has feature information."""
        readme = repo_data.get('readme', {})
        if readme.get('sections'):
            for section in readme['sections']:
                title = section.get('title', '').lower()
                if any(keyword in title for keyword in ['feature', 'capability', 'function']):
                    return True
        return False
    
    def _has_installation_info(self, repo_data: Dict[str, Any]) -> bool:
        """Check if repository has installation information."""
        # Has dependency files
        if repo_data.get('dependencies'):
            return True
        
        # Has installation info in README
        readme = repo_data.get('readme', {})
        if readme.get('sections'):
            for section in readme['sections']:
                title = section.get('title', '').lower()
                if any(keyword in title for keyword in ['install', 'setup', 'getting started']):
                    return True
        
        return False
    
    def _is_api_project(self, repo_data: Dict[str, Any]) -> bool:
        """Detect if this is an API/web service project."""
        # Check for web frameworks in dependencies
        dependencies = repo_data.get('dependencies', {})
        
        web_frameworks = {
            'python': ['flask', 'django', 'fastapi', 'tornado', 'pyramid'],
            'node': ['express', 'koa', 'hapi', 'nestjs', 'fastify'],
            'java': ['spring', 'jersey', 'dropwizard'],
            'go': ['gin', 'echo', 'fiber', 'gorilla'],
            'rust': ['actix', 'warp', 'rocket']
        }
        
        for lang, frameworks in web_frameworks.items():
            if lang in dependencies:
                for dep_file, deps in dependencies[lang].items():
                    if isinstance(deps, dict) and 'dependencies' in deps:
                        deps_dict = deps['dependencies']
                        if isinstance(deps_dict, dict):
                            dep_names = list(deps_dict.keys())
                        else:
                            dep_names = []
                    elif isinstance(deps, list):
                        dep_names = deps
                    else:
                        continue
                    
                    for framework in frameworks:
                        if any(framework in dep.lower() for dep in dep_names):
                            return True
        
        # Check for API-related files
        api_indicators = ['api/', 'routes/', 'controllers/', 'endpoints/']
        structure = repo_data.get('structure', {})
        directories = structure.get('directories', [])
        
        return any(indicator.rstrip('/') in directories for indicator in api_indicators)
    
    def _is_complex_project(self, repo_data: Dict[str, Any]) -> bool:
        """Determine if project is complex enough to warrant structure documentation."""
        stats = repo_data.get('statistics', {})
        structure = repo_data.get('structure', {})
        
        # Complex if many files or deep directory structure
        return (
            stats.get('total_files', 0) > 20 or
            structure.get('max_depth', 0) > 3 or
            len(structure.get('directories', [])) > 5
        )
    
    def _has_dev_setup(self, repo_data: Dict[str, Any]) -> bool:
        """Check if project has development setup information."""
        # Has CI/CD files
        if repo_data.get('ci_cd'):
            return True
        
        # Has development dependencies
        dependencies = repo_data.get('dependencies', {})
        for lang_deps in dependencies.values():
            for dep_file, deps in lang_deps.items():
                if isinstance(deps, dict) and 'dev_dependencies' in deps:
                    if deps['dev_dependencies']:
                        return True
        
        # Has development-related files
        dev_files = ['Makefile', 'docker-compose.yml', '.env.example']
        config_files = repo_data.get('config_files', [])
        return any(dev_file in config_files for dev_file in dev_files)
    
    def _is_deployable_project(self, repo_data: Dict[str, Any]) -> bool:
        """Check if project appears to be deployable."""
        # Has Docker files
        config_files = repo_data.get('config_files', [])
        if any('docker' in f.lower() for f in config_files):
            return True
        
        # Has deployment-related dependencies or scripts
        dependencies = repo_data.get('dependencies', {})
        for lang_deps in dependencies.values():
            for dep_file, deps in lang_deps.items():
                if isinstance(deps, dict) and 'scripts' in deps:
                    scripts = deps['scripts']
                    if any(keyword in script for script in scripts.keys() 
                          for keyword in ['deploy', 'build', 'start', 'serve']):
                        return True
        
        return False
    
    def _get_primary_language(self, repo_data: Dict[str, Any]) -> str:
        """Get the primary programming language."""
        languages = repo_data.get('languages', {})
        if languages:
            return max(languages.keys(), key=lambda k: languages[k])
        return 'unknown'
    
    def _detect_project_type(self, repo_data: Dict[str, Any]) -> str:
        """Detect the type of project."""
        if self._is_api_project(repo_data):
            return 'web_api'
        
        languages = repo_data.get('languages', {})
        primary_lang = self._get_primary_language(repo_data)
        
        # Check for specific project types
        if 'html' in languages or 'css' in languages:
            return 'web_frontend'
        
        if primary_lang in ['python', 'java', 'go', 'rust', 'cpp']:
            return 'application'
        
        if primary_lang in ['javascript', 'typescript']:
            dependencies = repo_data.get('dependencies', {}).get('node', {})
            if any('react' in str(deps) or 'vue' in str(deps) or 'angular' in str(deps) 
                  for deps in dependencies.values()):
                return 'web_frontend'
            return 'application'
        
        return 'library'
    
    def _assess_complexity(self, repo_data: Dict[str, Any]) -> str:
        """Assess project complexity."""
        stats = repo_data.get('statistics', {})
        total_files = stats.get('total_files', 0)
        code_files = stats.get('code_files', 0)
        
        if total_files < 10 and code_files < 5:
            return 'simple'
        elif total_files < 50 and code_files < 20:
            return 'medium'
        else:
            return 'complex'
    
    def _generate_section_prompts(self, sections: List[Dict[str, Any]], 
                                repo_data: Dict[str, Any], 
                                ai_context: Dict[str, Any]) -> Dict[str, str]:
        """
        Generate specific prompts for each section.
        
        Args:
            sections: List of sections to generate
            repo_data: Repository data
            ai_context: AI learning context
            
        Returns:
            Dict mapping section titles to their prompts
        """
        prompts = {}
        
        # Load meta-prompt template
        meta_prompt = self._load_meta_prompt()
        
        for section in sections:
            title = section['title']
            prompts[title] = self._create_section_prompt(
                title, section, repo_data, ai_context, meta_prompt
            )
        
        return prompts
    
    def _create_section_prompt(self, title: str, section: Dict[str, Any], 
                             repo_data: Dict[str, Any], ai_context: Dict[str, Any],
                             meta_prompt: str) -> str:
        """
        Create a specific prompt for a documentation section.
        
        Args:
            title: Section title
            section: Section metadata
            repo_data: Repository data
            ai_context: AI learning context
            meta_prompt: Base meta-prompt template
            
        Returns:
            Formatted prompt for the section
        """
        # Base context
        context = f"""
Project: {repo_data.get('name', 'Unknown')}
Primary Language: {self._get_primary_language(repo_data)}
Project Type: {self._detect_project_type(repo_data)}
Complexity: {self._assess_complexity(repo_data)}
"""
        
        # Section-specific instructions
        section_instructions = self._get_section_instructions(title, repo_data)
        
        # Combine into full prompt
        prompt = f"""{meta_prompt}

## Context
{context}

## Section to Generate: {title}
{section['description']}

## Specific Instructions
{section_instructions}

## Repository Data
{self._format_repo_data_for_prompt(repo_data, title)}

## Output Requirements
- Write in clear, professional markdown
- Include code examples where appropriate
- Be concise but comprehensive
- Follow technical writing best practices
"""
        
        return prompt
    
    def _get_section_instructions(self, title: str, repo_data: Dict[str, Any]) -> str:
        """
        Get specific instructions for each section type.
        
        Args:
            title: Section title
            repo_data: Repository data
            
        Returns:
            Section-specific instructions
        """
        instructions = {
            'Project Overview': """
- Provide a clear, concise description of what the project does
- Explain the problem it solves or need it addresses
- Mention target audience or use cases
- Keep it under 3 paragraphs""",
            
            'Features': """
- List key features and capabilities
- Use bullet points for clarity
- Focus on user-facing functionality
- Highlight unique or standout features""",
            
            'Technology Stack': """
- List programming languages, frameworks, and major dependencies
- Organize by category (backend, frontend, database, etc.)
- Include version information where relevant
- Explain why key technologies were chosen""",
            
            'Installation': """
- Provide step-by-step installation instructions
- Include prerequisites and system requirements
- Cover different installation methods if applicable
- Include verification steps""",
            
            'Configuration': """
- Document environment variables and configuration options
- Provide example configuration files
- Explain required vs optional settings
- Include security considerations""",
            
            'Usage': """
- Provide basic usage examples
- Include code snippets and command-line examples
- Cover common use cases
- Show expected output where helpful""",
            
            'API Documentation': """
- Document all endpoints with HTTP methods
- Include request/response examples
- Document authentication requirements
- Provide error codes and handling""",
            
            'Project Structure': """
- Explain directory organization
- Describe purpose of key files and folders
- Use tree structure visualization
- Highlight important entry points""",
            
            'Development': """
- Explain development setup process
- Document build and run procedures
- Include debugging and testing workflows
- Provide contribution guidelines""",
            
            'Testing': """
- Explain how to run tests
- Document test structure and organization
- Include coverage information if available
- Provide guidelines for writing new tests""",
            
            'Deployment': """
- Provide deployment instructions for different environments
- Include Docker/containerization if applicable
- Document environment-specific configurations
- Include monitoring and maintenance notes""",
            
            'License': """
- State the license type clearly
- Include any usage restrictions or requirements
- Provide link to full license text
- Mention third-party license considerations"""
        }
        
        return instructions.get(title, "Generate comprehensive documentation for this section.")
    
    def _format_repo_data_for_prompt(self, repo_data: Dict[str, Any], section_title: str) -> str:
        """
        Format repository data relevant to the specific section.
        
        Args:
            repo_data: Repository data
            section_title: Current section being generated
            
        Returns:
            Formatted repository data string
        """
        # Select relevant data based on section
        relevant_data = {}
        
        if section_title in ['Project Overview', 'Features']:
            relevant_data['readme'] = repo_data.get('readme', {})
            relevant_data['languages'] = repo_data.get('languages', {})
        
        elif section_title == 'Technology Stack':
            relevant_data['languages'] = repo_data.get('languages', {})
            relevant_data['dependencies'] = repo_data.get('dependencies', {})
        
        elif section_title == 'Installation':
            relevant_data['dependencies'] = repo_data.get('dependencies', {})
            relevant_data['readme'] = repo_data.get('readme', {})
        
        elif section_title == 'Configuration':
            relevant_data['config_files'] = repo_data.get('config_files', [])
        
        elif section_title == 'Project Structure':
            relevant_data['structure'] = repo_data.get('structure', {})
        
        elif section_title == 'Testing':
            relevant_data['tests'] = repo_data.get('tests', {})
        
        elif section_title == 'License':
            relevant_data['license'] = repo_data.get('license')
        
        else:
            # Include basic info for other sections
            relevant_data = {
                'languages': repo_data.get('languages', {}),
                'entry_points': repo_data.get('entry_points', []),
                'readme': repo_data.get('readme', {})
            }
        
        return json.dumps(relevant_data, indent=2, default=str)
    
    def _load_meta_prompt(self) -> str:
        """
        Load or create the meta-prompt template.
        
        Returns:
            Meta-prompt template string
        """
        meta_prompt_path = self.prompts_dir / "meta_prompt.txt"
        
        if meta_prompt_path.exists():
            with open(meta_prompt_path, 'r', encoding='utf-8') as f:
                return f.read()
        
        # Create default meta-prompt
        default_meta_prompt = """
You are a senior technical writer and documentation engineer with expertise in creating clear, comprehensive project documentation. Your role is to analyze repository data and generate professional documentation sections that help developers understand and use the project effectively.

Key principles:
- Write for your target audience (developers, users, contributors)
- Be clear, concise, and actionable
- Include practical examples and code snippets
- Follow markdown best practices
- Maintain consistency in tone and style
- Focus on what users need to know to be successful

You have access to parsed repository data including code structure, dependencies, README content, and configuration files. Use this information to create accurate, helpful documentation.
"""
        
        with open(meta_prompt_path, 'w', encoding='utf-8') as f:
            f.write(default_meta_prompt)
        
        return default_meta_prompt
    
    def _create_prompt_templates(self):
        """
        Create prompt template files if they don't exist.
        """
        # Create outline prompt template
        outline_prompt_path = self.prompts_dir / "outline_prompt.txt"
        if not outline_prompt_path.exists():
            outline_prompt = """
Generate a structured outline for project documentation based on the provided repository analysis.

Consider:
- Project type and complexity
- Available information in the repository
- Target audience needs
- Standard documentation practices

Output a prioritized list of sections with descriptions.
"""
            with open(outline_prompt_path, 'w', encoding='utf-8') as f:
                f.write(outline_prompt)
        
        # Create section prompt template
        section_prompt_path = self.prompts_dir / "section_prompt.txt"
        if not section_prompt_path.exists():
            section_prompt = """
Generate a specific documentation section based on the provided outline and repository data.

Requirements:
- Follow the section description and requirements
- Use repository data to provide accurate information
- Include practical examples where appropriate
- Write in clear, professional markdown
- Be comprehensive but concise
"""
            with open(section_prompt_path, 'w', encoding='utf-8') as f:
                f.write(section_prompt)
    
    def _save_outline(self, outline: Dict[str, Any]):
        """
        Save the generated outline for reference.
        
        Args:
            outline: Generated outline data
        """
        outline_path = self.prompts_dir / "generated_outline.json"
        with open(outline_path, 'w', encoding='utf-8') as f:
            json.dump(outline, f, indent=2, default=str)
        
        print(f"📄 Outline saved to {outline_path}")


if __name__ == "__main__":
    # Test the doc planner
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python doc_planner.py <repo_data.json>")
        sys.exit(1)
    
    repo_data_path = Path(sys.argv[1])
    if not repo_data_path.exists():
        print(f"Repository data file does not exist: {repo_data_path}")
        sys.exit(1)
    
    with open(repo_data_path, 'r', encoding='utf-8') as f:
        repo_data = json.load(f)
    
    planner = DocPlanner()
    ai_context = {}  # Empty context for testing
    outline = planner.generate_outline(repo_data, ai_context)
    
    print("\n📋 Generated Outline:")
    print(json.dumps(outline, indent=2, default=str))