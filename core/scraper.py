import feedparser
from concurrent.futures import ThreadPoolExecutor
from config import RSS_FEEDS
from core.utils import clean_title, clean_url, logger


def fetch_feed(feed):
    news = []
    try:
        parsed = feedparser.parse(feed["url"])

        for entry in parsed.entries[:20]:
            news.append({
                "id": entry.get("link"),
                "title": clean_title(entry.get("title")),
                "url": clean_url(entry.get("link")),
                "source": feed["name"],
            })

    except Exception as e:
        logger.warning(f"⚠️ {feed['name']} error: {e}")

    return news


def fetch_all_news():
    all_news = []

    with ThreadPoolExecutor(max_workers=5) as ex:
        results = ex.map(fetch_feed, RSS_FEEDS)
        for r in results:
            all_news.extend(r)

    logger.info(f"📊 {len(all_news)} news fetched")
    return all_news
