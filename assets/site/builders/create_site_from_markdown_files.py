#!/usr/bin/env python3
"""
Markdown to HTML Converter
Converts .md files to HTML with linked CSS files from assets/site/style/css
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

def get_css_files(css_folder):
    """Get list of CSS files in the folder."""
    css_files = []
    css_path = Path(css_folder)
    
    if css_path.exists():
        for css_file in sorted(css_path.glob('*.css')):
            css_files.append(css_file.name)
    
    return css_files

def create_css_links(css_files, css_folder):
    """Create HTML link tags for CSS files."""
    links = []
    for css_file in css_files:
        links.append(f'    <link rel="stylesheet" href="{css_folder}/{css_file}">')
    return '\n'.join(links)

def create_html_template(title, content, footer_html, css_links, notice_html=None):
    """Create complete HTML document with linked CSS files and footer."""
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
{css_links}
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
    md_folder = 'assets/site/content' #/old_markdown'  # Current directory where .md files are
    css_folder = 'assets/site/style/css'
    html_folder = 'assets/site/view'
    
    # Absolute path from root
    css_folder = '/assets/site/style/css'
    
    # Get CSS files
    print("Finding CSS files...")
    css_files = get_css_files(css_folder)
    
    if not css_files:
        print(f"Warning: No CSS files found in {css_folder}")
    else:
        print(f"Found {len(css_files)} CSS file(s): {', '.join(css_files)}")
    
    # Create CSS link tags
    css_links = create_css_links(css_files, css_folder)
    
    # Read footer
    footer_path = 'footer.md'
    footer_html = ""
    if os.path.exists(footer_path):
        print("Reading footer.md...")
        footer_md = read_file(footer_path)
        footer_html = markdown.markdown(footer_md)
    else:
        print("Warning: footer.md not found")
    
    # Read notice
    notice_path = 'notice.md'
    notice_html = None
    if os.path.exists(notice_path):
        print("Reading notice.md...")
        notice_md = read_file(notice_path)
        notice_html = markdown.markdown(notice_md)
    else:
        print("Info: notice.md not found (optional)")
    
    # Create html folder if it doesn't exist
    os.makedirs(html_folder, exist_ok=True)
    
    # Find all .md files in current directory
    md_path = Path(md_folder)
    md_files = list(md_path.glob('*.md'))
    
    # Filter out footer.md and notice.md
    md_files = [f for f in md_files if f.name not in ['footer.md', 'notice.md']]
    
    if not md_files:
        print("No markdown files found to convert")
        return
    
    print(f"\nConverting {len(md_files)} markdown file(s)...\n")
    
    for md_file in md_files:
        # Read markdown content
        md_content = read_file(md_file)
        
        # Convert to HTML with extensions for better formatting
        html_content = markdown.markdown(
            md_content, 
            extensions=['extra', 'codehilite', 'tables', 'fenced_code']
        )
        
        # Determine if this is the home page
        is_home = md_file.stem.lower() in ['home', 'index', 'readme', 'introduction']
        
        # Create full HTML with template
        title = md_file.stem.replace('_', ' ').replace('-', ' ').title()
        full_html = create_html_template(
            title, 
            html_content, 
            footer_html, 
            css_links,
            notice_html if is_home else None
        )
        
        # Determine output filename - use index.html for introduction.md
        if md_file.stem.lower() == 'introduction':
            output_filename = 'index.html'
            print(f"Converted: {md_file.name} -> index.html (home page)")
        else:
            output_filename = f"{md_file.stem}.html"
            print(f"Converted: {md_file.name} -> {output_filename}")
        
        # Write to html folder
        output_file = os.path.join(html_folder, output_filename)
        write_file(output_file, full_html)
    
    print(f"\n{'='*60}")
    print(f"Conversion complete!")
    print(f"HTML files saved in: {html_folder}/")
    print(f"CSS files linked from: {css_folder}/")
    print(f"{'='*60}")

if __name__ == "__main__":
    try:
        convert_md_to_html()
    except Exception as e:
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()