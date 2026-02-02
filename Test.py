import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os
import re

URL = "https://www.espn.com/nhl/schedule"
OUTPUT_PATH = "data/hockey/games_of_day_nhl.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def clean_team_name_from_url(url):
    # /nhl/team/_/name/la/los-angeles-kings
    return url.split("/")[-1].replace("-", " ").title()

def get_today_upcoming_games():
    res = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")

    today_str = datetime.now().strftime("%A, %B %d, %Y").replace(" 0", " ")

    results = []

    for table_block in soup.select(".ScheduleTables"):
        title = table_block.select_one(".Table__Title")
        if not title:
            continue

        if title.text.strip() != today_str:
            continue

        table = table_block.select_one("table")
        if not table:
            continue

        headers = [th.text.strip().lower() for th in table.select("thead th")]
        if "time" not in headers:
            continue  # matchs déjà joués

        for row in table.select("tbody tr"):
            teams = row.select(".Table__Team")
            if len(teams) != 2:
                continue

            # Away
            away_link = teams[0].select_one("a[href*='/nhl/team']")
            away_logo = teams[0].select_one("img")
            away_name = clean_team_name_from_url(away_link["href"])
            away_logo_url = away_logo["src"] if away_logo else None

            # Home
            home_link = teams[1].select_one("a[href*='/nhl/team']")
            home_logo = teams[1].select_one("img")
            home_name = clean_team_name_from_url(home_link["href"])
            home_logo_url = home_logo["src"] if home_logo else None

            time_cell = row.select_one(".date__col a")
            if not time_cell:
                continue

            time = time_cell.text.strip()

            # gameId
            game_id = None
            match = re.search(r"gameId/(\d+)", time_cell["href"])
            if match:
                game_id = match.group(1)

            results.append({
                "league": "NHL",
                "date": today_str,
                "time": time,
                "gameId": game_id,
                "teams": {
                    "away": {
                        "name": away_name,
                        "logo": away_logo_url
                    },
                    "home": {
                        "name": home_name,
                        "logo": home_logo_url
                    }
                }
            })

    return results


def save_to_json(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    games = get_today_upcoming_games()
    save_to_json(games, OUTPUT_PATH)

    print(f"\n✅ {len(games)} matchs NHL du jour enregistrés dans : {OUTPUT_PATH}\n")