import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os
import re

# ================= CONFIG =================
BASE_URL = "https://www.espn.com/nhl/schedule"
OUTPUT_PATH = "data/hockey/games_of_day_nhl.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}
# ==========================================


def parse_team_from_url(team_href: str) -> dict:
    """
    Exemple:
    /nhl/team/_/name/bos/boston-bruins
    """
    team_href = team_href.rstrip("/")
    parts = team_href.split("/")

    team_id = parts[-2]
    slug = parts[-1]
    name = slug.replace("-", " ").title()

    return {
        "id": team_id,
        "name": name,
        "url": "https://www.espn.com" + team_href,
        "logo": f"https://a.espncdn.com/i/teamlogos/nhl/500/{team_id}.png"
    }


def convert_espn_date(date_text: str) -> str:
    """
    ESPN example:
    'Tuesday, February 4'
    """
    date_text = re.sub(r"^[A-Za-z]+,\s*", "", date_text)
    date_obj = datetime.strptime(date_text, "%B %d")
    date_obj = date_obj.replace(year=datetime.now().year)

    return date_obj.strftime("%Y%m%d")


def get_games_of_day():
    today_str = datetime.now().strftime("%Y%m%d")
    response = requests.get(BASE_URL, headers=HEADERS, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    games = []

    sections = soup.select("section")

    for section in sections:
        title = section.select_one("h2.Table__Title")
        if not title:
            continue

        espn_date = convert_espn_date(title.get_text(strip=True))

        # 🔥 On garde UNIQUEMENT les matchs du jour
        if espn_date != today_str:
            continue

        tables = section.select("table.Table")

        for table in tables:
            headers = [th.get_text(strip=True).lower() for th in table.select("thead th")]
            if "time" not in headers:
                continue

            rows = table.select("tbody tr")

            for row in rows:
                teams = row.select(".Table__Team a[href*='/nhl/team']")
                if len(teams) < 2:
                    continue

                away_team = parse_team_from_url(teams[0]["href"])
                home_team = parse_team_from_url(teams[1]["href"])

                time_cell = row.select_one("td.date__col a")
                if not time_cell:
                    continue

                match_time = time_cell.get_text(strip=True)
                match_url = "https://www.espn.com" + time_cell["href"]

                games.append({
                    "date": espn_date,
                    "time": match_time,
                    "match": f"{away_team['name']} v {home_team['name']}",
                    "score": "v",
                    "away": away_team,
                    "home": home_team,
                    "match_url": match_url
                })

    return {
        "source": "ESPN",
        "league": "NHL",
        "date": today_str,
        "games_count": len(games),
        "games": games
    }


def save_json(data: dict):
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    data = get_games_of_day()
    save_json(data)
    print(f"✅ {data['games_count']} matchs NHL DU JOUR enregistrés dans {OUTPUT_PATH}")