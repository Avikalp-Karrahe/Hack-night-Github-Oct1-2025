#!/usr/bin/env python3

import re
import os

def markdown_to_html(markdown_text):
    """Convert basic markdown to HTML"""
    html = markdown_text
    
    # Convert headers
    html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^#### (.*?)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
    html = re.sub(r'^##### (.*?)$', r'<h5>\1</h5>', html, flags=re.MULTILINE)
    html = re.sub(r'^###### (.*?)$', r'<h6>\1</h6>', html, flags=re.MULTILINE)
    
    # Convert bold and italic
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
    
    # Convert inline code
    html = re.sub(r'`(.*?)`', r'<code>\1</code>', html)
    
    # Convert code blocks
    html = re.sub(r'^```([\s\S]*?)```', r'<pre><code>\1</code></pre>', html, flags=re.MULTILINE)
    
    # Convert lists
    lines = html.split('\n')
    in_ul = False
    in_ol = False
    result_lines = []
    
    for line in lines:
        # Unordered list
        if re.match(r'^\s*[-*+]\s+', line):
            if not in_ul:
                result_lines.append('<ul>')
                in_ul = True
            if in_ol:
                result_lines.append('</ol>')
                in_ol = False
            item = re.sub(r'^\s*[-*+]\s+', '', line)
            result_lines.append(f'<li>{item}</li>')
        # Ordered list
        elif re.match(r'^\s*\d+\.\s+', line):
            if not in_ol:
                result_lines.append('<ol>')
                in_ol = True
            if in_ul:
                result_lines.append('</ul>')
                in_ul = False
            item = re.sub(r'^\s*\d+\.\s+', '', line)
            result_lines.append(f'<li>{item}</li>')
        else:
            if in_ul:
                result_lines.append('</ul>')
                in_ul = False
            if in_ol:
                result_lines.append('</ol>')
                in_ol = False
            result_lines.append(line)
    
    # Close any remaining lists
    if in_ul:
        result_lines.append('</ul>')
    if in_ol:
        result_lines.append('</ol>')
    
    html = '\n'.join(result_lines)
    
    # Convert line breaks to paragraphs
    paragraphs = html.split('\n\n')
    html_paragraphs = []
    for p in paragraphs:
        p = p.strip()
        if p and not p.startswith('<'):
            html_paragraphs.append(f'<p>{p}</p>')
        elif p:
            html_paragraphs.append(p)
    
    return '\n'.join(html_paragraphs)

def main():
    # Read the project plan markdown file
    try:
        with open('project_plan.md', 'r', encoding='utf-8') as f:
            markdown_content = f.read()
    except FileNotFoundError:
        print("❌ Error: project_plan.md not found")
        return
    
    # Convert markdown to HTML
    html_content = markdown_to_html(markdown_content)
    
    # Create a complete HTML document with styling
    full_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portfolio Website - Project Plan</title>
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
        ul, ol {{
            padding-left: 20px;
        }}
        li {{
            margin-bottom: 0.5em;
        }}
        blockquote {{
            border-left: 4px solid #3498db;
            margin: 0;
            padding-left: 20px;
            color: #666;
        }}
        p {{
            margin-bottom: 1em;
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
    
    # Write the HTML file
    output_file = 'project_plan.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_html)
    
    print(f'✅ HTML version created: {os.path.abspath(output_file)}')
    print('📄 You can open this file in a browser and use "Print to PDF" to create a PDF')
    print(f'🖨️  Or use: open "{output_file}" to view in browser')

if __name__ == '__main__':
    main()