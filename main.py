import time
import traceback
from concurrent.futures import ThreadPoolExecutor

from config import (
    INTERVAL_MINUTES,
    MAX_POSTS_PER_CYCLE,
)

from scraper import fetch_all_news
from processor import is_duplicate, format_message
from database import is_posted, save
from telegram import send_message
from utils import logger

# ============================
# Safe execution wrapper
# ============================

def safe_run(func, *args, retries=3, delay=2):
    for attempt in range(1, retries + 1):
        try:
            return func(*args)
        except Exception as e:
            logger.warning(f"⚠️ Attempt {attempt} failed: {e}")
            time.sleep(delay * attempt)
    return None

# ============================
# Process one news item
# ============================

def process_item(item, recent_titles):
    try:
        news_id = item["id"]
        title   = item["title"]

        if is_posted(news_id):
            return None

        if is_duplicate(title, recent_titles):
            logger.info(f"🔁 Duplicate skipped: {title[:60]}")
            return None

        msg = format_message(item)

        result = safe_run(send_message, msg)
        if not result:
            return None

        save(news_id, title)
        return title

    except Exception:
        logger.error(f"❌ Error processing item:\n{traceback.format_exc()}")
        return None

# ============================
# Main loop
# ============================

def run():
    logger.info("🚀 Bot started")

    recent_titles = []

    while True:
        try:
            logger.info("🔄 Fetching news...")

            news = safe_run(fetch_all_news)
            if not news:
                logger.warning("⚠️ No news fetched")
                time.sleep(INTERVAL_MINUTES * 60)
                continue

            posted = 0

            # limit posts
            items = news[:MAX_POSTS_PER_CYCLE]

            with ThreadPoolExecutor(max_workers=3) as executor:
                results = executor.map(
                    lambda item: process_item(item, recent_titles),
                    items
                )

            for r in results:
                if r:
                    recent_titles.append(r)
                    posted += 1

            logger.info(f"✅ Posted {posted} news")

        except Exception:
            logger.error(f"🔥 Main loop error:\n{traceback.format_exc()}")

        time.sleep(INTERVAL_MINUTES * 60)

# ============================
# Entry point
# ============================

if __name__ == "__main__":
    run()
