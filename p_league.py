import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta, timezone
import re
import os

LEAGUE = "eng.1"
BASE_URL = "https://www.espn.com/soccer/schedule/_/date/{date}/league/" + LEAGUE
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0"
}
JSON_FILE = "p_league.json"

# Calcul de la date d'hier en UTC
yesterday = datetime.now(timezone.utc) - timedelta(days=1)
date_str = yesterday.strftime("%Y%m%d")
url = BASE_URL.format(date=date_str)

print(f"📅 Récupération des matchs du {date_str}...")

# Charger les anciens matchs
if os.path.exists(JSON_FILE):
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        existing_matches = {match["gameId"]: match for match in json.load(f)}
else:
    existing_matches = {}

# Nouvelle récupération
new_matches = {}

res = requests.get(url, headers=HEADERS)
soup = BeautifulSoup(res.content, "html.parser")

tables = soup.select("div.ResponsiveTable")
for table in tables:
    date_title_tag = table.select_one("div.Table__Title")
    date_text = date_title_tag.text.strip() if date_title_tag else date_str

    rows = table.select("tbody > tr.Table__TR")
    for row in rows:
        try:
            away_team_tag = row.select_one("td.events__col span.Table__Team.away a.AnchorLink:last-child")
            home_team_tag = row.select_one("td.colspan__col span.Table__Team a.AnchorLink:last-child")
            score_tag = row.select_one("td.colspan__col a.AnchorLink.at")

            if not away_team_tag or not home_team_tag or not score_tag:
                continue

            team1 = away_team_tag.text.strip()
            team2 = home_team_tag.text.strip()
            score = score_tag.text.strip()

            # Filtrer les équipes non désirées
            if "USMNT" in team1 or "USWNT" in team1 or "USMNT" in team2 or "USWNT" in team2:
                continue

            # Filtrer les scores non joués (ex: " v ")
            if score.lower() == "v":
                continue

            match_url = score_tag["href"]
            match_id_match = re.search(r"gameId/(\d+)", match_url)
            if not match_id_match:
                continue

            game_id = match_id_match.group(1)

            if game_id not in existing_matches:
                match_data = {
                    "gameId": game_id,
                    "date": date_text,
                    "team1": team1,
                    "score": score,
                    "team2": team2,
                    "title": f"{team1} VS {team2}",
                    "match_url": "https://www.espn.com" + match_url
                }
                new_matches[game_id] = match_data
                existing_matches[game_id] = match_data

        except Exception as e:
            print(f"⚠️ Erreur lors du parsing : {e}")
            continue

# Sauvegarde mise à jour
with open(JSON_FILE, "w", encoding="utf-8") as f:
    json.dump(list(existing_matches.values()), f, indent=2, ensure_ascii=False)

print(f"\n✅ Mise à jour terminée ({len(existing_matches)} matchs au total, +{len(new_matches)} ajoutés).")
