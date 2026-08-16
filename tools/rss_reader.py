import feedparser
from datetime import datetime, timedelta
from config.settings import RSS_SOURCES

def fetch_articles(days_back: int = 7) -> list[dict]:
    all_articles = []
    cutoff_date = datetime.now() - timedelta(days=days_back)

    for url in RSS_SOURCES:
        feed = feedparser.parse(url)

        for entry in feed.entries:
            published = parse_date(entry)

            if published and published < cutoff_date:
                continue

            article = {
                "title":     entry.get("title", "No title"),
                "link":      entry.get("link", ""),
                "summary":   entry.get("summary", ""),
                "published": published.strftime("%Y-%m-%d") if published else "Unknown",
                "source":    feed.feed.get("title", url),
            }
            all_articles.append(article)

    return all_articles


def parse_date(entry) -> datetime | None:
    for field in ["published_parsed", "updated_parsed"]:
        value = entry.get(field)
        if value:
            try:
                return datetime(*value[:6])
            except Exception:
                continue
    return None

