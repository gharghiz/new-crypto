"""
Market service — CoinGecko integration with caching
"""

import time
import requests
from core.utils import logger
from config import COIN_MAP

_session = requests.Session()

# ============================
# Cache
# ============================

_cache = {}
CACHE_TTL = 300  # seconds

# ============================
# Fetch price
# ============================

def get_coin_id_from_title(title: str):
    title = title.lower()
    for keyword, coin_id in COIN_MAP.items():
        if keyword in title:
            return coin_id
    return None


def fetch_price(coin_id: str):
    try:
        resp = _session.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params={
                "ids": coin_id,
                "vs_currencies": "usd",
                "include_24hr_change": "true",
                "include_1hr_change": "true",
            },
            timeout=5,
        )

        data = resp.json().get(coin_id, {})
        if not data:
            return None

        price = data.get("usd", 0)
        change_1h = round(data.get("usd_1h_change", 0), 2)
        change_24h = round(data.get("usd_24h_change", 0), 2)

        return {
            "price": price,
            "change_1h": change_1h,
            "change_24h": change_24h,
        }

    except Exception as e:
        logger.warning(f"⚠️ Market API error: {e}")
        return None


def get_market_data(title: str):
    coin_id = get_coin_id_from_title(title)
    if not coin_id:
        return None

    now = time.time()

    # Check cache
    if coin_id in _cache:
        data, ts = _cache[coin_id]
        if now - ts < CACHE_TTL:
            return data

    # Fetch fresh
    data = fetch_price(coin_id)
    if not data:
        return None

    # Format
    def fmt_change(c):
        return f"{'▲' if c >= 0 else '▼'} {'+' if c >= 0 else ''}{c}%"

    formatted = {
        "price": f"${data['price']:,.2f}",
        "change_1h": fmt_change(data["change_1h"]),
        "change_24h": fmt_change(data["change_24h"]),
    }

    _cache[coin_id] = (formatted, now)
    return formatted
