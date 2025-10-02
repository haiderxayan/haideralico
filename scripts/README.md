# Daily Article Automation System

This system automatically generates and publishes a new UX blog article every day, then sends you an email notification with the article URL.

## 🚀 Features

- **Automated Content Generation**: Creates unique articles about UX topics daily
- **Jekyll Integration**: Automatically adds new posts to your Jekyll blog
- **Email Notifications**: Sends you the article URL via email
- **GitHub Actions**: Runs automatically every day at 9:00 AM UTC
- **Manual Trigger**: Can be run manually from GitHub Actions tab

## 📋 Setup Instructions

### 1. Install Dependencies

```bash
cd scripts
pip install -r requirements.txt
```

### 2. Configure Email Notifications

To receive email notifications, you need to set up a Gmail app password:

1. Go to [Google Account Settings](https://myaccount.google.com/)
2. Navigate to **Security** → **2-Step Verification** → **App passwords**
3. Generate a new app password for "Mail"
4. Set the environment variable:

```bash
export EMAIL_PASSWORD="your-gmail-app-password"
```

### 3. Test the System

```bash
python test_automation.py
```

### 4. Manual Test Run

```bash
python daily_article_generator.py
```

## 🔧 Configuration

### Email Settings

Edit `config.json` to customize email settings:

```json
{
  "email": {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "sender_email": "haiderxayan@gmail.com",
    "recipient_email": "haiderxayan@gmail.com"
  }
}
```

### Blog Settings

```json
{
  "blog": {
    "site_url": "https://haiderali.co",
    "posts_directory": "_posts",
    "default_read_time": 8,
    "default_image": "https://images.unsplash.com/photo-1551650975-87deedd944c3?w=1200&h=630&fit=crop"
  }
}
```

### Unsplash Access Key

To fetch topic-specific hero images, set your Unsplash access key before running the generator. You can either export it manually or create a `.env` file based on `.env.example`:

```bash
# Option 1: export for this shell
export UNSPLASH_ACCESS_KEY="your-unsplash-access-key"

# Option 2: copy the example and edit
cp .env.example .env
# update UNSPLASH_ACCESS_KEY (and EMAIL_PASSWORD if desired) in .env
```

In GitHub Actions, add the same value as the `UNSPLASH_ACCESS_KEY` repository secret so scheduled runs can fetch credited images instead of the generic fallback.

### Topics and Templates

The system includes 20 UX topics and 4 article templates:

**Topics**: User Research, Design Systems, Mobile UX, Accessibility, etc.

**Templates**:
- **Guide**: "The Complete Guide to {topic} in 2024"
- **Tips**: "10 Essential {topic} Tips Every Designer Should Know"
- **Trends**: "The Future of {topic}: Trends Shaping UX in 2024"
- **Case Study**: "How {topic} Transformed Our User Experience"

## 🤖 Automation

### GitHub Actions

The system runs automatically via GitHub Actions:

- **Schedule**: Every day at 9:00 AM UTC
- **Workflow**: `.github/workflows/daily-article.yml`
- **Manual Trigger**: Available in GitHub Actions tab

### Local Cron Job (Alternative)

If you prefer to run it locally instead of GitHub Actions:

```bash
# Edit crontab
crontab -e

# Add this line to run daily at 9 AM
0 9 * * * cd /path/to/your/blog/scripts && python daily_article_generator.py
```

## 📧 Email Notifications

You'll receive an email every day with:

- Article title
- Article URL
- Publication date
- Filename

Example email:
```
Subject: New Blog Post Published: The Complete Guide to User Research in 2024

Hello Haider!

Your daily blog post has been successfully generated and published!

📝 Article Details:
- Title: The Complete Guide to User Research in 2024
- Filename: 2024-01-15-the-complete-guide-to-user-research-in-2024.md
- URL: https://haiderali.co/2024/01/15/the-complete-guide-to-user-research-in-2024/
- Published: 2024-01-15 09:00:00

The article has been automatically added to your Jekyll site and should appear in the latest section of your blog.
```

## 🔍 Monitoring

### Check GitHub Actions

1. Go to your repository on GitHub
2. Click on "Actions" tab
3. Look for "Daily Article Generator" workflow
4. Check the latest run status

### Check Generated Articles

Articles are created in the `_posts/` directory with the format:
```
YYYY-MM-DD-article-title.md
```

### Check Email Logs

The script logs email sending status. Check the GitHub Actions logs for email delivery status.

## 🛠️ Troubleshooting

### Common Issues

1. **Email not sending**
   - Check EMAIL_PASSWORD environment variable
   - Verify Gmail app password is correct
   - Check GitHub Actions secrets

2. **Git push failing**
   - Ensure GitHub token has write permissions
   - Check if there are merge conflicts

3. **Article not appearing on site**
   - Check if Jekyll build is successful
   - Verify GitHub Pages deployment
   - Check article front matter format

### Debug Mode

Run with debug output:
```bash
python daily_article_generator.py --debug
```

## 📈 Customization

### Adding New Topics

Edit `config.json` and add topics to the `topics` array:

```json
{
  "topics": [
    "User Research",
    "Design Systems",
    "Your New Topic"
  ]
}
```

### Creating New Templates

Add new templates to `config.json`:

```json
{
  "templates": [
    {
      "type": "tutorial",
      "title_template": "Step-by-Step {topic} Tutorial",
      "intro_template": "Learn {topic} with this comprehensive tutorial..."
    }
  ]
}
```

### Modifying Article Content

Edit the `generate_article_content()` function in `daily_article_generator.py` to customize the article structure and content.

## 🔒 Security

- Email passwords are stored as GitHub Secrets
- No sensitive data is committed to the repository
- All external links use HTTPS
- Git operations use secure tokens

## 📞 Support

If you encounter any issues:

1. Check the GitHub Actions logs
2. Run the test script: `python test_automation.py`
3. Verify your configuration in `config.json`
4. Check your email settings and app password

---

**Happy blogging! 🎉**
