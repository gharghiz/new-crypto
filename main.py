import time
import traceback
from concurrent.futures import ThreadPoolExecutor

from core.scraper import fetch_all_news
from core.processor import (
    is_duplicate,
    is_important,
    format_message,
)
from services.telegram import send_message
from db.database import init_db, is_posted, save
from core.utils import logger


INTERVAL_SECONDS = 300
MAX_POSTS = 5


def process_item(item, recent_titles):
    try:
        title = item["title"]
        news_id = item["id"]

        if not is_important(title):
            return None

        if is_posted(news_id):
            return None

        if is_duplicate(title, recent_titles):
            logger.info(f"🔁 Duplicate: {title[:60]}")
            return None

        msg = format_message(item)

        res = send_message(msg)
        if not res:
            return None

        save(news_id, title, item["source"], item["url"])
        return title

    except Exception:
        logger.error(traceback.format_exc())
        return None


def run():
    logger.info("🚀 Bot started")
    init_db()

    recent_titles = []

    while True:
        try:
            news = fetch_all_news()
            news = news[:MAX_POSTS]

            with ThreadPoolExecutor(max_workers=3) as executor:
                results = executor.map(
                    lambda item: process_item(item, recent_titles),
                    news
                )

            for r in results:
                if r:
                    recent_titles.append(r)

            logger.info("✅ Cycle done")

        except Exception:
            logger.error(traceback.format_exc())

        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    run()
