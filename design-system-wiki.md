---
layout: design-system
title: "Design System Wiki - UX Design Standards & Guidelines"
description: "Comprehensive design system documentation for Haider Ali's portfolio website. Complete guidelines for typography, colors, components, and layout patterns for consistent UX design."
keywords: "design system, UX design guidelines, design standards, portfolio design, typography, color palette, component library, design patterns, user experience design"
author: "Haider Ali"
date: 2024-01-30
last_modified_at: 2024-01-30
permalink: /design-system-wiki/
image: https://images.unsplash.com/photo-1558655146-9f40138edfeb?w=1200&h=630&fit=crop&crop=center
image_alt: "Design system documentation and guidelines for UX design"
canonical_url: "https://haiderali.co/design-system-wiki/"
---

<!-- Breadcrumb Navigation -->
<nav class="wiki-breadcrumb" aria-label="Breadcrumb">
    <ol class="breadcrumb-list">
        <li class="breadcrumb-item">
            <a href="{{ '/' | relative_url }}">Home</a>
        </li>
        <li class="breadcrumb-item">
            <a href="{{ '/work/' | relative_url }}">Work</a>
        </li>
        <li class="breadcrumb-item breadcrumb-current" aria-current="page">
            Design System Wiki
        </li>
    </ol>
</nav>

<!-- Wiki Header -->
<div class="wiki-header">
    <h1 class="wiki-title">Design System Wiki</h1>
    <p class="wiki-subtitle">UX Design Standards & Guidelines</p>
    <div class="wiki-meta">
        <span class="last-updated">Last updated: {{ page.last_modified_at | date: "%B %d, %Y" }}</span>
        <span class="read-time">15 min read</span>
    </div>
</div>

<!-- Introduction -->
<div class="wiki-intro">
    <p>This design system wiki serves as the definitive reference for maintaining visual and structural consistency across the Haider Ali portfolio website. All future changes must adhere to these established patterns and standards.</p>
</div>

<!-- Visual Identity Section -->
<section id="visual-identity" class="wiki-section">
    <div class="section-header">
        <span class="section-icon">🎨</span>
        <h2 class="section-title">Visual Identity</h2>
    </div>
    
    <div class="section-content">
        <div class="subsection" id="color-palette">
            <h3 class="subsection-title">Color Palette</h3>
            
            <div class="color-palette">
                <div class="color-item">
                    <div class="color-swatch" style="background: #000000;"></div>
                    <div class="color-name">Primary Black</div>
                    <div class="color-value">#000000</div>
                </div>
                <div class="color-item">
                    <div class="color-swatch" style="background: #333333;"></div>
                    <div class="color-name">Primary Light</div>
                    <div class="color-value">#333333</div>
                </div>
                <div class="color-item">
                    <div class="color-swatch" style="background: #666666;"></div>
                    <div class="color-name">Secondary Gray</div>
                    <div class="color-value">#666666</div>
                </div>
                <div class="color-item">
                    <div class="color-swatch" style="background: #ffffff; border: 1px solid #e0e0e0;"></div>
                    <div class="color-name">Background White</div>
                    <div class="color-value">#ffffff</div>
                </div>
                <div class="color-item">
                    <div class="color-swatch" style="background: #f8f8f8;"></div>
                    <div class="color-name">Background Light</div>
                    <div class="color-value">#f8f8f8</div>
                </div>
                <div class="color-item">
                    <div class="color-swatch" style="background: #e0e0e0;"></div>
                    <div class="color-name">Border Color</div>
                    <div class="color-value">#e0e0e0</div>
                </div>
            </div>
            
            <div class="code-example">
                <div class="code-header">
                    <h4 class="code-title">SCSS Variables</h4>
                    <button class="code-copy">Copy</button>
                </div>
                <pre><code>// Primary Colors
$primary-color: #000000;        // Main brand color - pure black
$primary-light: #333333;        // Hover states, secondary elements
$secondary-color: #666666;      // Supporting text, borders

// Text Colors
$text-color: #000000;           // Primary text - pure black
$text-light: #666666;           // Secondary text, meta information

// Background Colors
$background-color: #ffffff;     // Main background - pure white
$background-light: #f8f8f8;     // Section backgrounds, cards
$background-dark: #000000;      // Dark sections (if needed)

// Border Colors
$border-color: #e0e0e0;         // Subtle borders, dividers</code></pre>
            </div>
        </div>

        <div class="subsection" id="typography">
            <h3 class="subsection-title">Typography</h3>
            
            <div class="component-example">
                <div class="example-header">
                    <h4 class="example-title">Font Family</h4>
                    <button class="example-toggle">Show Code</button>
                </div>
                <div class="example-preview">
                    <p style="font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 1.5rem; margin: 0;">
                        Inter Font Family - Clean and Modern
                    </p>
                </div>
                <div class="example-code">
                    <div class="code-example">
                        <div class="code-header">
                            <h4 class="code-title">SCSS</h4>
                            <button class="code-copy">Copy</button>
                        </div>
                        <pre><code>$base-font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;</code></pre>
                    </div>
                </div>
            </div>

            <div class="code-example">
                <div class="code-header">
                    <h4 class="code-title">Font Sizes & Weights</h4>
                    <button class="code-copy">Copy</button>
                </div>
                <pre><code>// Font Sizes
$base-font-size: 16px;          // Base body text
$small-font-size: 14px;         // Small text, meta information
$base-line-height: 1.6;         // Optimal reading line height

// Font Weights
- 300: Light (rarely used)
- 400: Regular (body text)
- 500: Medium (buttons, emphasis)
- 600: Semi-bold (headings, important text)
- 700: Bold (main headings, hero text)</code></pre>
            </div>
        </div>

        <div class="subsection" id="spacing">
            <h3 class="subsection-title">Spacing System</h3>
            
            <div class="code-example">
                <div class="code-header">
                    <h4 class="code-title">Spacing Variables</h4>
                    <button class="code-copy">Copy</button>
                </div>
                <pre><code>$spacing-unit: 30px;            // Base spacing unit

// Common Spacing Values
- 0.5rem (8px): Tight spacing
- 1rem (16px): Standard spacing
- 1.5rem (24px): Section spacing
- 2rem (32px): Large spacing
- 3rem (48px): Section padding
- 4rem (64px): Hero padding
- 5rem (80px): Major section padding</code></pre>
            </div>
        </div>
    </div>
</section>

<!-- Components Section -->
<section id="components" class="wiki-section">
    <div class="section-header">
        <span class="section-icon">🧩</span>
        <h2 class="section-title">Components</h2>
    </div>
    
    <div class="section-content">
        <div class="subsection" id="buttons">
            <h3 class="subsection-title">Buttons</h3>
            
            <div class="component-example">
                <div class="example-header">
                    <h4 class="example-title">Button Variants</h4>
                    <button class="example-toggle">Show Code</button>
                </div>
                <div class="example-preview">
                    <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                        <button style="background: #000000; color: white; padding: 12px 24px; border: none; font-weight: 500; cursor: pointer;">Primary Button</button>
                        <button style="background: transparent; color: #000000; padding: 12px 24px; border: 1px solid #000000; font-weight: 500; cursor: pointer;">Secondary Button</button>
                        <button style="background: transparent; color: #000000; padding: 12px 24px; border: 1px solid #e0e0e0; font-weight: 500; cursor: pointer;">Outline Button</button>
                    </div>
                </div>
                <div class="example-code">
                    <div class="code-example">
                        <div class="code-header">
                            <h4 class="code-title">HTML</h4>
                            <button class="code-copy">Copy</button>
                        </div>
                        <pre><code><a href="#" class="btn btn-primary">Primary Button</a>
<a href="#" class="btn btn-secondary">Secondary Button</a>
<a href="#" class="btn btn-outline">Outline Button</a></code></pre>
                    </div>
                </div>
            </div>

            <div class="code-example">
                <div class="code-header">
                    <h4 class="code-title">Button SCSS</h4>
                    <button class="code-copy">Copy</button>
                </div>
                <pre><code>.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 12px 24px;
  border-radius: 0;             // Sharp edges - NO rounded corners
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s ease;
  border: 1px solid transparent;
  cursor: pointer;
  
  &.btn-primary {
    background: $primary-color;
    color: white;
    
    &:hover {
      background: $primary-light;
    }
  }
  
  &.btn-secondary {
    background: transparent;
    color: $primary-color;
    border-color: $primary-color;
    
    &:hover {
      background: $primary-color;
      color: white;
    }
  }
  
  &.btn-outline {
    background: transparent;
    color: $text-color;
    border-color: $border-color;
    
    &:hover {
      background: $background-light;
      border-color: $primary-color;
      color: $primary-color;
    }
  }
}</code></pre>
            </div>
        </div>

        <div class="subsection" id="cards">
            <h3 class="subsection-title">Cards</h3>
            
            <div class="component-example">
                <div class="example-header">
                    <h4 class="example-title">Card Component</h4>
                    <button class="example-toggle">Show Code</button>
                </div>
                <div class="example-preview">
                    <div style="background: white; border: 1px solid #e0e0e0; padding: 2rem; max-width: 300px; position: relative;">
                        <div style="position: absolute; top: 0; left: 0; right: 0; height: 3px; background: #000000;"></div>
                        <h4 style="margin: 0 0 1rem 0; color: #000000;">Card Title</h4>
                        <p style="margin: 0; color: #666666;">This is a card component with sharp edges and subtle hover effects.</p>
                    </div>
                </div>
                <div class="example-code">
                    <div class="code-example">
                        <div class="code-header">
                            <h4 class="code-title">HTML</h4>
                            <button class="code-copy">Copy</button>
                        </div>
                        <pre><code><div class="card">
  <h4>Card Title</h4>
  <p>Card content goes here.</p>
</div></code></pre>
                    </div>
                </div>
            </div>
        </div>

        <div class="subsection" id="tags">
            <h3 class="subsection-title">Tags</h3>
            
            <div class="component-example">
                <div class="example-header">
                    <h4 class="example-title">Tag Component</h4>
                    <button class="example-toggle">Show Code</button>
                </div>
                <div class="example-preview">
                    <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
                        <span style="background: #f0f0f0; color: #666666; padding: 0.25rem 0.5rem; font-size: 0.7rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.3px;">DESIGN</span>
                        <span style="background: #f0f0f0; color: #666666; padding: 0.25rem 0.5rem; font-size: 0.7rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.3px;">UX</span>
                        <span style="background: #f0f0f0; color: #666666; padding: 0.25rem 0.5rem; font-size: 0.7rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.3px;">RESEARCH</span>
                    </div>
                </div>
                <div class="example-code">
                    <div class="code-example">
                        <div class="code-header">
                            <h4 class="code-title">HTML</h4>
                            <button class="code-copy">Copy</button>
                        </div>
                        <pre><code><span class="unified-tag">DESIGN</span>
<span class="unified-tag">UX</span>
<span class="unified-tag">RESEARCH</span></code></pre>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Patterns Section -->
<section id="patterns" class="wiki-section">
    <div class="section-header">
        <span class="section-icon">📐</span>
        <h2 class="section-title">Patterns</h2>
    </div>
    
    <div class="section-content">
        <div class="subsection" id="layouts">
            <h3 class="subsection-title">Layout Patterns</h3>
            
            <div class="code-example">
                <div class="code-header">
                    <h4 class="code-title">Container System</h4>
                    <button class="code-copy">Copy</button>
                </div>
                <pre><code>.container {
  max-width: 1200px;            // Maximum content width
  margin: 0 auto;               // Center alignment
  padding: 0 20px;              // Horizontal padding
  
  @include media-query($on-palm) {
    padding: 0 16px;            // Reduced padding on mobile
  }
}</code></pre>
            </div>
        </div>

        <div class="subsection" id="grids">
            <h3 class="subsection-title">Grid Systems</h3>
            
            <div class="code-example">
                <div class="code-header">
                    <h4 class="code-title">Responsive Grids</h4>
                    <button class="code-copy">Copy</button>
                </div>
                <pre><code>// Skills Grid (4 columns → 2 → 1)
.skills-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

// Portfolio Grid (3 columns → 2 → 1)
.portfolio-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

// Blog Posts Grid (3 columns → 2 → 1)
.blog-posts-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  
  @include media-query($on-laptop) {
    grid-template-columns: repeat(2, 1fr);
  }
  
  @include media-query($on-palm) {
    grid-template-columns: 1fr;
  }
}</code></pre>
            </div>
        </div>

        <div class="subsection" id="responsive">
            <h3 class="subsection-title">Responsive Design</h3>
            
            <div class="code-example">
                <div class="code-header">
                    <h4 class="code-title">Breakpoints</h4>
                    <button class="code-copy">Copy</button>
                </div>
                <pre><code>$on-palm: 768px;                // Mobile devices
$on-laptop: 1024px;             // Tablets and small laptops
$on-desktop: 1280px;            // Desktop screens</code></pre>
            </div>
        </div>
    </div>
</section>

<!-- Guidelines Section -->
<section id="guidelines" class="wiki-section">
    <div class="section-header">
        <span class="section-icon">📋</span>
        <h2 class="section-title">Guidelines</h2>
    </div>
    
    <div class="section-content">
        <div class="subsection" id="principles">
            <h3 class="subsection-title">Design Principles</h3>
            
            <div class="principles-grid">
                <div class="principle-card">
                    <div class="principle-icon">🎯</div>
                    <h4 class="principle-title">Minimalism & Clarity</h4>
                    <p class="principle-description">Sharp edges, clean typography, generous whitespace, and subtle shadows for a professional look.</p>
                </div>
                <div class="principle-card">
                    <div class="principle-icon">🔄</div>
                    <h4 class="principle-title">Consistency</h4>
                    <p class="principle-description">Unified tags, card patterns, button styles, and grid systems across all components.</p>
                </div>
                <div class="principle-card">
                    <div class="principle-icon">⚡</div>
                    <h4 class="principle-title">Performance</h4>
                    <p class="principle-description">Optimized images, lazy loading, minimal animations, and clean semantic HTML structure.</p>
                </div>
                <div class="principle-card">
                    <div class="principle-icon">♿</div>
                    <h4 class="principle-title">Accessibility</h4>
                    <p class="principle-description">High contrast, readable fonts, semantic markup, and descriptive alt text for all images.</p>
                </div>
            </div>
        </div>

        <div class="subsection" id="checklist">
            <h3 class="subsection-title">Implementation Checklist</h3>
            
            <div class="checklist">
                <h4 class="checklist-title">Visual Consistency</h4>
                <div class="checklist-items">
                    <div class="checklist-item">
                        <input type="checkbox" id="colors">
                        <label for="colors">Colors match the defined palette</label>
                    </div>
                    <div class="checklist-item">
                        <input type="checkbox" id="typography">
                        <label for="typography">Typography uses Inter font family</label>
                    </div>
                    <div class="checklist-item">
                        <input type="checkbox" id="spacing">
                        <label for="spacing">Spacing follows the spacing system</label>
                    </div>
                    <div class="checklist-item">
                        <input type="checkbox" id="corners">
                        <label for="corners">No rounded corners (border-radius: 0)</label>
                    </div>
                    <div class="checklist-item">
                        <input type="checkbox" id="shadows">
                        <label for="shadows">Consistent shadow usage</label>
                    </div>
                </div>
            </div>

            <div class="checklist">
                <h4 class="checklist-title">Layout Standards</h4>
                <div class="checklist-items">
                    <div class="checklist-item">
                        <input type="checkbox" id="responsive">
                        <label for="responsive">Responsive breakpoints implemented</label>
                    </div>
                    <div class="checklist-item">
                        <input type="checkbox" id="grids">
                        <label for="grids">Grid systems used appropriately</label>
                    </div>
                    <div class="checklist-item">
                        <input type="checkbox" id="container">
                        <label for="container">Container max-width respected</label>
                    </div>
                    <div class="checklist-item">
                        <input type="checkbox" id="mobile">
                        <label for="mobile">Mobile-first approach followed</label>
                    </div>
                </div>
            </div>
        </div>

        <div class="subsection" id="maintenance">
            <h3 class="subsection-title">Maintenance Guidelines</h3>
            
            <div class="code-example">
                <div class="code-header">
                    <h4 class="code-title">Regular Updates</h4>
                    <button class="code-copy">Copy</button>
                </div>
                <pre><code>// Maintenance Schedule
- Monthly: Review and update category mappings
- Quarterly: Audit image optimization and performance
- Annually: Review and update design system standards

// Version Control
- Document changes: Update this wiki when making system changes
- Test thoroughly: Verify changes across all breakpoints
- Maintain consistency: All team members must follow these standards</code></pre>
            </div>
        </div>
    </div>
</section>
