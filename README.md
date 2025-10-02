# Haider Ali - UX Designer Portfolio

A modern Jekyll-based portfolio website showcasing UX design work, writing, and professional experience.

## Branch Workflow

All changes now flow through the `pre-production` branch. Run local work and automation there, then open a pull request into `main` once the updates are reviewed. The daily article workflow also writes to `pre-production`, so nothing publishes to `main` until you merge it yourself.

## Getting Started

### Prerequisites

- Ruby (version 2.7 or higher)
- Bundler gem

### Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   bundle install
   ```

3. Serve the site locally:
   ```bash
   bundle exec jekyll serve
   ```

4. Open your browser and navigate to `http://localhost:4000`

## Project Structure

```
.
├── _config.yml          # Jekyll configuration
├── _layouts/            # Page layouts
│   ├── default.html     # Default layout
│   ├── page.html        # Page layout
│   └── post.html        # Blog post layout
├── _includes/           # Reusable components
│   ├── social.html      # Social media links
│   └── google-analytics.html
├── _posts/              # Blog posts
├── _sass/               # Sass partials
├── assets/              # Static assets
│   ├── css/             # Stylesheets
│   ├── js/              # JavaScript files
│   └── images/          # Images
├── index.html           # Homepage
├── work.md              # Work portfolio
├── writing.md           # Blog/writing page
├── reading.md           # Reading list
├── contact.md           # Contact page
└── Gemfile              # Ruby dependencies
```

## Features

- **Responsive Design**: Mobile-first approach with clean, modern aesthetics
- **3-Column Blog Layout**: UX Collective-inspired blog post grid
- **Portfolio Showcase**: Featured work with case studies
- **Reading List**: Curated books and resources
- **Contact Integration**: Multiple ways to get in touch
- **Sharp Edge Design**: Minimal, professional styling with backdrop blur effects

## Customization

### Site Configuration

Edit `_config.yml` to customize:
- Site title and description
- Navigation menu
- Social media links
- Contact information
- Build settings

### Styling

The main stylesheet is located at `assets/css/main.scss`. Features include:
- Modern design system with CSS variables
- Responsive grid layouts
- Hover effects and animations
- Sharp edge design aesthetic

### Adding Content

- **Pages**: Create `.md` or `.html` files in the root directory
- **Blog Posts**: Create files in `_posts/` with the format `YYYY-MM-DD-title.md`
- **Images**: Place images in `assets/images/`

## Deployment

### GitHub Pages

1. Push your code to a GitHub repository
2. Enable GitHub Pages in repository settings
3. Select the source branch (usually `main` or `gh-pages`)

### Other Hosting

Build the site for production:
```bash
bundle exec jekyll build
```

The generated site will be in the `_site` directory, ready for deployment to any static hosting service.

## License

This project is open source and available under the [MIT License](LICENSE).
