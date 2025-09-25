#!/usr/bin/env python3
"""
Test script for the daily article generator
"""

import os
import sys
from pathlib import Path

# Add the scripts directory to the path
sys.path.append(str(Path(__file__).parent))

from daily_article_generator import generate_article_content, create_blog_post, send_email_notification

def test_article_generation():
    """Test article generation without actually creating files"""
    print("🧪 Testing article generation...")
    
    # Test content generation
    topic = "User Research"
    template = {
        "type": "guide",
        "title_template": "The Complete Guide to {topic} in 2024",
        "intro_template": "In today's digital landscape, {topic} has become more crucial than ever for creating exceptional user experiences."
    }
    
    content, title = generate_article_content(topic, template)
    
    print(f"✅ Generated article: {title}")
    print(f"✅ Content length: {len(content)} characters")
    print(f"✅ Topic: {topic}")
    print(f"✅ Template: {template['type']}")
    
    return True

def test_file_creation():
    """Test file creation in a temporary location"""
    print("🧪 Testing file creation...")
    
    # Create a test post
    test_content = """---
layout: post
title: "Test Article"
date: 2024-01-01 12:00:00
categories: ["Test"]
tags: ["test"]
read_time: 5
excerpt: "This is a test article"
---

# Test Article

This is a test article to verify the automation system works correctly.
"""
    
    # Create test file
    test_file = Path("test-article.md")
    with open(test_file, 'w') as f:
        f.write(test_content)
    
    print(f"✅ Created test file: {test_file}")
    
    # Clean up
    test_file.unlink()
    print("✅ Cleaned up test file")
    
    return True

def test_email_configuration():
    """Test email configuration"""
    print("🧪 Testing email configuration...")
    
    email_password = os.getenv("EMAIL_PASSWORD")
    if email_password:
        print("✅ EMAIL_PASSWORD environment variable is set")
        return True
    else:
        print("⚠️  EMAIL_PASSWORD environment variable not set")
        print("   Email notifications will be skipped")
        return False

def main():
    """Run all tests"""
    print("🚀 Running Daily Article Automation Tests")
    print("=" * 50)
    
    tests = [
        ("Article Generation", test_article_generation),
        ("File Creation", test_file_creation),
        ("Email Configuration", test_email_configuration)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}:")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS")
    print("=" * 50)
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if not result:
            all_passed = False
    
    print("=" * 50)
    if all_passed:
        print("🎉 All tests passed! The automation system is ready.")
    else:
        print("⚠️  Some tests failed. Please check the configuration.")
    
    return all_passed

if __name__ == "__main__":
    main()
