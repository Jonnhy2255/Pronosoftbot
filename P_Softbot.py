import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup
import subprocess
import math
import itertools
import os

# 🔑 Récupération des clés depuis GitHub Secrets (variables d'environnement)
API_KEY = os.getenv("API_FOOTBALL_KEY")
ODDS_API_KEY = os.getenv("ODDS_API_KEY")
groq_keys = [
    os.getenv("GROQ_API_KEY"),
    os.getenv("GROQ_API_KEY1")
]

# En-têtes API Football
api_headers = {
    'x-apisports-key': API_KEY
}

# Paramètres API Odds
REGION = "eu"
MARKETS = "h2h,totals"

# Alternateur pour Groq
groq_key_index = 0

team_name_mapping = {
    "Bournemouth": "AFC Bournemouth",
    "Rep. Of Ireland": "Republic Of Ireland",
    "Sport Recife": "Sport",
    "RB Bragantino": "Red Bull Bragantino",
    "Fortaleza EC": "Fortaleza",
    "Gremio":"Grêmio",
    "Vitoria": "Vitória",
    "Vasco DA Gama": "Vasco da Gama",
    "Sao Paulo": "São Paulo",
    "Atletico-MG": "Atlético-MG",
    "Paris Saint Germain": "Paris Saint-Germain",
    "Atletico Madrid": "Atlético Madrid",
    "San Diego": "San Diego FC",
    "Austin": "Austin FC",
    "Seattle Sounders": "Seattle Sounders FC",
    "Los Angeles FC": "LAFC",
    "Santa Fe": "Independiente Santa Fe",
    "Qingdao Youth Island": "Qingdao Hainiu",
    "Atletico Nacional": "Atlético Nacional",
    "Henan Jianye": "Henan Songshan Longmen",
    "SHANGHAI SIPG": "Shanghai Port",
    "Al-Hilal Saudi FC": "Al Hilal",
    "Inter Miami": "Inter Miami CF",
    "Portuguesa FC": "Portuguesa",
    "2 de Mayo": "2 de Mayo",
    "America de Cali": "América de Cali",
    "Carabobo FC": "Carabobo",
    "Rapid": "Rapid Bucuresti",
    "Operario-PR": "Operario PR",
    "Arges Pitesti": "Fc Arges",
    "Libertad Asuncion": "Libertad",
    "General Caballero": "General Caballero JLM",
    "Real Esppor Club": "Deportivo La Guaira",
    "UCV": "Universidad Central",
    "Cuiaba": "Cuiabá",
    "remo": "Remo",
}

classement_ligue_mapping = {
    "Colombia": {
        "Primera A": {
            "url": "https://www.espn.com/soccer/standings/_/league/col.1",
            "odds_id": "none"
        }
    },
    "France": {
        "Ligue 1": {
            "url": "https://www.espn.com/soccer/standings/_/league/fra.1",
            "odds_id": "soccer_france_ligue_one"
        }
    },
    "Belgium": {
        "Jupiler Pro League": {
            "url": "https://www.espn.com/soccer/standings/_/league/bel.1",
            "odds_id": "soccer_belgium_first_div"
        }
    },
    "England": {
        "Premier League": {
            "url": "https://www.espn.com/soccer/standings/_/league/eng.1",
            "odds_id": "soccer_epl"
        },
        "National League": {
            "url": "https://www.espn.com/soccer/standings/_/league/eng.5",
            "odds_id": "none"
        }
    },
    "Netherlands": {
        "Eredivisie": {
            "url": "https://www.espn.com/soccer/standings/_/league/ned.1",
            "odds_id": "soccer_netherlands_eredivisie"
        }
    },
    "Portugal": {
        "Primeira Liga": {
            "url": "https://www.espn.com/soccer/standings/_/league/por.1",
            "odds_id": "soccer_portugal_primeira_liga"
        }
    },
    "Spain": {
        "La Liga": {
            "url": "https://www.espn.com/soccer/standings/_/league/esp.1",
            "odds_id": "soccer_spain_la_liga"
        }
    },
    "Germany": {
        "Bundesliga": {
            "url": "https://www.espn.com/soccer/standings/_/league/ger.1",
            "odds_id": "soccer_germany_bundesliga"
        }
    },
    "Austria": {
        "Bundesliga": {
            "url": "https://www.espn.com/soccer/standings/_/league/aut.1",
            "odds_id": "soccer_austria_bundesliga"
        }
    },
    "Italy": {
        "Serie A": {
            "url": "https://www.espn.com/soccer/standings/_/league/ita.1",
            "odds_id": "soccer_italy_serie_a"
        }
    },
    "Brazil": {
        "Serie A": {
            "url": "https://www.espn.com/soccer/standings/_/league/bra.1",
            "odds_id": "soccer_brazil_campeonato"
        },
        "Serie B": {
            "url": "https://www.espn.com/soccer/standings/_/league/bra.2",
            "odds_id": "soccer_brazil_serie_b"
        }
    },
    "Turkey": {
        "Süper Lig": {
            "url": "https://www.espn.com/soccer/standings/_/league/tur.1",
            "odds_id": "soccer_turkey_super_league"
        }
    },
    "Mexico": {
        "Liga MX": {
            "url": "https://www.espn.com/soccer/standings/_/league/mex.1",
            "odds_id": "soccer_mexico_ligamx"
        }
    },
    "USA": {
        "Major League Soccer": {
            "url": "https://www.espn.com/soccer/standings/_/league/usa.1",
            "odds_id": "soccer_usa_mls"
        }
    },
    "Japan": {
        "J1 League": {
            "url": "https://www.espn.com/soccer/standings/_/league/jpn.1",
            "odds_id": "soccer_japan_j_league"
        }
    },
    "Saudi-Arabia": {
        "Pro League": {
            "url": "https://www.espn.com/soccer/standings/_/league/ksa.1",
            "odds_id": "none"
        }
    },
    "Switzerland": {
        "Super League": {
            "url": "https://www.espn.com/soccer/standings/_/league/sui.1",
            "odds_id": "soccer_switzerland_superleague"
        }
    },
    "China": {
        "Super League": {
            "url": "https://www.espn.com/soccer/standings/_/league/chn.1",
            "odds_id": "soccer_china_superleague"
        }
    },
    "Russia": {
        "Premier League": {
            "url": "https://www.espn.com/soccer/standings/_/league/rus.1",
            "odds_id": "none"
        }
    },
    "Greece": {
        "Super League 1": {
            "url": "https://www.espn.com/soccer/standings/_/league/gre.1",
            "odds_id": "soccer_greece_super_league"
        }
    },
    "Chile": {
        "Primera División": {
            "url": "https://www.espn.com/soccer/standings/_/league/chi.1",
            "odds_id": "soccer_chile_campeonato"
        }
    },
    "Peru": {
        "Primera División": {
            "url": "https://www.espn.com/soccer/standings/_/league/per.1",
            "odds_id": "none"
        }
    },
    "Sweden": {
        "Allsvenskan": {
            "url": "https://www.espn.com/soccer/standings/_/league/swe.1",
            "odds_id": "soccer_sweden_allsvenskan"
        }
    },
    "Argentina": {
        "Primera Nacional": {
            "url": "https://www.espn.com/soccer/standings/_/league/arg.2",
            "odds_id": "soccer_argentina_primera_division"
        }
    },
    "Paraguay": {
        "Division Profesional": {
            "url": "https://www.espn.com/soccer/standings/_/league/par.1",
            "odds_id": "none"
        }
    },
    "Venezuela": {
        "Primera División": {
            "url": "https://www.espn.com/soccer/standings/_/league/ven.1",
            "odds_id": "none"
        }
    },
    "Romania": {
        "Liga I": {
            "url": "https://www.espn.com/soccer/standings/_/league/rou.1",
            "odds_id": "none"
        }
    }
}

teams_urls = {
    # Bloc Europe du dernier JSON
    
}

headers = {'User-Agent': 'Mozilla/5.0'}

PREDICTIONS = []
FAILED_TEAMS = set()
IGNORED_ZERO_FORM_TEAMS = []

def get_match_stats(game_id):
    """
    Récupère les statistiques détaillées d'un match ESPN via son game_id.
    Retourne un dict { "Possession": (home, away), ... }
    """
    url = f"https://africa.espn.com/football/match/_/gameId/{game_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/117.0.0.0 Safari/537.36",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        stats_section = soup.find("section", {"data-testid": "prism-LayoutCard"})
        stats_divs = stats_section.find_all("div", class_="LOSQp") if stats_section else []
        
        stats = {}
        for div in stats_divs:
            stat_name_tag = div.find("span", class_="OkRBU")
            if not stat_name_tag:
                continue
            stat_name = stat_name_tag.get_text(strip=True)
            values = div.find_all("span", class_="bLeWt")
            if len(values) >= 2:
                team1_value = values[0].get_text(strip=True)
                team2_value = values[1].get_text(strip=True)
                stats[stat_name] = (team1_value, team2_value)

        print(f"📊 Stats récupérées pour match {game_id}: {len(stats)} statistiques trouvées")
        return stats

    except Exception as e:
        print(f"❌ Erreur récupération stats match {game_id} : {e}")
        return {}

# 🧠 Fonction DeepSeek avec alternance automatique des clés et retry automatique (VERSION AMÉLIORÉE)
def call_deepseek_analysis(prompt, max_retries=10):
    global groq_key_index

    for attempt in range(1, max_retries + 1):
        key = groq_keys[groq_key_index % len(groq_keys)]
        groq_key_index += 1

        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "deepseek-r1-distill-llama-70b",
            "messages": [
                {"role": "system", "content": "Tu es un expert en paris sportifs. Ton rôle est de faire une analyse complète du match en fonction des données fournies, puis de proposer UNE prédiction fiable parmi : victoire domicile, victoire extérieur, nul, +2.5 buts, -2.5 buts, BTTS oui, BTTS non, double chance (1X ou X2), total corners victoire domicile, total corners victoire extérieur, tirs cadrés victoire domicile, tirs cadrés victoire extérieur. Explique pourquoi en détail."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3
        }

        try:
            print(f"🧠 Tentative {attempt}/{max_retries} avec clé {(groq_key_index - 1) % len(groq_keys) + 1}...")
            response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
            response.raise_for_status()
            result = response.json()["choices"][0]["message"]["content"].strip()
            print(f"✅ Analyse IA réussie à la tentative {attempt}")
            return result
        except Exception as e:
            print(f"❌ Erreur DeepSeek (tentative {attempt}/{max_retries}) : {str(e)}")
            if attempt < max_retries:
                print("🔄 Nouvel essai dans 5 secondes...")
                import time
                time.sleep(5)  # Pause de 5 secondes avant retry
            else:
                error_msg = f"❌ Échec définitif après {max_retries} tentatives. Dernière erreur : {str(e)}"
                print(error_msg)
                return error_msg

# 🔮 Générateur de prompt détaillé (VERSION ENRICHIE AVEC STATS DÉTAILLÉES)
def generate_detailed_prompt(prediction_obj):
    home = prediction_obj["HomeTeam"]
    away = prediction_obj["AwayTeam"]
    stats_home = prediction_obj["stats_home"]
    stats_away = prediction_obj["stats_away"]
    odds = prediction_obj.get("odds", {})
    pos_home = prediction_obj.get("classement_home")
    pts_home = prediction_obj.get("points_classement_home")
    pos_away = prediction_obj.get("classement_away")
    pts_away = prediction_obj.get("points_classement_away")
    league = prediction_obj["league"]
    date = prediction_obj["date"]

    prompt = f"""
ANALYSE DE MATCH - {date}
{league}
{home} (DOMICILE) vs {away} (EXTÉRIEUR)

🏠 STATISTIQUES DE {home} (DOMICILE) :
- Classement : {pos_home}ᵉ avec {pts_home} points
- Moyenne buts marqués : {stats_home['moyenne_marques']:.2f}
- Moyenne buts encaissés : {stats_home['moyenne_encaisses']:.2f}
- Forme sur 6 matchs : {' '.join(stats_home['form_6'])} ({stats_home.get('total_points_6', 0)} points)
- Forme sur 10 matchs : {' '.join(stats_home['form_10'])} ({stats_home.get('total_points_10', 0)} points)
- Série domicile : {'-'.join(stats_home.get('serie_domicile', []))}
- Buts marqués domicile : {stats_home.get('buts_dom_marques', 0)}
- Buts encaissés domicile : {stats_home.get('buts_dom_encaisses', 0)}

✈️ STATISTIQUES DE {away} (EXTÉRIEUR) :
- Classement : {pos_away}ᵉ avec {pts_away} points
- Moyenne buts marqués : {stats_away['moyenne_marques']:.2f}
- Moyenne buts encaissés : {stats_away['moyenne_encaisses']:.2f}
- Forme sur 6 matchs : {' '.join(stats_away['form_6'])} ({stats_away.get('total_points_6', 0)} points)
- Forme sur 10 matchs : {' '.join(stats_away['form_10'])} ({stats_away.get('total_points_10', 0)} points)
- Série extérieur : {'-'.join(stats_away.get('serie_exterieur', []))}
- Buts marqués extérieur : {stats_away.get('buts_ext_marques', 0)}
- Buts encaissés extérieur : {stats_away.get('buts_ext_encaisses', 0)}

💰 COTES DISPONIBLES :
"""
    if odds and odds != {}:
        bookmaker = odds.get('bookmaker', 'N/A')
        prompt += f"Bookmaker : {bookmaker}\n"
        
        h2h = odds.get('h2h', {})
        if h2h:
            prompt += "- 1X2 : "
            for outcome, cote in h2h.items():
                prompt += f"{outcome} : {cote} | "
            prompt += "\n"
        
        totals = odds.get('totals', {})
        if totals:
            prompt += "- Total 2.5 : "
            for outcome, cote in totals.items():
                prompt += f"{outcome} : {cote} | "
            prompt += "\n"
    else:
        prompt += "Aucune cote disponible\n"

    # ✅ NOUVEAUTÉ 1 : Ajout des 10 derniers matchs complets avec nouvelle structure + STATS DÉTAILLÉES
    prompt += f"\n📅 10 DERNIERS MATCHS DE {home} (DOMICILE) AVEC STATISTIQUES DÉTAILLÉES :\n"
    last_matches_home = prediction_obj.get("last_matches_home", [])
    if last_matches_home:
        for i, match in enumerate(last_matches_home[:10], 1):
            if isinstance(match, dict) and all(key in match for key in ['date', 'home_team', 'away_team', 'score', 'competition', 'status']):
                date_match = match['date']
                team1 = match['home_team']
                team2 = match['away_team']
                competition = match['competition']
                score = match['score']
                status = match['status']
                game_id = match.get('game_id', 'N/A')
                url = match.get('url', 'N/A')
                
                prompt += f"  {i}. {date_match} | {team1} vs {team2} : {score} [{competition}] ({status}) [ID: {game_id}]\n"
                
                # ✅ NOUVEAU : Ajout des statistiques détaillées du match
                match_stats = match.get('stats', {})
                if match_stats:
                    prompt += f"     📊 Stats détaillées : "
                    for stat_name, (val1, val2) in match_stats.items():
                        prompt += f"{stat_name}: {val1}-{val2} | "
                    prompt += f"\n     🔗 URL: {url}\n"
                else:
                    prompt += f"     📊 Stats détaillées : Non disponibles\n"
    else:
        prompt += "  Aucun match détaillé disponible\n"

    prompt += f"\n📅 10 DERNIERS MATCHS DE {away} (EXTÉRIEUR) AVEC STATISTIQUES DÉTAILLÉES :\n"
    last_matches_away = prediction_obj.get("last_matches_away", [])
    if last_matches_away:
        for i, match in enumerate(last_matches_away[:10], 1):
            if isinstance(match, dict) and all(key in match for key in ['date', 'home_team', 'away_team', 'score', 'competition', 'status']):
                date_match = match['date']
                team1 = match['home_team']
                team2 = match['away_team']
                competition = match['competition']
                score = match['score']
                status = match['status']
                game_id = match.get('game_id', 'N/A')
                url = match.get('url', 'N/A')
                
                prompt += f"  {i}. {date_match} | {team1} vs {team2} : {score} [{competition}] ({status}) [ID: {game_id}]\n"
                
                # ✅ NOUVEAU : Ajout des statistiques détaillées du match
                match_stats = match.get('stats', {})
                if match_stats:
                    prompt += f"     📊 Stats détaillées : "
                    for stat_name, (val1, val2) in match_stats.items():
                        prompt += f"{stat_name}: {val1}-{val2} | "
                    prompt += f"\n     🔗 URL: {url}\n"
                else:
                    prompt += f"     📊 Stats détaillées : Non disponibles\n"
    else:
        prompt += "  Aucun match détaillé disponible\n"

    # ✅ NOUVEAUTÉ 2 : Ajout du classement complet de la ligue
    prompt += "\n🏆 CLASSEMENT COMPLET DE LA LIGUE :\n"
    classement_complet = prediction_obj.get("classement_complet", [])
    if classement_complet:
        for team_data in classement_complet[:20]:  # Limiter à 20 pour éviter un prompt trop long
            position = team_data.get('position', 'N/A')
            team_name = team_data.get('team', 'N/A')
            points = team_data.get('points', 'N/A')
            
            # Marquer les équipes du match en cours
            marker = ""
            if team_name == home:
                marker = " ← DOMICILE"
            elif team_name == away:
                marker = " ← EXTÉRIEUR"
            
            prompt += f"  {position}. {team_name} ({points} pts){marker}\n"
    else:
        prompt += "  Classement complet non disponible\n"

    # ✅ NOUVEAUTÉ 3 : Ajout des confrontations directes H2H (ÉLARGI À TOUS LES CHAMPIONNATS)
    confrontations_h2h = prediction_obj.get("confrontations_saison_derniere", [])
    if confrontations_h2h:
        prompt += f"\n🆚 CONFRONTATIONS DIRECTES (SAISON DERNIÈRE) :\n"
        for i, match in enumerate(confrontations_h2h, 1):
            date_h2h = match.get('date', 'N/A')
            team1_h2h = match.get('team1', 'N/A')
            team2_h2h = match.get('team2', 'N/A')
            score_h2h = match.get('score', 'N/A')
            competition_h2h = match.get('competition', 'N/A')
            source_h2h = match.get('source', 'N/A')
            prompt += f"  {i}. {date_h2h} | {team1_h2h} vs {team2_h2h} : {score_h2h} [{competition_h2h}] (Source: {source_h2h})\n"
    else:
        prompt += f"\n🆚 CONFRONTATIONS DIRECTES (SAISON DERNIÈRE) :\n  Aucune confrontation H2H disponible\n"

    prompt += f"""
MISSION :
1. Analyse comparative des deux équipes (forces/faiblesses)
2. Impact du facteur domicile/extérieur
3. Analyse des formes récentes et tendances à partir des matchs détaillés AVEC LEURS STATISTIQUES
4. Analyse du contexte du championnat grâce au classement complet
5. Prise en compte des confrontations directes récentes (si disponibles)
6. Évaluation des cotes (si disponibles)
7. ✨ NOUVEAU : Analyse approfondie des statistiques détaillées des matchs passés (possession, tirs, corners, etc.)
8. Prédiction finale claire : UNE SEULE recommandation parmi :
   - "Victoire domicile" ({home})
   - "Victoire extérieur" ({away})
   - "Match nul"
   - "Plus de 2.5 buts"
   - "Moins de 2.5 buts"
   - "BTTS oui" (Both Teams To Score)
   - "BTTS non"
   - "Double chance 1X" (domicile ou nul)
   - "Double chance X2" (nul ou extérieur)
   - "Total corners victoire domicile" (équipe domicile aura plus de corners)
   - "Total corners victoire extérieur" (équipe extérieur aura plus de corners)
   - "Tirs cadrés victoire domicile" (équipe domicile aura plus de tirs cadrés)
   - "Tirs cadrés victoire extérieur" (équipe extérieur aura plus de tirs cadrés)

Justifie ta prédiction avec toutes les données statistiques fournies, en tenant compte particulièrement des matchs récents détaillés avec leurs statistiques complètes, du contexte du classement et des confrontations directes.
"""
    return prompt

def get_odds_for_match(sport_odds_id, home_team_api, away_team_api, home_team_espn, away_team_espn):
    if sport_odds_id == "none":
        print(f"⚠️ Pas d'odds_id disponible pour ce championnat")
        return None

    url = f"https://api.the-odds-api.com/v4/sports/{sport_odds_id}/odds"
    params = {
        "apiKey": ODDS_API_KEY,
        "regions": REGION,
        "markets": MARKETS,
        "oddsFormat": "decimal"
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"❌ Erreur API Odds : {response.status_code}")
            return None

        matches = response.json()

        target_match = None
        for match in matches:
            home_odds = match['home_team']
            away_odds = match['away_team']

            if ((home_odds.lower() == home_team_api.lower() or away_odds.lower() == home_team_api.lower()) and 
                (home_odds.lower() == away_team_api.lower() or away_odds.lower() == away_team_api.lower())):
                target_match = match
                print(f"✅ Match trouvé avec noms API : {home_odds} vs {away_odds}")
                break

            if ((home_odds.lower() == home_team_espn.lower() or away_odds.lower() == home_team_espn.lower()) and 
                (home_odds.lower() == away_team_espn.lower() or away_odds.lower() == away_team_espn.lower())):
                target_match = match
                print(f"✅ Match trouvé avec noms ESPN : {home_odds} vs {away_odds}")
                break

        if not target_match:
            print(f"❌ Match non trouvé dans les cotes : {home_team_api} vs {away_team_api}")
            return None

        # ✅ Choix du bookmaker (priorité 1xBet, puis Betclic, sinon premier dispo)
        bookmaker = next((b for b in target_match['bookmakers'] if b['title'].lower() == "1xbet"), None)
        if not bookmaker:
            bookmaker = next((b for b in target_match['bookmakers'] if b['title'].lower() == "betclic"), None)
        if not bookmaker and target_match['bookmakers']:
            bookmaker = target_match['bookmakers'][0]

        if not bookmaker:
            print(f"⚠️ Aucun bookmaker disponible pour ce match")
            return None

        print(f"🏢 Bookmaker utilisé : {bookmaker['title']}")

        odds_data = {
            "bookmaker": bookmaker['title'],
            "h2h": {},
            "totals": {}
        }

        for market in bookmaker['markets']:
            if market['key'] == "h2h":
                print("🎯 Marché : 1X2")
                for outcome in market['outcomes']:
                    odds_data['h2h'][outcome['name']] = outcome['price']
                    print(f"    ➤ {outcome['name']} : Cote {outcome['price']}")
            elif market['key'] == "totals":
                print("🎯 Marché : Total 2.5 (Over/Under)")
                for outcome in market['outcomes']:
                    odds_data['totals'][outcome['name']] = outcome['price']
                    print(f"    ➤ {outcome['name']} : Cote {outcome['price']}")

        return odds_data

    except Exception as e:
        print(f"❌ Erreur lors de la récupération des cotes : {e}")
        return None

# 🔧 Classe réutilisable de scraping de classement (VERSION AMÉLIORÉE)
class ClassementScraper:
    def __init__(self, url):
        self.url = url
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.teams_positions = {}
        self.full_standings = []  # Nouveau : stockage du classement complet

    def scrape_table(self):
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 1. Extraire les noms d'équipes
            team_divs = soup.select('.team-link .hide-mobile a')
            team_names = [tag.text.strip() for tag in team_divs]
            
            # 2. Extraire les points (8e cellule de chaque ligne dans le 2e tableau)
            stat_rows = soup.select('.Table__Scroller .Table__TBODY > tr')
            team_points = []
            
            for row in stat_rows:
                cells = row.find_all("td")
                if len(cells) >= 8:
                    try:
                        points = int(cells[7].text.strip())
                    except ValueError:
                        points = None
                    team_points.append(points)
            
            # 3. Combiner équipes + points et créer le dictionnaire de positions
            teams_data = list(zip(team_names, team_points))
            
            print(f"🏆 Classement extrait de {self.url}:")
            for i, (team, pts) in enumerate(teams_data, start=1):
                if team and pts is not None:
                    self.teams_positions[team.lower()] = (i, team, pts)
                    self.full_standings.append({
                        "position": i,
                        "team": team,
                        "points": pts
                    })
                    print(f"  {i}. {team}: {pts} points")

        except Exception as e:
            print(f"❌ Erreur scraping classement : {e}")

    def get_position(self, team_query):
        # Utiliser le mapping pour convertir le nom API vers le nom ESPN
        mapped_team_name = team_name_mapping.get(team_query, team_query)
        
        # Recherche exacte d'abord
        if mapped_team_name.lower() in self.teams_positions:
            return self.teams_positions[mapped_team_name.lower()]
        
        # Recherche partielle ensuite
        for key, (position, full_name, points) in self.teams_positions.items():
            if mapped_team_name.lower() in key or key in mapped_team_name.lower():
                return position, full_name, points
        return None, None, None

    def get_full_standings(self):
        """Retourne le classement complet"""
        return self.full_standings

# 🧠 Fonction utilitaire get_team_classement_position (modifiée pour retourner le classement complet)
def get_team_classement_position(country, league, team_name):
    league_info = classement_ligue_mapping.get(country, {}).get(league)
    if not league_info:
        print(f"⚠️ Informations de ligue introuvables pour {country} - {league}")
        return None, None, None, []
    
    url = league_info["url"]
    odds_id = league_info["odds_id"]
    
    print(f"🔍 Recherche classement pour {team_name} dans {country} - {league} (odds_id: {odds_id})")
    scraper = ClassementScraper(url)
    scraper.scrape_table()
    
    # Utiliser le mapping pour convertir le nom API vers le nom ESPN
    mapped_team_name = team_name_mapping.get(team_name, team_name)
    position, full_name, points = scraper.get_position(mapped_team_name)
    full_standings = scraper.get_full_standings()
    
    if position:
        print(f"✅ {full_name} trouvé à la position {position} avec {points} points")
    else:
        print(f"❌ {team_name} (mappé: {mapped_team_name}) non trouvé dans le classement")
    
    return position, full_name, points, full_standings

def get_espn_name(api_team_name):
    mapped = team_name_mapping.get(api_team_name, api_team_name)
    if mapped != api_team_name:
        print(f"🔄 Mapping appliqué: '{api_team_name}' → '{mapped}'")
    return mapped

def format_date_fr(date_str, time_str):
    try:
        dt = datetime.strptime(date_str + " " + time_str, "%Y-%m-%d %H:%M")
        mois_fr = [
            "", "janvier", "février", "mars", "avril", "mai", "juin",
            "juillet", "août", "septembre", "octobre", "novembre", "décembre"
        ]
        mois = mois_fr[dt.month]
        return f"{dt.day} {mois} {dt.year} à {dt.strftime('%H:%M:%S')} UTC"
    except Exception as e:
        return f"{date_str} à {time_str}:00 UTC"

# 🆚 Fonction pour récupérer les confrontations directes de la saison passée (ÉLARGIE À TOUS LES CHAMPIONNATS)
def get_h2h_confrontations(home_team_espn, away_team_espn):
    """
    Récupère les confrontations directes de la saison passée depuis plusieurs fichiers JSON
    (Premier League, La Liga, Bundesliga, etc.)
    """
    fichiers_h2h = [
        {"file": "P_league.json", "name": "Premier League"},
        {"file": "laliga.json", "name": "La Liga"},
        {"file": "bundesliga.json", "name": "Bundesliga"}
    ]
    
    confrontations = []
    
    for fichier_info in fichiers_h2h:
        fichier = fichier_info["file"]
        nom_championnat = fichier_info["name"]
        
        if not os.path.exists(fichier):
            print(f"⚠️ Fichier {fichier} ({nom_championnat}) non trouvé")
            continue
        
        try:
            with open(fichier, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            matchs_trouvés = 0
            # Parcourir tous les matchs dans le fichier JSON
            for match in data:
                team1 = match.get("team1", "")
                team2 = match.get("team2", "")
                
                # Vérifier si les deux équipes correspondent (dans un sens ou l'autre)
                if ((team1 == home_team_espn and team2 == away_team_espn) or 
                    (team1 == away_team_espn and team2 == home_team_espn)):
                    match["source"] = nom_championnat  # Ajouter la source du championnat
                    confrontations.append(match)
                    matchs_trouvés += 1
            
            if matchs_trouvés > 0:
                print(f"🆚 {matchs_trouvés} confrontation(s) trouvée(s) dans {nom_championnat}")
        
        except Exception as e:
            print(f"❌ Erreur lors de la lecture de {fichier} ({nom_championnat}) : {e}")
    
    print(f"🆚 Total : {len(confrontations)} confrontation(s) directe(s) trouvée(s) pour {home_team_espn} vs {away_team_espn}")
    return confrontations

def get_today_matches_filtered():
    today = datetime.now().strftime('%Y-%m-%d')
    url = "https://v3.football.api-sports.io/fixtures"
    params = {
        "date": today,
        "timezone": "Africa/Abidjan"
    }
    allowed_league_ids = [72, 265, 281, 218, 113, 129, 250, 252, 299, 283, 43, 239, 61, 144, 39, 88, 94, 140, 197, 203, 98, 383, 207, 169, 235, 262, 307, 71, 253, 78, 135]
    résultats = []
    try:
        response = requests.get(url, headers=api_headers, params=params)
        response.raise_for_status()
        data = response.json()
        print(f"\n📅 Matchs du jour ({today}) :\n")
        for match in data.get("response", []):
            league_id = match['league']['id']
            league = match['league']['name']
            country = match['league']['country']
            home_api = match['teams']['home']['name']
            away_api = match['teams']['away']['name']
            logo_home = match['teams']['home']['logo']
            logo_away = match['teams']['away']['logo']
            time = match['fixture']['date'][11:16]
            date = match['fixture']['date'][:10]
            heure, minute = map(int, time.split(":"))
            if heure < 8:
                continue

            if league_id in allowed_league_ids:
                print(f"🏆 [{country}] {league} : {home_api} vs {away_api} à {time}")
                # Utiliser le mapping pour les noms ESPN
                home_espn = get_espn_name(home_api)
                away_espn = get_espn_name(away_api)
                
                if home_espn in teams_urls and away_espn in teams_urls:
                    print(f"\n🔎 Analyse automatique pour : {home_espn} & {away_espn}")
                    team1_stats = process_team(home_api, return_data=True)
                    team2_stats = process_team(away_api, return_data=True)
                    if team1_stats: team1_stats['nom'] = home_espn
                    if team2_stats: team2_stats['nom'] = away_espn
                    compare_teams_basic_stats(
                        team1_stats, team2_stats, home_api, away_api, date, time, league, country,
                        logo_home=logo_home, logo_away=logo_away, résultats=résultats
                    )
                else:
                    if home_espn in teams_urls:
                        process_team(home_api)
                    else:
                        FAILED_TEAMS.add(home_api)
                    if away_espn in teams_urls:
                        process_team(away_api)
                    else:
                        FAILED_TEAMS.add(away_api)
        
        # ✅ CORRECTION 1 : Récupérer le chemin retourné par sauvegarder_stats_brutes_json
        if résultats:
            chemin = sauvegarder_stats_brutes_json(résultats, today)  # ✅ Récupérer le chemin
            git_commit_and_push(chemin)  # ✅ Utiliser le bon chemin
        
        if FAILED_TEAMS:
            save_failed_teams_json(FAILED_TEAMS, today)
        if IGNORED_ZERO_FORM_TEAMS:
            save_ignored_teams_json(IGNORED_ZERO_FORM_TEAMS, today)
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des matchs : {e}")

def get_match_result_for_team(team_name, score, team1, team2):
    try:
        home_score, away_score = map(int, score.split(' - '))
    except Exception:
        return None
    
    # Utiliser le mapping pour comparer correctement
    mapped_team_name = team_name_mapping.get(team_name, team_name)
    mapped_team1 = team_name_mapping.get(team1, team1)
    mapped_team2 = team_name_mapping.get(team2, team2)
    
    if mapped_team_name == mapped_team1:
        return 'W' if home_score > away_score else 'D' if home_score == away_score else 'L'
    elif mapped_team_name == mapped_team2:
        return 'W' if away_score > home_score else 'D' if away_score == home_score else 'L'
    return None

def extract_goals(team_name, score, team1, team2):
    try:
        home_score, away_score = map(int, score.split(' - '))
    except Exception:
        return None, None, None
    
    # Utiliser le mapping pour comparer correctement
    mapped_team_name = team_name_mapping.get(team_name, team_name)
    mapped_team1 = team_name_mapping.get(team1, team1)
    mapped_team2 = team_name_mapping.get(team2, team2)
    
    if mapped_team_name == mapped_team1:
        return home_score, away_score, True
    elif mapped_team_name == mapped_team2:
        return away_score, home_score, False
    return None, None, None

def get_form_points(recent_form):
    points_map = {'W': 3, 'D': 1, 'L': 0}
    total = sum(points_map.get(r, 0) for r in recent_form)
    return total

def scrape_team_data(team_name, action):
    espn_team_name = get_espn_name(team_name)
    url = teams_urls.get(espn_team_name, {}).get(action)
    if not url:
        print(f"URL non trouvée pour {espn_team_name} et action {action}.")
        FAILED_TEAMS.add(team_name)
        return []
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        matches = soup.find_all('tr', class_='Table__TR')
        
        # ✅ NOUVELLE STRUCTURE - Objet au lieu de liste
        valid_results = []
        form_6 = []
        form_10 = []
        buts_dom_marques = 0
        buts_dom_encaisses = 0
        buts_ext_marques = 0
        buts_ext_encaisses = 0

        # 🏗️ Initialisation des séries domicile/extérieur
        serie_domicile = []
        serie_exterieur = []

        for match in matches:
            # Date
            date_tag = match.find('div', class_='matchTeams')
            date_text = date_tag.text.strip() if date_tag else "N/A"

            # Équipes
            teams = match.find_all('a', class_='AnchorLink Table__Team')
            team1 = teams[0].text.strip() if len(teams) > 0 else "N/A"
            team2 = teams[1].text.strip() if len(teams) > 1 else "N/A"

            # Compétition
            comp_tags = match.find_all('a', class_='AnchorLink')
            competition = comp_tags[1].text.strip() if len(comp_tags) > 1 else "N/A"

            # Score + Game ID (via l'URL du match)
            score_tag = match.find('a', href=lambda x: x and "gameId" in x)
            score = score_tag.text.strip() if score_tag else "N/A"
            game_id = "N/A"
            if score_tag and score_tag.get('href') and "gameId" in score_tag['href']:
                try:
                    game_id = score_tag['href'].split("gameId/")[1].split("/")[0]
                except:
                    game_id = "N/A"

            # Statut (FT, Postponed…) - essayer plusieurs sélecteurs
            status = "N/A"
            status_tag = match.find('span', {"data-testid": "result"})
            if not status_tag:
                # Fallback - chercher dans les derniers liens
                last_links = match.find_all('a', class_='AnchorLink')
                if last_links:
                    status = last_links[-1].text.strip()
            else:
                status = status_tag.text.strip()

            # Si toutes les infos clés sont présentes, créer l'objet match
            if all(val != "N/A" for val in [date_text, team1, team2, score]):
                match_obj = {
                    "game_id": game_id,
                    "date": date_text,
                    "home_team": team1,
                    "away_team": team2,
                    "score": score,
                    "status": status,
                    "competition": competition
                }

                # ✅ NOUVEAU : Enrichir avec les statistiques détaillées si game_id disponible
                if game_id != "N/A":
                    print(f"🔍 Récupération des stats détaillées pour le match {game_id}...")
                    match_stats = get_match_stats(game_id)
                    match_obj["stats"] = match_stats
                    match_obj["url"] = f"https://africa.espn.com/football/match/_/gameId/{game_id}"
                else:
                    match_obj["stats"] = {}
                    match_obj["url"] = "N/A"

                valid_results.append(match_obj)
                
                # Calculer les formes et stats avec la nouvelle structure
                result = get_match_result_for_team(espn_team_name, score, team1, team2)
                if result:
                    form_10.append(result)
                    if len(form_6) < 6:
                        form_6.append(result)

                    # 🔄 Ajout dans la bonne série - utiliser le mapping
                    mapped_team1 = team_name_mapping.get(team1, team1)
                    mapped_espn_name = team_name_mapping.get(espn_team_name, espn_team_name)
                    is_home = (mapped_team1 == mapped_espn_name)
                    if is_home:
                        serie_domicile.append(result)
                    else:
                        serie_exterieur.append(result)

                buts_m, buts_e, domicile = extract_goals(espn_team_name, score, team1, team2)
                if buts_m is not None and buts_e is not None:
                    if domicile:
                        buts_dom_marques += buts_m
                        buts_dom_encaisses += buts_e
                    else:
                        buts_ext_marques += buts_m
                        buts_ext_encaisses += buts_e
            
            if len(valid_results) >= 10:
                break
        
        nb_matchs = len(valid_results)
        if nb_matchs == 0:
            print("Aucun match trouvé.")
            FAILED_TEAMS.add(team_name)
            return []
        
        total_marques = buts_dom_marques + buts_ext_marques
        total_encaisses = buts_dom_encaisses + buts_ext_encaisses
        
        print(f"\n🗓️ {action.capitalize()} pour {espn_team_name} :")
        for match_obj in valid_results:
            print(f"ID: {match_obj['game_id']} | {match_obj['date']} | {match_obj['home_team']} vs {match_obj['away_team']} : {match_obj['score']} [{match_obj['competition']}] ({match_obj['status']})")
            # ✅ Afficher les stats si disponibles
            if match_obj.get('stats'):
                print(f"  📊 Stats: {len(match_obj['stats'])} statistiques récupérées")
                for stat_name, (val1, val2) in list(match_obj['stats'].items())[:3]:  # Afficher les 3 premières
                    print(f"    - {stat_name}: {val1} - {val2}")
                if len(match_obj['stats']) > 3:
                    print(f"    - ... et {len(match_obj['stats']) - 3} autres stats")
        
        total_points_6 = get_form_points(form_6)
        total_points_10 = get_form_points(form_10[:10])  # sécurité si <10
        
        print(f"\n📊 Forme courte (6 derniers matchs) : {' '.join(form_6)} (Total points : {total_points_6})")
        print(f"📊 Forme longue (10 derniers matchs) : {' '.join(form_10[:10])} (Total points : {total_points_10})")
        print(f"⚽ Buts marqués à domicile : {buts_dom_marques}")
        print(f"⚽ Buts encaissés à domicile : {buts_dom_encaisses}")
        print(f"⚽ Buts marqués à l'extérieur : {buts_ext_marques}")
        print(f"⚽ Buts encaissés à l'extérieur : {buts_ext_encaisses}")
        print(f"⚽ Total buts marqués : {total_marques}")
        print(f"🛡️ Total buts encaissés : {total_encaisses}")
        print(f"\n📈 Moyenne buts marqués par match : {total_marques / nb_matchs:.2f}")
        print(f"📉 Moyenne buts encaissés par match : {total_encaisses / nb_matchs:.2f}")

        # 💡 Affichage des séries
        print(f"🏠 Série domicile : {'-'.join(serie_domicile)}")
        print(f"✈️ Série extérieur : {'-'.join(serie_exterieur)}")

        return {
            "matches": valid_results,  # ✅ Maintenant c'est une liste d'objets avec nouvelle structure + STATS DÉTAILLÉES
            "moyenne_marques": total_marques / nb_matchs,
            "moyenne_encaisses": total_encaisses / nb_matchs,
            "form_6": form_6,
            "form_10": form_10[:10],
            "recent_form": form_6,  # compatibilité avec l'ancien code
            "serie_domicile": serie_domicile,
            "serie_exterieur": serie_exterieur,
            "buts_dom_marques": buts_dom_marques,
            "buts_dom_encaisses": buts_dom_encaisses,
            "buts_ext_marques": buts_ext_marques,
            "buts_ext_encaisses": buts_ext_encaisses,
            "total_marques": total_marques,
            "total_encaisses": total_encaisses,
            "total_points_6": total_points_6,
            "total_points_10": total_points_10,
            "total_points": total_points_6  # compatibilité avec l'ancien code
        }
    except Exception as e:
        print(f"Erreur scraping {espn_team_name} ({action}) : {e}")
        FAILED_TEAMS.add(team_name)
        return []

def compare_teams_basic_stats(
    t1, t2, name1, name2, match_date="N/A", match_time="N/A",
    league="N/A", country="N/A", logo_home=None, logo_away=None, résultats=None
):
    if not t1 or not t2:
        print("⚠️ Données insuffisantes pour la comparaison.")
        return

    # Vérifier si une équipe a une forme récente totalement vide (0 point)
    points1 = get_form_points(t1.get('form_6', []))
    points2 = get_form_points(t2.get('form_6', []))

    if points1 == 0:
        print(f"🚫 {name1} a une forme totalement vide (0 point), match ignoré.")
        IGNORED_ZERO_FORM_TEAMS.append(name1)
        return
    if points2 == 0:
        print(f"🚫 {name2} a une forme totalement vide (0 point), match ignoré.")
        IGNORED_ZERO_FORM_TEAMS.append(name2)
        return

    # 🏆 Récupération classement des équipes - utiliser le mapping (modifié pour récupérer le classement complet)
    pos_home, nom_classement_home, pts_home, full_standings_home = get_team_classement_position(country, league, name1)
    pos_away, nom_classement_away, pts_away, full_standings_away = get_team_classement_position(country, league, name2)

    if pos_home:
        print(f"📌 Classement de {nom_classement_home} : {pos_home}ᵉ avec {pts_home} points")
    if pos_away:
        print(f"📌 Classement de {nom_classement_away} : {pos_away}ᵉ avec {pts_away} points")

    # 💰 Récupération des cotes
    print(f"\n💰 Récupération des cotes...")
    home_espn = get_espn_name(name1)
    away_espn = get_espn_name(name2)
    
    league_info = classement_ligue_mapping.get(country, {}).get(league)
    odds_id = league_info.get("odds_id", "none") if league_info else "none"
    
    odds_data = get_odds_for_match(odds_id, name1, name2, home_espn, away_espn)

    # 🆚 Récupération des confrontations directes (ÉLARGI À TOUS LES CHAMPIONNATS)
    confrontations_h2h = get_h2h_confrontations(home_espn, away_espn)

    print(f"\n📅 Match prévu le {match_date} à {match_time}")
    print(f"🏆 Compétition : [{country}] {league}")
    print(f"⚔️ {name1} vs {name2}")
    
    print(f"\n🤝 Statistiques brutes :")
    print(f"{name1} ➤ Moy. buts marqués : {t1['moyenne_marques']:.2f} | Moy. encaissés : {t1['moyenne_encaisses']:.2f}")
    print(f"{name2} ➤ Moy. buts marqués : {t2['moyenne_marques']:.2f} | Moy. encaissés : {t2['moyenne_encaisses']:.2f}")

    print(f"\n📊 Forme courte (6) : {' '.join(t1['form_6'])} ({name1}) vs {' '.join(t2['form_6'])} ({name2})")
    print(f"📊 Forme longue (10) : {' '.join(t1['form_10'])} ({name1}) vs {' '.join(t2['form_10'])} ({name2})")

    print(f"🏠 Série domicile ({name1}) : {'-'.join(t1.get('serie_domicile', []))}")
    print(f"✈️ Série extérieur ({name2}) : {'-'.join(t2.get('serie_exterieur', []))}")

    # ✅ CRÉATION DE L'OBJET AVEC NOUVELLE STRUCTURE DES MATCHS + STATS DÉTAILLÉES
    prediction_obj = {
        "id": len(PREDICTIONS) + 1,
        "HomeTeam": name1,
        "AwayTeam": name2,
        "date": format_date_fr(match_date, match_time),
        "league": f"{country} - {league}",
        "type": "stats_brutes_avec_cotes_et_ia_avec_stats_detaillees",
        "odds": odds_data,  # Cotes des bookmakers
        "stats_home": {
            "moyenne_marques": t1['moyenne_marques'],
            "moyenne_encaisses": t1['moyenne_encaisses'],
            "form_6": t1['form_6'],
            "form_10": t1['form_10'],
            "recent_form": t1['form_6'],  # compatibilité
            "total_points_6": t1.get('total_points_6', 0),
            "total_points_10": t1.get('total_points_10', 0),
            "total_points": t1.get('total_points_6', 0),  # compatibilité
            "serie_domicile": t1.get('serie_domicile', []),
            "buts_dom_marques": t1.get('buts_dom_marques', 0),
            "buts_dom_encaisses": t1.get('buts_dom_encaisses', 0),
            "buts_ext_marques": t1.get('buts_ext_marques', 0),
            "buts_ext_encaisses": t1.get('buts_ext_encaisses', 0),
            "total_marques": t1.get('total_marques', 0),
            "total_encaisses": t1.get('total_encaisses', 0)
        },
        "stats_away": {
            "moyenne_marques": t2['moyenne_marques'],
            "moyenne_encaisses": t2['moyenne_encaisses'],
            "form_6": t2['form_6'],
            "form_10": t2['form_10'],
            "recent_form": t2['form_6'],  # compatibilité
            "total_points_6": t2.get('total_points_6', 0),
            "total_points_10": t2.get('total_points_10', 0),
            "total_points": t2.get('total_points_6', 0),  # compatibilité
            "serie_exterieur": t2.get('serie_exterieur', []),
            "buts_dom_marques": t2.get('buts_dom_marques', 0),
            "buts_dom_encaisses": t2.get('buts_dom_encaisses', 0),
            "buts_ext_marques": t2.get('buts_ext_marques', 0),
            "buts_ext_encaisses": t2.get('buts_ext_encaisses', 0),
            "total_marques": t2.get('total_marques', 0),
            "total_encaisses": t2.get('total_encaisses', 0)
        },
        # ✅ NOUVEAUX CHAMPS : MATCHS COMPLETS AVEC NOUVELLE STRUCTURE + STATS DÉTAILLÉES
        "last_matches_home": t1.get('matches', []),  # Les 10 vrais matchs avec objets + STATS DÉTAILLÉES
        "last_matches_away": t2.get('matches', []),  # Les 10 vrais matchs avec objets + STATS DÉTAILLÉES
        # ✅ CLASSEMENT DES ÉQUIPES
        "classement": {
            name1: {"position": pos_home, "points": pts_home} if pos_home else None,
            name2: {"position": pos_away, "points": pts_away} if pos_away else None
        },
        # ✅ CLASSEMENT COMPLET DE LA LIGUE
        "classement_complet": full_standings_home if full_standings_home else full_standings_away,
        # ✅ CONFRONTATIONS DIRECTES (ÉLARGI À TOUS LES CHAMPIONNATS)
        "confrontations_saison_derniere": confrontations_h2h,
        # Anciens champs conservés pour compatibilité
        "logo_home": logo_home,
        "logo_away": logo_away,
        "classement_home": pos_home,
        "classement_away": pos_away,
        "points_classement_home": pts_home,
        "points_classement_away": pts_away,
        "nom_classement_home": nom_classement_home,
        "nom_classement_away": nom_classement_away,
        "country_fr": f"{country} - {league}"
    }

    # 🔮 Génération d'analyse IA avec DeepSeek (AVEC RETRY AUTOMATIQUE + STATS DÉTAILLÉES)
    print(f"\n🧠 Lancement de l'analyse IA DeepSeek avec retry automatique + stats détaillées...")
    prompt = generate_detailed_prompt(prediction_obj)
    analyse_ia = call_deepseek_analysis(prompt, max_retries=10)  # ✅ 10 tentatives max

    prediction_obj["analyse_ia"] = analyse_ia
    print(f"\n🧠 Analyse IA DeepSeek :\n{'='*60}")
    print(analyse_ia)
    print(f"{'='*60}\n")

    PREDICTIONS.append(prediction_obj)
    if résultats is not None:
        résultats.append(prediction_obj)

    print("\n📚 Note : Statistiques brutes avec cotes + analyse IA DeepSeek avec retry + matchs complets avec stats détaillées + classement complet + H2H élargi.")

def process_team(team_name, return_data=False):
    print(f"\n🧠 Analyse pour l'équipe : {get_espn_name(team_name)}")
    data = scrape_team_data(team_name, 'results')
    print("\n" + "-" * 60 + "\n")
    return data if return_data else None

def sauvegarder_stats_brutes_json(predictions_simples, date_str):
    total_predictions = len(predictions_simples)

    for p in predictions_simples:
        p['country_fr'] = p['league']

    data_complete = {
        "metadata": {
            "date_generation": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "date_matchs": date_str,
            "version_algorithme": "7.5 - STATISTIQUES BRUTES + FORMES 6/10 + POINTS CLASSEMENT + COTES + ANALYSE IA DEEPSEEK ENRICHIE + MATCHS COMPLETS AVEC STATS DÉTAILLÉES + CLASSEMENT COMPLET + H2H ÉLARGI + 10 RETRY IA + NOUVELLES PRÉDICTIONS",
            "total_predictions": total_predictions,
            "mode": "stats_brutes_avec_cotes_et_ia_complete_enrichie_retry_nouvelle_structure_avec_stats_detaillees_10_retry",
            "note": "Collecte des statistiques brutes complètes : moyennes, formes récentes (6 et 10 matchs), séries domicile/extérieur, classements avec points + cotes des bookmakers + analyse IA DeepSeek ENRICHIE avec matchs détaillés (nouvelle structure objet avec game_id, date, home_team, away_team, score, status, competition + STATS DÉTAILLÉES ESPN) + classement complet + confrontations directes H2H élargies + 10 retry automatique IA avec pause 5s + nouvelles prédictions corners et tirs cadrés",
            "ia_model": "deepseek-r1-distill-llama-70b",
            "groq_keys_count": len(groq_keys),
            "retry_config": {
                "max_retries": 10,
                "retry_delay_seconds": 5
            },
            "nouvelles_predictions": [
                "Total corners victoire domicile",
                "Total corners victoire extérieur", 
                "Tirs cadrés victoire domicile",
                "Tirs cadrés victoire extérieur"
            ],
            "nouveautes_v7_5": [
                "Augmentation du nombre de retry de 5 à 10 tentatives",
                "Pause de 5 secondes entre chaque retry au lieu de 2",
                "Ajout de 4 nouvelles prédictions possibles : corners et tirs cadrés par équipe",
                "Nom de fichier simplifié : prédiction-YYYY-MM-DD-analyse-ia.json"
            ]
        },
        "statistiques_brutes_avec_ia": {
            "count": len(predictions_simples),
            "details": predictions_simples
        }
    }
    
    # ✅ Nouveau nom de fichier simplifié
    chemin = f"prédiction-{date_str}-analyse-ia.json"
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(data_complete, f, ensure_ascii=False, indent=2)
    print(f"✅ Statistiques brutes complètes avec cotes et analyse IA enrichie + stats détaillées sauvegardées dans : {chemin}")
    print(f"📊 Total: {total_predictions} analyses complètes avec cotes + IA DeepSeek enrichie + 10 retry + H2H élargi + stats détaillées ESPN + nouvelles prédictions")
    
    return chemin

def save_failed_teams_json(failed_teams, date_str):
    chemin = f"teams_failed_{date_str}.json"
    data = {"teams_failed": sorted(list(failed_teams))}
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"❗ Liste des équipes sans données sauvegardée dans : {chemin}")

def save_ignored_teams_json(ignored_teams, date_str):
    chemin = f"teams_ignored_zero_form_{date_str}.json"
    data = {"teams_ignored_zero_form": sorted(list(set(ignored_teams)))}
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"🛑 Équipes ignorées pour forme nulle sauvegardées dans : {chemin}")

def git_commit_and_push(filepath):
    try:
        subprocess.run(["git", "config", "--global", "user.email", "github-actions[bot]@users.noreply.github.com"], check=True)
        subprocess.run(["git", "config", "--global", "user.name", "github-actions[bot]"], check=True)
        subprocess.run(["git", "add", filepath], check=True)
        subprocess.run(["git", "commit", "-m", f"📊 Statistiques brutes complètes du {datetime.now().strftime('%Y-%m-%d')} - Version 7.5 STATS BRUTES + FORMES 6/10 + POINTS CLASSEMENT + COTES + ANALYSE IA DEEPSEEK ENRICHIE + MATCHS COMPLETS AVEC STATS DÉTAILLÉES ESPN + CLASSEMENT COMPLET + H2H ÉLARGI + 10 RETRY IA + NOUVELLES PRÉDICTIONS CORNERS/TIRS"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("✅ Statistiques brutes complètes avec cotes et analyse IA enrichie + stats détaillées ESPN poussées avec succès sur GitHub.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur Git : {e}")

def main():
    print("📊 Bienvenue dans l'analyse v7.5 : STATISTIQUES BRUTES COMPLÈTES + ANALYSE IA DEEPSEEK ENRICHIE + 10 RETRY + H2H ÉLARGI + STATS DÉTAILLÉES ESPN + NOUVELLES PRÉDICTIONS !")
    print("🧹 Toutes les fonctionnalités d'analyse avancée ont été supprimées")
    print("📈 Collecte complète des statistiques brutes :")
    print("   - Moyennes buts marqués/encaissés")
    print("   - Forme récente (6 derniers matchs)")
    print("   - Forme longue (10 derniers matchs)")
    print("   - Séries domicile/extérieur")
    print("   - Classements des équipes avec points")
    print("   - Points de forme (6 et 10 matchs)")
    print("   💰 - Cotes des bookmakers (1xBet prioritaire, puis Betclic)")
    print("   🧠 - Analyse IA DeepSeek ENRICHIE avec alternance automatique des clés Groq")
    print("   🔄 - Retry automatique (10 tentatives avec pause 5s) si l'IA échoue")
    print("   📋 - 10 vrais matchs complets avec structure objet (game_id, date, home_team, away_team, score, status, competition)")
    print("   📊 - ✨ NOUVEAU : Statistiques détaillées ESPN pour chaque match passé (possession, tirs, corners, etc.)")
    print("   🏆 - Classement complet de la ligue")
    print("   🆚 - Confrontations directes H2H élargies (P_league.json, laliga.json, bundesliga.json)")
    print("   ✨ - Prompt IA enrichi avec toutes ces données détaillées + statistiques ESPN des matchs")
    print("   🎯 - ✨ NOUVELLES PRÉDICTIONS : Total corners victoire domicile/extérieur, Tirs cadrés victoire domicile/extérieur")
    print("🚫 Aucun ajustement, bonus, malus")
    print("🔮 Prédictions basées sur l'analyse IA DeepSeek enrichie avec 10 retry automatique + stats détaillées + nouvelles prédictions")
    print("🔄 Mapping automatique des noms d'équipes conservé")
    print("🛑 Filtrage automatique des équipes avec forme nulle conservé")
    print("📄 Nom de fichier simplifié : prédiction-YYYY-MM-DD-analyse-ia.json")
    print("📊 Analyse pure et complète des statistiques brutes + IA enrichie + 10 retry + H2H élargi + stats détaillées ESPN + nouvelles prédictions des matchs du jour...\n")
    get_today_matches_filtered()
    print(f"\n📋 Résumé de la session:")
    print(f"   📊 {len(PREDICTIONS)} analyses complètes de statistiques brutes avec cotes et IA enrichie + stats détaillées ESPN générées")
    print(f"   🧠 Analyse IA DeepSeek ENRICHIE avec 10 retry automatique (pause 5s) intégrée")
    print(f"   🔑 {len(groq_keys)} clés Groq disponibles")
    print(f"   📋 Matchs complets avec nouvelle structure objet et classements complets intégrés dans le prompt IA")
    print(f"   📊 ✨ NOUVEAU : Statistiques détaillées ESPN récupérées pour chaque match passé")
    print(f"   🆚 Confrontations H2H élargies (Premier League, La Liga, Bundesliga) disponibles dans le prompt IA")
    print(f"   🔄 Système de retry automatique (10 tentatives avec pause 5s) pour garantir les analyses IA")
    print(f"   ✅ Structure objet des matchs passés avec game_id, date, home_team, away_team, score, status, competition + STATS DÉTAILLÉES")
    print(f"   🎯 ✨ NOUVELLES PRÉDICTIONS : Total corners et tirs cadrés par équipe disponibles")
    print(f"   📄 Fichier généré : prédiction-YYYY-MM-DD-analyse-ia.json")
    if IGNORED_ZERO_FORM_TEAMS:
        print(f"   🚫 {len(set(IGNORED_ZERO_FORM_TEAMS))} équipes ignorées pour forme nulle")
    print("\n✨ Merci d'avoir utilisé le script v7.5 - Statistiques brutes complètes avec cotes et IA DeepSeek enrichie + 10 retry + H2H élargi + stats détaillées ESPN + nouvelles prédictions !")

if __name__ == "__main__":
    main()
