#!/usr/bin/env python3
"""
Markdown to HTML Converter
Converts .md files from about/ folder to HTML with CSS styling
"""

import os
import markdown
from pathlib import Path

def read_file(filepath):
    """Read content from a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(filepath, content):
    """Write content to a file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def get_css_content(css_folder):
    """Read all CSS files and combine them."""
    css_content = ""
    css_path = Path(css_folder)
    
    if css_path.exists():
        for css_file in sorted(css_path.glob('*.css')):
            css_content += read_file(css_file) + "\n"
    
    return css_content

def create_html_template(title, content, footer_html, css_content, notice_html=None):
    """Create complete HTML document with CSS and footer."""
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        {css_content}
        
        /* Additional styling for structure */
        body {{
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
        }}
        
        .notice-banner {{
            background-color: #fff3cd;
            border-bottom: 2px solid #ffc107;
            padding: 15px 20px;
            text-align: center;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        footer {{
            margin-top: 60px;
            padding: 20px;
            background-color: #f8f9fa;
            border-top: 1px solid #dee2e6;
        }}
    </style>
</head>
<body>
"""
    
    # Add notice banner if provided (only for home page)
    if notice_html:
        html += f"""    <div class="notice-banner">
        {notice_html}
    </div>
"""
    
    # Add main content
    html += f"""    <div class="container">
        {content}
    </div>
    
    <footer>
        <div class="container">
            {footer_html}
        </div>
    </footer>
</body>
</html>"""
    
    return html

def convert_md_to_html():
    """Main function to convert markdown files to HTML."""
    # Define paths
    about_folder = 'assets/site/content/old_markdown'
    css_folder = 'assets/site/style/css'
    html_folder = 'assets/site/html'
    
    # Read CSS content
    print("Reading CSS files...")
    css_content = get_css_content(css_folder)
    
    # Read footer
    footer_path = os.path.join(about_folder, 'footer.md')
    footer_html = ""
    if os.path.exists(footer_path):
        print("Reading footer.md...")
        footer_md = read_file(footer_path)
        footer_html = markdown.markdown(footer_md)
    else:
        print("Warning: footer.md not found")
    
    # Read notice
    notice_path = os.path.join(about_folder, 'notice.md')
    notice_html = None
    if os.path.exists(notice_path):
        print("Reading notice.md...")
        notice_md = read_file(notice_path)
        notice_html = markdown.markdown(notice_md)
    else:
        print("Warning: notice.md not found")
    
    # Create html folder if it doesn't exist
    os.makedirs(html_folder, exist_ok=True)
    
    # Process all .md files in about folder
    about_path = Path(about_folder)
    if not about_path.exists():
        print(f"Error: {about_folder} folder not found")
        return
    
    md_files = list(about_path.glob('*.md'))
    
    # Filter out footer.md and notice.md
    md_files = [f for f in md_files if f.name not in ['footer.md', 'notice.md']]
    
    if not md_files:
        print("No markdown files found to convert")
        return
    
    print(f"\nConverting {len(md_files)} markdown file(s)...\n")
    
    for md_file in md_files:
        # Read markdown content
        md_content = read_file(md_file)
        
        # Convert to HTML
        html_content = markdown.markdown(md_content, extensions=['extra', 'codehilite'])
        
        # Determine if this is the home page
        is_home = md_file.stem.lower() in ['home', 'index', 'readme']
        
        # Create full HTML with template
        title = md_file.stem.replace('_', ' ').replace('-', ' ').title()
        full_html = create_html_template(
            title, 
            html_content, 
            footer_html, 
            css_content,
            notice_html if is_home else None
        )
        
        # Write to html folder
        output_file = os.path.join(html_folder, f"{md_file.stem}.html")
        write_file(output_file, full_html)
        
        print(f"Converted: {md_file.name} -> {md_file.stem}.html")
    
    print(f"\nConversion complete! HTML files saved in '{html_folder}/' folder")

if __name__ == "__main__":
    convert_md_to_html()
