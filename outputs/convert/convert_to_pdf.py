#!/usr/bin/env python3
"""
Simple Markdown to PDF converter for GitRead Project Plan
Fallback solution when pandoc/pdfkit are not available
"""

import os
import sys
from pathlib import Path

def create_html_from_markdown(md_file_path, html_file_path):
    """Convert markdown to HTML with basic styling"""
    
    # Read markdown content
    with open(md_file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Basic markdown to HTML conversion (simplified)
    html_content = md_content
    
    # Convert headers
    html_content = html_content.replace('# ', '<h1>').replace('\n', '</h1>\n', 1)
    html_content = html_content.replace('## ', '<h2>').replace('\n', '</h2>\n', 1)
    html_content = html_content.replace('### ', '<h3>').replace('\n', '</h3>\n', 1)
    html_content = html_content.replace('#### ', '<h4>').replace('\n', '</h4>\n', 1)
    
    # Convert bold text
    import re
    html_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html_content)
    
    # Convert code blocks
    html_content = re.sub(r'```([\s\S]*?)```', r'<pre><code>\1</code></pre>', html_content)
    html_content = re.sub(r'`(.*?)`', r'<code>\1</code>', html_content)
    
    # Convert lists
    lines = html_content.split('\n')
    in_list = False
    result_lines = []
    
    for line in lines:
        if line.strip().startswith('- '):
            if not in_list:
                result_lines.append('<ul>')
                in_list = True
            result_lines.append(f'<li>{line.strip()[2:]}</li>')
        else:
            if in_list:
                result_lines.append('</ul>')
                in_list = False
            result_lines.append(line)
    
    if in_list:
        result_lines.append('</ul>')
    
    html_content = '\n'.join(result_lines)
    
    # Add HTML structure and CSS
    full_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>GitRead v2 Project Plan</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 5px;
            margin-top: 30px;
        }}
        h3 {{
            color: #7f8c8d;
            margin-top: 25px;
        }}
        h4 {{
            color: #95a5a6;
        }}
        code {{
            background-color: #f8f9fa;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Monaco', 'Menlo', monospace;
        }}
        pre {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            border-left: 4px solid #3498db;
        }}
        ul {{
            padding-left: 20px;
        }}
        li {{
            margin-bottom: 5px;
        }}
        strong {{
            color: #2c3e50;
        }}
        .emoji {{
            font-size: 1.2em;
        }}
        @media print {{
            body {{
                max-width: none;
                margin: 0;
                padding: 15px;
            }}
            h1, h2 {{
                page-break-after: avoid;
            }}
        }}
    </style>
</head>
<body>
{html_content}
</body>
</html>
"""
    
    # Write HTML file
    with open(html_file_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    return html_file_path

def main():
    # File paths
    base_dir = Path('/Users/avikalpkarrahe/Desktop/UCD 24-25/JS\'25/NonSense/GitRead/outputs')
    md_file = base_dir / 'GitRead_v2_Project_Plan.md'
    html_file = base_dir / 'GitRead_v2_Project_Plan.html'
    
    if not md_file.exists():
        print(f"Error: Markdown file not found at {md_file}")
        return 1
    
    try:
        # Convert to HTML
        html_path = create_html_from_markdown(md_file, html_file)
        print(f"✅ HTML version created: {html_path}")
        print(f"📄 You can open this file in a browser and use 'Print to PDF' to create a PDF")
        print(f"🖨️  Or use: open '{html_path}' to view in browser")
        
        return 0
        
    except Exception as e:
        print(f"Error converting file: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())