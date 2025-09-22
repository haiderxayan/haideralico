# Jekyll Website

A modern Jekyll-based website with a clean, responsive design.

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
├── about.md             # About page
└── Gemfile              # Ruby dependencies
```

## Customization

### Site Configuration

Edit `_config.yml` to customize:
- Site title and description
- Navigation menu
- Social media links
- Google Analytics
- Build settings

### Styling

The main stylesheet is located at `assets/css/main.scss`. It imports the Minima theme and adds custom styles.

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
