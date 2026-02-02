import os
import re
from pathlib import Path
import markdown

class StaticSiteGenerator:
    def __init__(self, site_path="../content/", output_path="../view/"):
        self.site_path = Path(site_path)
        self.output_path = Path(output_path)
        self.header_content = ""
        self.footer_content = ""
        
    def extract_number(self, filename):
        """Extract leading number from filename"""
        match = re.match(r'^(\d+)', filename)
        return int(match.group(1)) if match else 0
    
    def read_markdown(self, filepath):
        """Read and convert markdown to HTML"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return markdown.markdown(content, extensions=['extra', 'codehilite'])
    
    def load_edges(self):
        """Load header and footer from edges directory"""
        edges_path = self.site_path / "edges"
        
        header_file = edges_path / "header.md"
        if header_file.exists():
            self.header_content = self.read_markdown(header_file)
        
        footer_file = edges_path / "footer.md"
        if footer_file.exists():
            self.footer_content = self.read_markdown(footer_file)
    
    def get_sorted_files(self, directory, reverse=False):
        """Get markdown files sorted by leading number"""
        files = [f for f in directory.glob("*.md") if f.name not in ['header.md', 'footer.md']]
        sorted_files = sorted(files, key=lambda x: self.extract_number(x.stem), reverse=reverse)
        return sorted_files
    
    def create_card(self, content, title=""):
        """Wrap content in a card structure"""
        return f'''
        <div class="card">
            {f'<h3>{title}</h3>' if title else ''}
            {content}
        </div>
        '''
    
    def create_page(self, title, cards_html, active_page=""):
        """Create complete HTML page with navigation"""
        nav_items = {
            "Home": "index.html",
            "Education": "education.html",
            "Experience": "experience.html",
            "Blog": "blog.html"
        }
        
        nav_html = ""
        for name, link in nav_items.items():
            active_class = "active" if name.lower() == active_page.lower() else ""
            nav_html += f'<a href="{link}" class="{active_class}">{name}</a>'
        
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }}
        
        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .header-content {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
        }}
        
        .header-content h1 {{
            margin-bottom: 0.5rem;
        }}
        
        nav {{
            background: white;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            position: sticky;
            top: 0;
            z-index: 100;
        }}
        
        nav .nav-container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
            display: flex;
            gap: 1rem;
        }}
        
        nav a {{
            display: inline-block;
            padding: 1rem 1.5rem;
            text-decoration: none;
            color: #667eea;
            font-weight: 500;
            transition: all 0.3s ease;
            border-bottom: 3px solid transparent;
        }}
        
        nav a:hover {{
            background: #f5f5f5;
            border-bottom-color: #667eea;
        }}
        
        nav a.active {{
            border-bottom-color: #667eea;
            color: #764ba2;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 2rem auto;
            padding: 0 2rem;
        }}
        
        .card {{
            background: white;
            border-radius: 8px;
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        
        .card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        
        .card h3 {{
            color: #667eea;
            margin-bottom: 1rem;
            font-size: 1.5rem;
        }}
        
        .card p {{
            margin-bottom: 1rem;
        }}
        
        .card ul, .card ol {{
            margin-left: 2rem;
            margin-bottom: 1rem;
        }}
        
        .blog-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 2rem;
            margin-top: 2rem;
        }}
        
        .blog-card {{
            background: white;
            border-radius: 8px;
            padding: 1.5rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
            cursor: pointer;
        }}
        
        .blog-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        
        .blog-card h3 {{
            color: #667eea;
            margin-bottom: 1rem;
        }}
        
        footer {{
            background: #2d3748;
            color: white;
            padding: 2rem 0;
            margin-top: 4rem;
        }}
        
        .footer-content {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
        }}
        
        @media (max-width: 768px) {{
            nav .nav-container {{
                flex-direction: column;
                gap: 0;
            }}
            
            nav a {{
                padding: 0.75rem 1rem;
            }}
            
            .blog-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <header>
        <div class="header-content">
            {self.header_content}
        </div>
    </header>
    
    <nav>
        <div class="nav-container">
            {nav_html}
        </div>
    </nav>
    
    <div class="container">
        {cards_html}
    </div>
    
    <footer>
        <div class="footer-content">
            {self.footer_content}
        </div>
    </footer>
</body>
</html>'''
    
    def generate_about_page(self):
        """Generate homepage from about directory"""
        about_path = self.site_path / "about"
        if not about_path.exists():
            return
        
        files = self.get_sorted_files(about_path, reverse=False)
        cards_html = ""
        
        for file in files:
            content = self.read_markdown(file)
            cards_html += self.create_card(content)
        
        html = self.create_page("Home", cards_html, "Home")
        
        output_file = self.output_path / "index.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
    
    def generate_standard_page(self, directory_name, page_title):
        """Generate education/experience pages (largest to smallest)"""
        dir_path = self.site_path / directory_name
        if not dir_path.exists():
            return
        
        files = self.get_sorted_files(dir_path, reverse=True)
        cards_html = ""
        
        for file in files:
            content = self.read_markdown(file)
            cards_html += self.create_card(content)
        
        html = self.create_page(page_title, cards_html, page_title)
        
        output_file = self.output_path / f"{directory_name}.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
    
    def generate_blog_page(self):
        """Generate blog page with subdirectories"""
        blog_path = self.site_path / "blog"
        if not blog_path.exists():
            return
        
        subdirs = [d for d in blog_path.iterdir() if d.is_dir()]
        cards_html = '<div class="blog-grid">'
        
        for subdir in sorted(subdirs):
            files = self.get_sorted_files(subdir, reverse=True)
            
            if files:
                # Create a blog post page for each subdirectory
                post_cards = ""
                for file in files:
                    content = self.read_markdown(file)
                    post_cards += self.create_card(content)
                
                post_html = self.create_page(subdir.name, post_cards, "Blog")
                post_file = self.output_path / f"blog_{subdir.name}.html"
                
                with open(post_file, 'w', encoding='utf-8') as f:
                    f.write(post_html)
                
                # Create blog card linking to the post
                cards_html += f'''
                <div class="blog-card" onclick="window.location.href='blog_{subdir.name}.html'">
                    <h3>{subdir.name.replace('_', ' ').title()}</h3>
                    <p>Click to read more...</p>
                </div>
                '''
        
        cards_html += '</div>'
        
        html = self.create_page("Blog", cards_html, "Blog")
        output_file = self.output_path / "blog.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
    
    def generate(self):
        """Generate entire website"""
        self.output_path.mkdir(parents=True, exist_ok=True)
        
        print("Loading header and footer...")
        self.load_edges()
        
        print("Generating homepage...")
        self.generate_about_page()
        
        print("Generating education page...")
        self.generate_standard_page("education", "Education")
        
        print("Generating experience page...")
        self.generate_standard_page("experience", "Experience")
        
        print("Generating blog pages...")
        self.generate_blog_page()
        
        print(f"Website generated successfully in {self.output_path}")

if __name__ == "__main__":
    generator = StaticSiteGenerator()
    generator.generate()