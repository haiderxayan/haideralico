source "https://rubygems.org"

# Use the official GitHub Pages environment (Jekyll + plugins)
gem "github-pages", group: :jekyll_plugins

# If you want to override the default theme, keep minima (optional)
gem "minima", "~> 2.5", group: :jekyll_plugins

# Project-specific plugins (also included by github-pages, harmless to keep)
group :jekyll_plugins do
  gem "jekyll-feed"
  gem "jekyll-sitemap"
  gem "jekyll-seo-tag"
end

# Windows and JRuby does not include zoneinfo files
platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end

# Performance-booster for watching directories on Windows
gem "wdm", "~> 0.1.1", :platforms => [:mingw, :x64_mingw, :mswin]

# Lock `http_parser.rb` gem to `v0.6.x` on JRuby builds
gem "http_parser.rb", "~> 0.6.0", :platforms => [:jruby]

# Webrick is no longer bundled with Ruby as of Ruby 3.0
gem "webrick", "~> 1.7"
