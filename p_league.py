import json
import os
from datetime import datetime, timezone

# Ton dictionnaire complet de ligues
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

# Fonction pour convertir la date "Tuesday, October 14, 2025" → datetime
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%A, %B %d, %Y")
    except ValueError:
        return None

# Définir la plage de dates à supprimer (11 octobre → aujourd’hui)
start_date = datetime.strptime("Saturday, October 11, 2025", "%A, %B %d, %Y")
end_date = datetime.now(timezone.utc)

print(f"🧹 Suppression des matchs du {start_date.strftime('%d %B %Y')} au {end_date.strftime('%d %B %Y')}...\n")

# Parcourir chaque ligue et nettoyer
for league_name, league_info in LEAGUES.items():
    json_file = league_info["json"]

    if not os.path.exists(json_file):
        print(f"⚠️ {league_name} : fichier {json_file} introuvable.")
        continue

    with open(json_file, "r", encoding="utf-8") as f:
        matches = json.load(f)

    before_count = len(matches)

    # Garder seulement les matchs avant le 11 octobre
    filtered_matches = []
    for match in matches:
        match_date = parse_date(match["date"])
        if not match_date:
            continue
        # On garde les matchs en dehors de la plage à supprimer
        if not (start_date <= match_date <= end_date):
            filtered_matches.append(match)

    after_count = len(filtered_matches)

    # Sauvegarde
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(filtered_matches, f, indent=2, ensure_ascii=False)

    print(f"✅ {league_name} : {before_count - after_count} matchs supprimés, {after_count} restants.")

print("\n🎯 Nettoyage global terminé.")