Syndication and Canonical SEO Rules

Goal: When you republish articles on other platforms (Medium, DEV, Substack, LinkedIn, etc.), search engines should recognize haiderali.co as the original source so your site accrues the SEO value.

What the site already enforces
- Canonical tag: Every post includes a rel=canonical pointing to the post’s URL on haiderali.co.
- Structured data: Each post outputs BlogPosting JSON‑LD with the canonical URL.
- Open Graph/Twitter: og:url and twitter:title/description are aligned with the canonical.
- Microformats: rel="syndication-source" and rel="original-source" are emitted for posts.

Your cross‑posting checklist
1) Always set the canonical URL to the original on haiderali.co
   - Medium: Add “Customize canonical link” in the story options and paste the original URL.
   - DEV.to: Set canonical_url in the front matter or UI.
   - Substack: Add the original URL under “Add canonical link” (in post settings) or in the head markup if available.
   - LinkedIn Articles: Include a note at the top: “Originally published at https://haiderali.co/…”. LinkedIn does not expose canonical fields; the attribution note and consistent links help.

2) Publish to haiderali.co first, then syndicate
   - This ensures your post is crawled with the canonical first, reducing duplicate‑content risk.

3) Keep titles/slugs consistent across platforms
   - Use the same headline and a similar slug. Consistent metadata strengthens the canonical signal.

4) Optional: Add an attribution line in the body
   - “Originally published at https://haiderali.co/…” near the top or bottom.

5) Avoid full‑text duplication where platforms can’t set canonical
   - Post an excerpt + link instead when a platform does not support setting a canonical URL.

6) Sitemaps and indexing
   - The site publishes /sitemap.xml. Submit your sitemap in Google Search Console and Bing Webmaster Tools.
   - Use Search Console “Inspect URL” to expedite indexing for new articles.

Notes on redirects and URL changes
- We enabled jekyll-redirect-from and add redirect_from automatically when category paths change. If you change a post’s date or slug, add its old path to redirect_from to preserve SEO equity.

