import feedparser
import datetime

FEEDS = {
    "The Block": "https://www.theblock.co/rss.xml",
    "Decrypt": "https://decrypt.co/feed",
    "Bitcoin Magazine": "https://bitcoinmagazine.com/feed",
}


def fetch_all_feeds():
    articles = []
    for source, url in FEEDS.items():
        try:
            print(f"[fetcher] Fetching {source} ...")
            feed = feedparser.parse(url)
            for entry in feed.entries:
                article = {
                    "source": source,
                    "title": entry.get("title", ""),
                    "link": entry.get("link", ""),
                    "summary": entry.get("summary", entry.get("description", "")),
                    "published": entry.get("published", str(datetime.datetime.utcnow())),
                }
                articles.append(article)
            print(f"[fetcher] {source}: {len(feed.entries)} articles fetched")
        except Exception as e:
            print(f"[fetcher] ERROR fetching {source}: {e}")
    return articles
