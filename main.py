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
from datetime import datetime, timezone
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
from agents.enhanced_claude_generator import EnhancedClaudeGenerator


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
        self.enhanced_claude_generator = EnhancedClaudeGenerator()
        
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
        
        # Create repository-specific output directory
        repo_output_dir = self.output_dir / repo_name
        repo_output_dir.mkdir(exist_ok=True)
        print(f"📁 Repository output directory: {repo_output_dir}")
        
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
            'start_time': datetime.now(timezone.utc).isoformat(),
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
            
            # Save primary documentation (Markdown) in repository-specific folder
            output_path = repo_output_dir / base_filename
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(final_doc)
            
            pipeline_results['outputs']['documentation_path'] = str(output_path)
            print(f"✅ Documentation generated: {output_path}")
            
            # Generate PDF version in repository-specific folder
            print("📄 Generating PDF version...")
            try:
                # Update formatter to use repo-specific output directory
                original_output_dir = self.formatter.output_dir
                self.formatter.output_dir = repo_output_dir
                pdf_path = self.formatter.format_document(filled_doc, output_format='pdf', base_filename=base_filename)
                self.formatter.output_dir = original_output_dir  # Restore original
                pipeline_results['outputs']['pdf_path'] = pdf_path
                print(f"✅ PDF generated: {pdf_path}")
            except Exception as e:
                error_msg = f"PDF generation failed: {str(e)}"
                print(f"⚠️ {error_msg}")
                pipeline_results['errors'].append(error_msg)
                
                # Fallback: Generate HTML and provide conversion instructions
                try:
                    print("📄 Generating HTML fallback for PDF conversion...")
                    original_output_dir = self.formatter.output_dir
                    self.formatter.output_dir = repo_output_dir
                    html_path = self.formatter.format_document(filled_doc, output_format='html', base_filename=base_filename)
                    self.formatter.output_dir = original_output_dir  # Restore original
                    pipeline_results['outputs']['html_path'] = html_path
                    print(f"✅ HTML generated: {html_path}")
                    print("💡 To convert to PDF: Open HTML in browser and use 'Print to PDF'")
                except Exception as html_error:
                    fallback_error = f"HTML fallback also failed: {str(html_error)}"
                    print(f"⚠️ {fallback_error}")
                    pipeline_results['errors'].append(fallback_error)
            
            # Generate Claude Desktop Prompts in repository-specific folder
            print("🤖 Generating Claude Desktop prompts...")
            try:
                claude_prompts = self._generate_claude_prompts(github_url, repo_data, final_doc, base_filename)
                claude_prompts_filename = base_filename.replace('.md', '_claude_prompts.md')
                claude_prompts_path = repo_output_dir / claude_prompts_filename
                
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
                    # Update test generator to use repo-specific output directory
                    original_test_output_dir = self.test_generator.outputs_dir
                    self.test_generator.outputs_dir = Path(repo_output_dir)
                    test_results = self.test_generator.generate_tests(repo_data, filled_doc)
                    self.test_generator.outputs_dir = original_test_output_dir  # Restore original
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
                    # Update reviewer to use repo-specific output directory
                    original_review_output_dir = self.reviewer.outputs_dir
                    self.reviewer.outputs_dir = Path(repo_output_dir)
                    review_results = self.reviewer.review_documentation(
                        filled_doc, repo_data, test_results
                    )
                    self.reviewer.outputs_dir = original_review_output_dir  # Restore original
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
            
            # Save regeneration block in repository-specific folder
            regen_filename = f"{repo_name}_regeneration_block.md"
            regen_path = repo_output_dir / regen_filename
            with open(regen_path, 'w', encoding='utf-8') as f:
                f.write(regeneration_block)
            
            pipeline_results['outputs']['regeneration_block'] = regeneration_block
            pipeline_results['outputs']['regeneration_block_path'] = str(regen_path)
            print(f"✅ Regeneration block saved: {regen_path}")
            
            # Final Summary
            pipeline_results['end_time'] = datetime.now(timezone.utc).isoformat()
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
            pipeline_results['end_time'] = datetime.now(timezone.utc).isoformat()
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
        timestamp = datetime.now(timezone.utc).isoformat()
        
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
        """Generate enhanced Claude Desktop prompts using the new generator."""
        return self.enhanced_claude_generator.generate_enhanced_prompts(
            github_url=github_url,
            repo_data=repo_data,
            documentation=documentation,
            base_filename=base_filename
        )
    
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