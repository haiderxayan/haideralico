#!/usr/bin/env python3
"""
Daily Article Generator for Haider Ali's UX Blog
Generates a new blog post every day and sends email notification
"""

import os
import sys
import json
import re
import requests
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
import mimetypes
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

# Optional APIs / Integrations
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
USED_IMG_STORE = BLOG_ROOT / "assets" / "data" / "used_unsplash.json"
CATEGORY_STATE_STORE = BLOG_ROOT / "assets" / "data" / "category_cycle.json"

# Category rotation config (first category only)
# Matches site tags: Research & Strategy, Design, AI, Data Analytics, Content, Career, Development, News & Culture
CYCLE_CATEGORIES = [
    "research-strategy",
    "design",
    "ai",
    "data-analytics",
    "content",
    "career",
    "development",
    "news-culture",
]
NON_AI_CATEGORIES = [c for c in CYCLE_CATEGORIES if c != "ai"]

# Map categories to topic pools to keep content relevant
CATEGORY_TOPIC_POOL = {
    "research-strategy": [
        "User Research", "Design Thinking", "Usability Testing", "Information Architecture", "User Psychology"
    ],
    "design": [
        "Design Systems", "Interaction Design", "Prototyping", "Wireframing", "Visual Design", "Micro-interactions"
    ],
    "ai": [
        "AI in UX", "Voice Interface Design", "AR/VR UX"
    ],
    "data-analytics": [
        "Conversion Optimization", "Data Analytics"
    ],
    "content": [
        "Content Strategy"
    ],
    "career": [
        "Design Ethics"
    ],
    "development": [
        "Prototyping", "Interaction Design"
    ],
    "news-culture": [
        "Design Ethics", "Design Systems"
    ],
}

def _load_used_image_ids():
    try:
        if USED_IMG_STORE.exists():
            return set(json.loads(USED_IMG_STORE.read_text(encoding='utf-8')))
    except Exception:
        pass
    return set()

def _save_used_image_ids(ids: set):
    USED_IMG_STORE.parent.mkdir(parents=True, exist_ok=True)
    USED_IMG_STORE.write_text(json.dumps(sorted(list(ids))), encoding='utf-8')

def _load_category_state():
    try:
        if CATEGORY_STATE_STORE.exists():
            return json.loads(CATEGORY_STATE_STORE.read_text(encoding='utf-8'))
    except Exception:
        pass
    return {"index": -1, "last_date": "", "last_primary": ""}

def _save_category_state(state: dict):
    CATEGORY_STATE_STORE.parent.mkdir(parents=True, exist_ok=True)
    CATEGORY_STATE_STORE.write_text(json.dumps(state), encoding='utf-8')

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

def slugify(text: str) -> str:
    """Create a URL-friendly slug similar to Jekyll's default."""
    allowed = "abcdefghijklmnopqrstuvwxyz0123456789-"
    text = (text or "").strip().lower()
    # Replace separators with hyphens
    for ch in [" ", "_", "/", "\\", ":", ";", ",", ".", "|", "(", ")", "[", "]", "{" ,"}"]:
        text = text.replace(ch, "-")
    # Collapse multiple hyphens
    while "--" in text:
        text = text.replace("--", "-")
    # Keep only allowed
    return "".join(c for c in text if c in allowed).strip("-")

def sanitize_categories(categories):
    """Ensure categories are SEO-friendly (hyphenated, lowercase)."""
    return [slugify(c) for c in categories if c]

def fetch_unsplash_image(topic: str):
    """Fetch an Unsplash image for the topic.
    Returns (image_url, image_alt, credit_text, credit_url).
    Requires UNSPLASH_ACCESS_KEY for author credits. Fallback to source.unsplash.com without author.
    """
    topic_query = slugify(topic) or "ux"
    if UNSPLASH_ACCESS_KEY:
        try:
            api_url = "https://api.unsplash.com/search/photos"
            params = {
                "query": topic,
                "orientation": "landscape",
                "per_page": 10,
                "order_by": "relevant",
                "content_filter": "high",
            }
            headers = {
                "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}",
                "Accept-Version": "v1",
                "User-Agent": "Daily-Article-Generator"
            }
            r = requests.get(api_url, params=params, headers=headers, timeout=12)
            if r.status_code == 200:
                data = r.json()
                results = data.get("results") or []
                used_ids = _load_used_image_ids()
                chosen = None
                for photo in results:
                    pid = photo.get("id")
                    if pid and pid not in used_ids:
                        chosen = photo
                        used_ids.add(pid)
                        _save_used_image_ids(used_ids)
                        break
                if not chosen and results:
                    chosen = results[0]
                if chosen:
                    base = chosen["urls"].get("raw") or chosen["urls"].get("regular")
                    if base:
                        sep = '&' if '?' in base else '?'
                        img_url = f"{base}{sep}w=1200&h=630&fit=crop&auto=format"
                    else:
                        img_url = chosen["urls"].get("regular")
                    alt = chosen.get("alt_description") or f"{topic} illustration"
                    user = chosen.get("user", {})
                    author = user.get("name") or user.get("username") or "Unsplash contributor"
                    author_url = user.get("links", {}).get("html") or "https://unsplash.com/"
                    credit_text = f"Photo by {author} on Unsplash"
                    credit_url = author_url
                    return img_url, alt, credit_text, credit_url
        except Exception:
            pass
    # Fallback: random featured image (no author credit available)
    img_url = f"https://source.unsplash.com/featured/1200x630/?{topic_query}"
    alt = f"{topic} in UX Design"
    credit_text = "Image via Unsplash"
    credit_url = "https://unsplash.com/"
    return img_url, alt, credit_text, credit_url


def _ext_from_content_type(ct: str) -> str:
    ct = (ct or '').lower()
    if 'image/webp' in ct:
        return 'webp'
    if 'image/png' in ct:
        return 'png'
    if 'image/jpeg' in ct or 'image/jpg' in ct:
        return 'jpg'
    if 'image/svg' in ct:
        return 'svg'
    return 'jpg'


def cache_image_locally(image_url: str, now: datetime, title_slug: str) -> Optional[str]:
    """Download and cache the image into assets/images/posts/YYYY/MM/slug.ext.
    Returns site-relative path (starting with /assets/...) or None on failure.
    """
    try:
        y = now.strftime('%Y')
        m = now.strftime('%m')
        out_dir = BLOG_ROOT / 'assets' / 'images' / 'posts' / y / m
        out_dir.mkdir(parents=True, exist_ok=True)
        # Download
        headers = {"User-Agent": "Daily-Article-Generator"}
        resp = requests.get(image_url, headers=headers, timeout=20, stream=True)
        if resp.status_code != 200:
            return None
        ext = _ext_from_content_type(resp.headers.get('Content-Type', ''))
        out_path = out_dir / f"{title_slug}.{ext}"
        with open(out_path, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=65536):
                if chunk:
                    f.write(chunk)
        # Return site-relative path
        rel = out_path.relative_to(BLOG_ROOT)
        return f"/{rel.as_posix()}"
    except Exception:
        return None

def _next_primary_category(now: datetime) -> str:
    """Cycle primary categories with special rule: AI every alternate day.
    Non-AI days rotate through NON_AI_CATEGORIES and persist state.
    """
    today_key = now.strftime('%Y-%m-%d')
    # Even ordinal -> AI day
    ai_today = (now.toordinal() % 2 == 0)
    state = _load_category_state()
    if ai_today:
        state.update({"last_date": today_key, "last_primary": "ai"})
        _save_category_state(state)
        return "ai"
    # Non-AI: keep same within the same day; otherwise advance
    last_date = state.get("last_date")
    last_primary = state.get("last_primary")
    if last_date == today_key and last_primary and last_primary != "ai":
        return last_primary
    idx = (int(state.get("index", -1)) + 1) % len(NON_AI_CATEGORIES)
    primary = NON_AI_CATEGORIES[idx]
    state.update({"index": idx, "last_date": today_key, "last_primary": primary})
    _save_category_state(state)
    return primary

def _tokenize(text: str):
    words = re.findall(r"[a-zA-Z]{4,}", (text or "").lower())
    return set(words)

def _load_existing_bodies(limit=12):
    bodies = []
    try:
        posts = sorted(POSTS_DIR.glob('*.md'), key=lambda p: p.stat().st_mtime, reverse=True)
        for p in posts[:limit]:
            txt = p.read_text(encoding='utf-8')
            if txt.startswith('---'):
                parts = txt.split('\n---\n', 1)
                if len(parts) == 2:
                    bodies.append(parts[1])
    except Exception:
        pass
    return bodies

def _too_similar(new_text: str, existing_texts: list[str], threshold=0.6):
    new_tokens = _tokenize(new_text)
    if not new_tokens:
        return False
    for body in existing_texts:
        tokens = _tokenize(body)
        if not tokens:
            continue
        inter = len(new_tokens & tokens)
        union = len(new_tokens | tokens)
        if union and (inter / union) >= threshold:
            return True
    return False

def _parse_front_matter(text: str):
    if not text.startswith('---\n'):
        return None, text
    parts = text.split('\n---\n', 1)
    if len(parts) != 2:
        return None, text
    return parts[0][4:], parts[1]

def _extract_meta(fm: str):
    meta = {"categories": [], "title": None, "date": None}
    m = re.search(r"^title:\s*(.+)$", fm, re.MULTILINE)
    if m:
        meta["title"] = m.group(1).strip().strip('"')
    m = re.search(r"^date:\s*(.+)$", fm, re.MULTILINE)
    if m:
        meta["date"] = m.group(1).strip()
    m = re.search(r"^categories:\s*\[(.*?)\]\s*$", fm, re.MULTILINE)
    if m:
        cats = [c.strip().strip('"\'') for c in m.group(1).split(',') if c.strip()]
        meta["categories"] = cats
    return meta

def _compute_url(categories, date_str, filename, site_url):
    segs = [s for s in categories if s]
    y = m = d = None
    try:
        dt = datetime.fromisoformat(date_str.split()[0])
        y, m, d = dt.strftime('%Y'), dt.strftime('%m'), dt.strftime('%d')
    except Exception:
        parts = filename.split('-', 3)
        if len(parts) >= 3:
            y, m, d = parts[0], parts[1], parts[2]
    slug = filename.replace('.md', '').split('-', 3)[-1]
    cat_path = '/'.join(segs)
    return f"{site_url}/{cat_path}/{y}/{m}/{d}/{slug}/"

def _related_links(categories, site_url, exclude_filename, limit=3):
    links = []
    if not categories:
        return links
    catset = set(categories)
    try:
        posts = sorted(POSTS_DIR.glob('*.md'), key=lambda p: p.stat().st_mtime, reverse=True)
        scored = []
        for p in posts:
            if p.name == exclude_filename:
                continue
            txt = p.read_text(encoding='utf-8')
            fm, body = _parse_front_matter(txt)
            if not fm:
                continue
            meta = _extract_meta(fm)
            overlap = len(catset & set(meta.get('categories') or []))
            if overlap == 0:
                continue
            url = _compute_url(meta.get('categories') or [], meta.get('date') or '', p.name, site_url)
            title = meta.get('title') or p.name
            scored.append((overlap, url, title))
        scored.sort(key=lambda x: (-x[0], x[2]))
        for s in scored[:limit]:
            links.append(f"- [{s[2]}]({s[1]})")
    except Exception:
        pass
    return links

def generate_article_content(topic, template, site_url: str, enforce_uniqueness: bool = True):
    """Generate article content with strong SEO and interlinking.

    When enforce_uniqueness is False, similarity checks are skipped so the
    caller can fall back to generating content even after repeated collisions.
    """
    # Titles and intro
    title = template["title_template"].format(topic=topic)
    intro = template["intro_template"].format(topic=topic)

    # SEO image + credit
    image_url, image_alt, credit_text, credit_url = fetch_unsplash_image(topic)

    # SEO description
    description = (intro[:155] + "...") if len(intro) > 158 else intro

    # Establish timestamp once so categories, front matter, and canonical stay aligned
    now = datetime.now(timezone.utc)

    # Categories and tags (SEO-friendly, hyphenated) with rotation rules
    primary_category = _next_primary_category(now)
    # Choose a topic relevant to the chosen category when possible
    topic_pool = CATEGORY_TOPIC_POOL.get(primary_category) or UX_TOPICS
    if topic not in topic_pool:
        topic = random.choice(topic_pool)
    secondary_category = slugify(topic)
    categories = sanitize_categories([primary_category, secondary_category])
    tags = [secondary_category, "ux", "design", "user-experience"]

    # Body with interlinking anchors
    more_on_topic_link = f"{site_url}/insights/#" + primary_category
    writing_link = f"{site_url}/writing/"
    contact_link = f"{site_url}/contact/"

    # Try to cache image locally for performance/stability
    title_slug = slugify(title)
    local_image = cache_image_locally(image_url, now, title_slug)
    image_path_for_frontmatter = local_image or image_url

    content = f"""---
layout: post
title: "{title}"
date: {now.strftime('%Y-%m-%d %H:%M:%S %z')}
categories: ["{categories[0]}", "{categories[1]}"]
tags: [{', '.join(f'"{t}"' for t in tags)}]
read_time: 8
excerpt: "{description}"
image: "{image_path_for_frontmatter}"
image_alt: "{image_alt}"
image_credit_text: "{credit_text}"
image_credit_url: "{credit_url}"
canonical_url: "{site_url}/{"/".join(categories)}/{now.strftime('%Y/%m/%d')}/{slugify(title)}/"
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

## Further Reading

- Explore more on this topic: [{topic} insights]({more_on_topic_link})
- See all writing: [Writing hub]({writing_link})
- Work with me: [Contact]({contact_link})

## Related Articles

{chr(10).join(_related_links(categories, site_url, exclude_filename='', limit=4))}

## Conclusion

{topic} is an essential component of modern UX design. By following the principles and best practices outlined in this article, you can create more effective and user-centered experiences. Remember to stay updated with the latest trends and continuously refine your approach based on user feedback and data.

---

*This article was automatically generated as part of our daily UX insights series. For tailored help, [contact us]({contact_link}).*
"""

    # Simple uniqueness guard: if content too similar to recent posts, re-roll
    if enforce_uniqueness and _too_similar(content, _load_existing_bodies(), threshold=0.6):
        raise ValueError("Generated content too similar to recent posts; retry with different topic/template")
    return content, title, categories

def generate_article_sections(topic, article_type):
    """Generate article sections based on topic and type"""
    # This is a simplified version - you can expand this with more sophisticated content generation
    return []

def create_blog_post(content, title):
    """Create a new blog post file"""
    # Generate filename from title
    safe_title = slugify(title)
    
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
        # Track used Unsplash image IDs for uniqueness across posts
        used_store_rel = Path('assets/data/used_unsplash.json')
        if (BLOG_ROOT / used_store_rel).exists():
            subprocess.run(['git', 'add', str(used_store_rel)], cwd=BLOG_ROOT, check=True)
        # Track category rotation state (so reruns don't advance)
        cat_store_rel = Path('assets/data/category_cycle.json')
        if (BLOG_ROOT / cat_store_rel).exists():
            subprocess.run(['git', 'add', str(cat_store_rel)], cwd=BLOG_ROOT, check=True)
        
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
    
    # Select random topic and template with simple de-duplication by title slug
    existing_slugs = set()
    for p in POSTS_DIR.glob('*.md'):
        try:
            base = p.name.split('-', 3)[-1].rsplit('.', 1)[0]
            existing_slugs.add(base)
        except Exception:
            pass

    attempts = 0
    topic = None
    template = None
    title_slug = None
    while attempts < 10:
        t = random.choice(UX_TOPICS)
        temp = random.choice(ARTICLE_TEMPLATES)
        candidate_title = temp["title_template"].format(topic=t)
        candidate_slug = slugify(candidate_title)
        if candidate_slug not in existing_slugs:
            topic = t
            template = temp
            title_slug = candidate_slug
            break
        attempts += 1
    if topic is None:
        # fall back to any combination
        topic = random.choice(UX_TOPICS)
        template = random.choice(ARTICLE_TEMPLATES)
    
    print(f"📝 Generating article about: {topic}")
    print(f"📋 Using template: {template['type']}")
    
    # Site URL from config/env
    site_url = os.getenv("SITE_URL", "https://haiderali.co")

    content = None
    title = None
    categories = None

    # Generate article content, retry up to 5 times for uniqueness
    for _ in range(5):
        try:
            content, title, categories = generate_article_content(topic, template, site_url, enforce_uniqueness=True)
            break
        except ValueError:
            topic = random.choice(UX_TOPICS)
            template = random.choice(ARTICLE_TEMPLATES)
    # Fallback: skip uniqueness guard so the run still produces an article
    if content is None or title is None or categories is None:
        print("⚠️  Could not generate a unique article after retries; creating fallback content.")
        last_error = None
        for _ in range(5):
            topic = random.choice(UX_TOPICS)
            template = random.choice(ARTICLE_TEMPLATES)
            try:
                content, title, categories = generate_article_content(topic, template, site_url, enforce_uniqueness=False)
                break
            except Exception as err:
                last_error = err
                continue
        else:
            raise RuntimeError("Failed to generate article content even after fallback attempts") from last_error

    # Create blog post file
    filepath, filename = create_blog_post(content, title)
    print(f"✅ Created blog post: {filename}")
    
    # Generate canonical URL consistent with permalink: /:categories/:year/:month/:day/:title/
    now = datetime.now(timezone.utc)
    y = now.strftime('%Y')
    m = now.strftime('%m')
    d = now.strftime('%d')
    slug = filename.replace('.md', '').split('-', 3)[-1]
    # Join categories as path segments
    cat_path = '/'.join(categories)
    article_url = f"{site_url}/{cat_path}/{y}/{m}/{d}/{slug}/"
    
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
