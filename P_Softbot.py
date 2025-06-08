import requests
from datetime import datetime
from bs4 import BeautifulSoup
import json
import locale
import subprocess  # AJOUT pour GitHub Actions

API_KEY = '1933761904aae9724ca6497102b2e094'

api_headers = {
    'x-apisports-key': API_KEY
}

teams_urls = {
  "AFC Bournemouth": {
    "results": "https://www.espn.com/soccer/team/results/_/id/349/afc-bournemouth"
  },
  "Arsenal": {
    "results": "https://www.espn.com/soccer/team/results/_/id/359/arsenal"
  },
  "France": {
    "results": "https://www.espn.com/soccer/team/results/_/id/478/france"
  },
  "Portugal": {
    "results": "https://www.espn.com/soccer/team/results/_/id/482/portugal"
  },
  "Germany": {
    "results": "https://www.espn.com/soccer/team/results/_/id/481/germany"
  },
  "Spain": {
    "results": "https://www.espn.com/soccer/team/results/_/id/164/spain"
  },
  "Wales": {
    "results": "https://www.espn.com/soccer/team/results/_/id/578/wales"
  },
  "Turkey": {
    "results": "https://www.espn.com/soccer/team/results/_/id/465/turkey"
  },
  "Ukraine": {
    "results": "https://www.espn.com/soccer/team/results/_/id/457/ukraine"
  },
  "Sweden": {
    "results": "https://www.espn.com/soccer/team/results/_/id/466/sweden"
  },
  "Switzerland": {
    "results": "https://www.espn.com/soccer/team/results/_/id/475/switzerland"
  },
  "Slovenia": {
    "results": "https://www.espn.com/soccer/team/results/_/id/472/slovenia"
  },
  "Slovakia": {
    "results": "https://www.espn.com/soccer/team/results/_/id/468/slovakia"
  },
  "Scotland": {
    "results": "https://www.espn.com/soccer/team/results/_/id/580/scotland"
  },
  "Serbia": {
    "results": "https://www.espn.com/soccer/team/results/_/id/6757/serbia"
  },
  "Romania": {
    "results": "https://www.espn.com/soccer/team/results/_/id/473/romania"
  },
  "Rep. Of Ireland": {
    "results": "https://www.espn.com/soccer/team/results/_/id/476/republic-of-ireland"
  },
  "Norway": {
    "results": "https://www.espn.com/soccer/team/results/_/id/464/norway"
  },
  "Poland": {
    "results": "https://www.espn.com/soccer/team/results/_/id/471/poland"
  },
  "Northern Ireland": {
    "results": "https://www.espn.com/soccer/team/results/_/id/586/northern-ireland"
  },
  "Netherlands": {
    "results": "https://www.espn.com/soccer/team/results/_/id/449/netherlands"
  },
  "North Macedonia": {
    "results": "https://www.espn.com/soccer/team/results/_/id/463/north-macedonia"
  },
  "Montenegro": {
    "results": "https://www.espn.com/soccer/team/results/_/id/6775/montenegro"
  },
  "Moldova": {
    "results": "https://www.espn.com/soccer/team/results/_/id/483/moldova"
  },
  "Latvia": {
    "results": "https://www.espn.com/soccer/team/results/_/id/456/latvia"
  },
  "Kazakhstan": {
    "results": "https://www.espn.com/soccer/team/results/_/id/2619/kazakhstan"
  },
  "Kosovo": {
    "results": "https://www.espn.com/soccer/team/results/_/id/18272/kosovo"
  },
  "Italy": {
    "results": "https://www.espn.com/soccer/team/results/_/id/162/italy"
  },
  "Israel": {
    "results": "https://www.espn.com/soccer/team/results/_/id/461/israel"
  },
  "Malta": {
    "results": "https://www.espn.com/soccer/team/results/_/id/453/malta"
  },
  "Luxembourg": {
    "results": "https://www.espn.com/soccer/team/results/_/id/582/luxembourg"
  },
  "Lithuania": {
    "results": "https://www.espn.com/soccer/team/results/_/id/460/lithuania"
  },
  "Iceland": {
    "results": "https://www.espn.com/soccer/team/results/_/id/470/iceland"
  },
  "Hungary": {
    "results": "https://www.espn.com/soccer/team/results/_/id/480/hungary"
  },
  "Greece": {
    "results": "https://www.espn.com/soccer/team/results/_/id/455/greece"
  },
  "Gibraltar": {
    "results": "https://www.espn.com/soccer/team/results/_/id/16721/gibraltar"
  },
  "Finland": {
    "results": "https://www.espn.com/soccer/team/results/_/id/458/finland"
  },
  "Faroe Islands": {
    "results": "https://www.espn.com/soccer/team/results/_/id/447/faroe-islands"
  },
  "Estonia": {
    "results": "https://www.espn.com/soccer/team/results/_/id/444/estonia"
  },
  "England": {
    "results": "https://www.espn.com/soccer/team/results/_/id/448/england"
  },
  "Denmark": {
    "results": "https://www.espn.com/soccer/team/results/_/id/479/denmark"
  },
  "Czechia": {
    "results": "https://www.espn.com/soccer/team/results/_/id/450/czechia"
  },
  "Cyprus": {
    "results": "https://www.espn.com/soccer/team/results/_/id/445/cyprus"
  },
  "Croatia": {
    "results": "https://www.espn.com/soccer/team/results/_/id/477/croatia"
  },
  "Bulgaria": {
    "results": "https://www.espn.com/soccer/team/results/_/id/462/bulgaria"
  },
  "Bosnia and Herzegovina": {
    "results": "https://www.espn.com/soccer/team/results/_/id/452/bosnia-and-herzegovina"
  },
  "Belgium": {
    "results": "https://www.espn.com/soccer/team/results/_/id/459/belgium"
  },
  "Belarus": {
    "results": "https://www.espn.com/soccer/team/results/_/id/583/belarus"
  },
  "Austria": {
    "results": "https://www.espn.com/soccer/team/results/_/id/474/austria"
  },
  "Azerbaijan": {
    "results": "https://www.espn.com/soccer/team/results/_/id/581/azerbaijan"
  },
  "Armenia": {
    "results": "https://www.espn.com/soccer/team/results/_/id/579/armenia"
  },
  "Andorra": {
    "results": "https://www.espn.com/soccer/team/results/_/id/587/andorra"
  },
  "Albania": {
    "results": "https://www.espn.com/soccer/team/results/_/id/585/albania"
  }
}

headers = {'User-Agent': 'Mozilla/5.0'}

# Liste globale pour stocker les prédictions du jour
PREDICTIONS = []

def format_date_fr(date_str, time_str):
    # date_str au format 'YYYY-MM-DD'
    try:
        dt = datetime.strptime(date_str + " " + time_str, "%Y-%m-%d %H:%M")
        # Pour forcer l'affichage en français même si la locale n'est pas dispo, on formate à la main
        mois_fr = [
            "", "janvier", "février", "mars", "avril", "mai", "juin",
            "juillet", "août", "septembre", "octobre", "novembre", "décembre"
        ]
        mois = mois_fr[dt.month]
        return f"{dt.day} {mois} {dt.year} à {dt.strftime('%H:%M:%S')} UTC"
    except Exception as e:
        return f"{date_str} à {time_str}:00 UTC"

def get_today_matches_filtered():
    today = datetime.now().strftime('%Y-%m-%d')
    url = "https://v3.football.api-sports.io/fixtures"

    params = {
        "date": today,
        "timezone": "Africa/Abidjan"
    }

    allowed_league_ids = [5, 10, 71, 253, 78, 135]

    résultats = []  # AJOUT pour stocker les prédictions du jour

    try:
        response = requests.get(url, headers=api_headers, params=params)
        response.raise_for_status()
        data = response.json()

        print(f"\n📅 Matchs du jour ({today}) :\n")

        for match in data.get("response", []):
            league_id = match['league']['id']
            league = match['league']['name']
            country = match['league']['country']
            home = match['teams']['home']['name']
            away = match['teams']['away']['name']
            time = match['fixture']['date'][11:16]
            date = match['fixture']['date'][:10]

            if league_id in allowed_league_ids:
                print(f"🏆 [{country}] {league} : {home} vs {away} à {time}")

                # Analyse automatique si les 2 équipes sont connues
                if home in teams_urls and away in teams_urls:
                    print(f"\n🔎 Analyse automatique pour : {home} & {away}")
                    team1_stats = process_team(home, return_data=True)
                    team2_stats = process_team(away, return_data=True)
                    compare_teams_and_predict_score(
                        team1_stats, team2_stats, home, away, date, time, league, country, résultats=résultats
                    )
                else:
                    if home in teams_urls:
                        process_team(home)
                    if away in teams_urls:
                        process_team(away)

        # AJOUT : Sauvegarde et push des résultats s'il y en a eu
        if 'résultats' in locals() and résultats:
            sauvegarder_prediction_json(résultats, today)
            fichier = f"prédiction-{today}-analyse-ia.json"
            git_commit_and_push(fichier)

    except Exception as e:
        print(f"❌ Erreur lors de la récupération des matchs : {e}")

def get_match_result_for_team(team_name, score, team1, team2):
    try:
        home_score, away_score = map(int, score.split(' - '))
    except Exception:
        return None
    if team_name == team1:
        return 'W' if home_score > away_score else 'D' if home_score == away_score else 'L'
    elif team_name == team2:
        return 'W' if away_score > home_score else 'D' if away_score == home_score else 'L'
    return None

def extract_goals(team_name, score, team1, team2):
    try:
        home_score, away_score = map(int, score.split(' - '))
    except Exception:
        return None, None, None
    if team_name == team1:
        return home_score, away_score, True
    elif team_name == team2:
        return away_score, home_score, False
    return None, None, None

def analyze_trends(match_data, team_name, return_values=False):
    if len(match_data) < 6:
        print("\n⚠️ Pas assez de données pour analyse des tendances.")
        if return_values:
            return 0.0, 0.0
        return

    first_3 = match_data[-3:]
    last_3 = match_data[:3]

    def compute_avg(data):
        scored = conceded = 0
        count = 0
        for (_, team1, team2, _, score, _) in data:
            b_m, b_e, _ = extract_goals(team_name, score, team1, team2)
            if b_m is not None and b_e is not None:
                scored += b_m
                conceded += b_e
                count += 1
        return (scored / count if count else 0), (conceded / count if count else 0)

    avg_first = compute_avg(first_3)
    avg_last = compute_avg(last_3)

    def format_diff(v1, v2):
        delta = v2 - v1
        trend = "↗️" if delta > 0 else "↘️" if delta < 0 else "➡️"
        return f"{v1:.2f} → {v2:.2f} {trend}"

    print("\n📊 Tendances (3 premiers vs 3 derniers matchs) :")
    print(f"   ⚽ Moyenne buts marqués   : {format_diff(avg_first[0], avg_last[0])}")
    print(f"   🛡️ Moyenne buts encaissés : {format_diff(avg_first[1], avg_last[1])}")

    if return_values:
        delta_scored = avg_last[0] - avg_first[0]
        delta_conceded = avg_last[1] - avg_first[1]
        return delta_scored, delta_conceded

def get_form_points(recent_form):
    points_map = {'W': 3, 'D': 1, 'L': 0}
    total = sum(points_map.get(r, 0) for r in recent_form)
    ratio = total / (len(recent_form)*3) if recent_form else 0
    return total, ratio

def scrape_team_data(team_name, action):
    url = teams_urls.get(team_name, {}).get(action)
    if not url:
        print(f"URL non trouvée pour {team_name} et action {action}.")
        return []

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        matches = soup.find_all('tr', class_='Table__TR')
        valid_results = []
        recent_form = []

        buts_dom_marques = 0
        buts_dom_encaisses = 0
        buts_ext_marques = 0
        buts_ext_encaisses = 0

        for match in matches:
            date = match.find('div', class_='matchTeams')
            date_text = date.text.strip() if date else "N/A"

            teams = match.find_all('a', class_='AnchorLink Table__Team')
            team1 = teams[0].text.strip() if len(teams) > 0 else "N/A"
            team2 = teams[1].text.strip() if len(teams) > 1 else "N/A"

            competition = match.find_all('a', class_='AnchorLink')[1].text.strip() if len(match.find_all('a', 'AnchorLink')) > 1 else "N/A"
            score = match.find('span').text.strip() if match.find('span') else "N/A"
            status = match.find_all('a', class_='AnchorLink')[-1].text.strip() if match.find_all('a', 'AnchorLink') else "N/A"

            if all(val != "N/A" for val in [date_text, team1, team2, score]):
                valid_results.append((date_text, team1, team2, competition, score, status))

                result = get_match_result_for_team(team_name, score, team1, team2)
                if result:
                    recent_form.append(result)

                buts_m, buts_e, domicile = extract_goals(team_name, score, team1, team2)
                if buts_m is not None and buts_e is not None:
                    if domicile:
                        buts_dom_marques += buts_m
                        buts_dom_encaisses += buts_e
                    else:
                        buts_ext_marques += buts_m
                        buts_ext_encaisses += buts_e

            if len(valid_results) >= 6:
                break

        nb_matchs = len(valid_results)
        if nb_matchs == 0:
            print("Aucun match trouvé.")
            return []

        total_marques = buts_dom_marques + buts_ext_marques
        total_encaisses = buts_dom_encaisses + buts_ext_encaisses

        print(f"\n🗓️ {action.capitalize()} pour {team_name} :")
        for result in valid_results:
            print(" | ".join(result))

        points_map = {'W': 3, 'D': 1, 'L': 0}
        total_points = sum(points_map.get(r, 0) for r in recent_form)

        print(f"\n📊 Forme récente (6 derniers matchs) : {' '.join(recent_form)} (Total points : {total_points})")
        print(f"⚽ Buts marqués à domicile : {buts_dom_marques}")
        print(f"⚽ Buts encaissés à domicile : {buts_dom_encaisses}")
        print(f"⚽ Buts marqués à l'extérieur : {buts_ext_marques}")
        print(f"⚽ Buts encaissés à l'extérieur : {buts_ext_encaisses}")
        print(f"⚽ Total buts marqués : {total_marques}")
        print(f"🛡️ Total buts encaissés : {total_encaisses}")
        print(f"\n📈 Moyenne buts marqués par match : {total_marques / nb_matchs:.2f}")
        print(f"📉 Moyenne buts encaissés par match : {total_encaisses / nb_matchs:.2f}")

        delta_scored, delta_conceded = analyze_trends(valid_results, team_name, return_values=True)

        return {
            "matches": valid_results,
            "moyenne_marques": total_marques / nb_matchs,
            "moyenne_encaisses": total_encaisses / nb_matchs,
            "recent_form": recent_form,
            "trend_scored": delta_scored,
            "trend_conceded": delta_conceded
        }

    except Exception as e:
        print(f"Erreur scraping {team_name} ({action}) : {e}")
        return []

def confidence_total(total_pred):
    diff = abs(total_pred - 3)
    if diff >= 1.5:
        return 90
    elif diff >= 1.0:
        return 80
    elif diff >= 0.7:
        return 75
    elif diff >= 0.4:
        return 65
    else:
        return 55

def confidence_btts(pred_t1, pred_t2, t1, t2):
    if pred_t1 >= 1.5 and pred_t2 >= 1.5:
        def_ok_1 = t1['moyenne_encaisses'] >= 1.0
        def_ok_2 = t2['moyenne_encaisses'] >= 1.0
        if def_ok_1 and def_ok_2:
            return 85
        elif def_ok_1 or def_ok_2:
            return 75
        else:
            return 65
    return 0

def confidence_victory(diff, adj, forme):
    if diff >= 2.0:
        return 90
    elif diff >= 1.5:
        return 80
    elif diff >= 1.0:
        return 60 + int((diff-1.0)*20)
    else:
        return 0

def confidence_win_or_draw(diff, adj, forme):
    if diff >= 1.0:
        conf = 75 + int(min((diff-1.0)*10, 15))
        conf += int(abs(adj)*10) + int(abs(forme)*10)
        return min(conf, 90)
    elif 0.1 < diff < 0.7:
        conf = 60 + int(30 * (diff-0.1)/0.6)
        conf += int(abs(adj)*10) + int(abs(forme)*10)
        return min(conf, 90)
    return 0

def count_defeats(recent_form):
    return sum(1 for r in recent_form if r == 'L')

def compare_teams_and_predict_score(
    t1, t2, name1, name2, match_date="N/A", match_time="N/A",
    league="N/A", country="N/A", résultats=None
):
    if not t1 or not t2:
        print("⚠️ Données insuffisantes pour la comparaison.")
        return

    print(f"\n📅 Match prévu le {match_date} à {match_time}")
    print(f"🏆 Compétition : [{country}] {league}")
    print(f"⚔️ {name1} vs {name2}")

    print(f"\n🤝 Comparaison directe :")
    print(f"{name1} ➤ Moy. buts marqués : {t1['moyenne_marques']:.2f} | Moy. encaissés : {t1['moyenne_encaisses']:.2f}")
    print(f"{name2} ➤ Moy. buts marqués : {t2['moyenne_marques']:.2f} | Moy. encaissés : {t2['moyenne_encaisses']:.2f}")

    adj1 = t1['trend_scored'] - t1['trend_conceded']
    adj2 = t2['trend_scored'] - t2['trend_conceded']

    points1, ratio1 = get_form_points(t1.get('recent_form', []))
    points2, ratio2 = get_form_points(t2.get('recent_form', []))
    forme_adj1 = (ratio1 - 0.5) * 0.5
    forme_adj2 = (ratio2 - 0.5) * 0.5

    pred_t1 = (t1['moyenne_marques'] + t2['moyenne_encaisses']) / 2
    pred_t2 = (t2['moyenne_marques'] + t1['moyenne_encaisses']) / 2

    pred_t1 += adj1*0.5 + forme_adj1
    pred_t2 += adj2*0.5 + forme_adj2

    pred_t1 = max(pred_t1, 0.1)
    pred_t2 = max(pred_t2, 0.1)

    print(f"\n🛠️ Ajustements appliqués :")
    print(f"{name1} ➤ Tendance:{adj1:+.2f} | Forme:{forme_adj1:+.2f}")
    print(f"{name2} ➤ Tendance:{adj2:+.2f} | Forme:{forme_adj2:+.2f}")

    print(f"\n🔮 **Score estimé final** :")
    print(f"{name1} {pred_t1:.1f} - {pred_t2:.1f} {name2}")

    total_pred = pred_t1 + pred_t2

    print("\n🔎 Prédictions détaillées :")

    conf_total = confidence_total(total_pred)
    pred_safe = None
    conf_safe = 0

    # On stocke la meilleure prédiction dans pred_safe/conf_safe
    if total_pred >= 3.0:
        print(f"👉 Prédiction total : **+2.5 buts** (Confiance : {conf_total}%)")
        pred_safe = "+2.5 buts"
        conf_safe = conf_total
    else:
        print(f"👉 Prédiction total : **-3.5 buts** (Confiance : {conf_total}%)")
        pred_safe = "-3.5 buts"
        conf_safe = conf_total

    conf_btts = confidence_btts(pred_t1, pred_t2, t1, t2)
    if conf_btts:
        print(f"👉 Prédiction : **Les deux équipes marquent** (Confiance : {conf_btts}%)")
        if conf_btts > conf_safe:
            pred_safe = "Les deux équipes marquent"
            conf_safe = conf_btts

    diff = abs(pred_t1 - pred_t2)

    defeats_t1 = count_defeats(t1.get('recent_form', []))
    defeats_t2 = count_defeats(t2.get('recent_form', []))
    both_at_least_3_defeats = (defeats_t1 >= 3 and defeats_t2 >= 3)

    if pred_t1 > pred_t2:
        conf_draw = confidence_win_or_draw(diff, adj1, forme_adj1)
        conf_vic = confidence_victory(diff, adj1, forme_adj1)
        if 0.1 < diff < 0.7:
            print(f"👉 Prédiction : **Victoire ou nul {name1}** (Confiance : {conf_draw}%)")
            if conf_draw > conf_safe:
                pred_safe = f"Victoire ou nul {name1}"
                conf_safe = conf_draw
        elif diff >= 1.0 and not both_at_least_3_defeats:
            print(f"👉 Prédiction : **Victoire {name1}** (Confiance : {conf_vic}%)")
            if conf_vic > conf_safe:
                pred_safe = f"Victoire {name1}"
                conf_safe = conf_vic
        elif diff >= 1.0 and both_at_least_3_defeats:
            print(f"👉 Prédiction : **Victoire ou nul {name1}** (Confiance : {conf_draw}%)")
            if conf_draw > conf_safe:
                pred_safe = f"Victoire ou nul {name1}"
                conf_safe = conf_draw
    elif pred_t2 > pred_t1:
        conf_draw = confidence_win_or_draw(diff, adj2, forme_adj2)
        conf_vic = confidence_victory(diff, adj2, forme_adj2)
        if 0.1 < diff < 0.7:
            print(f"👉 Prédiction : **Victoire ou nul {name2}** (Confiance : {conf_draw}%)")
            if conf_draw > conf_safe:
                pred_safe = f"Victoire ou nul {name2}"
                conf_safe = conf_draw
        elif diff >= 1.0 and not both_at_least_3_defeats:
            print(f"👉 Prédiction : **Victoire {name2}** (Confiance : {conf_vic}%)")
            if conf_vic > conf_safe:
                pred_safe = f"Victoire {name2}"
                conf_safe = conf_vic
        elif diff >= 1.0 and both_at_least_3_defeats:
            print(f"👉 Prédiction : **Victoire ou nul {name2}** (Confiance : {conf_draw}%)")
            if conf_draw > conf_safe:
                pred_safe = f"Victoire ou nul {name2}"
                conf_safe = conf_draw

    print("\n📚 Note : Prédictions issues de la tendance, forme récente et stats offensives/défensives. La fiabilité (%) est une estimation statistique, non une certitude.")

    # Ajout de la prédiction dans la liste globale PREDICTIONS
    # On ne stocke que les matchs où les deux équipes sont connues et la prédiction la plus sûre existe
    if pred_safe and conf_safe:
        prediction_obj = {
            "HomeTeam": name1,
            "AwayTeam": name2,
            "confidence": conf_safe,
            "date": format_date_fr(match_date, match_time),
            "league": league,
            "prediction": pred_safe,
            "type": "safes"
        }
        PREDICTIONS.append(prediction_obj)
        if résultats is not None:
            résultats.append(prediction_obj)

def process_team(team_name, return_data=False):
    print(f"\n🧠 Analyse pour l'équipe : {team_name}")
    data = scrape_team_data(team_name, 'results')
    print("\n" + "-" * 60 + "\n")
    return data if return_data else None

# Fonction pour sauvegarder les prédictions dans un fichier JSON custom
def sauvegarder_prediction_json(predictions, date_str):
    chemin = f"prédiction-{date_str}-analyse-ia.json"
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(predictions, f, ensure_ascii=False, indent=2)
    print(f"✅ Prédictions sauvegardées dans : {chemin}")

# Fonction pour git add/commit/push
def git_commit_and_push(filepath):
    try:
        subprocess.run(["git", "config", "--global", "user.email", "github-actions[bot]@users.noreply.github.com"], check=True)
        subprocess.run(["git", "config", "--global", "user.name", "github-actions[bot]"], check=True)
        subprocess.run(["git", "add", filepath], check=True)
        subprocess.run(["git", "commit", "-m", f"📊 Prédictions IA du {datetime.now().strftime('%Y-%m-%d')}"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("✅ Prédictions poussées avec succès sur GitHub.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur Git : {e}")

def main():
    print("⚽️ Bienvenue dans l'analyse IA pour tous les matchs du jour (sans saisie manuelle).\n")
    get_today_matches_filtered()
    print("\nMerci d'avoir utilisé le script IA ⚽️📊. À bientôt !")

if __name__ == "__main__":
    main()
