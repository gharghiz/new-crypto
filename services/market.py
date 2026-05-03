import requests
from config import COIN_MAP


def get_market_data(title):
    title = title.lower()

    coin_id = None
    for k, v in COIN_MAP.items():
        if k in title:
            coin_id = v
            break

    if not coin_id:
        return None

    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params={
                "ids": coin_id,
                "vs_currencies": "usd",
                "include_1hr_change": "true",
                "include_24hr_change": "true",
            }
        ).json()

        data = r.get(coin_id, {})
        price = data.get("usd", 0)
        c1 = round(data.get("usd_1h_change", 0), 2)
        c24 = round(data.get("usd_24h_change", 0), 2)

        return {
            "price": f"${price:,.2f}",
            "change_1h": f"{c1}%",
            "change_24h": f"{c24}%"
        }

    except Exception:
        return None
