import requests
import time
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from core.utils import logger

URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"


def send_message(text):
    for _ in range(3):
        try:
            r = requests.post(URL, json={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": text,
                "parse_mode": "HTML"
            }, timeout=10)

            if r.status_code == 200:
                return True

            if r.status_code == 429:
                time.sleep(5)

        except Exception as e:
            logger.warning(e)

    return False
