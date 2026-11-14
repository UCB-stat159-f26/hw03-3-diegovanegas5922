
import re
from urllib.request import Request, urlopen
import ast
import pandas as pd

def _normalize_name(player_name):
    return re.sub(r"[^a-zA-Z]", "", player_name).lower()

def _download_matches(url_name):
    url = ("https://www.tennisabstract.com/jsmatches/"f"{url_name}Career.js")

    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})

    with urlopen(request, timeout=30) as response:
        content = response.read()

    if not content:
        raise ValueError("No match data was found.")

    return content.decode("utf-8")

def _parse_matches(js_text):
    match = re.search(r"var\s+morematchmx\s*=\s*(\[.*?\])\s*;", js_text, flags=re.DOTALL,)
    if not match:
        raise ValueError("Could not find career match data.")
    return ast.literal_eval(match.group(1))

def _calculate_age(birth_date, match_date):
    return (match_date - birth_date).days / 365.2425

def _opponent_age(value, match_date):
    value = str(value).strip()
    if not value:
        return float("nan")
    if re.fullmatch(r"\d{8}", value):
        birth_date = pd.to_datetime(value, format="%Y%m%d", errors="coerce")
        if pd.isna(birth_date):
            return float("nan")
        return _calculate_age(birth_date, match_date)
    return pd.to_numeric(value, errors="coerce")

def _process_match(match, birth_date):
    match_date = pd.to_datetime(match[0], format="%Y%m%d", errors="coerce")
    if pd.isna(match_date):
        return None
    player_age= _calculate_age(birth_date, match_date)
    opponent_age = _opponent_age(match[16], match_date)

    return {"Match_Date": match_date,"Tournament": match[1],"Surface": match[2],
            "Opponent": match[11], "Player_Age": player_age, "Opponent_Age": opponent_age,
            "Age_Difference": player_age - opponent_age,"Result": {"W": "Win", "L": "Loss"}.get(match[4]),}

def _clean_matches(matches, birth_date):
    rows = [_process_match(match, birth_date) for match in matches if len(match) > 16 and match[4] in ("W", "L")]
    df = pd.DataFrame(row for row in rows if row is not None)
    if df.empty:
        raise ValueError("No valid matches were found.")

    df = df.dropna(subset=["Player_Age", "Opponent_Age", "Result"])

    return df[(df["Player_Age"] >= 0) & (df["Opponent_Age"] >= 0)].copy()


