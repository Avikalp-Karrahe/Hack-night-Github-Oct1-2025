#!/usr/bin/env python3
"""
PDF Converter Agent

Provides fallback PDF generation using Python libraries when pandoc is not available.
Uses markdown2 and weasyprint/reportlab for conversion.
"""

import re
import os
from pathlib import Path
from typing import Optional


class PythonPDFConverter:
    """Fallback PDF converter using pure Python libraries."""
    
    def __init__(self, output_dir="outputs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Check for available libraries
        self.weasyprint_available = self._check_weasyprint()
        self.reportlab_available = self._check_reportlab()
    
    def convert_markdown_to_pdf(self, markdown_content: str, output_filename: str = "project_doc.pdf") -> str:
        """
        Convert markdown content to PDF using available Python libraries.
        
        Args:
            markdown_content: Markdown content to convert
            output_filename: Output PDF filename
            
        Returns:
            Path to generated PDF file
        """
        if self.weasyprint_available:
            return self._convert_with_weasyprint(markdown_content, output_filename)
        elif self.reportlab_available:
            return self._convert_with_reportlab(markdown_content, output_filename)
        else:
            return self._convert_with_html_fallback(markdown_content, output_filename)
    
    def _check_weasyprint(self) -> bool:
        """Check if weasyprint is available."""
        try:
            import weasyprint
            return True
        except ImportError:
            return False
    
    def _check_reportlab(self) -> bool:
        """Check if reportlab is available."""
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
            return True
        except ImportError:
            return False
    
    def _convert_with_weasyprint(self, markdown_content: str, output_filename: str) -> str:
        """Convert using weasyprint (best quality)."""
        try:
            import weasyprint
            from markdown import markdown
            
            # Convert markdown to HTML
            html_content = markdown(markdown_content, extensions=['toc', 'tables', 'fenced_code'])
            
            # Create styled HTML
            styled_html = self._create_styled_html(html_content)
            
            # Generate PDF
            pdf_path = self.output_dir / output_filename
            weasyprint.HTML(string=styled_html).write_pdf(str(pdf_path))
            
            print(f"✅ PDF generated with WeasyPrint: {pdf_path}")
            return str(pdf_path)
            
        except Exception as e:
            print(f"⚠️ WeasyPrint conversion failed: {e}")
            raise
    
    def _convert_with_reportlab(self, markdown_content: str, output_filename: str) -> str:
        """Convert using reportlab (basic formatting)."""
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
            from reportlab.lib.units import inch
            
            pdf_path = self.output_dir / output_filename
            
            # Create PDF document
            doc = SimpleDocTemplate(str(pdf_path), pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            
            # Parse markdown content into paragraphs
            lines = markdown_content.split('\n')
            for line in lines:
                line = line.strip()
                if not line:
                    story.append(Spacer(1, 12))
                elif line.startswith('# '):
                    story.append(Paragraph(line[2:], styles['Title']))
                elif line.startswith('## '):
                    story.append(Paragraph(line[3:], styles['Heading1']))
                elif line.startswith('### '):
                    story.append(Paragraph(line[4:], styles['Heading2']))
                else:
                    story.append(Paragraph(line, styles['Normal']))
            
            doc.build(story)
            
            print(f"✅ PDF generated with ReportLab: {pdf_path}")
            return str(pdf_path)
            
        except Exception as e:
            print(f"⚠️ ReportLab conversion failed: {e}")
            raise
    
    def _convert_with_html_fallback(self, markdown_content: str, output_filename: str) -> str:
        """Create HTML file with instructions for manual PDF conversion."""
        # Convert markdown to HTML using basic regex
        html_content = self._basic_markdown_to_html(markdown_content)
        styled_html = self._create_styled_html(html_content)
        
        # Save HTML file
        html_filename = output_filename.replace('.pdf', '.html')
        html_path = self.output_dir / html_filename
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(styled_html)
        
        print(f"✅ HTML generated for manual PDF conversion: {html_path}")
        print("💡 To convert to PDF: Open HTML in browser and use 'Print to PDF'")
        
        return str(html_path)
    
    def _basic_markdown_to_html(self, markdown_text: str) -> str:
        """Convert basic markdown to HTML without external dependencies."""
        html = markdown_text
        
        # Convert headers
        html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^#### (.*?)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
        
        # Convert bold and italic
        html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
        
        # Convert inline code
        html = re.sub(r'`(.*?)`', r'<code>\1</code>', html)
        
        # Convert code blocks
        html = re.sub(r'^```([\s\S]*?)```', r'<pre><code>\1</code></pre>', html, flags=re.MULTILINE)
        
        # Convert paragraphs
        paragraphs = html.split('\n\n')
        html_paragraphs = []
        for p in paragraphs:
            p = p.strip()
            if p and not p.startswith('<'):
                html_paragraphs.append(f'<p>{p}</p>')
            elif p:
                html_paragraphs.append(p)
        
        return '\n'.join(html_paragraphs)
    
    def _create_styled_html(self, html_content: str) -> str:
        """Create a complete HTML document with styling."""
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project Documentation</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: #2c3e50;
            margin-top: 2em;
            margin-bottom: 0.5em;
        }}
        h1 {{
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 5px;
        }}
        code {{
            background-color: #f8f9fa;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Monaco', 'Menlo', monospace;
            color: #e74c3c;
        }}
        pre {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            border-left: 4px solid #3498db;
        }}
        pre code {{
            color: #333;
            background: none;
            padding: 0;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 1em 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
        }}
        @media print {{
            body {{
                max-width: none;
                margin: 0;
                padding: 15px;
            }}
            h1, h2, h3, h4, h5, h6 {{
                page-break-after: avoid;
            }}
        }}
    </style>
</head>
<body>
{html_content}
</body>
</html>'''


if __name__ == "__main__":
    # Test the converter
    converter = PythonPDFConverter()
    
    test_markdown = """
# Test Document

## Introduction

This is a **test** document with *italic* text and `inline code`.

### Code Block

```python
def hello_world():
    print("Hello, World!")
```

## Conclusion

This concludes the test document.
"""
    
    try:
        result = converter.convert_markdown_to_pdf(test_markdown, "test.pdf")
        print(f"Test conversion successful: {result}")
    except Exception as e:
        print(f"Test conversion failed: {e}")