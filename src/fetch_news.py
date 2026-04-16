import feedparser
from dateutil import parser


def fetch_feed(feed_name, feed_url):
    parsed = feedparser.parse(feed_url)
    stories = []

    for entry in parsed.entries:
        title = entry.get("title", "").strip()
        link = entry.get("link", "").strip()
        summary = entry.get("summary", "").strip()
        published_raw = entry.get("published") or entry.get("updated") or ""

        try:
            published_at = parser.parse(published_raw).isoformat() if published_raw else ""
        except Exception:
            published_at = ""

        if title and link:
            stories.append(
                {
                    "source": feed_name,
                    "title": title,
                    "link": link,
                    "summary": summary,
                    "published_at": published_at,
                }
            )

    return stories