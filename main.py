#!/usr/bin/env python3
"""
PromptSwitch Agent v2 - Main Entry Point

Meta-Prompt: You are PromptSwitch v2, an advanced AI documentation agent that follows
DX engineering best practices including meta-prompting, prompt chaining, modular design,
and regeneration blocks for continuous improvement.

An AI agent that reads GitHub repositories and generates comprehensive project documentation
with integrated testing, quality review, and iterative improvement capabilities.
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from agents.repo_cloner import RepoCloner
from agents.parser import RepoParser
from agents.doc_planner import DocPlanner
from agents.section_filler import SectionFiller
from agents.formatter import DocumentFormatter
from agents.test_generator import TestGenerator
from agents.review_agent import ReviewAgent


class PromptSwitchAgent:
    """
    Main PromptSwitch v2 agent orchestrator.
    
    Meta-Prompt Context:
    - Role: Senior Documentation Engineering Agent
    - Task: Orchestrate full documentation lifecycle with quality assurance
    - Approach: Prompt chaining with validation and regeneration loops
    - Standards: DX best practices with measurable quality outcomes
    """
    
    def __init__(self, output_dir="outputs", prompts_dir="prompts"):
        self.output_dir = Path(output_dir)
        self.prompts_dir = Path(prompts_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.prompts_dir.mkdir(exist_ok=True)
        
        # Initialize agent components (Prompt Chain)
        self.cloner = RepoCloner()
        self.parser = RepoParser()
        self.planner = DocPlanner()
        self.filler = SectionFiller()
        self.formatter = DocumentFormatter()
        self.test_generator = TestGenerator(prompts_dir=str(self.prompts_dir), 
                                          outputs_dir=str(self.output_dir))
        self.reviewer = ReviewAgent(prompts_dir=str(self.prompts_dir), 
                                   outputs_dir=str(self.output_dir))
        
        # Load AI learning context and system prompts
        self.ai_learning_path = project_root / "Learn_AI"
        self.project_docs_path = project_root / "Project Docs"
        self.system_prompt = self._load_system_prompt()
    
    def _extract_repo_name(self, github_url: str) -> str:
        """
        Extract repository name from GitHub URL for use in output filenames.
        
        Args:
            github_url: GitHub repository URL
            
        Returns:
            Repository name in format 'owner_repo'
        """
        import re
        
        # Remove .git suffix if present
        url = github_url.rstrip('.git')
        
        # Extract owner and repo name from various GitHub URL formats
        patterns = [
            r'github\.com[:/]([^/]+)/([^/]+)/?$',  # https://github.com/owner/repo or git@github.com:owner/repo
            r'github\.com/([^/]+)/([^/]+)/.*',      # https://github.com/owner/repo/anything
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                owner, repo = match.groups()
                # Clean up any remaining path components
                repo = repo.split('/')[0]
                return f"{owner}_{repo}"
        
        # Fallback: use last part of URL
        return url.split('/')[-1] or "unknown_repo"
    
    def process_repository(self, github_url, output_filename="project_doc.md", 
                         enable_testing=True, enable_review=True):
        """
        Main processing pipeline implementing DX prompt chaining workflow.
        
        Meta-Prompt: Execute comprehensive documentation generation with
        integrated testing, quality review, and regeneration feedback loops.
        
        Args:
            github_url: Repository URL to process
            output_filename: Output documentation filename (will be prefixed with repo name)
            enable_testing: Whether to generate tests (default: True)
            enable_review: Whether to run quality review (default: True)
        
        Returns:
            Dict containing all generated outputs and quality metrics
        """
        print(f"🚀 PromptSwitch Agent v2 starting for: {github_url}")
        print(f"📋 System Prompt Loaded: {len(self.system_prompt)} characters")
        
        # Extract repository name for output filename
        repo_name = self._extract_repo_name(github_url)
        
        # Create repository-specific output filename
        if output_filename == "project_doc.md":  # Default filename
            base_filename = f"{repo_name}_documentation.md"
        else:
            # Preserve user-specified filename but add repo prefix
            name_parts = output_filename.rsplit('.', 1)
            if len(name_parts) == 2:
                base_filename = f"{repo_name}_{name_parts[0]}.{name_parts[1]}"
            else:
                base_filename = f"{repo_name}_{output_filename}"
        
        print(f"📝 Output will be saved as: {base_filename}")
        
        pipeline_results = {
            'start_time': datetime.utcnow().isoformat(),
            'github_url': github_url,
            'repo_name': repo_name,
            'output_filename': base_filename,
            'outputs': {},
            'quality_metrics': {},
            'errors': [],
            'success': False
        }
        
        try:
            # PHASE 1: Repository Analysis (Prompt Chain Step 1-2)
            print("\n=== PHASE 1: Repository Analysis ===")
            
            # Step 1: Clone repository or use local directory
            print("📥 Setting up repository...")
            
            # Check if input is a local directory or GitHub URL
            if os.path.isdir(github_url):
                repo_path = Path(github_url)
                print(f"📁 Using local directory: {repo_path}")
                # Update repo_name for local directories
                repo_name = repo_path.name
                # Update pipeline results with corrected repo name
                pipeline_results['repo_name'] = repo_name
                base_filename = f"{repo_name}_documentation.md" if output_filename == "project_doc.md" else f"{repo_name}_{output_filename}"
                pipeline_results['output_filename'] = base_filename
                print(f"📝 Updated output filename: {base_filename}")
            else:
                repo_path = self.cloner.clone_repo(github_url)
                print(f"📁 Repository cloned to: {repo_path}")
            
            # Step 2: Parse repository structure
            print("🔍 Parsing repository structure...")
            repo_data = self.parser.parse_repository(repo_path)
            pipeline_results['outputs']['repo_data'] = repo_data
            
            # Step 3: Load AI learning context
            print("🧠 Loading AI learning context...")
            ai_context = self._load_ai_context()
            
            # PHASE 2: Documentation Generation (Prompt Chain Step 3-5)
            print("\n=== PHASE 2: Documentation Generation ===")
            
            # Step 4: Generate document outline (Prompt Chain: Planning)
            print("📋 Generating document outline...")
            outline = self.planner.generate_outline(repo_data, ai_context)
            pipeline_results['outputs']['outline'] = outline
            
            # Step 5: Fill document sections (Prompt Chain: Content Generation)
            print("✍️ Filling document sections...")
            filled_doc = self.filler.fill_sections(outline, repo_data, ai_context)
            pipeline_results['outputs']['filled_sections'] = filled_doc
            
            # Step 6: Format and save final document (Prompt Chain: Formatting)
            print("📄 Formatting final document...")
            final_doc = self.formatter.format_document(filled_doc)
            
            # Save primary documentation (Markdown)
            output_path = self.output_dir / base_filename
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(final_doc)
            
            pipeline_results['outputs']['documentation_path'] = str(output_path)
            print(f"✅ Documentation generated: {output_path}")
            
            # Generate PDF version
            print("📄 Generating PDF version...")
            try:
                pdf_path = self.formatter.format_document(filled_doc, output_format='pdf', base_filename=base_filename)
                pipeline_results['outputs']['pdf_path'] = pdf_path
                print(f"✅ PDF generated: {pdf_path}")
            except Exception as e:
                error_msg = f"PDF generation failed: {str(e)}"
                print(f"⚠️ {error_msg}")
                pipeline_results['errors'].append(error_msg)
                
                # Fallback: Generate HTML and provide conversion instructions
                try:
                    print("📄 Generating HTML fallback for PDF conversion...")
                    html_path = self.formatter.format_document(filled_doc, output_format='html', base_filename=base_filename)
                    pipeline_results['outputs']['html_path'] = html_path
                    print(f"✅ HTML generated: {html_path}")
                    print("💡 To convert to PDF: Open HTML in browser and use 'Print to PDF'")
                except Exception as html_error:
                    fallback_error = f"HTML fallback also failed: {str(html_error)}"
                    print(f"⚠️ {fallback_error}")
                    pipeline_results['errors'].append(fallback_error)
            
            # Generate Claude Desktop Prompts
            print("🤖 Generating Claude Desktop prompts...")
            try:
                claude_prompts = self._generate_claude_prompts(github_url, repo_data, final_doc, base_filename)
                claude_prompts_filename = base_filename.replace('.md', '_claude_prompts.md')
                claude_prompts_path = self.output_dir / claude_prompts_filename
                
                with open(claude_prompts_path, 'w', encoding='utf-8') as f:
                    f.write(claude_prompts)
                
                pipeline_results['outputs']['claude_prompts_path'] = str(claude_prompts_path)
                print(f"✅ Claude Desktop prompts generated: {claude_prompts_path}")
            except Exception as e:
                error_msg = f"Claude prompts generation failed: {str(e)}"
                print(f"⚠️ {error_msg}")
                pipeline_results['errors'].append(error_msg)
            
            # PHASE 3: Test Generation (Prompt Chain Step 6)
            test_results = None
            if enable_testing:
                print("\n=== PHASE 3: Test Generation ===")
                try:
                    test_results = self.test_generator.generate_tests(repo_data, filled_doc)
                    pipeline_results['outputs']['test_results'] = test_results
                    print(f"✅ Test generation complete: {len(test_results.get('test_files', []))} test files")
                except Exception as e:
                    error_msg = f"Test generation failed: {str(e)}"
                    print(f"⚠️ {error_msg}")
                    pipeline_results['errors'].append(error_msg)
            
            # PHASE 4: Quality Review (Prompt Chain Step 7)
            review_results = None
            if enable_review:
                print("\n=== PHASE 4: Quality Review ===")
                try:
                    review_results = self.reviewer.review_documentation(
                        filled_doc, repo_data, test_results
                    )
                    pipeline_results['outputs']['review_results'] = review_results
                    pipeline_results['quality_metrics'] = review_results['quality_scores']
                    print(f"✅ Quality review complete: {review_results['overall_score']:.1f}/100")
                except Exception as e:
                    error_msg = f"Quality review failed: {str(e)}"
                    print(f"⚠️ {error_msg}")
                    pipeline_results['errors'].append(error_msg)
            
            # PHASE 5: Regeneration Block Creation (Prompt Chain Step 8)
            print("\n=== PHASE 5: Regeneration Block Creation ===")
            regeneration_block = self._generate_v2_regeneration_block(
                pipeline_results, repo_data, review_results, test_results
            )
            pipeline_results['outputs']['regeneration_block'] = regeneration_block
            
            # Final Summary
            pipeline_results['end_time'] = datetime.utcnow().isoformat()
            pipeline_results['success'] = True
            
            print("\n=== PIPELINE COMPLETE ===")
            print(f"📊 Quality Score: {pipeline_results['quality_metrics'].get('overall', 'N/A')}")
            print(f"🧪 Tests Generated: {len(test_results.get('test_files', []) if test_results else [])}")
            print(f"📝 Outputs: {len(pipeline_results['outputs'])} files")
            print(f"⚠️ Errors: {len(pipeline_results['errors'])}")
            
            # Display output files
            if 'documentation_path' in pipeline_results['outputs']:
                print(f"📄 Markdown: {pipeline_results['outputs']['documentation_path']}")
            if 'pdf_path' in pipeline_results['outputs']:
                print(f"📄 PDF: {pipeline_results['outputs']['pdf_path']}")
            elif 'html_path' in pipeline_results['outputs']:
                print(f"📄 HTML (for PDF conversion): {pipeline_results['outputs']['html_path']}")
            
            return pipeline_results
            
        except Exception as e:
            error_msg = f"Pipeline failed: {str(e)}"
            print(f"❌ {error_msg}")
            pipeline_results['errors'].append(error_msg)
            pipeline_results['success'] = False
            pipeline_results['end_time'] = datetime.utcnow().isoformat()
            raise
        finally:
            # Cleanup cloned repository (but not local directories)
            if 'repo_path' in locals() and not os.path.isdir(github_url):
                self.cloner.cleanup(repo_path)
                print(f"🧹 Cleaned up {repo_path}")
            elif 'repo_path' in locals():
                print(f"📁 Local directory preserved: {repo_path}")
    
    def _load_ai_context(self):
        """Load context from AI learning materials and project docs."""
        context = {
            'ai_learning': {},
            'project_docs': {},
            'past_outputs': []
        }
        
        # Load AI learning materials
        if self.ai_learning_path.exists():
            for file_path in self.ai_learning_path.rglob('*'):
                if file_path.is_file():
                    context['ai_learning'][file_path.name] = str(file_path)
        
        # Load project documentation
        if self.project_docs_path.exists():
            for file_path in self.project_docs_path.rglob('*.md'):
                if file_path.is_file():
                    with open(file_path, 'r', encoding='utf-8') as f:
                        context['project_docs'][file_path.name] = f.read()
        
        # Load past outputs for comparison
        if self.output_dir.exists():
            for file_path in self.output_dir.glob('*.md'):
                if file_path.is_file():
                    context['past_outputs'].append(str(file_path))
        
        return context
    
    def _load_system_prompt(self):
        """Load system prompt for meta-prompting context."""
        system_prompt_path = self.prompts_dir / "system_prompt.txt"
        if system_prompt_path.exists():
            with open(system_prompt_path, 'r', encoding='utf-8') as f:
                return f.read()
        return "PromptSwitch v2 System Prompt not found - using default behavior."
    
    def _generate_v2_regeneration_block(self, pipeline_results, repo_data, 
                                       review_results=None, test_results=None):
        """
        Generate comprehensive regeneration block following DX best practices.
        
        Meta-Prompt: Create structured handoff documentation that enables
        continuous improvement and tracks progress across iterations.
        """
        timestamp = datetime.utcnow().isoformat()
        
        # Calculate summary metrics
        total_outputs = len(pipeline_results['outputs'])
        error_count = len(pipeline_results['errors'])
        quality_score = 'N/A'
        if review_results:
            quality_score = f"{review_results['overall_score']:.1f}/100"
        
        regen_content = f"""# PromptSwitch v2 Regeneration Block

**Phase:** PromptSwitch v2 - Complete Pipeline Execution  
**Timestamp:** {timestamp}  
**Repository:** {pipeline_results['github_url']}  
**Success:** {'✅ Yes' if pipeline_results['success'] else '❌ No'}  
**Quality Score:** {quality_score}

## Changes This Pass

- ✅ Complete prompt chaining pipeline implemented
- ✅ Meta-prompting applied across all agents
- ✅ Test generation agent created and executed
- ✅ Quality review agent implemented with comprehensive scoring
- ✅ Regeneration block management automated
- ✅ DX best practices integrated throughout workflow

## Pipeline Execution Summary

### Phase 1: Repository Analysis
- **Repository Cloning:** ✅ Completed
- **Structure Parsing:** ✅ Completed  
- **Context Loading:** ✅ Completed

### Phase 2: Documentation Generation
- **Outline Generation:** ✅ Completed
- **Section Filling:** ✅ Completed
- **Document Formatting:** ✅ Completed

### Phase 3: Test Generation
- **Status:** {'✅ Completed' if test_results else '⚠️ Skipped/Failed'}
- **Tests Generated:** {len(test_results.get('test_files', []) if test_results else [])}
- **Test Strategy:** {test_results.get('strategy', {}).get('approach', 'N/A') if test_results else 'N/A'}

### Phase 4: Quality Review
- **Status:** {'✅ Completed' if review_results else '⚠️ Skipped/Failed'}
- **Overall Score:** {quality_score}
- **Approval Status:** {review_results.get('approval_status', 'N/A') if review_results else 'N/A'}

## Quality Breakdown

{self._format_quality_breakdown(review_results) if review_results else '- Quality review not available'}

## Outputs Generated

{chr(10).join(f'- **{key.replace("_", " ").title()}:** {value if isinstance(value, str) else "Generated"}' for key, value in pipeline_results['outputs'].items())}

## Errors and Issues

{chr(10).join(f'- {error}' for error in pipeline_results['errors']) if pipeline_results['errors'] else '- No errors encountered'}

## Recommended Next Steps

{self._generate_next_steps(pipeline_results, review_results, test_results)}

## Metrics and Performance

- **Total Outputs:** {total_outputs}
- **Error Count:** {error_count}
- **Pipeline Duration:** {self._calculate_duration(pipeline_results)}
- **Success Rate:** {('100%' if pipeline_results['success'] else '0%')}

## Inputs Used

- Repository structure and code analysis
- AI learning context from Learn_AI/ directory
- Project documentation from Project Docs/
- System prompt and review prompts
- DX engineering best practices

## Context for Next Iteration

- **Primary Language:** {repo_data.get('primary_language', 'Unknown')}
- **Project Type:** {self._infer_project_type(repo_data)}
- **Complexity Level:** {self._assess_complexity(repo_data)}
- **Documentation Maturity:** {self._assess_doc_maturity(review_results) if review_results else 'Unknown'}

---

*Generated by PromptSwitch v2 Agent - {timestamp}*
"""
        
        # Save regeneration block
        regen_path = self.output_dir / "regeneration_block.md"
        with open(regen_path, 'w', encoding='utf-8') as f:
            f.write(regen_content)
        
        print(f"📝 Regeneration block saved: {regen_path}")
        return regen_content


    def _format_quality_breakdown(self, review_results):
        """Format quality breakdown for regeneration block."""
        if not review_results or 'quality_scores' not in review_results:
            return '- Quality breakdown not available'
        
        breakdown = []
        for criterion, score in review_results['quality_scores'].items():
            status = '✅' if score >= 80 else '⚠️' if score >= 60 else '❌'
            breakdown.append(f'- **{criterion.title()}:** {score:.1f}/100 {status}')
        
        return chr(10).join(breakdown)
    
    def _generate_next_steps(self, pipeline_results, review_results, test_results):
        """Generate contextual next steps based on results."""
        steps = []
        
        # Quality-based recommendations
        if review_results:
            if review_results['overall_score'] < 70:
                steps.append('1. Address critical quality issues identified in review')
                steps.append('2. Implement high-priority recommendations')
            elif review_results['overall_score'] < 85:
                steps.append('1. Implement medium-priority improvements')
                steps.append('2. Enhance content depth and examples')
            else:
                steps.append('1. Fine-tune documentation based on user feedback')
        
        # Test-based recommendations
        if test_results:
            test_count = len(test_results.get('test_files', []))
            if test_count == 0:
                steps.append('2. Investigate test generation issues')
            else:
                steps.append(f'2. Review and validate {test_count} generated test files')
                steps.append('3. Integrate tests into CI/CD pipeline')
        
        # Error-based recommendations
        if pipeline_results['errors']:
            steps.append('4. Resolve pipeline errors for next iteration')
        
        # Default next steps
        if not steps:
            steps = [
                '1. Deploy documentation to production environment',
                '2. Gather user feedback and usage analytics',
                '3. Plan next iteration based on user needs'
            ]
        
        return chr(10).join(steps)
    
    def _calculate_duration(self, pipeline_results):
        """Calculate pipeline execution duration."""
        try:
            start = datetime.fromisoformat(pipeline_results['start_time'])
            end = datetime.fromisoformat(pipeline_results['end_time'])
            duration = end - start
            return f"{duration.total_seconds():.1f} seconds"
        except:
            return "Unknown"
    
    def _infer_project_type(self, repo_data):
        """Infer project type from repository data."""
        files = repo_data.get('files', [])
        file_content = ' '.join(files).lower()
        
        if 'package.json' in file_content:
            return 'JavaScript/Node.js Project'
        elif 'requirements.txt' in file_content or 'setup.py' in file_content:
            return 'Python Project'
        elif 'pom.xml' in file_content or 'build.gradle' in file_content:
            return 'Java Project'
        elif 'cargo.toml' in file_content:
            return 'Rust Project'
        elif 'go.mod' in file_content:
            return 'Go Project'
        else:
            return 'General Project'
    
    def _assess_complexity(self, repo_data):
        """Assess project complexity based on repository data."""
        file_count = len(repo_data.get('files', []))
        
        if file_count < 10:
            return 'Low'
        elif file_count < 50:
            return 'Medium'
        else:
            return 'High'
    
    def _assess_doc_maturity(self, review_results):
        """Assess documentation maturity based on review results."""
        if not review_results:
            return 'Unknown'
        
        score = review_results.get('overall_score', 0)
        if score >= 85:
            return 'Mature'
        elif score >= 70:
            return 'Developing'
        else:
            return 'Initial'
    
    def _generate_claude_prompts(self, github_url, repo_data, documentation, base_filename):
        """Generate Claude Desktop prompts for recreating the documentation."""
        # Extract repository name from URL (just the repo part, not owner_repo)
        full_repo_name = github_url.split('/')[-1]  # e.g., 'react'
        display_repo_name = self._extract_repo_name(github_url)  # e.g., 'facebook_react'
        
        # Extract key information from repo_data
        primary_language = repo_data.get('languages', {}).get('primary', 'Unknown')
        file_count = len(repo_data.get('files', []))
        project_type = repo_data.get('project_type', 'Unknown')
        
        # Extract project-specific features and purpose from documentation
        project_features = self._extract_project_features(documentation, full_repo_name)
        project_purpose = self._extract_project_purpose(documentation, full_repo_name)
        
        # Get first 1000 characters of documentation as sample
        doc_sample = documentation[:1000] + "..." if len(documentation) > 1000 else documentation
        
        prompts_content = f"""# Claude Desktop Prompts for Building {display_repo_name}

These prompts will help you **build and implement** the **{display_repo_name}** project from scratch using Claude Desktop, based on the analyzed documentation.

## Project Information

- **GitHub URL:** {github_url}
- **Primary Language:** {primary_language}
- **Project Type:** {project_type}
- **File Count:** {file_count}
- **Reference Documentation:** {base_filename}

## Project Overview

```markdown
{doc_sample}
```

---

## Prompt 1: Project Setup & Architecture Planning

```
You are a senior full-stack developer and software architect. I need you to help me build {project_purpose} using {primary_language}.

**Project Context:**
- Primary Language: {primary_language}
- Project Type: {project_type}
- Reference Repository: {github_url}
- Target Complexity: Based on {file_count} files
- Key Features to Build: {project_features}

**Your Role:**
- Expert {primary_language} developer with 10+ years experience
- Software architecture specialist for {project_type} applications
- DevOps and deployment expert
- Code quality advocate

**Task:**
Help me plan and set up the foundational architecture for {project_purpose}:

1. **Project Initialization**
   - Create proper directory structure
   - Set up version control (git)
   - Initialize package management ({primary_language}-specific)
   - Configure development environment

2. **Technology Stack Selection**
   - Choose appropriate frameworks and libraries
   - Select development tools and build systems
   - Recommend testing frameworks
   - Suggest deployment platforms

3. **Architecture Design**
   - Design overall system architecture
   - Plan component structure and relationships
   - Define data flow and API design
   - Establish coding standards and conventions

4. **Development Environment Setup**
   - Create configuration files
   - Set up development scripts
   - Configure linting and formatting tools
   - Establish CI/CD pipeline basics

**Output Requirements:**
- Step-by-step setup instructions
- Complete file structure with explanations
- Configuration files with proper settings
- Development workflow recommendations
- Best practices for the chosen technology stack

**Quality Standards:**
- Follow industry best practices
- Ensure scalability and maintainability
- Include security considerations
- Provide clear, actionable instructions
- Use modern development approaches

Please provide a comprehensive project setup plan that I can follow to create a solid foundation for building this {project_type} application.
```

---

## Prompt 2: Core Implementation & Feature Development

```
You are an expert {primary_language} developer and system implementer. Building on the project setup from the previous step, I need you to help me implement the core functionality.

**Previous Setup Context:**
[PASTE THE OUTPUT FROM PROMPT 1 HERE]

**Project Details:**
- Repository Reference: {github_url}
- Technology Stack: {primary_language}, {project_type}
- Target: Build {project_purpose}
- Core Features: {project_features}

**Your Enhanced Role:**
- Senior {primary_language} developer
- API design specialist
- Database architect (if applicable)
- Frontend/Backend integration expert
- Performance optimization specialist

**Implementation Tasks:**

1. **Core Application Logic**
   - Implement main application entry points for {project_purpose}
   - Create core business logic modules
   - Set up routing and navigation (if applicable)
   - Implement data models and schemas

2. **Feature Implementation**
   - Build these specific features: {project_features}
   - Create user interfaces for the core functionality
   - Implement API endpoints and services
   - Add data persistence and management

3. **Integration & Communication**
   - Set up inter-component communication
   - Implement external API integrations
   - Configure database connections
   - Add authentication and authorization

4. **Error Handling & Validation**
   - Implement comprehensive error handling
   - Add input validation and sanitization
   - Create logging and monitoring systems
   - Set up debugging and development tools

5. **Testing Implementation**
   - Write unit tests for core functionality
   - Create integration tests
   - Set up test automation
   - Implement code coverage reporting

**Code Quality Requirements:**
- Write clean, readable, and maintainable code
- Follow established coding standards
- Include comprehensive comments and documentation
- Implement proper error handling
- Use design patterns appropriately

**Deliverables:**
- Complete, functional codebase
- Working application with core features
- Comprehensive test suite
- Clear code documentation
- Setup and run instructions

**Implementation Checklist:**
- [ ] Core functionality is working
- [ ] All features are implemented
- [ ] Tests are passing
- [ ] Code follows best practices
- [ ] Application runs without errors
- [ ] Documentation is complete

Please provide complete, working code implementations that I can use to build {project_purpose} with these key features: {project_features}.
```

---

## Prompt 3: Deployment, Optimization & Production Readiness

```
You are a DevOps engineer and production systems specialist. I need you to help me deploy, optimize, and make my {project_type} application production-ready.

**Complete Implementation Context:**
[PASTE ALL PREVIOUS OUTPUTS HERE]

**Project Status:**
- Repository Reference: {github_url}
- Technology: {primary_language} {project_type}
- Current State: Functional {project_purpose} with core features
- Target: Production-ready deployment
- Features Implemented: {project_features}

**Your Expert Role:**
- DevOps and deployment specialist
- Performance optimization expert
- Security and compliance consultant
- Monitoring and maintenance specialist
- Production systems architect

**Production Readiness Tasks:**

1. **Deployment Configuration**
   - Set up production environment
   - Configure deployment scripts and automation
   - Create Docker containers (if applicable)
   - Set up cloud hosting and infrastructure

2. **Performance Optimization**
   - Optimize application performance
   - Implement caching strategies
   - Configure load balancing (if needed)
   - Optimize database queries and connections

3. **Security Implementation**
   - Implement security best practices
   - Set up SSL/TLS certificates
   - Configure environment variables and secrets
   - Add security headers and protections

4. **Monitoring & Logging**
   - Set up application monitoring
   - Configure error tracking and alerting
   - Implement performance metrics
   - Create health check endpoints

5. **Documentation & Maintenance**
   - Create deployment documentation
   - Write operational runbooks
   - Set up backup and recovery procedures
   - Plan maintenance and update strategies

**Production Standards:**
- High availability and reliability
- Scalable architecture
- Comprehensive monitoring
- Security compliance
- Automated deployment processes

**Final Deliverables:**
- Production deployment configuration
- Monitoring and alerting setup
- Security implementation
- Operational documentation
- Maintenance procedures

**Production Checklist:**
- [ ] Application deploys successfully
- [ ] All security measures are in place
- [ ] Monitoring and logging are working
- [ ] Performance is optimized
- [ ] Backup and recovery are configured
- [ ] Documentation is complete
- [ ] Application is publicly accessible
- [ ] All production requirements are met

Please provide a complete production deployment solution that makes my {project_purpose} ready for real-world use, following industry best practices for reliability, security, and performance.
```

---

## Implementation Guide

### How to Use These Prompts:

1. **Sequential Development**: Follow prompts in order (Setup → Implementation → Deployment)
2. **Context Preservation**: Always include previous outputs in subsequent prompts
3. **Customization**: Adapt technical details to your specific requirements
4. **Iterative Refinement**: Ask for clarifications and improvements as needed

### Expected Outcomes:

- **Functional Application**: Complete, working {project_purpose} built with {primary_language}
- **Production Ready**: Deployed application ready for real users  
- **Best Practices**: Code following industry standards and conventions
- **Comprehensive Documentation**: Setup, usage, and maintenance guides
- **Key Features**: {project_features}

### Development Tips:

- Start with the basic setup and gradually add complexity
- Test each component thoroughly before moving to the next step
- Ask for specific code examples and implementations
- Request explanations for any unclear concepts or decisions
- Adapt the suggestions to your specific use case and requirements

### Success Criteria:

- ✅ Project builds and runs without errors
- ✅ All core features are implemented and working
- ✅ Application is deployed and accessible
- ✅ Code quality meets professional standards
- ✅ Documentation enables others to understand and contribute

---

*Generated by PromptSwitch v2 for building {project_purpose} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        return prompts_content
    
    def _extract_project_features(self, documentation, repo_name):
         """Extract key features from documentation."""
         features = []
         doc_lower = documentation.lower()
         repo_lower = repo_name.lower()
         
         # Project-specific features based on repo name
         if 'react' in repo_lower:
             features.extend(['Component-based architecture', 'Virtual DOM', 'JSX syntax', 'State management', 'Hooks API'])
         elif 'vscode' in repo_lower or 'code' in repo_lower:
             features.extend(['Code editing', 'Syntax highlighting', 'Extensions system', 'Debugging tools', 'Git integration'])
         elif 'linux' in repo_lower:
             features.extend(['Process management', 'Memory management', 'File system', 'Device drivers', 'System calls'])
         elif 'hello' in repo_lower:
             features.extend(['Basic output', 'Simple program structure'])
         else:
             # Generic feature extraction based on documentation content
             if 'api' in doc_lower:
                 features.append('REST API')
             if 'database' in doc_lower or 'db' in doc_lower:
                 features.append('Database integration')
             if 'auth' in doc_lower or 'login' in doc_lower:
                 features.append('Authentication')
             if 'web' in doc_lower or 'frontend' in doc_lower:
                 features.append('Web interface')
             if 'cli' in doc_lower or 'command' in doc_lower:
                 features.append('Command-line interface')
             if 'test' in doc_lower:
                 features.append('Testing framework')
             if 'ui' in doc_lower or 'user interface' in doc_lower:
                 features.append('User interface')
             if 'mobile' in doc_lower:
                 features.append('Mobile support')
         
         return ', '.join(features) if features else 'Core application functionality'
    
    def _extract_project_purpose(self, documentation, repo_name):
         """Extract project purpose from documentation."""
         doc_lower = documentation.lower()
         
         # Look for specific project types based on repo name and content
         if 'react' in repo_name.lower():
             return "a React JavaScript library for building user interfaces"
         elif 'vscode' in repo_name.lower() or 'code' in repo_name.lower():
             return "a code editor application"
         elif 'linux' in repo_name.lower():
             return "an operating system kernel"
         elif 'hello' in repo_name.lower():
             return "a simple Hello World application"
         elif 'api' in doc_lower:
             return "a REST API application"
         elif 'web' in doc_lower and 'frontend' in doc_lower:
             return "a web frontend application"
         elif 'cli' in doc_lower or 'command' in doc_lower:
             return "a command-line tool"
         elif 'library' in doc_lower:
             return "a software library"
         elif 'framework' in doc_lower:
             return "a software framework"
         
         # Try to find purpose in project summary section
         if '## Project Summary' in documentation:
             summary_start = documentation.find('## Project Summary')
             summary_section = documentation[summary_start:summary_start+500]
             lines = summary_section.split('\n')[2:6]  # Skip header and get next few lines
             for line in lines:
                 line = line.strip()
                 if line and not line.startswith('#') and len(line) > 20:
                     purpose = line.replace('*', '').replace('`', '').strip()
                     if purpose and not purpose.startswith('|'):
                         return purpose
         
         # Fallback to repo name
         return f"a {repo_name.replace('_', ' ').replace('-', ' ')} application"


def main():
    """Command-line interface for PromptSwitch v2 agent."""
    parser = argparse.ArgumentParser(
        description="PromptSwitch Agent v2 - Generate comprehensive project documentation with testing and quality review"
    )
    parser.add_argument(
        "github_url",
        help="GitHub repository URL to analyze or local directory path"
    )
    parser.add_argument(
        "-o", "--output",
        default="project_doc.md",
        help="Output filename (default: project_doc.md)"
    )
    parser.add_argument(
        "--output-dir",
        default="outputs",
        help="Output directory (default: outputs)"
    )
    parser.add_argument(
        "--no-tests",
        action="store_true",
        help="Skip test generation phase"
    )
    parser.add_argument(
        "--no-review",
        action="store_true",
        help="Skip quality review phase"
    )
    parser.add_argument(
        "--prompts-dir",
        default="prompts",
        help="Prompts directory (default: prompts)"
    )
    
    args = parser.parse_args()
    
    # Initialize and run PromptSwitch v2 agent
    agent = PromptSwitchAgent(output_dir=args.output_dir, prompts_dir=args.prompts_dir)
    
    try:
        results = agent.process_repository(
            args.github_url, 
            args.output,
            enable_testing=not args.no_tests,
            enable_review=not args.no_review
        )
        
        if results['success']:
            print("\n🎉 PromptSwitch v2 pipeline completed successfully!")
            return 0
        else:
            print("\n💥 PromptSwitch v2 pipeline completed with errors.")
            return 1
            
    except Exception as e:
        print(f"\n💥 PromptSwitch v2 pipeline failed: {str(e)}")
        return 1


if __name__ == "__main__":
    main()