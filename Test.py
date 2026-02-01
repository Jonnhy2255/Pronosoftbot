import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os

URL = "https://www.espn.com/nhl/schedule"
OUTPUT_PATH = "data/hockey/games_of_day_nhl.json"

def get_today_upcoming_games():
    res = requests.get(URL, headers={
        "User-Agent": "Mozilla/5.0"
    })
    soup = BeautifulSoup(res.text, "html.parser")

    # Format ESPN : Sunday, February 1, 2026
    today_str = datetime.now().strftime("%A, %B %d, %Y").replace(" 0", " ")

    results = []

    for table_block in soup.select(".ScheduleTables"):
        title = table_block.select_one(".Table__Title")
        if not title:
            continue

        table_date = title.text.strip()

        # Uniquement les matchs du jour
        if table_date != today_str:
            continue

        table = table_block.select_one("table")
        if not table:
            continue

        headers = [th.text.strip().lower() for th in table.select("thead th")]

        # On garde seulement les tableaux avec TIME (matchs non joués)
        if "time" not in headers:
            continue

        for row in table.select("tbody tr"):
            team_links = row.select(".Table__Team a:last-child")
            if len(team_links) != 2:
                continue

            away = team_links[0].text.strip()
            home = team_links[1].text.strip()

            time_cell = row.select_one(".date__col a")
            time = time_cell.text.strip() if time_cell else None

            game_link = row.select_one(".date__col a")
            game_id = None

            if game_link and "gameId" in game_link["href"]:
                game_id = game_link["href"].split("gameId/")[1].split("/")[0]

            results.append({
                "date": table_date,
                "time": time,
                "home": home,
                "away": away,
                "gameId": game_id
            })

    return results


def save_to_json(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    games = get_today_upcoming_games()
    save_to_json(games, OUTPUT_PATH)

    print(f"\n✅ {len(games)} matchs NHL du jour enregistrés avec noms complets dans : {OUTPUT_PATH}\n")