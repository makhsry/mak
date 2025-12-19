#!/usr/bin/env python3
"""
Resume Website Generator
Parses README.md and generates HTML files for GitHub Pages
"""

import re
import os
from pathlib import Path


class ResumeParser:
    def __init__(self, readme_path="README.md"):
        self.readme_path = readme_path
        self.content = self._read_file()
        self.sections = {}
        
    def _read_file(self):
        """Read the README.md file"""
        with open(self.readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def parse(self):
        """Parse the README.md file into sections"""
        # Extract contact info
        self.contact = self._extract_contact()
        
        # Extract summary sections
        self.prof_summary = self._extract_section_content("## Professional Summary")
        self.org_culture = self._extract_section_content("## Organizational Culture")
        self.tech_summary = self._extract_section_content("## Technical Summary")
        
        # Extract main sections
        self.education = self._parse_education()
        self.experience = self._parse_experience()
        self.awards = self._parse_awards()
        self.talks = self._parse_talks()
        self.publications = self._parse_publications()
        
    def _extract_contact(self):
        """Extract contact information"""
        contact_pattern = r'## Contact.*?<details.*?>(.*?)</details>'
        match = re.search(contact_pattern, self.content, re.DOTALL)
        if match:
            content = match.group(1)
            email = re.search(r'\*\*Email\*\*:\s*(.+)', content)
            mobile = re.search(r'\*\*Mobile\*\*:\s*(.+)', content)
            linkedin = re.search(r'\*\*LinkedIn\*\*:\s*(.+)', content)
            github = re.search(r'\*\*GitHub\*\*:\s*(.+)', content)
            scholar = re.search(r'\*\*Google Scholar\*\*:\s*(.+)', content)
            
            return {
                'email': email.group(1).strip() if email else '',
                'mobile': mobile.group(1).strip() if mobile else '',
                'linkedin': linkedin.group(1).strip() if linkedin else '',
                'github': github.group(1).strip() if github else '',
                'scholar': scholar.group(1).strip() if scholar else ''
            }
        return {}
    
    def _extract_section_content(self, section_title):
        """Extract content between section markers"""
        pattern = rf'{re.escape(section_title)}.*?<details.*?>(.*?)</details>'
        match = re.search(pattern, self.content, re.DOTALL)
        if match:
            return match.group(1).strip()
        return ""
    
    def _parse_education(self):
        """Parse education section"""
        education = []
        # Find education section
        edu_section = re.search(r'# Education(.*?)(?=# Experience|$)', self.content, re.DOTALL)
        if not edu_section:
            return education
        
        # Find each degree
        degrees = re.findall(r'## (.*?), <a href="(.*?)">(.*?)</a>.*?<details.*?>(.*?)</details>', 
                            edu_section.group(1), re.DOTALL)
        
        for degree_title, url, institution, content in degrees:
            # Extract year from title
            year_match = re.search(r'\((\d{4}.*?)\)', degree_title)
            years = year_match.group(1) if year_match else ""
            degree_name = re.sub(r'\s*\(.*?\)', '', degree_title).strip()
            
            # Extract project, goal, summary, tasks
            project = self._extract_field(content, "Project")
            goal = self._extract_field(content, "Project Goal")
            summary = self._extract_field(content, "Project Summary")
            tasks = self._extract_tasks(content)
            
            education.append({
                'degree': degree_name,
                'institution': institution,
                'url': url,
                'years': years,
                'project': project,
                'goal': goal,
                'summary': summary,
                'tasks': tasks
            })
        
        return education
    
    def _parse_experience(self):
        """Parse experience section"""
        experience = []
        # Find experience section
        exp_section = re.search(r'# Experience(.*?)(?=# Awards|$)', self.content, re.DOTALL)
        if not exp_section:
            return experience
        
        # Find each position
        positions = re.findall(r'## (.*?), <a href="(.*?)">(.*?)</a>.*?\(([^)]+)\).*?<details.*?>(.*?)</details>', 
                              exp_section.group(1), re.DOTALL)
        
        for title, url, org, dates, content in positions:
            # Extract project info
            project = self._extract_field(content, "Project")
            goal = self._extract_field(content, "Project Goal")
            tasks = self._extract_tasks(content)
            sample_projects = self._extract_sample_projects(content)
            
            # Check for "with" supervisor info
            with_match = re.search(r'with \[([^\]]+)\]\(([^)]+)\)', content)
            supervisor = with_match.group(1) if with_match else ""
            supervisor_url = with_match.group(2) if with_match else ""
            
            experience.append({
                'title': title.strip(),
                'organization': org.strip(),
                'url': url.strip(),
                'dates': dates.strip(),
                'project': project,
                'goal': goal,
                'tasks': tasks,
                'sample_projects': sample_projects,
                'supervisor': supervisor,
                'supervisor_url': supervisor_url
            })
        
        return experience
    
    def _parse_awards(self):
        """Parse awards section"""
        awards = []
        awards_section = re.search(r'# Awards(.*?)(?=# Talks|$)', self.content, re.DOTALL)
        if not awards_section:
            return awards
        
        # Find each award
        award_blocks = re.findall(r'## (.*?)\n.*?>>>(.*?)(?=\n.*?>.*?##|\n.*?---)', 
                                 awards_section.group(1), re.DOTALL)
        
        for title, content in award_blocks:
            # Extract amount and date from title
            amount_match = re.search(r'amounting\s+([\d,.]+ (?:CAD|Euros?))', title)
            date_match = re.search(r'([A-Z][a-z]+ \d{4})', title)
            
            amount = amount_match.group(1) if amount_match else ""
            date = date_match.group(1) if date_match else ""
            award_name = re.sub(r',?\s*amounting.*|,?\s*[A-Z][a-z]+ \d{4}', '', title).strip()
            
            # Extract issuer
            issuer_match = re.search(r'Issued by (.*?)(?:\n|$)', content)
            issuer = issuer_match.group(1).strip() if issuer_match else ""
            
            # Extract description
            desc_lines = [line.strip() for line in content.split('\n') 
                         if line.strip() and not line.strip().startswith('Issued by')]
            description = ' '.join(desc_lines)
            
            awards.append({
                'title': award_name,
                'date': date,
                'amount': amount,
                'issuer': issuer,
                'description': description
            })
        
        return awards
    
    def _parse_talks(self):
        """Parse talks section"""
        talks = []
        talks_section = re.search(r'# Talks(.*?)(?=# Publications|$)', self.content, re.DOTALL)
        if not talks_section:
            return talks
        
        # Find each talk
        talk_blocks = re.findall(r'## \*\*(.*?)\*\*, \[(.*?)\]\((.*?)\), (.*?), (.*?)\n.*?>>>(.*?)(?=\n.*?>.*?##|\n.*?---)', 
                                talks_section.group(1), re.DOTALL)
        
        for role, institution, url, location, date, content in talk_blocks:
            description = ' '.join([line.strip() for line in content.split('\n') if line.strip()])
            
            talks.append({
                'role': role.strip(),
                'institution': institution.strip(),
                'url': url.strip(),
                'location': location.strip(),
                'date': date.strip(),
                'description': description
            })
        
        return talks
    
    def _parse_publications(self):
        """Parse publications section"""
        pubs_section = re.search(r'# Publications(.*?)$', self.content, re.DOTALL)
        if not pubs_section:
            return []
        
        # Extract citations and h-index
        metrics_match = re.search(r'\*\*Citation\*\*\s+(\d+).*?\*\*h-index\*\*\s+(\d+)', pubs_section.group(1))
        citations = metrics_match.group(1) if metrics_match else "0"
        h_index = metrics_match.group(2) if metrics_match else "0"
        
        # Extract publication titles
        pub_titles = re.findall(r'>> \d+\.\s+\[(.*?)\]', pubs_section.group(1))
        
        return {
            'citations': citations,
            'h_index': h_index,
            'titles': pub_titles
        }
    
    def _extract_field(self, content, field_name):
        """Extract a specific field from content"""
        pattern = rf'\*\*{field_name}\*\*.*?>>>(.*?)(?=\n.*?>.*?\*\*|</details>)'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            text = match.group(1).strip()
            # Remove >> markers and clean up
            text = re.sub(r'^>>+\s*', '', text, flags=re.MULTILINE)
            return text
        return ""
    
    def _extract_tasks(self, content):
        """Extract tasks list"""
        tasks_pattern = r'\*\*Tasks Performed\*\*.*?>>>(.*?)(?=\n.*?>.*?\*\*|</details>|---)'
        match = re.search(tasks_pattern, content, re.DOTALL)
        if match:
            tasks_text = match.group(1)
            # Find all list items
            tasks = re.findall(r'>>?\s*-\s+(.*?)(?=\n.*?>>?\s*-|\n.*?>>?\s*<img|$)', 
                              tasks_text, re.DOTALL)
            return [task.strip() for task in tasks if task.strip()]
        return []
    
    def _extract_sample_projects(self, content):
        """Extract sample projects if they exist"""
        projects_pattern = r'\*\*Sample Projects\*\*.*?>>>(.*?)(?=\n.*?>.*?---)'
        match = re.search(projects_pattern, content, re.DOTALL)
        if match:
            projects_text = match.group(1)
            projects = re.findall(r'>>?\s*-\s+(.*?)(?=\n.*?>>?\s*-|$)', 
                                projects_text, re.DOTALL)
            return [proj.strip() for proj in projects if proj.strip()]
        return []


class HTMLGenerator:
    def __init__(self, parser):
        self.parser = parser
        self.output_dir = Path(".")
        
    def generate_all(self):
        """Generate all HTML files"""
        self.generate_index()
        self.generate_education()
        self.generate_experience()
        self.generate_awards()
        self.generate_talks()
        self.generate_publications()
        print("All HTML files generated successfully!")
    
    def _get_header(self, active_page=""):
        """Generate common header"""
        pages = [
            ("index.html", "Home"),
            ("education.html", "Education"),
            ("experience.html", "Experience"),
            ("awards.html", "Awards"),
            ("talks.html", "Talks"),
            ("publications.html", "Publications")
        ]
        
        nav_items = ""
        for page, title in pages:
            nav_items += f'                <li><a href="{page}">{title}</a></li>\n'
        
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{title}} - Milad Asgarpour Khansary</title>
    <link rel="stylesheet" href="assets/css/main.css">
</head>
<body>
    <header>
        <nav>
            <div class="logo">
                <a href="index.html">Milad Asgarpour Khansary</a>
            </div>
            <ul>
{nav_items}            </ul>
        </nav>
    </header>
'''
    
    def _get_footer(self):
        """Generate common footer"""
        contact = self.parser.contact
        return f'''
    <footer>
        <div class="footer-content">
            <div class="footer-section">
                <h4>About</h4>
                <p>Process Engineer specializing in chemical and mining engineering with expertise in data analytics and industrial system optimization.</p>
            </div>
            <div class="footer-section">
                <h4>Contact</h4>
                <p>Email: {contact.get('email', '')}</p>
                <p>Mobile: {contact.get('mobile', '')}</p>
            </div>
            <div class="footer-section">
                <h4>Links</h4>
                <p><a href="{contact.get('linkedin', '#')}" target="_blank">LinkedIn</a></p>
                <p><a href="{contact.get('github', '#')}" target="_blank">GitHub</a></p>
                <p><a href="{contact.get('scholar', '#')}" target="_blank">Google Scholar</a></p>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; 2025 Milad Asgarpour Khansary. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>'''
    
    def generate_index(self):
        """Generate index.html"""
        header = self._get_header().replace("{title}", "Home")
        contact = self.parser.contact
        
        # Extract bullet points from summaries
        prof_bullets = self._extract_bullets(self.parser.prof_summary)
        org_bullets = self._extract_bullets(self.parser.org_culture)
        tech_content = self._parse_tech_summary(self.parser.tech_summary)
        
        html = header + f'''
    <section class="hero">
        <div class="container">
            <h1>Milad Asgarpour Khansary</h1>
            <p>Process Engineer | Chemical & Mining Engineering | Data Analytics</p>
        </div>
    </section>

    <main class="container">
        <div class="intro-text">
            <p><strong>Note:</strong> This is a personal page, and all information presented here is for personal use and reference only, and I do not represent any organization or employer.</p>
        </div>

        <section class="section">
            <div class="section-header">
                <h2>Professional Summary</h2>
            </div>
            <div class="profile-box">
                <div class="profile-content">
                    {prof_bullets}
                </div>
            </div>
        </section>

        <section class="section">
            <div class="section-header">
                <h2>Organizational Culture</h2>
            </div>
            {org_bullets}
        </section>

        <section class="section">
            <div class="section-header">
                <h2>Technical Summary</h2>
            </div>
            {tech_content}
        </section>

        <section class="section">
            <div class="section-header">
                <h2>Contact</h2>
            </div>
            <ul style="line-height: 2;">
                <li><strong>Email:</strong> {contact.get('email', '')}</li>
                <li><strong>Mobile:</strong> {contact.get('mobile', '')}</li>
                <li><strong>LinkedIn:</strong> <a href="{contact.get('linkedin', '#')}" target="_blank">{contact.get('linkedin', '')}</a></li>
                <li><strong>GitHub:</strong> <a href="{contact.get('github', '#')}" target="_blank">{contact.get('github', '')}</a></li>
                <li><strong>Google Scholar:</strong> <a href="{contact.get('scholar', '#')}" target="_blank">Google Scholar Profile</a></li>
            </ul>
        </section>

        <section class="section">
            <div class="section-header">
                <h2>Quick Links</h2>
            </div>
            <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                <a href="education.html" class="btn-primary">Education</a>
                <a href="experience.html" class="btn-primary">Experience</a>
                <a href="awards.html" class="btn-primary">Awards & Recognition</a>
                <a href="talks.html" class="btn-primary">Talks & Presentations</a>
                <a href="publications.html" class="btn-primary">Publications</a>
            </div>
        </section>
    </main>
'''
        
        html += self._get_footer()
        
        with open(self.output_dir / "index.html", 'w', encoding='utf-8') as f:
            f.write(html)
        print("✓ Generated index.html")
    
    def generate_education(self):
        """Generate education.html"""
        header = self._get_header().replace("{title}", "Education")
        
        cards = ""
        for edu in self.parser.education:
            tasks_html = self._format_tasks(edu['tasks'])
            
            cards += f'''
                <div class="card">
                    <div class="card-content">
                        <h3 class="card-title">{edu['degree']}</h3>
                        <p class="card-meta"><a href="{edu['url']}" target="_blank">{edu['institution']}</a> | {edu['years']}</p>
                        
                        <h4 style="margin-top: 1rem; margin-bottom: 0.5rem;">Project</h4>
                        <p class="card-text">{edu['project']}</p>
                        
                        <h4 style="margin-top: 1rem; margin-bottom: 0.5rem;">Project Goal</h4>
                        <p class="card-text">{edu['goal']}</p>
'''
            
            if edu['summary']:
                cards += f'''
                        <h4 style="margin-top: 1rem; margin-bottom: 0.5rem;">Project Summary</h4>
                        <p class="card-text">{edu['summary']}</p>
'''
            
            if tasks_html:
                cards += f'''
                        <h4 style="margin-top: 1rem; margin-bottom: 0.5rem;">Tasks Performed</h4>
                        {tasks_html}
'''
            
            cards += '''
                    </div>
                </div>
'''
        
        html = header + f'''
    <main class="container">
        <section class="section">
            <div class="section-header">
                <h2>Education</h2>
            </div>

            <div class="cards">
{cards}            </div>
        </section>
    </main>
'''
        
        html += self._get_footer()
        
        with open(self.output_dir / "education.html", 'w', encoding='utf-8') as f:
            f.write(html)
        print("✓ Generated education.html")
    
    def generate_experience(self):
        """Generate experience.html"""
        header = self._get_header().replace("{title}", "Experience")
        
        cards = ""
        for exp in self.parser.experience:
            tasks_html = self._format_tasks(exp['tasks'])
            sample_proj_html = self._format_tasks(exp['sample_projects']) if exp['sample_projects'] else ""
            
            supervisor_text = ""
            if exp['supervisor']:
                supervisor_text = f'<p class="card-text">With <a href="{exp["supervisor_url"]}" target="_blank">{exp["supervisor"]}</a>.</p>'
            
            cards += f'''
                <div class="card">
                    <div class="card-content">
                        <h3 class="card-title">{exp['title']}</h3>
                        <p class="card-meta"><a href="{exp['url']}" target="_blank">{exp['organization']}</a></p>
                        <p class="card-meta">{exp['dates']}</p>
                        {supervisor_text}
'''
            
            if exp['project']:
                cards += f'''
                        <h4 style="margin-top: 1rem; margin-bottom: 0.5rem;">Project</h4>
                        <p class="card-text">{exp['project']}</p>
'''
            
            if exp['goal']:
                cards += f'''
                        <h4 style="margin-top: 1rem; margin-bottom: 0.5rem;">Project Goal</h4>
                        <p class="card-text">{exp['goal']}</p>
'''
            
            if tasks_html:
                cards += f'''
                        <h4 style="margin-top: 1rem; margin-bottom: 0.5rem;">Tasks Performed</h4>
                        {tasks_html}
'''
            
            if sample_proj_html:
                cards += f'''
                        <h4 style="margin-top: 1rem; margin-bottom: 0.5rem;">Sample Projects</h4>
                        {sample_proj_html}
'''
            
            cards += '''
                    </div>
                </div>
'''
        
        html = header + f'''
    <main class="container">
        <section class="section">
            <div class="section-header">
                <h2>Professional Experience</h2>
            </div>

            <div class="cards">
{cards}            </div>
        </section>
    </main>
'''
        
        html += self._get_footer()
        
        with open(self.output_dir / "experience.html", 'w', encoding='utf-8') as f:
            f.write(html)
        print("✓ Generated experience.html")
    
    def generate_awards(self):
        """Generate awards.html"""
        header = self._get_header().replace("{title}", "Awards")
        
        cards = ""
        for award in self.parser.awards:
            amount_text = f" | {award['amount']}" if award['amount'] else ""
            
            cards += f'''
                <div class="card">
                    <div class="card-content">
                        <h3 class="card-title">{award['title']}</h3>
                        <p class="card-meta">{award['date']}{amount_text}</p>
                        <p class="card-text">{award['issuer']}</p>
'''
            
            if award['description']:
                cards += f'''
                        <p class="card-text" style="margin-top: 0.5rem;">{award['description']}</p>
'''
            
            cards += '''
                    </div>
                </div>
'''
        
        html = header + f'''
    <main class="container">
        <section class="section">
            <div class="section-header">
                <h2>Awards & Recognition</h2>
            </div>

            <div class="cards">
{cards}            </div>
        </section>
    </main>
'''
        
        html += self._get_footer()
        
        with open(self.output_dir / "awards.html", 'w', encoding='utf-8') as f:
            f.write(html)
        print("✓ Generated awards.html")
    
    def generate_talks(self):
        """Generate talks.html"""
        header = self._get_header().replace("{title}", "Talks")
        
        cards = ""
        for talk in self.parser.talks:
            cards += f'''
                <div class="card">
                    <div class="card-content">
                        <h3 class="card-title">{talk['role']} - {talk['institution']}</h3>
                        <p class="card-meta"><a href="{talk['url']}" target="_blank">{talk['institution']}</a>, {talk['location']}</p>
                        <p class="card-meta">{talk['date']}</p>
                        <p class="card-text">{talk['description']}</p>
                    </div>
                </div>
'''
        
        html = header + f'''
    <main class="container">
        <section class="section">
            <div class="section-header">
                <h2>Talks & Presentations</h2>
            </div>

            <div class="cards">
{cards}            </div>
        </section>
    </main>
'''
        
        html += self._get_footer()
        
        with open(self.output_dir / "talks.html", 'w', encoding='utf-8') as f:
            f.write(html)
        print("✓ Generated talks.html")
    
    def generate_publications(self):
        """Generate publications.html"""
        header = self._get_header().replace("{title}", "Publications")
        contact = self.parser.contact
        pubs = self.parser.publications
        
        pub_list = ""
        for title in pubs['titles']:
            pub_list += f'''
                <li class="news-item">
                    <div class="news-title">{title}</div>
                </li>
'''
        
        html = header + f'''
    <main class="container">
        <section class="section">
            <div class="section-header">
                <h2>Publications</h2>
            </div>

            <div style="background: #f8f9fa; padding: 2rem; border-radius: 4px; border: 1px solid #e0e0e0; margin-bottom: 2rem;">
                <h3 style="margin-bottom: 1rem;">Metrics</h3>
                <p><strong>For an up-to-date list, please refer to <a href="{contact.get('scholar', '#')}" target="_blank">Google Scholar</a>.</strong></p>
                <p style="margin-top: 1rem;"><strong>Citations:</strong> {pubs['citations']} | <strong>h-index:</strong> {pubs['h_index']}</p>
            </div>

            <div class="section-header">
                <h3>Selected Publications</h3>
            </div>

            <ul class="news-list" style="list-style: none;">
{pub_list}            </ul>

            <div style="margin-top: 2rem; padding: 1.5rem; background: #e8f4f8; border-left: 4px solid #007bff; border-radius: 4px;">
                <p><strong>Note:</strong> For the most current and complete list of publications, including citation details and full-text access where available, please visit my <a href="{contact.get('scholar', '#')}" target="_blank">Google Scholar profile</a>.</p>
            </div>
        </section>
    </main>
'''
        
        html += self._get_footer()
        
        with open(self.output_dir / "publications.html", 'w', encoding='utf-8') as f:
            f.write(html)
        print("✓ Generated publications.html")
    
    def _extract_bullets(self, content):
        """Extract bullet points from content"""
        bullets = re.findall(r'-\s+(.*?)(?=\n\s*-|\n\s*---|\n\s*>|$)', content, re.DOTALL)
        if bullets:
            html = '<ul style="line-height: 2;">\n'
            for bullet in bullets:
                cleaned = bullet.strip().replace('\n', ' ')
                html += f'                <li>{cleaned}</li>\n'
            html += '            </ul>'
            return html
        return f'<p>{content}</p>'
    
    def _parse_tech_summary(self, content):
        """Parse technical summary with subsections"""
        sections = re.findall(r'\*\*(.*?)\*\*\s*>>+\s*-\s+(.*?)(?=\n\s*>\s*\*\*|\n\s*---)', 
                             content, re.DOTALL)
        
        html = ""
        for title, items in sections:
            cleaned_items = items.strip().replace('\n', ' ')
            html += f'''
            <h3 style="margin-top: 1.5rem; margin-bottom: 0.5rem;">{title}</h3>
            <p>{cleaned_items}</p>
'''
        return html
    
    def _format_tasks(self, tasks):
        """Format task list as HTML"""
        if not tasks:
            return ""
        
        html = '<ul class="card-text" style="margin-left: 1.5rem; line-height: 1.8;">\n'
        for task in tasks:
            html += f'                            <li>{task}</li>\n'
        html += '                        </ul>'
        return html


def main():
    """Main execution"""
    print("Resume Website Generator")
    print("=" * 50)
    
    # Check if README.md exists
    if not os.path.exists("README.md"):
        print("Error: README.md not found in current directory")
        return
    
    # Parse README.md
    print("📖 Parsing README.md...")
    parser = ResumeParser()
    parser.parse()
    
    # Generate HTML files
    print("Generating HTML files...")
    generator = HTMLGenerator(parser)
    generator.generate_all()
    
    print("=" * 50)
    print("Done! Your website is ready for GitHub Pages.")


if __name__ == "__main__":
    main()
