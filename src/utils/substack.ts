import Parser from 'rss-parser';

const { fetch } = globalThis;

type SubstackPost = {
  title: string;
  link: string;
  pubDate: string;
  'content:encoded'?: string;
  'content:encodedSnippet'?: string;
  'dc:creator'?: string;
  content?: string;
  contentSnippet?: string;
  guid: string;
  isoDate?: string;
  categories?: string[];
  enclosure?: {
    url: string;
    length: string;
    type: string;
  };
};

type StoryEntry = {
  id: string;
  data: {
    title: string;
    description: string;
    url: string;
    pubDate: Date;
    image?: string;
  };
};

const FALLBACK_STORIES: StoryEntry[] = [
  {
    id: 'fallback-1',
    data: {
      title: 'Why Drafts Matter More Than Final Releases',
      description:
        'Iterating in public builds trust and momentum. Here is a playbook for showing your work before it is "done".',
      url: 'https://userfirstinsights.substack.com',
      pubDate: new Date(Date.now() - 1000 * 60 * 60 * 24 * 2),
      image: 'https://images.unsplash.com/photo-1521737604893-d14cc237f11d?auto=format&fit=crop&w=1200&q=80',
    },
  },
  {
    id: 'fallback-2',
    data: {
      title: 'Rituals That Keep Teams Moving',
      description:
        'Three lightweight practices inspired by the Unfinished playbook to guide teams through constant change.',
      url: 'https://userfirstinsights.substack.com',
      pubDate: new Date(Date.now() - 1000 * 60 * 60 * 24 * 5),
      image: 'https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?auto=format&fit=crop&w=1200&q=80',
    },
  },
  {
    id: 'fallback-3',
    data: {
      title: 'Designing Trust Under Uncertainty',
      description:
        'Signals, language, and guardrails that help people stay confident when plans keep evolving.',
      url: 'https://userfirstinsights.substack.com',
      pubDate: new Date(Date.now() - 1000 * 60 * 60 * 24 * 9),
      image: 'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=1200&q=80',
    },
  },
];

const FEED_URLS = [
  'https://userfirstinsights.substack.com/feed.rss',
  'https://userfirstinsights.substack.com/feed',
  'https://userfirstinsights.substack.com/feed.xml',
];

function extractImage(item: SubstackPost): string | undefined {
  const content = item['content:encoded'] || item.content || '';
  const imgMatch = content.match(/<img[^>]+src=["']([^"']+)["']/i);
  if (imgMatch && imgMatch[1]) {
    return imgMatch[1];
  }
  if (item.enclosure?.url) {
    return item.enclosure.url;
  }
  return undefined;
}

function buildDescription(item: SubstackPost): string {
  const raw =
    item['content:encodedSnippet'] ||
    item.contentSnippet ||
    (item['content:encoded'] ? item['content:encoded'].replace(/<[^>]*>?/gm, '') : '') ||
    'Read more...';
  const trimmed = raw.trim();
  return trimmed.length > 220 ? `${trimmed.slice(0, 217)}...` : trimmed;
}

async function fetchFeed(parser: Parser<{}, SubstackPost>, feedUrl: string): Promise<StoryEntry[] | null> {
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 8000);
    const response = await fetch(feedUrl, {
      signal: controller.signal,
      headers: {
        'User-Agent':
          'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        Accept: 'application/rss+xml, application/xml;q=0.9, */*;q=0.8',
      },
    });
    clearTimeout(timeoutId);

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const xml = await response.text();
    const feed = await parser.parseString(xml);

    if (!feed.items || feed.items.length === 0) {
      return null;
    }

    return feed.items.map((item, index): StoryEntry => {
      return {
        id: item.guid || item.link || `story-${index}`,
        data: {
          title: item.title || 'Untitled',
          description: buildDescription(item),
          url: item.link || '#',
          pubDate: new Date(item.pubDate || item.isoDate || new Date().toISOString()),
          image: extractImage(item),
        },
      };
    });
  } catch (error) {
    console.error(`[Substack] Failed to load ${feedUrl}:`, error);
    return null;
  }
}

export async function getSubstackPosts(limit = 10): Promise<StoryEntry[]> {
  const parser = new Parser<{}, SubstackPost>();

  for (const feedUrl of FEED_URLS) {
    const items = await fetchFeed(parser, feedUrl);
    if (items && items.length > 0) {
      console.info(`[Substack] Loaded ${items.length} items from ${feedUrl}`);
      return items.slice(0, limit);
    }
  }

  console.warn('[Substack] Using fallback stories');
  return FALLBACK_STORIES.slice(0, limit);
}
