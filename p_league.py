import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta, timezone
import re
import os

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0"
}

LEAGUES = {
    "Premier League": {"code": "eng.1", "json": "p_league.json"},
    "LaLiga": {"code": "esp.1", "json": "laliga.json"},
    "Bundesliga": {"code": "ger.1", "json": "bundesliga.json"},
    "Argentina - Primera Nacional": {"code": "arg.2", "json": "Argentina_Primera_Nacional.json"},
    "Austria - Bundesliga": {"code": "aut.1", "json": "Austria_Bundesliga.json"},
    "Belgium - Jupiler Pro League": {"code": "bel.1", "json": "Belgium_Jupiler_Pro_League.json"},
    "Brazil - Serie A": {"code": "bra.1", "json": "Brazil_Serie_A.json"},
    "Brazil - Serie B": {"code": "bra.2", "json": "Brazil_Serie_B.json"},
    "Chile - Primera Division": {"code": "chi.1", "json": "Chile_Primera_Division.json"},
    "China - Super League": {"code": "chn.1", "json": "China_Super_League.json"},
    "Colombia - Primera A": {"code": "col.1", "json": "Colombia_Primera_A.json"},
    "England - National League": {"code": "eng.5", "json": "England_National_League.json"},
    "France - Ligue 1": {"code": "fra.1", "json": "France_Ligue_1.json"},
    "Greece - Super League 1": {"code": "gre.1", "json": "Greece_Super_League_1.json"},
    "Italy - Serie A": {"code": "ita.1", "json": "Italy_Serie_A.json"},
    "Japan - J1 League": {"code": "jpn.1", "json": "Japan_J1_League.json"},
    "Mexico - Liga MX": {"code": "mex.1", "json": "Mexico_Liga_MX.json"},
    "Netherlands - Eredivisie": {"code": "ned.1", "json": "Netherlands_Eredivisie.json"},
    "Paraguay - Division Profesional": {"code": "par.1", "json": "Paraguay_Division_Profesional.json"},
    "Peru - Primera Division": {"code": "per.1", "json": "Peru_Primera_Division.json"},
    "Portugal - Primeira Liga": {"code": "por.1", "json": "Portugal_Primeira_Liga.json"},
    "Romania - Liga I": {"code": "rou.1", "json": "Romania_Liga_I.json"},
    "Russia - Premier League": {"code": "rus.1", "json": "Russia_Premier_League.json"},
    "Saudi Arabia - Pro League": {"code": "ksa.1", "json": "Saudi_Arabia_Pro_League.json"},
    "Sweden - Allsvenskan": {"code": "swe.1", "json": "Sweden_Allsvenskan.json"},
    "Switzerland - Super League": {"code": "sui.1", "json": "Switzerland_Super_League.json"},
    "Turkey - Super Lig": {"code": "tur.1", "json": "Turkey_Super_Lig.json"},
    "USA - Major League Soccer": {"code": "usa.1", "json": "USA_Major_League_Soccer.json"},
    "Venezuela - Primera Division": {"code": "ven.1", "json": "Venezuela_Primera_Division.json"}
}

# 🗓️ Définir la plage : du 11 octobre à hier
start_date = datetime(2025, 10, 11, tzinfo=timezone.utc)
end_date = datetime.now(timezone.utc) - timedelta(days=1)

for league_name, league_info in LEAGUES.items():
    BASE_URL = f"https://www.espn.com/soccer/schedule/_/date/{{date}}/league/{league_info['code']}"
    JSON_FILE = league_info["json"]

    # Charger les anciens matchs
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            existing_matches = {match["gameId"]: match for match in json.load(f)}
    else:
        existing_matches = {}

    new_matches_total = 0

    # 🔁 Boucle sur chaque jour de la période
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime("%Y%m%d")
        print(f"\n📅 Récupération des matchs du {date_str} pour {league_name}...")

        try:
            res = requests.get(BASE_URL.format(date=date_str), headers=HEADERS)
            soup = BeautifulSoup(res.content, "html.parser")
        except Exception as e:
            print(f"⚠️ Erreur de requête pour {league_name}: {e}")
            current_date += timedelta(days=1)
            continue

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

                    if "USMNT" in team1 or "USWNT" in team1 or "USMNT" in team2 or "USWNT" in team2:
                        continue
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
                        existing_matches[game_id] = match_data
                        new_matches_total += 1

                except Exception as e:
                    print(f"⚠️ Erreur lors du parsing pour {league_name} : {e}")
                    continue

        current_date += timedelta(days=1)

    # Sauvegarde mise à jour
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(list(existing_matches.values()), f, indent=2, ensure_ascii=False)

    print(f"✅ {league_name} mise à jour : {len(existing_matches)} matchs au total, +{new_matches_total} ajoutés.")