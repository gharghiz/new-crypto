"""
Parallel RSS scraper
"""

import feedparser
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import RSS_FEEDS
from core.utils import logger, clean_title, clean_url

def fetch_feed(feed: dict):
    news = []
    try:
        parsed = feedparser.parse(feed["url"])

        for entry in parsed.entries[:25]:
            news_id = entry.get("id") or entry.get("link")
            title   = clean_title(entry.get("title", ""))
            url     = clean_url(entry.get("link", ""))

            if not news_id or not title:
                continue

            news.append({
                "id": news_id,
                "title": title,
                "url": url,
                "source": feed["name"],
            })

        logger.info(f"📡 {feed['name']}: {len(news)} items")

    except Exception as e:
        logger.warning(f"⚠️ Feed error ({feed['name']}): {e}")

    return news

def fetch_all_news():
    all_news = []

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(fetch_feed, feed) for feed in RSS_FEEDS]

        for future in as_completed(futures):
            try:
                all_news.extend(future.result())
            except Exception as e:
                logger.warning(f"⚠️ Scraper error: {e}")

    logger.info(f"📊 Total news: {len(all_news)}")
    return all_news
