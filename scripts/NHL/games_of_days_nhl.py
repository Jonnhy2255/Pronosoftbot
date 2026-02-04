import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os

# ================= CONFIG =================
BASE_URL = "https://www.espn.com/nhl/schedule/_/date/"
OUTPUT_PATH = "data/hockey/games_of_day_nhl.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}
# ==========================================


def get_today_url():
    today = datetime.now().strftime("%Y%m%d")
    return BASE_URL + today, today


def clean_text(text: str) -> str:
    return text.replace("\n", "").strip()


def parse_team_from_url(team_href: str) -> dict:
    """
    Exemple ESPN :
    /nhl/team/_/name/bos/boston-bruins
    """
    team_href = team_href.rstrip("/")
    parts = team_href.split("/")

    team_id = parts[-2]          # bos
    slug = parts[-1]             # boston-bruins
    name = slug.replace("-", " ").title()

    return {
        "id": team_id,
        "name": name,
        "url": "https://www.espn.com" + team_href,
        "logo": f"https://a.espncdn.com/i/teamlogos/nhl/500/{team_id}.png"
    }


def get_games_of_day():
    url, today_str = get_today_url()
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    games = []

    # Tables ESPN contenant les matchs
    tables = soup.select("table.Table")

    for table in tables:
        headers = [th.get_text(strip=True).lower() for th in table.select("thead th")]

        # On garde uniquement les tables avec colonne TIME (matchs à venir)
        if "time" not in headers:
            continue

        rows = table.select("tbody tr")

        for row in rows:
            team_links = row.select(".Table__Team a[href*='/nhl/team']")
            if len(team_links) < 2:
                continue

            away_team = parse_team_from_url(team_links[0]["href"])
            home_team = parse_team_from_url(team_links[1]["href"])

            # Heure + lien du match
            time_cell = row.select_one("td.date__col a")
            if not time_cell:
                continue

            match_time = clean_text(time_cell.get_text())
            match_url = "https://www.espn.com" + time_cell["href"]

            game = {
                "date": today_str,
                "time": match_time,
                "match": f"{away_team['name']} v {home_team['name']}",
                "score": "v",
                "away": away_team,
                "home": home_team,
                "match_url": match_url
            }

            games.append(game)

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
    print(f"✅ {data['games_count']} matchs NHL à venir enregistrés dans {OUTPUT_PATH}")