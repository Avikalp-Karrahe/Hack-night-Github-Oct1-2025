#!/usr/bin/env python3
"""
Document Formatter Agent

Formats the filled documentation sections into a clean, structured markdown file.
Optionally converts to PDF or HTML using pandoc.
"""

import json
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Any, Optional

# Import the Python PDF converter as fallback
try:
    from .pdf_converter import PythonPDFConverter
except ImportError:
    PythonPDFConverter = None


class DocumentFormatter:
    """Agent responsible for formatting and converting documentation."""
    
    def __init__(self, output_dir="outputs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Markdown formatting options
        self.markdown_config = {
            'line_length': 80,
            'use_tables': True,
            'code_highlighting': True,
            'toc_enabled': True
        }
        
        # Check for pandoc availability
        self.pandoc_available = self._check_pandoc()
    
    def format_document(self, filled_doc: Dict[str, Any], 
                       output_format: str = 'markdown',
                       include_toc: bool = True,
                       base_filename: str = None) -> str:
        """
        Format the filled documentation into final output.
        
        Args:
            filled_doc: Filled documentation from section_filler
            output_format: Output format ('markdown', 'html', 'pdf')
            include_toc: Whether to include table of contents
            base_filename: Base filename for output files (without extension)
            
        Returns:
            Formatted document content (for markdown) or file path (for others)
        """
        print(f"📄 Formatting document as {output_format}...")
        
        # Generate markdown content
        markdown_content = self._generate_markdown(filled_doc, include_toc)
        
        if output_format == 'markdown':
            return markdown_content
        
        # Save markdown first
        markdown_path = self.output_dir / "temp_project_doc.md"
        with open(markdown_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        try:
            if output_format == 'html':
                return self._convert_to_html(markdown_path, base_filename)
            elif output_format == 'pdf':
                return self._convert_to_pdf(markdown_path, base_filename)
            else:
                raise ValueError(f"Unsupported output format: {output_format}")
        finally:
            # Clean up temporary file
            if markdown_path.exists():
                markdown_path.unlink()
    
    def _generate_markdown(self, filled_doc: Dict[str, Any], include_toc: bool = True) -> str:
        """
        Generate formatted markdown content.
        
        Args:
            filled_doc: Filled documentation data
            include_toc: Whether to include table of contents
            
        Returns:
            Formatted markdown string
        """
        content = []
        
        # Document header
        project_name = filled_doc.get('project_name', 'Project Documentation')
        content.append(f"# {project_name}")
        content.append("")
        
        # Metadata section
        metadata = filled_doc.get('metadata', {})
        generation_info = filled_doc.get('generation_info', {})
        
        if metadata or generation_info:
            content.append("---")
            content.append("")
            
            if metadata.get('primary_language'):
                content.append(f"**Primary Language:** {metadata['primary_language']}")
            if metadata.get('project_type'):
                content.append(f"**Project Type:** {metadata['project_type'].replace('_', ' ').title()}")
            if metadata.get('complexity'):
                content.append(f"**Complexity:** {metadata['complexity'].title()}")
            
            if generation_info.get('timestamp'):
                content.append(f"**Generated:** {generation_info['timestamp']}")
            
            content.append("")
            content.append("---")
            content.append("")
        
        # Table of contents
        if include_toc:
            toc = self._generate_toc(filled_doc)
            if toc:
                content.append("## Table of Contents")
                content.append("")
                content.extend(toc)
                content.append("")
                content.append("---")
                content.append("")
        
        # Document sections
        sections = filled_doc.get('sections', {})
        
        # Sort sections by priority and logical order
        section_order = self._get_section_order()
        sorted_sections = self._sort_sections(sections, section_order)
        
        for title, section_data in sorted_sections:
            content.append(f"## {title}")
            content.append("")
            
            section_content = section_data.get('content', '')
            
            # Clean up section content
            cleaned_content = self._clean_section_content(section_content, title)
            content.append(cleaned_content)
            content.append("")
            
            # Add section metadata as comment if in debug mode
            if section_data.get('fallback_used'):
                content.append("<!-- Generated using fallback template -->")
                content.append("")
        
        # Footer
        content.append("---")
        content.append("")
        content.append("## 📄 Documentation Info")
        content.append("")
        content.append("*This documentation was generated automatically by **PromptSwitch**.*")
        content.append("")
        content.append("**Created by:** [Avikalp Karrahe](https://github.com/Avikalp-Karrahe)")
        content.append("")
        content.append("**Connect with me:**")
        content.append("- 🔗 [LinkedIn](https://www.linkedin.com/in/avikalp-karrahe/)")
        content.append("- 💼 [GitHub](https://github.com/Avikalp-Karrahe)")
        content.append("- 🚀 [PromptSwitch Repository](https://github.com/Avikalp-Karrahe/PromptSwitch)")
        
        if generation_info.get('timestamp'):
            timestamp = generation_info['timestamp']
            content.append("")
            content.append(f"*Generated on: {timestamp}*")
        
        return "\n".join(content)
    
    def _generate_toc(self, filled_doc: Dict[str, Any]) -> List[str]:
        """
        Generate table of contents.
        
        Args:
            filled_doc: Filled documentation data
            
        Returns:
            List of TOC lines
        """
        toc = []
        sections = filled_doc.get('sections', {})
        
        # Sort sections by priority and logical order
        section_order = self._get_section_order()
        sorted_sections = self._sort_sections(sections, section_order)
        
        for title, section_data in sorted_sections:
            # Create anchor link
            anchor = title.lower().replace(' ', '-').replace('/', '')
            toc.append(f"- [{title}](#{anchor})")
        
        return toc
    
    def _get_section_order(self) -> List[str]:
        """
        Get the logical order for documentation sections.
        
        Returns:
            List of section titles in preferred order
        """
        return [
            'Project Overview',
            'Features',
            'Technology Stack',
            'Installation',
            'Configuration',
            'Usage',
            'API Documentation',
            'Project Structure',
            'Development',
            'Testing',
            'Deployment',
            'Contributing',
            'License'
        ]
    
    def _sort_sections(self, sections: Dict[str, Any], 
                      preferred_order: List[str]) -> List[tuple]:
        """
        Sort sections by preferred order and priority.
        
        Args:
            sections: Dictionary of sections
            preferred_order: Preferred section order
            
        Returns:
            List of (title, section_data) tuples in sorted order
        """
        def get_sort_key(item):
            title, section_data = item
            
            # Primary sort: preferred order
            try:
                order_index = preferred_order.index(title)
            except ValueError:
                order_index = len(preferred_order)  # Put unknown sections at end
            
            # Secondary sort: priority
            priority = section_data.get('priority', 'medium')
            priority_value = {'high': 0, 'medium': 1, 'low': 2}.get(priority, 1)
            
            return (order_index, priority_value)
        
        return sorted(sections.items(), key=get_sort_key)
    
    def _clean_section_content(self, content: str, title: str) -> str:
        """
        Clean and format section content.
        
        Args:
            content: Raw section content
            title: Section title
            
        Returns:
            Cleaned content
        """
        if not content:
            return f"*{title} section is empty.*"
        
        lines = content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Remove duplicate headers (section title already added)
            if line.startswith('#') and title in line:
                continue
            
            # Clean up extra whitespace
            line = line.rstrip()
            cleaned_lines.append(line)
        
        # Remove leading/trailing empty lines
        while cleaned_lines and not cleaned_lines[0]:
            cleaned_lines.pop(0)
        while cleaned_lines and not cleaned_lines[-1]:
            cleaned_lines.pop()
        
        return '\n'.join(cleaned_lines)
    
    def _check_pandoc(self) -> bool:
        """
        Check if pandoc is available for format conversion.
        
        Returns:
            True if pandoc is available
        """
        try:
            result = subprocess.run(['pandoc', '--version'], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def _convert_to_html(self, markdown_path: Path, base_filename: str = None) -> str:
        """
        Convert markdown to HTML using pandoc.
        
        Args:
            markdown_path: Path to markdown file
            base_filename: Base filename for output (without extension)
            
        Returns:
            Path to generated HTML file
        """
        if not self.pandoc_available:
            raise RuntimeError("Pandoc is not available. Install pandoc to convert to HTML.")
        
        # Use base_filename if provided, otherwise default
        if base_filename:
            html_filename = base_filename.replace('.md', '.html') if base_filename.endswith('.md') else f"{base_filename}.html"
        else:
            html_filename = "project_doc.html"
        
        html_path = self.output_dir / html_filename
        
        cmd = [
            'pandoc',
            str(markdown_path),
            '-o', str(html_path),
            '--standalone',
            '--toc',
            '--css', self._create_css_file(),
            '--highlight-style', 'github'
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(f"✅ HTML generated: {html_path}")
            return str(html_path)
        except subprocess.CalledProcessError as e:
            print(f"❌ HTML conversion failed: {e.stderr}")
            raise
    
    def _convert_to_pdf(self, markdown_path: Path, base_filename: str = None) -> str:
        """
        Convert markdown to PDF using pandoc with multiple fallback engines.
        
        Args:
            markdown_path: Path to markdown file
            base_filename: Base filename for output (without extension)
            
        Returns:
            Path to generated PDF file
        """
        if not self.pandoc_available:
            raise RuntimeError(
                "Pandoc is not available. Install pandoc to convert to PDF.\n"
                "Install with: brew install pandoc (macOS) or apt-get install pandoc (Ubuntu)"
            )
        
        # Use base_filename if provided, otherwise default
        if base_filename:
            pdf_filename = base_filename.replace('.md', '.pdf') if base_filename.endswith('.md') else f"{base_filename}.pdf"
        else:
            pdf_filename = "project_doc.pdf"
        
        pdf_path = self.output_dir / pdf_filename
        
        # Try different PDF engines in order of preference
        engines = ['xelatex', 'pdflatex', 'wkhtmltopdf']
        
        for engine in engines:
            try:
                print(f"🔄 Trying PDF conversion with {engine}...")
                
                if engine == 'wkhtmltopdf':
                    # Different command structure for wkhtmltopdf
                    cmd = [
                        'pandoc',
                        str(markdown_path),
                        '-o', str(pdf_path),
                        '--pdf-engine=wkhtmltopdf',
                        '--toc',
                        '-V', 'margin-top=1in',
                        '-V', 'margin-bottom=1in',
                        '-V', 'margin-left=1in',
                        '-V', 'margin-right=1in'
                    ]
                else:
                    # LaTeX-based engines with enhanced formatting to match Reference.pdf template
                    cmd = [
                        'pandoc',
                        str(markdown_path),
                        '-o', str(pdf_path),
                        f'--pdf-engine={engine}',
                        '--toc',
                        '--toc-depth=3',
                        '-V', 'geometry:margin=1in',
                        '-V', 'fontsize=11pt',
                        '-V', 'documentclass=article',
                        '-V', 'colorlinks=true',
                        '-V', 'linkcolor=blue',
                        '-V', 'urlcolor=blue',
                        '--number-sections',
                        '--standalone'
                    ]
                
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                print(f"✅ PDF generated with {engine}: {pdf_path}")
                return str(pdf_path)
                
            except subprocess.CalledProcessError as e:
                print(f"⚠️ {engine} failed: {e.stderr.strip() if e.stderr else 'Unknown error'}")
                continue
        
        # If all pandoc engines failed, try Python fallback
        if PythonPDFConverter:
            try:
                print("🔄 Trying Python-based PDF conversion...")
                converter = PythonPDFConverter(str(self.output_dir))
                
                # Read the markdown content
                with open(markdown_path, 'r', encoding='utf-8') as f:
                    markdown_content = f.read()
                
                result_path = converter.convert_markdown_to_pdf(markdown_content, "project_doc.pdf")
                return result_path
                
            except Exception as e:
                print(f"⚠️ Python PDF conversion also failed: {e}")
        
        # If everything failed, provide helpful error message
        error_msg = (
            "PDF conversion failed with all available methods.\n"
            "Install requirements:\n"
            "  • Pandoc: brew install pandoc (macOS)\n"
            "  • XeLaTeX: brew install --cask mactex (macOS)\n"
            "  • wkhtmltopdf: brew install wkhtmltopdf (macOS)\n"
            "  • Python libraries: pip install weasyprint markdown\n"
            "  • Or use the HTML output and print to PDF from browser"
        )
        raise RuntimeError(error_msg)
    
    def _create_css_file(self) -> str:
        """
        Create a CSS file for HTML styling.
        
        Returns:
            Path to CSS file
        """
        css_path = self.output_dir / "style.css"
        
        css_content = """
/* GitRead Documentation Styles */

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.6;
    max-width: 900px;
    margin: 0 auto;
    padding: 2rem;
    color: #333;
}

h1, h2, h3, h4, h5, h6 {
    color: #2c3e50;
    margin-top: 2rem;
    margin-bottom: 1rem;
}

h1 {
    border-bottom: 3px solid #3498db;
    padding-bottom: 0.5rem;
}

h2 {
    border-bottom: 1px solid #bdc3c7;
    padding-bottom: 0.3rem;
}

code {
    background-color: #f8f9fa;
    padding: 0.2rem 0.4rem;
    border-radius: 3px;
    font-family: 'SF Mono', Monaco, 'Cascadia Code', monospace;
}

pre {
    background-color: #f8f9fa;
    border: 1px solid #e9ecef;
    border-radius: 5px;
    padding: 1rem;
    overflow-x: auto;
}

blockquote {
    border-left: 4px solid #3498db;
    margin: 1rem 0;
    padding-left: 1rem;
    color: #7f8c8d;
}

table {
    border-collapse: collapse;
    width: 100%;
    margin: 1rem 0;
}

th, td {
    border: 1px solid #ddd;
    padding: 0.5rem;
    text-align: left;
}

th {
    background-color: #f8f9fa;
    font-weight: 600;
}

.toc {
    background-color: #f8f9fa;
    border: 1px solid #e9ecef;
    border-radius: 5px;
    padding: 1rem;
    margin: 2rem 0;
}

.toc ul {
    margin: 0;
    padding-left: 1.5rem;
}

a {
    color: #3498db;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

.metadata {
    background-color: #f8f9fa;
    border-left: 4px solid #3498db;
    padding: 1rem;
    margin: 2rem 0;
}
"""
        
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(css_content)
        
        return str(css_path)
    
    def generate_summary_report(self, filled_doc: Dict[str, Any]) -> str:
        """
        Generate a summary report of the documentation generation.
        
        Args:
            filled_doc: Filled documentation data
            
        Returns:
            Summary report content
        """
        sections = filled_doc.get('sections', {})
        generation_info = filled_doc.get('generation_info', {})
        metadata = filled_doc.get('metadata', {})
        
        report = []
        report.append("# GitRead Generation Report")
        report.append("")
        
        # Basic statistics
        total_sections = len(sections)
        total_words = sum(section.get('word_count', 0) for section in sections.values())
        fallback_sections = sum(1 for section in sections.values() if section.get('fallback_used'))
        
        report.append("## Statistics")
        report.append("")
        report.append(f"- **Total Sections:** {total_sections}")
        report.append(f"- **Total Words:** {total_words:,}")
        report.append(f"- **Fallback Sections:** {fallback_sections}")
        report.append(f"- **Success Rate:** {((total_sections - fallback_sections) / total_sections * 100):.1f}%")
        report.append("")
        
        # Section details
        report.append("## Section Details")
        report.append("")
        report.append("| Section | Priority | Words | Status |")
        report.append("|---------|----------|-------|--------|")
        
        for title, section in sections.items():
            priority = section.get('priority', 'medium')
            word_count = section.get('word_count', 0)
            status = "Fallback" if section.get('fallback_used') else "Generated"
            report.append(f"| {title} | {priority} | {word_count} | {status} |")
        
        report.append("")
        
        # Metadata
        if metadata:
            report.append("## Project Metadata")
            report.append("")
            for key, value in metadata.items():
                report.append(f"- **{key.replace('_', ' ').title()}:** {value}")
            report.append("")
        
        # Generation info
        if generation_info:
            report.append("## Generation Information")
            report.append("")
            for key, value in generation_info.items():
                if key != 'timestamp':
                    report.append(f"- **{key.replace('_', ' ').title()}:** {value}")
            report.append("")
        
        return "\n".join(report)
    
    def save_summary_report(self, filled_doc: Dict[str, Any]) -> Path:
        """
        Save summary report to file.
        
        Args:
            filled_doc: Filled documentation data
            
        Returns:
            Path to saved report
        """
        report_content = self.generate_summary_report(filled_doc)
        report_path = self.output_dir / "generation_report.md"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"📊 Generation report saved: {report_path}")
        return report_path


if __name__ == "__main__":
    # Test the formatter
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python formatter.py <filled_doc.json>")
        sys.exit(1)
    
    filled_doc_path = Path(sys.argv[1])
    if not filled_doc_path.exists():
        print(f"Filled document file does not exist: {filled_doc_path}")
        sys.exit(1)
    
    with open(filled_doc_path, 'r', encoding='utf-8') as f:
        filled_doc = json.load(f)
    
    formatter = DocumentFormatter()
    
    # Generate markdown
    markdown_content = formatter.format_document(filled_doc, 'markdown')
    
    # Save markdown
    output_path = formatter.output_dir / "test_project_doc.md"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"✅ Test documentation generated: {output_path}")
    
    # Generate summary report
    formatter.save_summary_report(filled_doc)