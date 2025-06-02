#!/usr/bin/env python3
"""
Section Filler Agent

Fills documentation sections using the generated outline and prompt chaining.
This implements the core prompt chaining strategy (Prompt 2-N).
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional


class SectionFiller:
    """Agent responsible for filling documentation sections using prompt chaining."""
    
    def __init__(self, prompts_dir="prompts"):
        self.prompts_dir = Path(prompts_dir)
        self.prompts_dir.mkdir(exist_ok=True)
        
        # Enhanced section templates for comprehensive content
        self.section_templates = {
            'Project Summary & Goals': self._generate_enhanced_overview_template,
            'Key Features & Use Cases': self._generate_enhanced_features_template,
            'Technology Stack': self._generate_enhanced_tech_stack_template,
            'Setup Instructions': self._generate_enhanced_setup_template,
            'Configuration Required': self._generate_enhanced_configuration_template,
            'Usage': self._generate_usage_template,
            'API Documentation': self._generate_api_template,
            'Project Structure': self._generate_structure_template,
            'Major Components & Modules': self._generate_development_template,
            'Execution Plan': self._generate_development_template,
            'Development Workflow': self._generate_development_template,
            'Testing Strategy': self._generate_testing_template,
            'Deployment Checklist': self._generate_deployment_template,
            'Troubleshooting & Tips': self._generate_development_template,
            'Performance Optimization': self._generate_development_template,
            'Contributing Guidelines': self._generate_development_template,
            'License': self._generate_license_template
        }
    
    def fill_sections(self, outline: Dict[str, Any], repo_data: Dict[str, Any], 
                     ai_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fill all sections in the outline with content.
        
        Args:
            outline: Generated outline from doc_planner
            repo_data: Parsed repository data
            ai_context: AI learning context
            
        Returns:
            Dict containing filled documentation sections
        """
        print("✍️ Filling documentation sections...")
        
        filled_doc = {
            'metadata': outline.get('metadata', {}),
            'project_name': outline.get('project_name', 'Unknown Project'),
            'sections': {},
            'generation_info': {
                'timestamp': datetime.utcnow().isoformat(),
                'total_sections': len(outline.get('sections', [])),
                'ai_context_used': bool(ai_context)
            }
        }
        
        sections = outline.get('sections', [])
        prompts = outline.get('prompts', {})
        
        # Process sections in priority order
        sorted_sections = sorted(sections, key=lambda x: self._get_priority_value(x.get('priority', 'medium')))
        
        for i, section in enumerate(sorted_sections, 1):
            title = section['title']
            print(f"📝 Filling section {i}/{len(sections)}: {title}")
            
            try:
                # Get section prompt
                section_prompt = prompts.get(title, '')
                
                # Fill section content
                content = self._fill_section(
                    title, section, section_prompt, repo_data, ai_context
                )
                
                filled_doc['sections'][title] = {
                    'content': content,
                    'priority': section.get('priority', 'medium'),
                    'required': section.get('required', False),
                    'description': section.get('description', ''),
                    'word_count': len(content.split()) if content else 0
                }
                
                print(f"✅ Completed {title} ({len(content.split()) if content else 0} words)")
                
            except Exception as e:
                print(f"⚠️ Error filling section {title}: {e}")
                # Use fallback content
                fallback_content = self._generate_fallback_content(title, repo_data)
                filled_doc['sections'][title] = {
                    'content': fallback_content,
                    'priority': section.get('priority', 'medium'),
                    'required': section.get('required', False),
                    'description': section.get('description', ''),
                    'error': str(e),
                    'fallback_used': True
                }
        
        # Save filled sections for reference
        self._save_filled_sections(filled_doc)
        
        print(f"✅ All sections filled successfully")
        return filled_doc
    
    def _get_priority_value(self, priority: str) -> int:
        """Convert priority string to numeric value for sorting."""
        priority_map = {'high': 1, 'medium': 2, 'low': 3}
        return priority_map.get(priority.lower(), 2)
    
    def _fill_section(self, title: str, section: Dict[str, Any], prompt: str,
                     repo_data: Dict[str, Any], ai_context: Dict[str, Any]) -> str:
        """
        Fill a specific section with content.
        
        Args:
            title: Section title
            section: Section metadata
            prompt: Generated prompt for this section
            repo_data: Repository data
            ai_context: AI learning context
            
        Returns:
            Generated section content
        """
        # In a real implementation, this would call an LLM API
        # For now, we'll use template-based generation
        
        # Try to use AI context and learning materials
        enhanced_content = self._generate_enhanced_content(title, repo_data, ai_context)
        if enhanced_content:
            return enhanced_content
        
        # Fall back to template-based generation
        template_func = self.section_templates.get(title)
        if template_func:
            return template_func(repo_data)
        
        # Ultimate fallback
        return self._generate_basic_content(title, section, repo_data)
    
    def _generate_enhanced_content(self, title: str, repo_data: Dict[str, Any], 
                                 ai_context: Dict[str, Any]) -> Optional[str]:
        """
        Generate enhanced content using AI context and learning materials.
        
        Args:
            title: Section title
            repo_data: Repository data
            ai_context: AI learning context
            
        Returns:
            Enhanced content if successful, None otherwise
        """
        # This would integrate with LLM APIs in a real implementation
        # For now, we'll use the AI context to inform template generation
        
        # Check if we have relevant past documentation
        past_outputs = ai_context.get('past_outputs', [])
        project_docs = ai_context.get('project_docs', {})
        
        # Use insights from past documentation to improve current generation
        if past_outputs or project_docs:
            return self._generate_context_aware_content(title, repo_data, ai_context)
        
        return None
    
    def _generate_context_aware_content(self, title: str, repo_data: Dict[str, Any],
                                      ai_context: Dict[str, Any]) -> str:
        """
        Generate content that's aware of past documentation and AI learning.
        
        Args:
            title: Section title
            repo_data: Repository data
            ai_context: AI learning context
            
        Returns:
            Context-aware content
        """
        # Get base template content
        template_func = self.section_templates.get(title)
        base_content = template_func(repo_data) if template_func else ""
        
        # Enhance with context from AI learning
        project_docs = ai_context.get('project_docs', {})
        
        # Add insights from project documentation
        if '03_docs.md' in project_docs:
            docs_content = project_docs['03_docs.md']
            if 'prompt' in docs_content.lower() and title == 'Project Overview':
                base_content += "\n\n> This project follows AI-assisted engineering principles with prompt chaining and meta-prompting strategies."
        
        return base_content
    
    def _generate_fallback_content(self, title: str, repo_data: Dict[str, Any]) -> str:
        """
        Generate fallback content when other methods fail.
        
        Args:
            title: Section title
            repo_data: Repository data
            
        Returns:
            Basic fallback content
        """
        template_func = self.section_templates.get(title)
        if template_func:
            return template_func(repo_data)
        
        return f"## {title}\n\nThis section needs to be filled with relevant information about the project."
    
    def _generate_basic_content(self, title: str, section: Dict[str, Any], 
                              repo_data: Dict[str, Any]) -> str:
        """
        Generate basic content for unknown section types.
        
        Args:
            title: Section title
            section: Section metadata
            repo_data: Repository data
            
        Returns:
            Basic section content
        """
        description = section.get('description', 'No description available.')
        return f"## {title}\n\n{description}\n\n*This section requires manual completion.*"
    
    # Helper methods for enhanced templates
    
    def _detect_project_type(self, repo_data: Dict[str, Any]) -> str:
        """Detect the type of project based on repository data."""
        languages = repo_data.get('languages', {})
        files = repo_data.get('files', [])
        
        # Check for web frontend indicators
        frontend_indicators = ['package.json', 'index.html', 'src/App.js', 'src/App.tsx', 'webpack.config.js']
        if any(indicator in str(files) for indicator in frontend_indicators):
            if 'TypeScript' in languages or 'JavaScript' in languages:
                return 'web_frontend'
        
        # Check for API/backend indicators
        api_indicators = ['app.py', 'main.py', 'server.js', 'index.js', 'requirements.txt']
        if any(indicator in str(files) for indicator in api_indicators):
            return 'web_api'
        
        # Check for mobile app
        mobile_indicators = ['android/', 'ios/', 'App.js', 'react-native']
        if any(indicator in str(files) for indicator in mobile_indicators):
            return 'mobile_app'
        
        # Check for desktop application
        desktop_indicators = ['.exe', '.app', 'main.cpp', 'main.c']
        if any(indicator in str(files) for indicator in desktop_indicators):
            return 'desktop_app'
        
        # Check for library/package
        library_indicators = ['setup.py', '__init__.py', 'lib/', 'src/lib']
        if any(indicator in str(files) for indicator in library_indicators):
            return 'library'
        
        # Default based on primary language
        primary_lang = max(languages.keys(), key=lambda k: languages[k]) if languages else 'Unknown'
        if primary_lang in ['JavaScript', 'TypeScript', 'HTML', 'CSS']:
            return 'web_project'
        elif primary_lang in ['Python', 'Java', 'C#', 'Go', 'Rust']:
            return 'application'
        else:
            return 'software_project'
    
    def _assess_complexity(self, repo_data: Dict[str, Any]) -> str:
        """Assess the complexity level of the project."""
        files = repo_data.get('files', [])
        languages = repo_data.get('languages', {})
        
        file_count = len(files)
        language_count = len(languages)
        
        # Calculate complexity score
        complexity_score = 0
        
        # File count factor
        if file_count > 100:
            complexity_score += 3
        elif file_count > 50:
            complexity_score += 2
        elif file_count > 20:
            complexity_score += 1
        
        # Language diversity factor
        if language_count > 5:
            complexity_score += 2
        elif language_count > 3:
            complexity_score += 1
        
        # Framework/technology indicators
        complex_indicators = ['docker', 'kubernetes', 'microservice', 'api', 'database', 'redis', 'mongodb']
        if any(indicator in str(files).lower() for indicator in complex_indicators):
            complexity_score += 2
        
        # Determine complexity level
        if complexity_score >= 5:
            return 'high'
        elif complexity_score >= 3:
            return 'medium'
        else:
            return 'low'
    
    # Template generation methods
    
    def _generate_enhanced_overview_template(self, repo_data: Dict[str, Any]) -> str:
        """Generate comprehensive Project Summary & Goals section."""
        project_name = repo_data.get('name', 'Unknown Project')
        readme = repo_data.get('readme', {})
        languages = repo_data.get('languages', {})
        primary_lang = max(languages.keys(), key=lambda k: languages[k]) if languages else 'Unknown'
        project_type = self._detect_project_type(repo_data)
        complexity = self._assess_complexity(repo_data)
        
        content = f"# {project_name} - Comprehensive Project Plan\n\n"
        content += f"**Repository:** [GitHub Repository URL]\n"
        content += f"**Primary Language:** {primary_lang}\n"
        content += f"**Project Type:** {project_type.replace('_', ' ').title()}\n"
        content += f"**Complexity:** {complexity.title()}\n"
        content += f"**Last Updated:** {datetime.now().strftime('%B %d, %Y')}\n\n"
        
        content += "---\n\n"
        
        # Table of Contents
        content += "## Table of Contents\n\n"
        toc_sections = [
            "Project Summary & Goals", "Key Features & Use Cases", "Technology Stack",
            "Project Structure", "Major Components & Modules", "Setup Instructions",
            "Configuration Required", "Execution Plan", "Development Workflow",
            "Deployment Checklist", "Troubleshooting & Tips", "Performance Optimization",
            "Contributing Guidelines"
        ]
        for i, section in enumerate(toc_sections, 1):
            anchor = section.lower().replace(' ', '-').replace('&', '').replace('--', '-')
            content += f"{i}. [{section}](#{anchor})\n"
        content += "\n---\n\n"
        
        # Project Summary & Goals
        content += "## Project Summary & Goals\n\n"
        
        # Overview subsection
        content += "### Overview\n\n"
        if readme.get('sections'):
            for section in readme['sections']:
                if not section.get('title') or len(section.get('content', '')) > 50:
                    description = section.get('content', '')[:500]
                    if description:
                        content += f"{description}\n\n"
                        break
        else:
            content += f"This is a {project_type.replace('_', ' ')} project built with modern {primary_lang} technologies, "
            content += f"featuring advanced development practices and comprehensive architecture. "
            content += f"The project demonstrates professional-grade software development with "
            content += f"emphasis on code quality, maintainability, and scalability.\n\n"
        
        # Primary Goals
        content += "### Primary Goals\n\n"
        if project_type == 'web_frontend':
            content += "• **Interactive Experience:** Provide engaging user interface with modern web technologies\n"
            content += "• **Performance:** Maintain fast loading times and responsive interactions\n"
            content += "• **Accessibility:** Ensure usability across devices and accessibility standards\n"
            content += "• **Modern Stack:** Demonstrate proficiency with cutting-edge web technologies\n"
        elif project_type == 'web_api':
            content += "• **Robust API:** Provide reliable and scalable API endpoints\n"
            content += "• **Performance:** Ensure fast response times and efficient data processing\n"
            content += "• **Security:** Implement comprehensive security measures and best practices\n"
            content += "• **Documentation:** Maintain clear and comprehensive API documentation\n"
        else:
            content += "• **Functionality:** Deliver core features with high reliability and performance\n"
            content += "• **Maintainability:** Ensure clean, well-documented, and extensible codebase\n"
            content += "• **User Experience:** Provide intuitive and efficient user interactions\n"
            content += "• **Quality:** Maintain high code quality with comprehensive testing\n"
        content += "\n"
        
        # Target Audience
        content += "### Target Audience\n\n"
        content += "• Developers and software engineers\n"
        content += "• Technical teams and project stakeholders\n"
        content += "• Students and learners in software development\n"
        content += "• Anyone interested in modern software architecture\n\n"
        
        return content
    
    def _generate_enhanced_features_template(self, repo_data: Dict[str, Any]) -> str:
        """Generate comprehensive Key Features & Use Cases section."""
        languages = repo_data.get('languages', {})
        readme = repo_data.get('readme', {})
        project_type = self._detect_project_type(repo_data)
        files = repo_data.get('files', [])
        
        content = "## Key Features & Use Cases\n\n"
        
        # Core Features subsection
        content += "### Core Features\n\n"
        
        # Try to extract features from README first
        features_found = False
        if readme.get('sections'):
            for section in readme['sections']:
                title = section.get('title', '').lower()
                if 'feature' in title or 'what' in title:
                    content += f"{section.get('content', '')}\n\n"
                    features_found = True
                    break
        
        if not features_found:
            # Generate comprehensive features based on project type
            if project_type == 'web_frontend':
                content += "#### User Interface & Experience\n"
                content += "• **Modern Web Interface:** Clean, intuitive design with responsive layout\n"
                content += "• **Interactive Components:** Dynamic user interactions and real-time feedback\n"
                content += "• **Cross-Platform Compatibility:** Works seamlessly across different browsers and devices\n"
                content += "• **Accessibility Features:** WCAG compliant design for inclusive user experience\n\n"
                
                content += "#### Technical Features\n"
                content += "• **Component-Based Architecture:** Modular and reusable UI components\n"
                content += "• **State Management:** Efficient data flow and application state handling\n"
                content += "• **Performance Optimization:** Fast loading times and smooth animations\n"
                content += "• **Modern Build Pipeline:** Automated testing, bundling, and deployment\n\n"
                
            elif project_type == 'web_api':
                content += "#### API Functionality\n"
                content += "• **RESTful API Design:** Well-structured endpoints following REST principles\n"
                content += "• **Data Processing:** Efficient handling of requests and responses\n"
                content += "• **Authentication & Security:** Secure user authentication and authorization\n"
                content += "• **Error Handling:** Comprehensive error management and logging\n\n"
                
                content += "#### Performance & Scalability\n"
                content += "• **High Performance:** Optimized for fast response times\n"
                content += "• **Scalable Architecture:** Designed to handle increasing load\n"
                content += "• **Database Integration:** Efficient data storage and retrieval\n"
                content += "• **Monitoring & Analytics:** Built-in performance tracking\n\n"
                
            else:
                primary_lang = max(languages.keys(), key=lambda k: languages[k]) if languages else 'Unknown'
                content += "#### Core Functionality\n"
                content += f"• **{primary_lang} Implementation:** Professional-grade code with modern practices\n"
                content += "• **Modular Design:** Clean architecture with separation of concerns\n"
                content += "• **Extensible Framework:** Easy to customize and extend functionality\n"
                content += "• **Comprehensive Documentation:** Well-documented codebase and APIs\n\n"
                
                content += "#### Quality & Maintenance\n"
                content += "• **Code Quality:** Following industry best practices and standards\n"
                content += "• **Testing Coverage:** Comprehensive test suite for reliability\n"
                content += "• **Version Control:** Proper Git workflow and branching strategy\n"
                content += "• **Continuous Integration:** Automated testing and deployment pipeline\n\n"
        
        # Use Cases subsection
        content += "### Use Cases\n\n"
        if project_type == 'web_frontend':
            content += "• **Portfolio Showcase:** Demonstrate web development skills and projects\n"
            content += "• **Business Website:** Professional online presence for companies\n"
            content += "• **Interactive Dashboard:** Data visualization and user management\n"
            content += "• **E-commerce Platform:** Online shopping and product catalog\n"
        elif project_type == 'web_api':
            content += "• **Mobile App Backend:** Provide data and services for mobile applications\n"
            content += "• **Third-Party Integration:** Connect with external services and APIs\n"
            content += "• **Microservices Architecture:** Part of larger distributed system\n"
            content += "• **Data Processing Pipeline:** Handle and transform large datasets\n"
        else:
            content += "• **Development Learning:** Educational resource for software development\n"
            content += "• **Production Deployment:** Ready-to-use solution for real-world applications\n"
            content += "• **Code Reference:** Example implementation for similar projects\n"
            content += "• **Foundation Framework:** Starting point for custom development\n"
        content += "\n"
        
        # Feature Highlights subsection
        content += "### Feature Highlights\n\n"
        
        # Analyze file structure for specific features
        feature_indicators = {
            'authentication': ['auth', 'login', 'jwt', 'passport'],
            'database': ['db', 'database', 'sql', 'mongo', 'redis'],
            'testing': ['test', 'spec', 'jest', 'pytest'],
            'api': ['api', 'endpoint', 'route', 'controller'],
            'ui_components': ['component', 'widget', 'ui', 'button'],
            'styling': ['css', 'scss', 'style', 'theme'],
            'build_tools': ['webpack', 'babel', 'gulp', 'grunt'],
            'deployment': ['docker', 'deploy', 'ci', 'cd']
        }
        
        detected_features = []
        for feature, indicators in feature_indicators.items():
            if any(indicator in str(files).lower() for indicator in indicators):
                detected_features.append(feature)
        
        if detected_features:
            for feature in detected_features[:6]:  # Limit to top 6 features
                feature_name = feature.replace('_', ' ').title()
                content += f"• **{feature_name}:** Advanced implementation with modern best practices\n"
        else:
            content += "• **Professional Architecture:** Well-structured and maintainable codebase\n"
            content += "• **Modern Technologies:** Built with current industry standards\n"
            content += "• **Scalable Design:** Prepared for future growth and enhancements\n"
        
        content += "\n"
        
        return content
    
    def _generate_enhanced_tech_stack_template(self, repo_data: Dict[str, Any]) -> str:
        """Generate comprehensive Technology Stack section."""
        languages = repo_data.get('languages', {})
        files = repo_data.get('files', [])
        project_type = self._detect_project_type(repo_data)
        
        content = "## Technology Stack\n\n"
        content += "This project leverages modern technologies and frameworks to deliver a robust, scalable, and maintainable solution. "
        content += "The technology choices reflect current industry best practices and ensure optimal performance and developer experience.\n\n"
        
        # Programming Languages
        if languages:
            content += "### Programming Languages\n\n"
            primary_lang = max(languages.keys(), key=lambda k: languages[k])
            
            for lang, count in sorted(languages.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / sum(languages.values())) * 100
                if lang == primary_lang:
                    content += f"- **{lang}** (Primary): {percentage:.1f}% - {count} files\n"
                    if lang == 'TypeScript':
                        content += "  - Type-safe JavaScript with enhanced developer experience\n"
                        content += "  - Compile-time error checking and IntelliSense support\n"
                    elif lang == 'JavaScript':
                        content += "  - Dynamic scripting for interactive web functionality\n"
                        content += "  - ES6+ features for modern development practices\n"
                    elif lang == 'Python':
                        content += "  - High-level programming with extensive library ecosystem\n"
                        content += "  - Excellent for rapid development and prototyping\n"
                else:
                    content += f"- **{lang}**: {percentage:.1f}% - {count} files\n"
            content += "\n"
        
        # Frontend Framework (for web projects)
        if project_type in ['web_frontend', 'web_project']:
            content += "### Frontend Framework\n\n"
            
            # Detect specific frameworks
            file_content = str(files).lower()
            if 'react' in file_content or 'jsx' in file_content:
                content += "- **React.js**: Component-based UI library for building interactive interfaces\n"
                content += "  - Virtual DOM for optimal performance\n"
                content += "  - Extensive ecosystem and community support\n"
                content += "  - Hooks for state management and lifecycle methods\n"
            elif 'vue' in file_content:
                content += "- **Vue.js**: Progressive framework for building user interfaces\n"
                content += "  - Reactive data binding and component system\n"
                content += "  - Gentle learning curve with powerful features\n"
            elif 'angular' in file_content:
                content += "- **Angular**: Full-featured framework for web applications\n"
                content += "  - TypeScript-first development approach\n"
                content += "  - Comprehensive tooling and CLI support\n"
            else:
                content += "- **Modern Web Technologies**: HTML5, CSS3, and JavaScript ES6+\n"
                content += "  - Semantic markup and responsive design principles\n"
                content += "  - Modern CSS features and layout techniques\n"
            content += "\n"
        
        # 3D Graphics & Animation (if applicable)
        if any(indicator in str(files).lower() for indicator in ['three', 'webgl', 'canvas', 'animation']):
            content += "### 3D Graphics & Animation\n\n"
            content += "- **Three.js**: Powerful 3D graphics library for web browsers\n"
            content += "  - WebGL-based rendering for high-performance 3D graphics\n"
            content += "  - Comprehensive scene graph and animation system\n"
            content += "  - Cross-platform compatibility and mobile support\n"
            content += "- **WebGL**: Low-level graphics API for hardware-accelerated rendering\n"
            content += "- **Canvas API**: 2D graphics and animation capabilities\n\n"
        
        # Development Tools
        content += "### Development Tools\n\n"
        
        # Detect build tools and development dependencies
        file_names = [str(f).lower() for f in files]
        
        build_tools = []
        if any('webpack' in f for f in file_names):
            build_tools.append('**Webpack**: Module bundler and build tool')
        if any('vite' in f for f in file_names):
            build_tools.append('**Vite**: Fast build tool and development server')
        if any('babel' in f for f in file_names):
            build_tools.append('**Babel**: JavaScript compiler for modern syntax support')
        if any('eslint' in f for f in file_names):
            build_tools.append('**ESLint**: Code linting and quality enforcement')
        if any('prettier' in f for f in file_names):
            build_tools.append('**Prettier**: Code formatting and style consistency')
        if any('jest' in f or 'test' in f for f in file_names):
            build_tools.append('**Testing Framework**: Automated testing and quality assurance')
        
        if build_tools:
            for tool in build_tools:
                content += f"- {tool}\n"
        else:
            content += "- **Modern Development Stack**: Industry-standard tools and practices\n"
            content += "- **Code Quality Tools**: Linting, formatting, and testing utilities\n"
            content += "- **Build Optimization**: Automated bundling and optimization processes\n"
        
        # Package Management
        if any('package.json' in f for f in file_names):
            content += "- **npm/yarn**: Package management and dependency resolution\n"
        elif any('requirements.txt' in f or 'pyproject.toml' in f for f in file_names):
            content += "- **pip/Poetry**: Python package management and virtual environments\n"
        elif any('pom.xml' in f or 'build.gradle' in f for f in file_names):
            content += "- **Maven/Gradle**: Java build automation and dependency management\n"
        
        content += "\n"
        
        # File Breakdown
        content += "### File Breakdown\n\n"
        if languages:
            content += "| Language | Files | Percentage | Purpose |\n"
            content += "|----------|-------|------------|---------|\n"
            
            for lang, count in sorted(languages.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / sum(languages.values())) * 100
                purpose = self._get_language_purpose(lang, project_type)
                content += f"| {lang} | {count} | {percentage:.1f}% | {purpose} |\n"
            content += "\n"
        
        # Architecture Overview
        content += "### Architecture Overview\n\n"
        if project_type == 'web_frontend':
            content += "- **Component-Based Architecture**: Modular UI components for reusability\n"
            content += "- **State Management**: Centralized application state handling\n"
            content += "- **Responsive Design**: Mobile-first approach with flexible layouts\n"
            content += "- **Performance Optimization**: Code splitting and lazy loading\n"
        elif project_type == 'web_api':
            content += "- **RESTful API Design**: Resource-based endpoints with HTTP methods\n"
            content += "- **Layered Architecture**: Separation of concerns with distinct layers\n"
            content += "- **Database Integration**: Efficient data persistence and retrieval\n"
            content += "- **Security Implementation**: Authentication, authorization, and validation\n"
        else:
            content += "- **Modular Design**: Clean separation of functionality and concerns\n"
            content += "- **Scalable Structure**: Organized codebase for easy maintenance\n"
            content += "- **Best Practices**: Following industry standards and conventions\n"
            content += "- **Documentation**: Comprehensive code documentation and comments\n"
        
        content += "\n"
        
        return content
    
    def _get_language_purpose(self, language: str, project_type: str) -> str:
        """Get the purpose description for a programming language in the context of the project."""
        purposes = {
            'TypeScript': 'Type-safe application logic and components',
            'JavaScript': 'Dynamic functionality and user interactions',
            'HTML': 'Markup structure and semantic content',
            'CSS': 'Styling, layout, and visual presentation',
            'SCSS': 'Advanced styling with variables and mixins',
            'Python': 'Backend logic and data processing',
            'Java': 'Enterprise application development',
            'C++': 'System-level programming and performance',
            'C#': '.NET application development',
            'Go': 'Concurrent backend services',
            'Rust': 'Memory-safe system programming',
            'PHP': 'Server-side web development',
            'Ruby': 'Web application framework',
            'Swift': 'iOS and macOS application development',
            'Kotlin': 'Android application development'
        }
        
        return purposes.get(language, 'Application development and functionality')
    
    def _generate_enhanced_setup_template(self, repo_data: Dict[str, Any]) -> str:
        """Generate comprehensive Setup Instructions section."""
        languages = repo_data.get('languages', {})
        files = repo_data.get('files', [])
        file_names = [str(f).lower() for f in files]
        project_type = self._detect_project_type(repo_data)
        project_name = repo_data.get('name', 'project')
        
        content = "## Setup Instructions\n\n"
        content += "This section provides comprehensive instructions for setting up the development environment and running the project locally. "
        content += "Follow these steps carefully to ensure a smooth setup process.\n\n"
        
        # Prerequisites
        content += "### Prerequisites\n\n"
        content += "Before you begin, ensure you have the following software installed on your system:\n\n"
        
        if any('package.json' in f for f in file_names):
            content += "#### Required Software\n\n"
            content += "- **Node.js** (v16.0.0 or higher)\n"
            content += "  - Download from [nodejs.org](https://nodejs.org/)\n"
            content += "  - Verify installation: `node --version`\n"
            content += "- **npm** (v8.0.0 or higher) or **yarn** (v1.22.0 or higher)\n"
            content += "  - npm comes with Node.js\n"
            content += "  - For yarn: `npm install -g yarn`\n"
            content += "- **Git** for version control\n"
            content += "  - Download from [git-scm.com](https://git-scm.com/)\n\n"
            
            if project_type == 'web_frontend':
                content += "#### Optional Tools\n\n"
                content += "- **Visual Studio Code** with recommended extensions:\n"
                content += "  - ES7+ React/Redux/React-Native snippets\n"
                content += "  - Prettier - Code formatter\n"
                content += "  - ESLint\n"
                content += "  - Auto Rename Tag\n"
                content += "- **Chrome DevTools** for debugging\n\n"
                
        elif any('requirements.txt' in f for f in file_names):
            content += "#### Required Software\n\n"
            content += "- **Python** (v3.8.0 or higher)\n"
            content += "  - Download from [python.org](https://python.org/)\n"
            content += "  - Verify installation: `python --version`\n"
            content += "- **pip** (Python package installer)\n"
            content += "  - Usually comes with Python\n"
            content += "  - Verify installation: `pip --version`\n"
            content += "- **Git** for version control\n\n"
            
            content += "#### Recommended Tools\n\n"
            content += "- **Virtual Environment** (venv or conda)\n"
            content += "- **IDE**: PyCharm, VS Code, or similar\n"
            content += "- **Database**: PostgreSQL, MySQL, or SQLite\n\n"
        else:
            content += "- **Git** for version control\n"
            content += "- **Code Editor** (VS Code, Sublime Text, etc.)\n"
            content += "- **Terminal/Command Line** access\n\n"
        
        # System Requirements
        content += "### System Requirements\n\n"
        content += "#### Minimum Requirements\n\n"
        content += "- **Operating System**: Windows 10, macOS 10.15, or Linux (Ubuntu 18.04+)\n"
        content += "- **RAM**: 4GB minimum, 8GB recommended\n"
        content += "- **Storage**: 2GB free space\n"
        content += "- **Internet Connection**: Required for initial setup and dependencies\n\n"
        
        content += "#### Recommended Specifications\n\n"
        content += "- **RAM**: 16GB for optimal performance\n"
        content += "- **CPU**: Multi-core processor (Intel i5/AMD Ryzen 5 or better)\n"
        content += "- **Storage**: SSD for faster build times\n\n"
        
        # Step-by-Step Installation
        content += "### Step-by-Step Installation\n\n"
        
        # Step 1: Clone Repository
        content += "#### Step 1: Clone the Repository\n\n"
        content += "```bash\n"
        content += "# Clone the repository\n"
        content += "git clone https://github.com/username/" + project_name + ".git\n\n"
        content += "# Navigate to project directory\n"
        content += "cd " + project_name + "\n"
        content += "```\n\n"
        
        # Step 2: Install Dependencies
        content += "#### Step 2: Install Dependencies\n\n"
        
        if any('package.json' in f for f in file_names):
            content += "**Using npm:**\n"
            content += "```bash\n"
            content += "# Install all dependencies\n"
            content += "npm install\n\n"
            content += "# Install development dependencies\n"
            content += "npm install --dev\n"
            content += "```\n\n"
            
            content += "**Using yarn (alternative):**\n"
            content += "```bash\n"
            content += "# Install all dependencies\n"
            content += "yarn install\n\n"
            content += "# Or simply\n"
            content += "yarn\n"
            content += "```\n\n"
            
        elif any('requirements.txt' in f for f in file_names):
            content += "**Create and activate virtual environment:**\n"
            content += "```bash\n"
            content += "# Create virtual environment\n"
            content += "python -m venv venv\n\n"
            content += "# Activate virtual environment\n"
            content += "# On Windows:\n"
            content += "venv\\Scripts\\activate\n\n"
            content += "# On macOS/Linux:\n"
            content += "source venv/bin/activate\n"
            content += "```\n\n"
            
            content += "**Install Python dependencies:**\n"
            content += "```bash\n"
            content += "# Install required packages\n"
            content += "pip install -r requirements.txt\n\n"
            content += "# Install development dependencies (if available)\n"
            content += "pip install -r requirements-dev.txt\n"
            content += "```\n\n"
        
        # Step 3: Verify Installation
        content += "#### Step 3: Verify Installation\n\n"
        
        if any('package.json' in f for f in file_names):
            content += "```bash\n"
            content += "# Check if all dependencies are installed\n"
            content += "npm list --depth=0\n\n"
            content += "# Run development server (if available)\n"
            content += "npm run dev\n"
            content += "# or\n"
            content += "npm start\n"
            content += "```\n\n"
        elif any('requirements.txt' in f for f in file_names):
            content += "```bash\n"
            content += "# Verify Python installation\n"
            content += "python --version\n\n"
            content += "# Check installed packages\n"
            content += "pip list\n\n"
            content += "# Run the application (adjust command as needed)\n"
            content += "python main.py\n"
            content += "```\n\n"
        
        # Environment Setup
        content += "#### Step 4: Environment Setup\n\n"
        content += "1. **Copy environment template:**\n"
        content += "   ```bash\n"
        content += "   cp .env.example .env\n"
        content += "   ```\n\n"
        content += "2. **Configure environment variables** (see Configuration section)\n\n"
        content += "3. **Initialize database** (if applicable):\n"
        content += "   ```bash\n"
        content += "   # Run database migrations\n"
        content += "   npm run migrate\n"
        content += "   # or for Python projects\n"
        content += "   python manage.py migrate\n"
        content += "   ```\n\n"
        
        return content
    
    def _generate_enhanced_configuration_template(self, repo_data: Dict[str, Any]) -> str:
        """Generate comprehensive Configuration Required section."""
        files = repo_data.get('files', [])
        file_names = [str(f).lower() for f in files]
        project_type = self._detect_project_type(repo_data)
        languages = repo_data.get('languages', {})
        
        content = "## Configuration Required\n\n"
        content += "This section outlines all necessary configuration steps to ensure the application runs correctly in your environment. "
        content += "Proper configuration is essential for security, performance, and functionality.\n\n"
        
        # Environment Variables
        content += "### Environment Variables\n\n"
        content += "Environment variables are used to configure the application for different environments (development, staging, production) "
        content += "and to store sensitive information securely.\n\n"
        
        content += "#### Required Variables\n\n"
        content += "Create a `.env` file in the project root directory and configure the following variables:\n\n"
        
        if project_type == 'web_frontend':
            content += "```bash\n"
            content += "# Application Configuration\n"
            content += "NODE_ENV=development\n"
            content += "PORT=3000\n"
            content += "PUBLIC_URL=http://localhost:3000\n\n"
            
            content += "# API Configuration\n"
            content += "REACT_APP_API_BASE_URL=http://localhost:8000/api\n"
            content += "REACT_APP_API_VERSION=v1\n\n"
            
            content += "# Third-Party Services\n"
            content += "REACT_APP_GOOGLE_ANALYTICS_ID=your_ga_id\n"
            content += "REACT_APP_FIREBASE_API_KEY=your_firebase_key\n"
            content += "REACT_APP_STRIPE_PUBLIC_KEY=your_stripe_public_key\n\n"
            
            content += "# Development Tools\n"
            content += "GENERATE_SOURCEMAP=true\n"
            content += "ESLINT_NO_DEV_ERRORS=true\n"
            content += "```\n\n"
            
        elif project_type == 'web_api':
            content += "```bash\n"
            content += "# Server Configuration\n"
            content += "NODE_ENV=development\n"
            content += "PORT=8000\n"
            content += "HOST=localhost\n\n"
            
            content += "# Database Configuration\n"
            content += "DATABASE_URL=postgresql://username:password@localhost:5432/dbname\n"
            content += "DB_HOST=localhost\n"
            content += "DB_PORT=5432\n"
            content += "DB_NAME=your_database\n"
            content += "DB_USER=your_username\n"
            content += "DB_PASSWORD=your_password\n\n"
            
            content += "# Authentication & Security\n"
            content += "JWT_SECRET=your_super_secret_jwt_key\n"
            content += "JWT_EXPIRES_IN=7d\n"
            content += "BCRYPT_ROUNDS=12\n"
            content += "SESSION_SECRET=your_session_secret\n\n"
            
            content += "# External APIs\n"
            content += "STRIPE_SECRET_KEY=your_stripe_secret_key\n"
            content += "SENDGRID_API_KEY=your_sendgrid_key\n"
            content += "AWS_ACCESS_KEY_ID=your_aws_access_key\n"
            content += "AWS_SECRET_ACCESS_KEY=your_aws_secret_key\n"
            content += "```\n\n"
            
        else:
            content += "```bash\n"
            content += "# Application Settings\n"
            content += "APP_ENV=development\n"
            content += "APP_DEBUG=true\n"
            content += "APP_PORT=3000\n\n"
            
            content += "# Database Configuration\n"
            content += "DATABASE_URL=your_database_connection_string\n\n"
            
            content += "# API Keys and Secrets\n"
            content += "API_SECRET_KEY=your_secret_key\n"
            content += "ENCRYPTION_KEY=your_encryption_key\n"
            content += "```\n\n"
        
        # TypeScript Configuration (if applicable)
        if 'TypeScript' in languages:
            content += "### TypeScript Configuration\n\n"
            content += "The project uses TypeScript for type safety and enhanced developer experience. "
            content += "Configuration is managed through `tsconfig.json`.\n\n"
            
            content += "#### Key Configuration Options\n\n"
            content += "```json\n"
            content += "{\n"
            content += "  \"compilerOptions\": {\n"
            content += "    \"target\": \"ES2020\",\n"
            content += "    \"lib\": [\"DOM\", \"DOM.Iterable\", \"ES6\"],\n"
            content += "    \"allowJs\": true,\n"
            content += "    \"skipLibCheck\": true,\n"
            content += "    \"esModuleInterop\": true,\n"
            content += "    \"allowSyntheticDefaultImports\": true,\n"
            content += "    \"strict\": true,\n"
            content += "    \"forceConsistentCasingInFileNames\": true,\n"
            content += "    \"moduleResolution\": \"node\",\n"
            content += "    \"resolveJsonModule\": true,\n"
            content += "    \"isolatedModules\": true,\n"
            content += "    \"noEmit\": true,\n"
            content += "    \"jsx\": \"react-jsx\"\n"
            content += "  },\n"
            content += "  \"include\": [\"src\"],\n"
            content += "  \"exclude\": [\"node_modules\", \"build\"]\n"
            content += "}\n"
            content += "```\n\n"
            
            content += "#### Path Mapping\n\n"
            content += "Configure path aliases for cleaner imports:\n\n"
            content += "```json\n"
            content += "{\n"
            content += "  \"compilerOptions\": {\n"
            content += "    \"baseUrl\": \"src\",\n"
            content += "    \"paths\": {\n"
            content += "      \"@components/*\": [\"components/*\"],\n"
            content += "      \"@utils/*\": [\"utils/*\"],\n"
            content += "      \"@assets/*\": [\"assets/*\"],\n"
            content += "      \"@types/*\": [\"types/*\"]\n"
            content += "    }\n"
            content += "  }\n"
            content += "}\n"
            content += "```\n\n"
        
        # Build Configuration
        content += "### Build Configuration\n\n"
        
        if any('webpack' in f for f in file_names):
            content += "#### Webpack Configuration\n\n"
            content += "The project uses Webpack for module bundling and build optimization:\n\n"
            content += "- **Development**: Hot module replacement and source maps\n"
            content += "- **Production**: Code splitting, minification, and optimization\n"
            content += "- **Assets**: Image optimization and font loading\n"
            content += "- **Plugins**: HTML generation, CSS extraction, and bundle analysis\n\n"
            
        elif any('vite' in f for f in file_names):
            content += "#### Vite Configuration\n\n"
            content += "The project uses Vite for fast development and optimized builds:\n\n"
            content += "- **Development**: Lightning-fast HMR and instant server start\n"
            content += "- **Production**: Rollup-based bundling with tree-shaking\n"
            content += "- **Plugins**: Vue/React support, TypeScript, and CSS preprocessing\n\n"
        
        # Database Configuration (if applicable)
        if any(indicator in str(files).lower() for indicator in ['database', 'db', 'sql', 'mongo']):
            content += "### Database Configuration\n\n"
            content += "#### Connection Setup\n\n"
            content += "1. **Install database server** (PostgreSQL, MySQL, or MongoDB)\n"
            content += "2. **Create database** for the application\n"
            content += "3. **Configure connection string** in environment variables\n"
            content += "4. **Run migrations** to set up database schema\n\n"
            
            content += "#### Migration Commands\n\n"
            content += "```bash\n"
            content += "# Run database migrations\n"
            content += "npm run migrate\n\n"
            content += "# Seed database with initial data\n"
            content += "npm run seed\n\n"
            content += "# Reset database (development only)\n"
            content += "npm run db:reset\n"
            content += "```\n\n"
        
        # Security Configuration
        content += "### Security Configuration\n\n"
        content += "#### Important Security Notes\n\n"
        content += "- **Never commit** `.env` files to version control\n"
        content += "- **Use strong passwords** and secure API keys\n"
        content += "- **Enable HTTPS** in production environments\n"
        content += "- **Regularly update** dependencies for security patches\n"
        content += "- **Implement rate limiting** for API endpoints\n\n"
        
        content += "#### Environment-Specific Settings\n\n"
        content += "| Environment | Debug Mode | HTTPS | Database | Caching |\n"
        content += "|-------------|------------|-------|----------|---------|\n"
        content += "| Development | Enabled | Optional | Local | Disabled |\n"
        content += "| Staging | Limited | Required | Remote | Enabled |\n"
        content += "| Production | Disabled | Required | Remote | Enabled |\n\n"
        
        return content
    
    def _generate_usage_template(self, repo_data: Dict[str, Any]) -> str:
        """Generate Usage section."""
        content = "## Usage\n\n"
        
        entry_points = repo_data.get('entry_points', [])
        primary_lang = self._get_primary_language(repo_data)
        
        if entry_points:
            content += "### Basic Usage\n\n"
            for entry_point in entry_points:
                if entry_point.endswith('.py'):
                    content += f"```bash\npython {entry_point}\n```\n\n"
                elif entry_point.endswith('.js'):
                    content += f"```bash\nnode {entry_point}\n```\n\n"
                elif entry_point.endswith('.java'):
                    content += f"```bash\njava {entry_point.replace('.java', '')}\n```\n\n"
        else:
            content += "### Basic Usage\n\n"
            content += "[Usage examples to be documented]\n\n"
        
        # Add example based on project type
        project_type = self._detect_project_type(repo_data)
        
        if project_type == 'web_api':
            content += "### API Usage\n\n"
            content += "```bash\n"
            content += "# Start the server\n"
            content += "# Make API requests\n"
            content += "curl -X GET http://localhost:8000/api/endpoint\n"
            content += "```\n\n"
        
        return content
    
    def _generate_api_template(self, repo_data: Dict[str, Any]) -> str:
        """Generate API Documentation section."""
        content = "## API Documentation\n\n"
        
        content += "### Base URL\n\n"
        content += "```\n"
        content += "http://localhost:8000/api\n"
        content += "```\n\n"
        
        content += "### Endpoints\n\n"
        content += "#### GET /endpoint\n\n"
        content += "Description of the endpoint.\n\n"
        content += "**Response:**\n"
        content += "```json\n"
        content += "{\n"
        content += '  "status": "success",\n'
        content += '  "data": {}\n'
        content += "}\n"
        content += "```\n\n"
        
        return content
    
    def _generate_structure_template(self, repo_data: Dict[str, Any]) -> str:
        """Generate Project Structure section."""
        content = "## Project Structure\n\n"
        
        structure = repo_data.get('structure', {})
        tree = structure.get('tree', {})
        
        if tree:
            content += "```\n"
            content += self._format_tree(tree)
            content += "```\n\n"
        
        # Describe key directories
        directories = structure.get('directories', [])
        if directories:
            content += "### Directory Description\n\n"
            for directory in directories:
                content += f"- `{directory}/`: [Description needed]\n"
            content += "\n"
        
        return content
    
    def _format_tree(self, tree: Dict[str, Any], prefix: str = "", is_last: bool = True) -> str:
        """Format tree structure for display."""
        result = ""
        name = tree.get('name', '')
        tree_type = tree.get('type', 'file')
        
        # Add current node
        connector = "└── " if is_last else "├── "
        result += f"{prefix}{connector}{name}"
        if tree_type == 'directory':
            result += "/"
        result += "\n"
        
        # Add children
        children = tree.get('children', [])
        if children:
            new_prefix = prefix + ("    " if is_last else "│   ")
            for i, child in enumerate(children):
                is_last_child = i == len(children) - 1
                result += self._format_tree(child, new_prefix, is_last_child)
        
        return result
    
    def _generate_development_template(self, repo_data: Dict[str, Any]) -> str:
        """Generate Development section."""
        content = "## Development\n\n"
        
        content += "### Development Setup\n\n"
        content += "1. Follow the installation instructions\n"
        content += "2. Install development dependencies\n"
        content += "3. Set up your development environment\n\n"
        
        # Check for development tools
        config_files = repo_data.get('config_files', [])
        
        if 'Makefile' in config_files:
            content += "### Build Commands\n\n"
            content += "```bash\n"
            content += "make build\n"
            content += "make test\n"
            content += "make clean\n"
            content += "```\n\n"
        
        return content
    
    def _generate_testing_template(self, repo_data: Dict[str, Any]) -> str:
        """Generate Testing section."""
        content = "## Testing\n\n"
        
        tests = repo_data.get('tests', {})
        test_dirs = tests.get('directories', [])
        test_files = tests.get('files', [])
        frameworks = tests.get('frameworks', [])
        
        if test_dirs or test_files:
            content += "### Running Tests\n\n"
            
            if 'pytest' in frameworks:
                content += "```bash\n"
                content += "pytest\n"
                content += "```\n\n"
            elif 'jest' in frameworks:
                content += "```bash\n"
                content += "npm test\n"
                content += "```\n\n"
            else:
                content += "[Test running instructions to be documented]\n\n"
            
            if test_dirs:
                content += "### Test Structure\n\n"
                for test_dir in test_dirs:
                    content += f"- `{test_dir}`: Test files\n"
                content += "\n"
        else:
            content += "No tests found in the repository. Consider adding tests to improve code quality.\n\n"
        
        return content
    
    def _generate_deployment_template(self, repo_data: Dict[str, Any]) -> str:
        """Generate Deployment section."""
        content = "## Deployment\n\n"
        
        config_files = repo_data.get('config_files', [])
        
        if any('docker' in f.lower() for f in config_files):
            content += "### Docker Deployment\n\n"
            content += "```bash\n"
            content += "docker build -t project-name .\n"
            content += "docker run -p 8000:8000 project-name\n"
            content += "```\n\n"
        
        content += "### Production Considerations\n\n"
        content += "- Environment variables configuration\n"
        content += "- Database setup and migrations\n"
        content += "- Security considerations\n"
        content += "- Monitoring and logging\n\n"
        
        return content
    
    def _generate_license_template(self, repo_data: Dict[str, Any]) -> str:
        """Generate License section."""
        content = "## License\n\n"
        
        license_file = repo_data.get('license')
        
        if license_file:
            content += f"This project is licensed under the terms specified in the `{license_file}` file.\n\n"
        else:
            content += "License information not found. Please add a LICENSE file to specify the terms of use.\n\n"
        
        return content
    
    # Helper methods
    
    def _get_primary_language(self, repo_data: Dict[str, Any]) -> str:
        """Get the primary programming language."""
        languages = repo_data.get('languages', {})
        if languages:
            return max(languages.keys(), key=lambda k: languages[k])
        return 'unknown'
    
    def _detect_project_type(self, repo_data: Dict[str, Any]) -> str:
        """Detect the type of project."""
        # This is a simplified version of the detection logic
        dependencies = repo_data.get('dependencies', {})
        
        # Check for web frameworks
        web_indicators = ['flask', 'django', 'express', 'spring']
        for lang_deps in dependencies.values():
            if isinstance(lang_deps, dict):
                for dep_file, deps in lang_deps.items():
                    if isinstance(deps, dict) and 'dependencies' in deps:
                        deps_dict = deps['dependencies']
                        if isinstance(deps_dict, dict):
                            dep_names = list(deps_dict.keys())
                            if any(indicator in ' '.join(dep_names).lower() for indicator in web_indicators):
                                return 'web_api'
        
        return 'application'
    
    def _save_filled_sections(self, filled_doc: Dict[str, Any]):
        """
        Save filled sections for reference.
        
        Args:
            filled_doc: Filled documentation data
        """
        output_path = self.prompts_dir / "filled_sections.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(filled_doc, f, indent=2, default=str)
        
        print(f"📄 Filled sections saved to {output_path}")


if __name__ == "__main__":
    # Test the section filler
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python section_filler.py <outline.json> <repo_data.json>")
        sys.exit(1)
    
    outline_path = Path(sys.argv[1])
    repo_data_path = Path(sys.argv[2])
    
    if not outline_path.exists():
        print(f"Outline file does not exist: {outline_path}")
        sys.exit(1)
    
    if not repo_data_path.exists():
        print(f"Repository data file does not exist: {repo_data_path}")
        sys.exit(1)
    
    with open(outline_path, 'r', encoding='utf-8') as f:
        outline = json.load(f)
    
    with open(repo_data_path, 'r', encoding='utf-8') as f:
        repo_data = json.load(f)
    
    filler = SectionFiller()
    ai_context = {}  # Empty context for testing
    filled_doc = filler.fill_sections(outline, repo_data, ai_context)
    
    print("\n📄 Filled Documentation:")
    for title, section in filled_doc['sections'].items():
        print(f"\n### {title}")
        print(f"Priority: {section['priority']}")
        print(f"Word count: {section['word_count']}")
        print(f"Content preview: {section['content'][:100]}...")