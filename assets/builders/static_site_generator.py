import os
import re
import shutil
from pathlib import Path
import markdown

class StaticSiteGenerator:
    def __init__(self, site_path="../content/", output_path="../view/", css_path="../style/css/v01/"):
        self.site_path = Path(site_path)
        self.output_path = Path(output_path)
        self.css_path = Path(css_path)
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
    <link rel="stylesheet" href="css/main.css">
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
    
    def copy_css_files(self):
        """Copy CSS files to output directory"""
        css_output_path = self.output_path / "css"
        css_output_path.mkdir(parents=True, exist_ok=True)
        
        # Copy all CSS files from the css directory
        if self.css_path.exists():
            for css_file in self.css_path.glob("*.css"):
                shutil.copy2(css_file, css_output_path / css_file.name)
                print(f"Copied {css_file.name} to output directory")
    
    def generate(self):
        """Generate entire website"""
        self.output_path.mkdir(parents=True, exist_ok=True)
        
        print("Copying CSS files...")
        self.copy_css_files()
        
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
