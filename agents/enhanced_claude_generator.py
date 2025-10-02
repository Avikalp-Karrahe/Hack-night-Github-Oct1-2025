#!/usr/bin/env python3
"""
Enhanced Claude Desktop Prompt Generator

Advanced agent for generating realistic, functional Claude Desktop prompts
that can accurately replicate or build repositories with precise, executable instructions.
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime

# Opik for LLM observability
import opik
from opik import track


class EnhancedClaudeGenerator:
    """
    Enhanced Claude Desktop prompt generator with deep project analysis
    and executable instruction generation.
    """
    
    def __init__(self):
        self.framework_patterns = {
            'react': {
                'files': ['package.json'],
                'dependencies': ['react', '@types/react', 'react-dom'],
                'indicators': ['jsx', 'tsx', 'components/', 'src/App.jsx', 'src/App.tsx']
            },
            'vue': {
                'files': ['package.json'],
                'dependencies': ['vue', '@vue/cli', 'nuxt'],
                'indicators': ['.vue', 'src/App.vue', 'components/']
            },
            'angular': {
                'files': ['package.json', 'angular.json'],
                'dependencies': ['@angular/core', '@angular/cli'],
                'indicators': ['src/app/', '.component.ts', '.service.ts']
            },
            'next': {
                'files': ['package.json', 'next.config.js'],
                'dependencies': ['next', 'react'],
                'indicators': ['pages/', 'app/', '_app.js', '_document.js']
            },
            'vite': {
                'files': ['vite.config.js', 'vite.config.ts', 'package.json'],
                'dependencies': ['vite', '@vitejs/plugin-react'],
                'indicators': ['index.html', 'src/main.jsx', 'src/main.tsx']
            },
            'express': {
                'files': ['package.json'],
                'dependencies': ['express', 'node'],
                'indicators': ['server.js', 'app.js', 'routes/', 'middleware/']
            },
            'fastapi': {
                'files': ['requirements.txt', 'pyproject.toml'],
                'dependencies': ['fastapi', 'uvicorn'],
                'indicators': ['main.py', 'app/', 'routers/']
            },
            'django': {
                'files': ['requirements.txt', 'manage.py'],
                'dependencies': ['django'],
                'indicators': ['settings.py', 'urls.py', 'models.py']
            },
            'flask': {
                'files': ['requirements.txt'],
                'dependencies': ['flask'],
                'indicators': ['app.py', 'run.py', 'templates/']
            },
            'supabase': {
                'files': ['package.json'],
                'dependencies': ['@supabase/supabase-js'],
                'indicators': ['supabase/', '.env.local']
            },
            'tailwind': {
                'files': ['tailwind.config.js', 'tailwind.config.ts', 'package.json'],
                'dependencies': ['tailwindcss', 'autoprefixer', 'postcss'],
                'indicators': ['src/index.css', 'styles/globals.css']
            },
            'shadcn': {
                'files': ['components.json', 'package.json'],
                'dependencies': ['@radix-ui/react-', 'lucide-react', 'class-variance-authority'],
                'indicators': ['components/ui/', 'lib/utils.ts']
            }
        }
        
        self.project_types = {
            'web_frontend': ['react', 'vue', 'angular', 'next', 'vite'],
            'web_backend': ['express', 'fastapi', 'django', 'flask'],
            'fullstack': ['next', 'nuxt', 'sveltekit'],
            'mobile': ['react-native', 'flutter', 'ionic'],
            'desktop': ['electron', 'tauri', 'flutter'],
            'library': ['typescript', 'javascript', 'python'],
            'cli_tool': ['node', 'python', 'go', 'rust']
        }
    
    @track(name="claude_prompt_generation")
    def generate_enhanced_prompts(self, github_url: str, repo_data: Dict[str, Any], 
                                documentation: str, base_filename: str) -> str:
        """
        Generate enhanced Claude Desktop prompts with deep project analysis.
        
        Args:
            github_url: Repository URL
            repo_data: Parsed repository data
            documentation: Generated documentation
            base_filename: Base filename for outputs
            
        Returns:
            Formatted Claude Desktop prompts
        """
        # Deep analysis of the project
        tech_stack = self._analyze_technology_stack(repo_data)
        project_context = self._extract_project_context(documentation, repo_data)
        setup_requirements = self._analyze_setup_requirements(repo_data, tech_stack)
        architecture_info = self._analyze_architecture(repo_data, documentation)
        
        # Generate project-specific prompts
        prompts_content = self._generate_project_prompts(
            github_url=github_url,
            repo_data=repo_data,
            tech_stack=tech_stack,
            project_context=project_context,
            setup_requirements=setup_requirements,
            architecture_info=architecture_info,
            base_filename=base_filename
        )
        
        return prompts_content
    
    def _analyze_technology_stack(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform deep analysis of the technology stack."""
        tech_stack = {
            'primary_language': self._get_primary_language(repo_data),
            'frameworks': [],
            'libraries': [],
            'tools': [],
            'databases': [],
            'deployment': [],
            'testing': [],
            'styling': [],
            'build_tools': []
        }
        
        # Analyze dependencies for frameworks and libraries
        dependencies = repo_data.get('dependencies', {})
        repo_path = Path(repo_data.get('path', ''))
        
        # Check for frameworks
        for framework, config in self.framework_patterns.items():
            if self._detect_framework(repo_path, dependencies, config):
                if framework in ['react', 'vue', 'angular', 'next', 'vite']:
                    tech_stack['frameworks'].append(framework)
                elif framework in ['tailwind', 'shadcn']:
                    tech_stack['styling'].append(framework)
                elif framework in ['supabase']:
                    tech_stack['databases'].append(framework)
        
        # Analyze package.json for additional insights
        if 'node' in dependencies:
            package_json = dependencies['node'].get('package.json', {})
            if package_json:
                tech_stack['libraries'].extend(self._extract_key_libraries(package_json))
                tech_stack['tools'].extend(self._extract_dev_tools(package_json))
        
        # Analyze Python requirements
        if 'python' in dependencies:
            python_deps = dependencies['python']
            tech_stack['libraries'].extend(self._extract_python_libraries(python_deps))
        
        return tech_stack
    
    def _detect_framework(self, repo_path: Path, dependencies: Dict, config: Dict) -> bool:
        """Detect if a specific framework is used in the project."""
        # Check for required files
        for file_pattern in config.get('files', []):
            if list(repo_path.glob(file_pattern)):
                # Check dependencies if package.json exists
                if 'package.json' in file_pattern and 'node' in dependencies:
                    package_data = dependencies['node'].get('package.json', {})
                    deps = {**package_data.get('dependencies', {}), 
                           **package_data.get('devDependencies', {})}
                    
                    for dep in config.get('dependencies', []):
                        if any(dep in key for key in deps.keys()):
                            return True
                else:
                    return True
        
        # Check for indicator files/directories
        for indicator in config.get('indicators', []):
            if list(repo_path.glob(f"**/{indicator}")):
                return True
        
        return False
    
    def _extract_project_context(self, documentation: str, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract comprehensive project context from documentation and repo data."""
        context = {
            'purpose': '',
            'features': [],
            'domain': '',
            'complexity': 'medium',
            'target_users': [],
            'key_components': [],
            'business_logic': []
        }
        
        # Extract purpose from documentation
        context['purpose'] = self._extract_purpose_advanced(documentation)
        
        # Extract features with better analysis
        context['features'] = self._extract_features_advanced(documentation, repo_data)
        
        # Determine domain
        context['domain'] = self._determine_domain(documentation, repo_data)
        
        # Assess complexity
        context['complexity'] = self._assess_complexity_advanced(repo_data, documentation)
        
        # Extract key components
        context['key_components'] = self._extract_key_components(repo_data)
        
        return context
    
    def _analyze_setup_requirements(self, repo_data: Dict[str, Any], 
                                  tech_stack: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze specific setup requirements for the project."""
        requirements = {
            'prerequisites': [],
            'environment_setup': [],
            'dependencies': [],
            'configuration': [],
            'build_steps': [],
            'development_setup': []
        }
        
        # Determine prerequisites based on tech stack
        primary_lang = tech_stack['primary_language']
        frameworks = tech_stack['frameworks']
        
        if primary_lang == 'typescript' or 'javascript' in primary_lang:
            requirements['prerequisites'].extend(['Node.js (v18+)', 'npm or yarn or bun'])
            
            if 'react' in frameworks:
                requirements['environment_setup'].append('React development environment')
            if 'next' in frameworks:
                requirements['environment_setup'].append('Next.js development setup')
            if 'vite' in frameworks:
                requirements['environment_setup'].append('Vite build tool setup')
        
        elif primary_lang == 'python':
            requirements['prerequisites'].extend(['Python 3.8+', 'pip', 'virtual environment'])
            
        # Add database requirements
        if 'supabase' in tech_stack['databases']:
            requirements['configuration'].extend([
                'Supabase project setup',
                'Environment variables configuration',
                'Database schema setup'
            ])
        
        return requirements
    
    def _generate_project_prompts(self, github_url: str, repo_data: Dict[str, Any],
                                tech_stack: Dict[str, Any], project_context: Dict[str, Any],
                                setup_requirements: Dict[str, Any], architecture_info: Dict[str, Any],
                                base_filename: str) -> str:
        """Generate comprehensive, executable Claude Desktop prompts."""
        
        repo_name = self._extract_repo_name(github_url)
        project_name = project_context.get('purpose', repo_name).replace('a ', '').replace('an ', '')
        
        # Determine the primary framework for specialized prompts
        primary_framework = self._get_primary_framework(tech_stack)
        
        prompts_content = f"""# Claude Desktop Prompts for Building {project_name}

These prompts will help you **build and implement** the **{project_name}** project from scratch using Claude Desktop, based on comprehensive analysis of the repository.

## Project Information

- **GitHub URL:** {github_url}
- **Primary Language:** {tech_stack['primary_language']}
- **Project Type:** {self._determine_project_type(tech_stack)}
- **File Count:** {len(repo_data.get('files', []))}
- **Live Demo:** {self._extract_demo_url(repo_data)}
- **Complexity:** {project_context['complexity'].title()}
- **Reference Documentation:** {base_filename}

## Project Overview

**{project_name}** is {project_context['purpose']}.

### Core Features
{self._format_features_list(project_context['features'])}

### Technology Stack
{self._format_tech_stack(tech_stack)}

### Architecture Overview
{self._format_architecture(architecture_info)}

---

## Prompt 1: Project Setup & Environment Configuration

```
You are a senior full-stack developer and {primary_framework} specialist. I need you to help me build {project_name}, {project_context['purpose']}.

**Project Context:**
- Primary Language: {tech_stack['primary_language']}
- Framework: {primary_framework}
- Reference Repository: {github_url}
- Target Complexity: {project_context['complexity'].title()} ({len(repo_data.get('files', []))} files)
- Core Purpose: {project_context['purpose']}

**Technology Stack:**
{self._format_tech_stack_for_prompt(tech_stack)}

**Your Role:**
- Expert {tech_stack['primary_language']}/{primary_framework} developer with 10+ years experience
- {project_context['domain']} application specialist
- Modern web development and tooling expert
- Code quality and best practices advocate

**Task:**
Help me set up the foundational architecture for {project_name}:

{self._generate_setup_instructions(tech_stack, setup_requirements)}

**Output Requirements:**
- Fully configured {primary_framework} project
- All necessary dependencies installed
- Proper project structure for {project_context['domain']} application
- Development environment ready for implementation
- Working build and development scripts

**Quality Standards:**
{self._generate_quality_standards(tech_stack, primary_framework)}

Please provide the complete project setup with all configuration files and explain each step clearly.
```

---

## Prompt 2: Core Implementation & Feature Development

```
You are an expert {primary_framework} developer and {project_context['domain']} application architect. Building on the project setup from the previous step, I need you to implement the core functionality.

**Previous Setup Context:**
[PASTE THE OUTPUT FROM PROMPT 1 HERE]

**Project Details:**
- Repository Reference: {github_url}
- Technology Stack: {self._format_tech_stack_simple(tech_stack)}
- Target: Build {project_context['purpose']}
- Core Features: {', '.join(project_context['features'][:5])}

**Your Enhanced Role:**
- Senior {tech_stack['primary_language']}/{primary_framework} developer
- {project_context['domain']} domain expert
- API design and integration specialist
- Performance optimization expert

**Implementation Tasks:**

{self._generate_implementation_tasks(project_context, tech_stack)}

**Code Quality Requirements:**
{self._generate_code_quality_requirements(tech_stack)}

**Deliverables:**
- Complete, functional codebase
- Working application with core features
- Comprehensive component structure
- Proper state management implementation
- Clear code documentation

**Implementation Checklist:**
{self._generate_implementation_checklist(project_context['features'])}

Please provide complete, working code implementations that I can use to build {project_name} with these key features.
```

---

## Prompt 3: Advanced Features & Production Optimization

```
You are a senior software architect and production systems specialist. I need you to implement advanced features and optimize my {project_name} for production deployment.

**Complete Implementation Context:**
[PASTE ALL PREVIOUS OUTPUTS HERE]

**Project Status:**
- Repository Reference: {github_url}
- Technology: {tech_stack['primary_language']} with {primary_framework}
- Current State: Functional {project_name} with core features
- Target: Production-ready application with advanced features

**Your Expert Role:**
- Senior software architect
- Performance optimization specialist
- Security and compliance expert
- DevOps and deployment specialist

**Advanced Implementation Tasks:**

{self._generate_advanced_tasks(project_context, tech_stack)}

**Production Optimization:**
{self._generate_production_optimization(tech_stack)}

**Final Deliverables:**
- Production-optimized application
- Advanced feature implementations
- Security hardening
- Performance monitoring
- Deployment configuration

**Production Checklist:**
{self._generate_production_checklist(tech_stack)}

Please provide a complete production-ready implementation with all advanced features and optimizations.
```

---

## Implementation Guide

### Development Workflow:
1. **Sequential Development**: Follow prompts in order (Setup → Core → Advanced)
2. **Context Preservation**: Always include previous outputs in subsequent prompts
3. **Iterative Testing**: Test each component before proceeding
4. **Quality Validation**: Ensure code quality at each step

### Expected Outcomes:
- **Functional Application**: Complete, working {project_name}
- **Modern Architecture**: Built with {primary_framework} best practices
- **Production Ready**: Optimized for real-world deployment
- **Comprehensive Features**: {', '.join(project_context['features'][:3])}

### Success Criteria:
- ✅ Project builds and runs without errors
- ✅ All core features are implemented and working
- ✅ Code follows {primary_framework} best practices
- ✅ Application is responsive and performant
- ✅ Production deployment is successful

---

*Generated by Enhanced PromptSwitch for {project_name} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        return prompts_content
    
    # Helper methods for prompt generation
    def _extract_repo_name(self, github_url: str) -> str:
        """Extract clean repository name from GitHub URL."""
        return github_url.split('/')[-1].replace('.git', '')
    
    def _get_primary_language(self, repo_data: Dict[str, Any]) -> str:
        """Get the primary programming language."""
        languages = repo_data.get('languages', {})
        if isinstance(languages, dict) and languages:
            return max(languages.items(), key=lambda x: x[1])[0]
        return 'Unknown'
    
    def _get_primary_framework(self, tech_stack: Dict[str, Any]) -> str:
        """Determine the primary framework."""
        frameworks = tech_stack.get('frameworks', [])
        if frameworks:
            return frameworks[0].title()
        
        primary_lang = tech_stack.get('primary_language', '').lower()
        if 'typescript' in primary_lang or 'javascript' in primary_lang:
            return 'React'  # Default assumption for JS/TS projects
        elif primary_lang == 'python':
            return 'FastAPI'  # Default assumption for Python projects
        
        return tech_stack.get('primary_language', 'Unknown').title()
    
    def _determine_project_type(self, tech_stack: Dict[str, Any]) -> str:
        """Determine the project type based on technology stack."""
        frameworks = tech_stack.get('frameworks', [])
        
        for proj_type, type_frameworks in self.project_types.items():
            if any(fw in frameworks for fw in type_frameworks):
                return proj_type.replace('_', ' ').title()
        
        primary_lang = tech_stack.get('primary_language', '').lower()
        if 'typescript' in primary_lang or 'javascript' in primary_lang:
            return 'Web Application'
        elif primary_lang == 'python':
            return 'Backend Application'
        
        return 'Software Application'
    
    def _extract_demo_url(self, repo_data: Dict[str, Any]) -> str:
        """Extract demo URL from repository data."""
        readme = repo_data.get('readme', {})
        content = readme.get('content', '')
        
        # Look for common demo URL patterns
        demo_patterns = [
            r'https?://[^\s]+\.vercel\.app[^\s]*',
            r'https?://[^\s]+\.netlify\.app[^\s]*',
            r'https?://[^\s]+\.herokuapp\.com[^\s]*',
            r'https?://[^\s]+\.github\.io[^\s]*',
            r'https?://[^\s]+\.lovable\.app[^\s]*'
        ]
        
        for pattern in demo_patterns:
            match = re.search(pattern, content)
            if match:
                return match.group(0).rstrip(')')
        
        return 'Not available'
    
    # Additional helper methods would continue here...
    # (Implementation continues with all the formatting and analysis methods)
    
    def _format_features_list(self, features: List[str]) -> str:
        """Format features as a bulleted list."""
        if not features:
            return "- Core application functionality"
        return '\n'.join(f"- **{feature}**" for feature in features[:8])
    
    def _format_tech_stack(self, tech_stack: Dict[str, Any]) -> str:
        """Format technology stack for display."""
        lines = []
        if tech_stack.get('frameworks'):
            lines.append(f"- **Frontend:** {', '.join(tech_stack['frameworks'])}")
        if tech_stack.get('styling'):
            lines.append(f"- **Styling:** {', '.join(tech_stack['styling'])}")
        if tech_stack.get('databases'):
            lines.append(f"- **Backend:** {', '.join(tech_stack['databases'])}")
        if tech_stack.get('tools'):
            lines.append(f"- **Tools:** {', '.join(tech_stack['tools'][:3])}")
        
        return '\n'.join(lines) if lines else f"- **Primary:** {tech_stack.get('primary_language', 'Unknown')}"
    
    # Placeholder methods - would need full implementation
    def _extract_key_libraries(self, package_json: Dict) -> List[str]:
        """Extract key libraries from package.json."""
        return []
    
    def _extract_dev_tools(self, package_json: Dict) -> List[str]:
        """Extract development tools from package.json."""
        return []
    
    def _extract_python_libraries(self, python_deps: Dict) -> List[str]:
        """Extract Python libraries from dependencies."""
        return []
    
    def _extract_purpose_advanced(self, documentation: str) -> str:
        """Extract project purpose with advanced analysis."""
        # Look for purpose indicators in documentation
        purpose_patterns = [
            r'(?i)(?:is|provides|offers|enables|helps|allows|creates|builds)\s+([^.!?]+)',
            r'(?i)(?:purpose|goal|objective|aim):\s*([^.!?]+)',
            r'(?i)(?:description|summary):\s*([^.!?]+)',
            r'(?i)(?:about|overview):\s*([^.!?]+)'
        ]
        
        for pattern in purpose_patterns:
            match = re.search(pattern, documentation[:2000])
            if match:
                purpose = match.group(1).strip()
                if len(purpose) > 10 and len(purpose) < 200:
                    return purpose.lower()
        
        # Fallback to generic purpose
        return "a modern web application"
    
    def _extract_features_advanced(self, documentation: str, repo_data: Dict) -> List[str]:
        """Extract features with advanced analysis."""
        features = set()
        
        # Common feature patterns
        feature_patterns = [
            r'(?i)features?:\s*\n((?:\s*[-*]\s*[^\n]+\n?)+)',
            r'(?i)capabilities?:\s*\n((?:\s*[-*]\s*[^\n]+\n?)+)',
            r'(?i)functionality:\s*\n((?:\s*[-*]\s*[^\n]+\n?)+)',
            r'(?i)includes?:\s*\n((?:\s*[-*]\s*[^\n]+\n?)+)'
        ]
        
        for pattern in feature_patterns:
            match = re.search(pattern, documentation)
            if match:
                feature_text = match.group(1)
                # Extract individual features
                feature_lines = re.findall(r'[-*]\s*([^\n]+)', feature_text)
                for feature in feature_lines[:8]:  # Limit to 8 features
                    clean_feature = re.sub(r'[^\w\s-]', '', feature.strip())
                    if len(clean_feature) > 5:
                        features.add(clean_feature)
        
        # Look for technology-specific features
        if 'react' in documentation.lower():
            features.update(['Component-based architecture', 'State management', 'Responsive UI'])
        if 'api' in documentation.lower():
            features.add('API integration')
        if 'database' in documentation.lower() or 'supabase' in documentation.lower():
            features.add('Data persistence')
        if 'auth' in documentation.lower():
            features.add('User authentication')
        
        # Analyze file structure for features
        files = repo_data.get('files', [])
        if any('component' in f.lower() for f in files):
            features.add('Component library')
        if any('test' in f.lower() for f in files):
            features.add('Testing framework')
        if any('config' in f.lower() for f in files):
            features.add('Configuration management')
        
        return list(features)[:8] if features else ['User interface', 'Data management', 'API integration']
    
    def _determine_domain(self, documentation: str, repo_data: Dict) -> str:
        """Determine application domain."""
        domain_keywords = {
            'e-commerce': ['shop', 'cart', 'payment', 'product', 'order'],
            'social media': ['social', 'post', 'follow', 'like', 'share', 'comment'],
            'productivity': ['task', 'todo', 'project', 'manage', 'organize'],
            'finance': ['finance', 'money', 'bank', 'payment', 'transaction'],
            'education': ['learn', 'course', 'student', 'teach', 'education'],
            'healthcare': ['health', 'medical', 'patient', 'doctor', 'clinic'],
            'entertainment': ['game', 'music', 'video', 'media', 'entertainment'],
            'business': ['business', 'crm', 'enterprise', 'company', 'corporate']
        }
        
        doc_lower = documentation.lower()
        for domain, keywords in domain_keywords.items():
            if any(keyword in doc_lower for keyword in keywords):
                return domain
        
        return 'web development'
    
    def _generate_setup_instructions(self, tech_stack: Dict, requirements: Dict) -> str:
        """Generate setup instructions based on tech stack."""
        primary_lang = tech_stack.get('primary_language', '').lower()
        frameworks = tech_stack.get('frameworks', [])
        
        instructions = []
        
        if 'javascript' in primary_lang or 'typescript' in primary_lang:
            instructions.append("1. **Project Initialization**")
            instructions.append("   - Install Node.js (v18 or higher)")
            instructions.append("   - Create new project directory")
            
            if 'react' in frameworks:
                instructions.append("   - Initialize React project with Vite or Create React App")
                instructions.append("   - Install React and TypeScript dependencies")
            elif 'next' in frameworks:
                instructions.append("   - Initialize Next.js project")
                instructions.append("   - Configure TypeScript and ESLint")
            elif 'vite' in frameworks:
                instructions.append("   - Initialize Vite project")
                instructions.append("   - Configure build tools and plugins")
            
            instructions.append("2. **Development Environment**")
            instructions.append("   - Set up package.json with scripts")
            instructions.append("   - Configure development server")
            instructions.append("   - Install development dependencies")
            
            if 'tailwind' in tech_stack.get('styling', []):
                instructions.append("3. **Styling Setup**")
                instructions.append("   - Install and configure Tailwind CSS")
                instructions.append("   - Set up PostCSS configuration")
                instructions.append("   - Create base styles and utilities")
            
            if 'supabase' in tech_stack.get('databases', []):
                instructions.append("4. **Backend Configuration**")
                instructions.append("   - Set up Supabase project")
                instructions.append("   - Configure environment variables")
                instructions.append("   - Initialize database schema")
        
        elif primary_lang == 'python':
            instructions.extend([
                "1. **Python Environment Setup**",
                "   - Install Python 3.8+ and pip",
                "   - Create virtual environment",
                "   - Install project dependencies",
                "2. **Framework Configuration**",
                "   - Set up FastAPI or Django project",
                "   - Configure database connections",
                "   - Set up development server"
            ])
        
        return '\n'.join(instructions) if instructions else "1. **Project Initialization**\n   - Set up development environment\n   - Install dependencies\n   - Configure build tools"

    def _assess_complexity_advanced(self, repo_data: Dict, documentation: str) -> str:
        """Assess project complexity."""
        file_count = len(repo_data.get('files', []))
        if file_count > 100:
            return "complex"
        elif file_count > 50:
            return "medium"
        return "simple"
    
    def _extract_key_components(self, repo_data: Dict) -> List[str]:
        """Extract key components from repository structure."""
        return []
    
    def _analyze_architecture(self, repo_data: Dict, documentation: str) -> Dict[str, Any]:
        """Analyze project architecture."""
        return {"pattern": "component-based", "structure": "modular"}
    
    def _format_architecture(self, architecture_info: Dict) -> str:
        """Format architecture information."""
        return f"- **Pattern:** {architecture_info.get('pattern', 'Standard')}\n- **Structure:** {architecture_info.get('structure', 'Organized')}"
    
    def _format_tech_stack_for_prompt(self, tech_stack: Dict) -> str:
        """Format tech stack for prompt context."""
        return f"Primary: {tech_stack.get('primary_language', 'Unknown')}, Frameworks: {', '.join(tech_stack.get('frameworks', []))}"
    
    def _generate_setup_instructions(self, tech_stack: Dict, requirements: Dict) -> str:
        """Generate setup instructions based on tech stack."""
        return "1. **Project Initialization**\n   - Set up development environment\n   - Install dependencies\n   - Configure build tools"
    
    def _generate_quality_standards(self, tech_stack: Dict, framework: str) -> str:
        """Generate quality standards for the project."""
        return f"- Follow {framework} best practices\n- Use TypeScript for type safety\n- Implement responsive design"
    
    def _format_tech_stack_simple(self, tech_stack: Dict) -> str:
        """Simple tech stack formatting."""
        return f"{tech_stack.get('primary_language', 'Unknown')} + {', '.join(tech_stack.get('frameworks', []))}"
    
    def _generate_implementation_tasks(self, context: Dict, tech_stack: Dict) -> str:
        """Generate implementation tasks."""
        return "1. **Core Components**\n   - Build main application structure\n   - Implement key features"
    
    def _generate_code_quality_requirements(self, tech_stack: Dict) -> str:
        """Generate code quality requirements."""
        return "- Write clean, maintainable code\n- Follow established patterns\n- Include proper error handling"
    
    def _generate_implementation_checklist(self, features: List[str]) -> str:
        """Generate implementation checklist."""
        return '\n'.join(f"- [ ] {feature} implementation" for feature in features[:5])
    
    def _generate_advanced_tasks(self, context: Dict, tech_stack: Dict) -> str:
        """Generate advanced implementation tasks."""
        return "1. **Performance Optimization**\n   - Code splitting and lazy loading\n   - Bundle optimization"
    
    def _generate_production_optimization(self, tech_stack: Dict) -> str:
        """Generate production optimization steps."""
        return "- Build optimization\n- Security hardening\n- Performance monitoring"
    
    def _generate_production_checklist(self, tech_stack: Dict) -> str:
        """Generate production readiness checklist."""
        return "- [ ] Application builds successfully\n- [ ] All tests pass\n- [ ] Security measures implemented"


if __name__ == "__main__":
    # Test the enhanced generator
    generator = EnhancedClaudeGenerator()
    print("Enhanced Claude Generator initialized successfully!")