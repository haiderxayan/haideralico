#!/bin/bash

# Load local environment overrides if present
if [ -f ".env" ]; then
    set -a
    export $(grep -v '^#' .env | xargs)
    set +a
fi

echo "🚀 Setting up Daily Article Automation for Haider Ali's Blog"

# Guard against running on main
current_branch=$(git -C .. rev-parse --abbrev-ref HEAD 2>/dev/null)
if [ "$current_branch" = "main" ]; then
    echo "⚠️  You're on the main branch. Switch to pre-production before running automation."
    exit 1
fi
echo "=========================================================="

# Check if we're in the right directory
if [ ! -f "daily_article_generator.py" ]; then
    echo "❌ Error: Please run this script from the scripts directory"
    exit 1
fi

# Create scripts directory if it doesn't exist
mkdir -p scripts

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Make the script executable
chmod +x daily_article_generator.py

# Check if git is configured
echo "🔧 Checking Git configuration..."
if ! git config user.name > /dev/null 2>&1; then
    echo "⚠️  Git user.name not configured. Please run:"
    echo "   git config --global user.name 'Your Name'"
    echo "   git config --global user.email 'your.email@example.com'"
fi

# Check for email password environment variable
echo "📧 Email Configuration:"
if [ -z "$EMAIL_PASSWORD" ]; then
    echo "⚠️  EMAIL_PASSWORD environment variable not set."
    echo "   To enable email notifications, set your Gmail app password:"
    echo "   export EMAIL_PASSWORD='your-gmail-app-password'"
    echo ""
    echo "   To get a Gmail app password:"
    echo "   1. Go to Google Account settings"
    echo "   2. Security → 2-Step Verification → App passwords"
    echo "   3. Generate a new app password for 'Mail'"
    echo "   4. Use that password as EMAIL_PASSWORD"
else
    echo "✅ EMAIL_PASSWORD is configured"
fi

# Check for Unsplash access key
echo "🖼️ Unsplash Integration:"
if [ -z "$UNSPLASH_ACCESS_KEY" ]; then
    echo "⚠️  UNSPLASH_ACCESS_KEY not set."
    echo "   Daily posts will fall back to a generic image until you export it:"
    echo "   export UNSPLASH_ACCESS_KEY='your-unsplash-access-key'"
else
    echo "✅ UNSPLASH_ACCESS_KEY detected"
fi

# Test the script
echo "🧪 Testing the article generator..."
python daily_article_generator.py --test

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Set up your Gmail app password (see instructions above)"
echo "2. Test the script manually: python daily_article_generator.py"
echo "3. The GitHub Actions workflow will run daily at 9:00 AM UTC"
echo "4. You can also run it manually from the GitHub Actions tab"
echo ""
echo "🔧 Manual execution:"
echo "   cd scripts && python daily_article_generator.py"
echo ""
echo "📧 Email notifications will be sent to: haiderxayan@gmail.com"
echo "🌐 Articles will be published to: https://haiderali.co"
