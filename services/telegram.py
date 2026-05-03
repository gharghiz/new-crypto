"""
Telegram service — sending messages with retry + rate limit handling
"""

import time
import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from core.utils import logger

_session = requests.Session()

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

MAX_RETRIES = 3


def send_message(text: str, disable_preview: bool = True):
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": disable_preview,
    }

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = _session.post(TELEGRAM_API, json=payload, timeout=10)

            # Success
            if resp.status_code == 200:
                logger.info("✅ Sent to Telegram")
                return resp.json()

            # Rate limit
            if resp.status_code == 429:
                retry_after = resp.json().get("parameters", {}).get("retry_after", 5)
                logger.warning(f"⏳ Rate limited — waiting {retry_after}s")
                time.sleep(retry_after)
                continue

            # Other errors
            logger.error(f"❌ Telegram error {resp.status_code}: {resp.text}")
            return None

        except Exception as e:
            logger.warning(f"⚠️ Attempt {attempt} failed: {e}")
            time.sleep(2 * attempt)

    return None


def send_price_alert(symbol: str, price: float, change_1h: float):
    sign = "+" if change_1h >= 0 else ""
    direction = "🚀 Surge" if change_1h >= 0 else "🔴 Drop"

    price_str = f"${price:,.2f}" if price >= 1 else f"${price:.6f}"

    msg = (
        f"⚡️ <b>Price Alert — {symbol}</b>\n\n"
        f"{direction} in the last hour!\n\n"
        f"💰 {price_str}\n"
        f"📈 1h: {sign}{change_1h}%\n"
    )

    return send_message(msg)
