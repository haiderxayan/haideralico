# Stay Unfinished Website Style Guide

## 1. Brand Foundations
- **Voice**
  - Curious, optimistic, and encouraging; celebrate iteration over perfection.
  - Write in the first person when speaking as the author, second person for calls to action.
- **Core Narrative**
  - Theme of momentum, experimentation, and creative resilience.
  - Reinforce the "Stay Unfinished" mindset across headings, CTAs, and supportive copy.

## 2. Color System
Defined in `tailwind.config.js` under `theme.extend.colors.primary`.
- **Primary / CTA**: `primary` (`#3B82F6`), hover/pressed state `primary-dark` (`#2563EB`).
- **Secondary Neutrals**: Tailwind `slate` palette (`slate-50` backgrounds, `slate-900` headings, `slate-600` body text).
- **Accent Usage**: Primary color reserved for buttons, badges, links, gradients, and key stats.
- **Gradients**: Use Tailwind utilities `bg-gradient-to-r from-primary via-primary-dark to-slate-900` for hero and promotional bands.

## 3. Typography
- **Fonts**: Global `font-family: "Atkinson", sans-serif` via `global.css`. Use Tailwind `font-semibold` for headings, `font-medium` for buttons.
- **Headings**: Sentence case; call-to-action headings may use emphasized words wrapped in `<span class="text-primary">`.
- **Body Copy**: Tailwind `text-slate-600` for paragraphs, `text-lg` for hero sections, `text-base` elsewhere.
- **Quotes**: Wrap testimonials in `<blockquote>` with Tailwind classes `rounded-3xl bg-white p-6 shadow ring-1 ring-slate-100`.

## 4. Layout & Spacing
- **Layout Wrapper**: Use `PageLayout.astro` for new static pages to maintain header/footer and consistent max width.
- **Content Width**: Tailwind `max-w-3xl` or `max-w-5xl` for primary content blocks; center with `mx-auto` and horizontal padding `px-4 sm:px-6 lg:px-8`.
- **Vertical Rhythm**: Apply `space-y-*` or `gap-*` utilities instead of manual margins. Default section spacing: `mt-16` or `mt-20`.
- **Cards**: Apply `rounded-3xl bg-white shadow ring-1 ring-slate-100` for white cards, `bg-slate-900 text-white` for inverted variants.

## 5. Components & Patterns
- **Buttons**: Primary button `class="inline-flex items-center justify-center rounded-full bg-primary px-6 py-3 text-base font-semibold text-white shadow transition hover:bg-primary-dark"`. Secondary button uses bordered pill `border border-slate-200 text-primary hover:border-primary hover:bg-primary/10`.
- **Badges**: Use `inline-flex items-center gap-2 rounded-full bg-primary/10 px-4 py-2 text-sm font-medium text-primary` for highlight tags (e.g., "New release").
- **Navigation**: `Header.astro` encapsulates brand link and pill navigation. New nav links should use `HeaderLink.astro` for stateful styling.
- **Footer**: Keep `Footer.astro` copy aligned with brand voice; updates should preserve the two-line structure.
- **Forms**: Inputs use `rounded-lg border border-slate-200 px-4 py-3 text-slate-700 shadow-sm` with focus ring `focus:ring-2 focus:ring-primary/20`.

## 6. Imagery & Media
- **Photography**: Rounded rectangles (`rounded-3xl`) with subtle shadow `shadow-xl` and ring `ring-1 ring-slate-200`.
- **Illustrations**: Maintain desaturated or monochrome overlays; avoid clashing colors outside the defined palette.
- **Icons**: Prefer Outline-style icons (Heroicons or similar). Apply `text-slate-600` or `text-primary` depending on emphasis.

## 7. Content Blocks
- **Stats**: Display within `<dl>` using `grid gap-6 sm:grid-cols-3`; numbers in `text-2xl font-semibold text-slate-900` and labels in `text-sm uppercase tracking-wide text-slate-500`.
- **Testimonials**: Use card pattern with quote text `text-lg text-slate-700` and footer `text-sm font-semibold text-slate-500`.
- **Callouts**: Gradient bands should include CTA buttons or link to contact/blog.

## 8. Blog & Markdown Styling
- **Listing Cards**: Adopt card pattern with metadata band, `text-slate-600` excerpt, and `inline-flex` CTA link.
- **Post Layout**: Use `prose prose-slate max-w-none` for markdown content, ensure hero image applies `rounded-3xl` and `shadow` classes.
- **Comments Section**: Surround embedded widgets (Giscus) with `rounded-3xl bg-white p-6 shadow ring-1 ring-slate-100`.

## 9. Accessibility & Interaction
- **Focus States**: Always include `focus-visible:outline` utilities on interactive elements.
- **Contrast**: Ensure text on gradients or images meets WCAG AA. Use `text-white/80` for secondary text on dark backgrounds.
- **Motion**: Default transitions (`transition`, `hover:`) should be subtle (`duration-150`/`duration-200`). Avoid large-scale animations unless purposeful.

## 10. Implementation Notes
- **Utilities First**: Favor Tailwind utilities; only add custom CSS in `global.css` when patterns cannot be expressed with utilities.
- **Consistent Imports**: For new pages, import assets via ES module (e.g., `import Cover from '../assets/cover.jpg';`).
- **Future Work**: Keep this guide updated when introducing new components or palette adjustments. Reference it before designing additional sections or pages.
