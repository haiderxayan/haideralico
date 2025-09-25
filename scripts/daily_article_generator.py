#!/usr/bin/env python3
"""
Daily Article Generator for Haider Ali's UX Blog
Generates a new blog post every day and sends email notification
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
from pathlib import Path
import subprocess
import random

# Import GitHub notification system
from github_notifications import create_github_issue

# Configuration
BLOG_ROOT = Path(__file__).parent.parent
POSTS_DIR = BLOG_ROOT / "_posts"
EMAIL_CONFIG = {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "sender_email": "haiderxayan@gmail.com",
    "sender_password": os.getenv("EMAIL_PASSWORD"),  # Set this as environment variable
    "recipient_email": "haiderxayan@gmail.com"
}

# UX Topics for article generation
UX_TOPICS = [
    "User Research",
    "Design Systems", 
    "Mobile UX",
    "Accessibility",
    "User Psychology",
    "Information Architecture",
    "Interaction Design",
    "Usability Testing",
    "Design Thinking",
    "User Journey Mapping",
    "Wireframing",
    "Prototyping",
    "Visual Design",
    "Content Strategy",
    "Conversion Optimization",
    "AI in UX",
    "Voice Interface Design",
    "AR/VR UX",
    "Micro-interactions",
    "Design Ethics"
]

# Article templates and structures
ARTICLE_TEMPLATES = [
    {
        "type": "guide",
        "title_template": "The Complete Guide to {topic} in 2024",
        "intro_template": "In today's digital landscape, {topic} has become more crucial than ever for creating exceptional user experiences. This comprehensive guide will walk you through everything you need to know about {topic} and how to implement it effectively in your projects."
    },
    {
        "type": "tips",
        "title_template": "10 Essential {topic} Tips Every Designer Should Know",
        "intro_template": "Mastering {topic} is key to creating user-centered designs that truly resonate with your audience. Here are 10 essential tips that will elevate your {topic} skills and help you create more effective user experiences."
    },
    {
        "type": "trends",
        "title_template": "The Future of {topic}: Trends Shaping UX in 2024",
        "intro_template": "As we navigate through 2024, {topic} continues to evolve at a rapid pace. Understanding these emerging trends is crucial for staying ahead in the UX field. Let's explore what's shaping the future of {topic}."
    },
    {
        "type": "case_study",
        "title_template": "How {topic} Transformed Our User Experience",
        "intro_template": "In this case study, we'll explore how implementing {topic} led to significant improvements in user satisfaction and business metrics. Discover the strategies, challenges, and results from this real-world implementation."
    }
]

def generate_article_content(topic, template):
    """Generate article content using AI or template-based approach"""
    
    # For now, we'll use a template-based approach
    # You can integrate with OpenAI API later for more dynamic content
    
    title = template["title_template"].format(topic=topic)
    intro = template["intro_template"].format(topic=topic)
    
    # Generate article sections based on topic and type
    sections = generate_article_sections(topic, template["type"])
    
    content = f"""---
layout: post
title: "{title}"
date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
categories: ["UX Design", "{topic}"]
tags: ["{topic.lower()}", "ux", "design", "user experience"]
read_time: 8
excerpt: "{intro[:150]}..."
image: "https://images.unsplash.com/photo-1551650975-87deedd944c3?w=1200&h=630&fit=crop"
image_alt: "{topic} in UX Design"
---

{intro}

## Why {topic} Matters

{topic} plays a crucial role in creating user-centered designs that not only look great but also function seamlessly. In today's competitive digital landscape, understanding and implementing effective {topic} strategies can be the difference between a successful product and one that fails to engage users.

## Key Principles

When working with {topic}, there are several fundamental principles to keep in mind:

1. **User-Centered Approach**: Always prioritize the needs and goals of your users
2. **Consistency**: Maintain consistent patterns and behaviors across your design
3. **Accessibility**: Ensure your {topic} solutions are inclusive and accessible to all users
4. **Iteration**: Continuously test and refine your {topic} implementations

## Best Practices

Here are some proven best practices for effective {topic}:

### 1. Start with Research
Before implementing any {topic} solution, conduct thorough user research to understand your audience's needs, pain points, and behaviors.

### 2. Create User Personas
Develop detailed user personas that represent your target audience. This will help guide your {topic} decisions and ensure you're designing for real users.

### 3. Test Early and Often
Implement a continuous testing strategy to validate your {topic} choices. Use both quantitative and qualitative methods to gather insights.

### 4. Document Everything
Maintain comprehensive documentation of your {topic} decisions, rationale, and outcomes. This will help your team stay aligned and learn from past experiences.

## Common Challenges

While implementing {topic}, you may encounter several challenges:

- **Stakeholder Alignment**: Getting buy-in from all stakeholders can be difficult
- **Resource Constraints**: Limited time and budget can impact the quality of your {topic} work
- **Technical Limitations**: Sometimes technical constraints may limit your {topic} options
- **User Adoption**: Ensuring users actually adopt and use your {topic} solutions

## Tools and Resources

Here are some essential tools for {topic}:

- **Research Tools**: UserTesting, Maze, Hotjar
- **Design Tools**: Figma, Sketch, Adobe XD
- **Prototyping**: InVision, Principle, Framer
- **Analytics**: Google Analytics, Mixpanel, Amplitude

## Conclusion

{topic} is an essential component of modern UX design. By following the principles and best practices outlined in this article, you can create more effective and user-centered experiences. Remember to stay updated with the latest trends and continuously refine your approach based on user feedback and data.

## Next Steps

Ready to implement {topic} in your projects? Start by:

1. Conducting user research to understand your audience
2. Creating a {topic} strategy that aligns with your business goals
3. Building prototypes and testing with real users
4. Iterating based on feedback and data

---

*This article was automatically generated as part of our daily UX insights series. For more personalized content and consulting services, [contact us](/contact/).*
"""
    
    return content, title

def generate_article_sections(topic, article_type):
    """Generate article sections based on topic and type"""
    # This is a simplified version - you can expand this with more sophisticated content generation
    return []

def create_blog_post(content, title):
    """Create a new blog post file"""
    # Generate filename from title
    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_title = safe_title.replace(' ', '-').lower()
    
    # Create filename with date
    date_str = datetime.now().strftime('%Y-%m-%d')
    filename = f"{date_str}-{safe_title}.md"
    filepath = POSTS_DIR / filename
    
    # Write the file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filepath, filename

def send_github_notification(title, url, filename, topic, template_type):
    """Send GitHub notification with article details"""
    try:
        success = create_github_issue(title, url, filename, topic, template_type)
        if success:
            print(f"✅ GitHub notification sent successfully!")
        else:
            print(f"⚠️  GitHub notification failed")
        return success
        
    except Exception as e:
        print(f"❌ Failed to send GitHub notification: {e}")
        return False

def commit_and_push_changes(filename):
    """Commit the new blog post to git"""
    try:
        # Add the new file
        subprocess.run(['git', 'add', f'_posts/{filename}'], cwd=BLOG_ROOT, check=True)
        
        # Commit with a descriptive message
        commit_message = f"Add daily article: {filename}"
        subprocess.run(['git', 'commit', '-m', commit_message], cwd=BLOG_ROOT, check=True)
        
        # Push to remote repository
        subprocess.run(['git', 'push'], cwd=BLOG_ROOT, check=True)
        
        print(f"Successfully committed and pushed {filename}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Git operation failed: {e}")
        return False

def main():
    """Main function to generate daily article"""
    print("🚀 Starting daily article generation...")
    
    # Ensure posts directory exists
    POSTS_DIR.mkdir(exist_ok=True)
    
    # Select random topic and template
    topic = random.choice(UX_TOPICS)
    template = random.choice(ARTICLE_TEMPLATES)
    
    print(f"📝 Generating article about: {topic}")
    print(f"📋 Using template: {template['type']}")
    
    # Generate article content
    content, title = generate_article_content(topic, template)
    
    # Create blog post file
    filepath, filename = create_blog_post(content, title)
    print(f"✅ Created blog post: {filename}")
    
    # Generate URL (assuming your site is deployed)
    site_url = "https://haiderali.co"
    date_str = datetime.now().strftime('%Y-%m-%d')
    clean_filename = filename.replace('.md', '').replace(f'{date_str}-', '')
    article_url = f"{site_url}/{datetime.now().strftime('%Y/%m/%d')}/{clean_filename}/"
    
    # Send GitHub notification
    print("📱 Sending GitHub notification...")
    github_notification_sent = send_github_notification(title, article_url, filename, topic, template["type"])
    
    # Commit and push changes
    print("🔄 Committing and pushing changes...")
    git_success = commit_and_push_changes(filename)
    
    # Summary
    print("\n" + "="*50)
    print("📊 DAILY ARTICLE GENERATION SUMMARY")
    print("="*50)
    print(f"✅ Article created: {filename}")
    print(f"✅ Title: {title}")
    print(f"✅ Topic: {topic}")
    print(f"✅ Template: {template['type']}")
    print(f"✅ URL: {article_url}")
    print(f"📱 GitHub notification: {'Success' if github_notification_sent else 'Failed'}")
    print(f"🔄 Git push: {'Success' if git_success else 'Failed'}")
    print("="*50)
    
    return {
        "success": True,
        "filename": filename,
        "title": title,
        "url": article_url,
        "github_notification_sent": github_notification_sent,
        "git_success": git_success
    }

if __name__ == "__main__":
    main()
