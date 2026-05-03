import logging
import html
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("crypto")


def safe_html(text):
    return html.escape(str(text))


def clean_title(title):
    title = re.sub(r"\s+", " ", str(title)).strip()
    return title[:200]


def clean_url(url):
    return url.split("?")[0] if url else ""
