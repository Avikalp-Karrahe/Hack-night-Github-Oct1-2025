#!/usr/bin/env python3
"""
Convert Markdown files to PDF using markdown and weasyprint
"""

import markdown
import sys
import os
from pathlib import Path

try:
    from weasyprint import HTML, CSS
except ImportError:
    print("weasyprint not installed. Installing...")
    os.system("pip3 install weasyprint")
    from weasyprint import HTML, CSS

def markdown_to_pdf(md_file, pdf_file):
    """Convert markdown file to PDF"""
    try:
        # Read markdown content
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Convert markdown to HTML
        html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
        
        # Add basic CSS styling
        css_style = """
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 40px;
            color: #333;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #2c3e50;
            margin-top: 30px;
        }
        code {
            background-color: #f4f4f4;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }
        pre {
            background-color: #f8f8f8;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        """
        
        # Create full HTML document
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>{css_style}</style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        
        # Convert to PDF
        HTML(string=full_html).write_pdf(pdf_file)
        print(f"✅ Successfully converted {md_file} to {pdf_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error converting {md_file} to PDF: {str(e)}")
        return False

def main():
    """Main function to convert both documentation files"""
    base_dir = Path('outputs')
    
    # Files to convert
    files_to_convert = [
        ('GitRead_documentation.md', 'GitRead_documentation.pdf'),
        ('GitRead_documentation_claude_prompts.md', 'GitRead_documentation_claude_prompts.pdf')
    ]
    
    success_count = 0
    
    for md_file, pdf_file in files_to_convert:
        md_path = base_dir / md_file
        pdf_path = base_dir / pdf_file
        
        if md_path.exists():
            if markdown_to_pdf(md_path, pdf_path):
                success_count += 1
        else:
            print(f"⚠️ Markdown file not found: {md_path}")
    
    print(f"\n📊 Conversion Summary: {success_count}/{len(files_to_convert)} files converted successfully")
    
    if success_count == len(files_to_convert):
        print("🎉 All files converted to PDF successfully!")
        return 0
    else:
        print("⚠️ Some files failed to convert")
        return 1

if __name__ == "__main__":
    sys.exit(main())