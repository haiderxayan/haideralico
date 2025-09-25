# 🚀 Daily Article Automation - Quick Setup Guide

Your automated daily blog article system is ready! Here's how to get it running:

## ✅ What's Already Done

- ✅ Article generator script created
- ✅ GitHub Actions workflow configured
- ✅ Email notification system built
- ✅ Test system verified working
- ✅ 20 UX topics and 4 article templates ready

## 🔧 Quick Setup (5 minutes)

### 1. Set Up Email Notifications

To receive daily email notifications with article URLs:

1. **Get Gmail App Password:**
   - Go to [Google Account Settings](https://myaccount.google.com/)
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"

2. **Add to GitHub Secrets:**
   - Go to your GitHub repository
   - Settings → Secrets and variables → Actions
   - Add new secret: `EMAIL_PASSWORD` = your app password

### 2. Enable GitHub Actions

The workflow is already configured to run daily at 9:00 AM UTC. It will:
- Generate a new UX article
- Add it to your blog
- Commit and push changes
- Send you an email with the URL

### 3. Test It Now

You can test the system immediately:

1. **Go to GitHub Actions tab** in your repository
2. **Find "Daily Article Generator"** workflow
3. **Click "Run workflow"** to test manually

## 📧 What You'll Receive

Every day at 9:00 AM UTC, you'll get an email like this:

```
Subject: New Blog Post Published: The Complete Guide to User Research in 2024

Hello Haider!

Your daily blog post has been successfully generated and published!

📝 Article Details:
- Title: The Complete Guide to User Research in 2024
- URL: https://haiderali.co/2024/01/15/the-complete-guide-to-user-research-in-2024/
- Published: 2024-01-15 09:00:00

The article has been automatically added to your Jekyll site and should appear in the latest section of your blog.
```

## 🎯 Article Topics

The system will randomly select from 20 UX topics:
- User Research, Design Systems, Mobile UX
- Accessibility, User Psychology, Information Architecture
- Interaction Design, Usability Testing, Design Thinking
- And 11 more topics!

## 📝 Article Types

4 different article formats:
- **Guides**: "The Complete Guide to {topic} in 2024"
- **Tips**: "10 Essential {topic} Tips Every Designer Should Know"
- **Trends**: "The Future of {topic}: Trends Shaping UX in 2024"
- **Case Studies**: "How {topic} Transformed Our User Experience"

## 🔍 Monitoring

- **Check GitHub Actions**: Repository → Actions tab
- **View Articles**: They appear in your blog's latest section
- **Email Logs**: Check GitHub Actions logs for email status

## 🛠️ Customization

Want to modify topics or templates? Edit:
- `scripts/config.json` - Topics and templates
- `scripts/daily_article_generator.py` - Article content structure

## 🚨 Troubleshooting

**No emails?**
- Check GitHub Secrets has `EMAIL_PASSWORD`
- Verify Gmail app password is correct

**Articles not appearing?**
- Check GitHub Actions logs
- Verify Jekyll build is successful

**Want to change schedule?**
- Edit `.github/workflows/daily-article.yml`
- Change the cron schedule (currently `0 9 * * *` = 9 AM UTC daily)

## 🎉 You're All Set!

Once you add the `EMAIL_PASSWORD` secret to GitHub, the system will:
1. Run automatically every day at 9:00 AM UTC
2. Generate a unique UX article
3. Publish it to your blog
4. Email you the URL

**No manual intervention required!** 🚀

---

**Need help?** Check the detailed documentation in `scripts/README.md`
