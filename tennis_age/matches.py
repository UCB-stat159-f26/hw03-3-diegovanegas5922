
import re
from urllib.request import Request, urlopen

def _normalize_name(player_name):
    return re.sub(r"[^a-zA-Z]", "", player_name).lower()

def _download_matches(url_name):
    url = (
        "https://www.tennisabstract.com/jsmatches/"
        f"{url_name}Career.js"
    )

    request = Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urlopen(request, timeout=30) as response:
        content = response.read()

    if not content:
        raise ValueError("No match data was found.")

    return content.decode("utf-8")


