import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
	// Load Markdown and MDX files in the `src/content/blog/` directory.
	loader: glob({ base: './src/content/blog', pattern: '**/*.{md,mdx}' }),
	// Type-check frontmatter using a schema
	schema: ({ image }) =>
		z.object({
			title: z.string(),
			description: z.string(),
			// Transform string to Date object
			pubDate: z.coerce.date(),
			updatedDate: z.coerce.date().optional(),
			heroImage: image().optional(),
		}),
});

const stories = defineCollection({
	// Load Markdown and MDX files in the `src/content/stories/` directory.
	loader: glob({ base: './src/content/stories', pattern: '**/*.{md,mdx}' }),
	// Type-check frontmatter using a schema
	schema: ({ image }) =>
		z.object({
			title: z.string(),
			description: z.string(),
			url: z.string().url(),
			pubDate: z.coerce.date(),
			image: image().optional(),
		}),
});

const releaseNotes = defineCollection({
	loader: glob({ base: './src/content/release-notes', pattern: '**/*.{md,mdx}' }),
	schema: z.object({
		title: z.string(),
		version: z.string(),
		summary: z.string(),
		date: z.coerce.date(),
	}),
});

export const collections = { blog, stories, releaseNotes };
