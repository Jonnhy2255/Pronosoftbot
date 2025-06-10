import requests
from datetime import datetime
from bs4 import BeautifulSoup
import json
import locale
import subprocess

API_KEY = '1933761904aae9724ca6497102b2e094'

api_headers = {
    'x-apisports-key': API_KEY
}

team_name_mapping = {
    "Bournemouth": "AFC Bournemouth",
    "Rep. Of Ireland": "Republic Of Ireland",
}
teams_urls = {
    # Bloc Europe du dernier JSON
    "Wales": {"results": "https://www.espn.com/soccer/team/results/_/id/578/wales"},
    "Turkey": {"results": "https://www.espn.com/soccer/team/results/_/id/465/turkey"},
    "Ukraine": {"results": "https://www.espn.com/soccer/team/results/_/id/457/ukraine"},
    "Sweden": {"results": "https://www.espn.com/soccer/team/results/_/id/466/sweden"},
    "Switzerland": {"results": "https://www.espn.com/soccer/team/results/_/id/475/switzerland"},
    "Slovenia": {"results": "https://www.espn.com/soccer/team/results/_/id/472/slovenia"},
    "Slovakia": {"results": "https://www.espn.com/soccer/team/results/_/id/468/slovakia"},
    "Scotland": {"results": "https://www.espn.com/soccer/team/results/_/id/580/scotland"},
    "Serbia": {"results": "https://www.espn.com/soccer/team/results/_/id/6757/serbia"},
    "Romania": {"results": "https://www.espn.com/soccer/team/results/_/id/473/romania"},
    "Norway": {"results": "https://www.espn.com/soccer/team/results/_/id/464/norway"},
    "Poland": {"results": "https://www.espn.com/soccer/team/results/_/id/471/poland"},
    "Northern Ireland": {"results": "https://www.espn.com/soccer/team/results/_/id/586/northern-ireland"},
    "Netherlands": {"results": "https://www.espn.com/soccer/team/results/_/id/449/netherlands"},
    "North Macedonia": {"results": "https://www.espn.com/soccer/team/results/_/id/463/north-macedonia"},
    "Montenegro": {"results": "https://www.espn.com/soccer/team/results/_/id/6775/montenegro"},
    "Moldova": {"results": "https://www.espn.com/soccer/team/results/_/id/483/moldova"},
    "Latvia": {"results": "https://www.espn.com/soccer/team/results/_/id/456/latvia"},
    "Kazakhstan": {"results": "https://www.espn.com/soccer/team/results/_/id/2619/kazakhstan"},
    "Kosovo": {"results": "https://www.espn.com/soccer/team/results/_/id/18272/kosovo"},
    "Italy": {"results": "https://www.espn.com/soccer/team/results/_/id/162/italy"},
    "Israel": {"results": "https://www.espn.com/soccer/team/results/_/id/461/israel"},
    "Malta": {"results": "https://www.espn.com/soccer/team/results/_/id/453/malta"},
    "Luxembourg": {"results": "https://www.espn.com/soccer/team/results/_/id/582/luxembourg"},
    "Lithuania": {"results": "https://www.espn.com/soccer/team/results/_/id/460/lithuania"},
    "Iceland": {"results": "https://www.espn.com/soccer/team/results/_/id/470/iceland"},
    "Hungary": {"results": "https://www.espn.com/soccer/team/results/_/id/480/hungary"},
    "Greece": {"results": "https://www.espn.com/soccer/team/results/_/id/455/greece"},
    "Gibraltar": {"results": "https://www.espn.com/soccer/team/results/_/id/16721/gibraltar"},
    "Finland": {"results": "https://www.espn.com/soccer/team/results/_/id/458/finland"},
    "Faroe Islands": {"results": "https://www.espn.com/soccer/team/results/_/id/447/faroe-islands"},
    "Estonia": {"results": "https://www.espn.com/soccer/team/results/_/id/444/estonia"},
    "England": {"results": "https://www.espn.com/soccer/team/results/_/id/448/england"},
    "Denmark": {"results": "https://www.espn.com/soccer/team/results/_/id/479/denmark"},
    "Czechia": {"results": "https://www.espn.com/soccer/team/results/_/id/450/czechia"},
    "Cyprus": {"results": "https://www.espn.com/soccer/team/results/_/id/445/cyprus"},
    "Croatia": {"results": "https://www.espn.com/soccer/team/results/_/id/477/croatia"},
    "Bulgaria": {"results": "https://www.espn.com/soccer/team/results/_/id/462/bulgaria"},
    "Bosnia and Herzegovina": {"results": "https://www.espn.com/soccer/team/results/_/id/452/bosnia-and-herzegovina"},
    "Belgium": {"results": "https://www.espn.com/soccer/team/results/_/id/459/belgium"},
    "Belarus": {"results": "https://www.espn.com/soccer/team/results/_/id/583/belarus"},
    "Austria": {"results": "https://www.espn.com/soccer/team/results/_/id/474/austria"},
    "Azerbaijan": {"results": "https://www.espn.com/soccer/team/results/_/id/581/azerbaijan"},
    "Armenia": {"results": "https://www.espn.com/soccer/team/results/_/id/579/armenia"},
    "Andorra": {"results": "https://www.espn.com/soccer/team/results/_/id/587/andorra"},
    "Albania": {"results": "https://www.espn.com/soccer/team/results/_/id/585/albania"},
    # Bloc Afrique, Asie, Caraïbes, etc. (et quelques doublons pour sécurité)
    "Angola": {"results": "https://www.espn.com/soccer/team/results/_/id/653/angola"},
    "Botswana": {"results": "https://www.espn.com/soccer/team/results/_/id/4245/botswana"},
    "Comoros": {"results": "https://www.espn.com/soccer/team/results/_/id/8601/comoros"},
    "Eswatini": {"results": "https://www.espn.com/soccer/team/results/_/id/6686/eswatini"},
    "Lesotho": {"results": "https://www.espn.com/soccer/team/results/_/id/6640/lesotho"},
    "Madagascar": {"results": "https://www.espn.com/soccer/team/results/_/id/5533/madagascar"},
    "Malawi": {"results": "https://www.espn.com/soccer/team/results/_/id/4325/malawi"},
    "Mauritius": {"results": "https://www.espn.com/soccer/team/results/_/id/5534/mauritius"},
    "Mozambique": {"results": "https://www.espn.com/soccer/team/results/_/id/8939/mozambique"},
    "Namibia": {"results": "https://www.espn.com/soccer/team/results/_/id/6725/namibia"},
    "South Africa": {"results": "https://www.espn.com/soccer/team/results/_/id/467/south-africa"},
    "Tanzania": {"results": "https://www.espn.com/soccer/team/results/_/id/5778/tanzania"},
    "Zimbabwe": {"results": "https://www.espn.com/soccer/team/results/_/id/4214/zimbabwe"},
    "Afghanistan": {"results": "https://www.espn.com/soccer/team/results/_/id/5780/afghanistan"},
    "Algeria": {"results": "https://www.espn.com/soccer/team/results/_/id/624/algeria"},
    "Anguilla": {"results": "https://www.espn.com/soccer/team/results/_/id/8942/anguilla"},
    "Aruba": {"results": "https://www.espn.com/soccer/team/results/_/id/2642/aruba"},
    "Barbados": {"results": "https://www.espn.com/soccer/team/results/_/id/2637/barbados"},
    "Benin": {"results": "https://www.espn.com/soccer/team/results/_/id/2844/benin"},
    "Bonaire": {"results": "https://www.espn.com/soccer/team/results/_/id/19314/bonaire"},
    "British Virgin Islands": {"results": "https://www.espn.com/soccer/team/results/_/id/2644/british-virgin-islands"},
    "Brunei Darussalam": {"results": "https://www.espn.com/soccer/team/results/_/id/10525/brunei-darussalam"},
    "Burkina Faso": {"results": "https://www.espn.com/soccer/team/results/_/id/2845/burkina-faso"},
    "Burundi": {"results": "https://www.espn.com/soccer/team/results/_/id/5779/burundi"},
    "Cambodia": {"results": "https://www.espn.com/soccer/team/results/_/id/5518/cambodia"},
    "Cameroon": {"results": "https://www.espn.com/soccer/team/results/_/id/656/cameroon"},
    "Canada": {"results": "https://www.espn.com/soccer/team/results/_/id/206/canada"},
    "Cape Verde Islands": {"results": "https://www.espn.com/soccer/team/results/_/id/2597/cape-verde-islands"},
    "Central African Republic": {"results": "https://www.espn.com/soccer/team/results/_/id/10528/central-african-republic"},
    "Chad": {"results": "https://www.espn.com/soccer/team/results/_/id/8941/chad"},
    "Chile": {"results": "https://www.espn.com/soccer/team/results/_/id/207/chile"},
    "Congo DR": {"results": "https://www.espn.com/soccer/team/results/_/id/2850/congo-dr"},
    "Costa Rica": {"results": "https://www.espn.com/soccer/team/results/_/id/214/costa-rica"},
    "Curacao": {"results": "https://www.espn.com/soccer/team/results/_/id/11678/curacao"},
    "Dominica": {"results": "https://www.espn.com/soccer/team/results/_/id/13582/dominica"},
    "Dominican Republic": {"results": "https://www.espn.com/soccer/team/results/_/id/2649/dominican-republic"},
    "El Salvador": {"results": "https://www.espn.com/soccer/team/results/_/id/2650/el-salvador"},
    "Equatorial Guinea": {"results": "https://www.espn.com/soccer/team/results/_/id/8938/equatorial-guinea"},
    "Gabon": {"results": "https://www.espn.com/soccer/team/results/_/id/4231/gabon"},
    "Gambia": {"results": "https://www.espn.com/soccer/team/results/_/id/7368/gambia"},
    "Georgia": {"results": "https://www.espn.com/soccer/team/results/_/id/584/georgia"},
    "Ghana": {"results": "https://www.espn.com/soccer/team/results/_/id/4469/ghana"},
    "Guatemala": {"results": "https://www.espn.com/soccer/team/results/_/id/2652/guatemala"},
    "Guinea-Bissau": {"results": "https://www.espn.com/soccer/team/results/_/id/8602/guinea-bissau"},
    "Haiti": {"results": "https://www.espn.com/soccer/team/results/_/id/2654/haiti"},
    "Honduras": {"results": "https://www.espn.com/soccer/team/results/_/id/215/honduras"},
    "Hong Kong": {"results": "https://www.espn.com/soccer/team/results/_/id/1928/hong-kong"},
    "India": {"results": "https://www.espn.com/soccer/team/results/_/id/4385/india"},
    "Iran": {"results": "https://www.espn.com/soccer/team/results/_/id/469/iran"},
    "Ivory Coast": {"results": "https://www.espn.com/soccer/team/results/_/id/4789/ivory-coast"},
    "Jamaica": {"results": "https://www.espn.com/soccer/team/results/_/id/1038/jamaica"},
    "Japan": {"results": "https://www.espn.com/soccer/team/results/_/id/627/japan"},
    "Jordan": {"results": "https://www.espn.com/soccer/team/results/_/id/2917/jordan"},
    "Kenya": {"results": "https://www.espn.com/soccer/team/results/_/id/2848/kenya"},
    "Laos": {"results": "https://www.espn.com/soccer/team/results/_/id/7348/laos"},
    "Lebanon": {"results": "https://www.espn.com/soccer/team/results/_/id/4388/lebanon"},
    "Liberia": {"results": "https://www.espn.com/soccer/team/results/_/id/4205/liberia"},
    "Liechtenstein": {"results": "https://www.espn.com/soccer/team/results/_/id/589/liechtenstein"},
    "Lithuania": {"results": "https://www.espn.com/soccer/team/results/_/id/460/lithuania"},
    "Luxembourg": {"results": "https://www.espn.com/soccer/team/results/_/id/582/luxembourg"},
    "Macau": {"results": "https://www.espn.com/soccer/team/results/_/id/6722/macau"},
    "Malaysia": {"results": "https://www.espn.com/soccer/team/results/_/id/2405/malaysia"},
    "Maldives": {"results": "https://www.espn.com/soccer/team/results/_/id/4390/maldives"},
    "Mali": {"results": "https://www.espn.com/soccer/team/results/_/id/2849/mali"},
    "Malta": {"results": "https://www.espn.com/soccer/team/results/_/id/453/malta"},
    "Mauritania": {"results": "https://www.espn.com/soccer/team/results/_/id/8940/mauritania"},
    "Mexico": {"results": "https://www.espn.com/soccer/team/results/_/id/203/mexico"},
    "Moldova": {"results": "https://www.espn.com/soccer/team/results/_/id/483/moldova"},
    "Montenegro": {"results": "https://www.espn.com/soccer/team/results/_/id/6775/montenegro"},
    "Morocco": {"results": "https://www.espn.com/soccer/team/results/_/id/2869/morocco"},
    "Mozambique": {"results": "https://www.espn.com/soccer/team/results/_/id/8939/mozambique"},
    "Nepal": {"results": "https://www.espn.com/soccer/team/results/_/id/5785/nepal"},
    "New Zealand": {"results": "https://www.espn.com/soccer/team/results/_/id/2666/new-zealand"},
    "Nicaragua": {"results": "https://www.espn.com/soccer/team/results/_/id/2658/nicaragua"},
    "Niger": {"results": "https://www.espn.com/soccer/team/results/_/id/8937/niger"},
    "Nigeria": {"results": "https://www.espn.com/soccer/team/results/_/id/657/nigeria"},
    "North Korea": {"results": "https://www.espn.com/soccer/team/results/_/id/4860/north-korea"},
    "Northern Ireland": {"results": "https://www.espn.com/soccer/team/results/_/id/586/northern-ireland"},
    "Norway": {"results": "https://www.espn.com/soccer/team/results/_/id/464/norway"},
    "Oman": {"results": "https://www.espn.com/soccer/team/results/_/id/2841/oman"},
    "Poland": {"results": "https://www.espn.com/soccer/team/results/_/id/471/poland"},
    "Panama": {"results": "https://www.espn.com/soccer/team/results/_/id/2659/panama"},
    "Puerto Rico": {"results": "https://www.espn.com/soccer/team/results/_/id/11766/puerto-rico"},
    "Republic Of Ireland": {"results": "https://www.espn.com/soccer/team/results/_/id/476/republic-of-ireland"},
    "Russia": {"results": "https://www.espn.com/soccer/team/results/_/id/454/russia"},
    "Rwanda": {"results": "https://www.espn.com/soccer/team/results/_/id/2851/rwanda"},
    "Saudi Arabia": {"results": "https://www.espn.com/soccer/team/results/_/id/655/saudi-arabia"},
    "Scotland": {"results": "https://www.espn.com/soccer/team/results/_/id/580/scotland"},
    "Senegal": {"results": "https://www.espn.com/soccer/team/results/_/id/654/senegal"},
    "Singapore": {"results": "https://www.espn.com/soccer/team/results/_/id/4384/singapore"},
    "Slovakia": {"results": "https://www.espn.com/soccer/team/results/_/id/468/slovakia"},
    "Slovenia": {"results": "https://www.espn.com/soccer/team/results/_/id/472/slovenia"},
    "South Africa": {"results": "https://www.espn.com/soccer/team/results/_/id/467/south-africa"},
    "South Korea": {"results": "https://www.espn.com/soccer/team/results/_/id/451/south-korea"},
    "Sri Lanka": {"results": "https://www.espn.com/soccer/team/results/_/id/5782/sri-lanka"},
    "St Kitts and Nevis": {"results": "https://www.espn.com/soccer/team/results/_/id/2662/st-kitts-and-nevis"},
    "St Martin": {"results": "https://www.espn.com/soccer/team/results/_/id/10596/st-martin"},
    "St Vincent and the Grenadines": {"results": "https://www.espn.com/soccer/team/results/_/id/13584/st-vincent-and-the-grenadines"},
    "Sudan": {"results": "https://www.espn.com/soccer/team/results/_/id/4319/sudan"},
    "Sweden": {"results": "https://www.espn.com/soccer/team/results/_/id/466/sweden"},
    "Switzerland": {"results": "https://www.espn.com/soccer/team/results/_/id/475/switzerland"},
    "Tajikistan": {"results": "https://www.espn.com/soccer/team/results/_/id/6723/tajikistan"},
    "Tanzania": {"results": "https://www.espn.com/soccer/team/results/_/id/5778/tanzania"},
    "Thailand": {"results": "https://www.espn.com/soccer/team/results/_/id/4396/thailand"},
    "Timor-Leste": {"results": "https://www.espn.com/soccer/team/results/_/id/8664/timor-leste"},
    "Trinidad and Tobago": {"results": "https://www.espn.com/soccer/team/results/_/id/2627/trinidad-and-tobago"},
    "Tunisia": {"results": "https://www.espn.com/soccer/team/results/_/id/659/tunisia"},
    "Turkey": {"results": "https://www.espn.com/soccer/team/results/_/id/465/turkey"},
    "Uganda": {"results": "https://www.espn.com/soccer/team/results/_/id/4211/uganda"},
    "Ukraine": {"results": "https://www.espn.com/soccer/team/results/_/id/457/ukraine"},
    "United States": {"results": "https://www.espn.com/soccer/team/results/_/id/660/united-states"},
    "Venezuela": {"results": "https://www.espn.com/soccer/team/results/_/id/213/venezuela"},
    "Vietnam": {"results": "https://www.espn.com/soccer/team/results/_/id/7349/vietnam"},
    "Wales": {"results": "https://www.espn.com/soccer/team/results/_/id/578/wales"},
    "Zambia": {"results": "https://www.espn.com/soccer/team/results/_/id/4277/zambia"},
    "Zanzibar": {"results": "https://www.espn.com/soccer/team/results/_/id/5815/zanzibar"},
    "Zimbabwe": {"results": "https://www.espn.com/soccer/team/results/_/id/4214/zimbabwe"},
    # Ajoutez d'autres équipes si besoin
}


headers = {'User-Agent': 'Mozilla/5.0'}

PREDICTIONS = []

def get_espn_name(api_team_name):
    mapped = team_name_mapping.get(api_team_name)
    if not mapped:
        print(f"⚠️ Pas de correspondance trouvée pour '{api_team_name}' ! Utilisation du nom API.")
        return api_team_name
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

def get_today_matches_filtered():
    today = datetime.now().strftime('%Y-%m-%d')
    url = "https://v3.football.api-sports.io/fixtures"
    params = {
        "date": today,
        "timezone": "Africa/Abidjan"
    }
    allowed_league_ids = [5, 10, 71, 253, 78, 135]
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
            time = match['fixture']['date'][11:16]
            date = match['fixture']['date'][:10]
            if league_id in allowed_league_ids:
                print(f"🏆 [{country}] {league} : {home_api} vs {away_api} à {time}")
                home_espn = get_espn_name(home_api)
                away_espn = get_espn_name(away_api)
                if home_espn in teams_urls and away_espn in teams_urls:
                    print(f"\n🔎 Analyse automatique pour : {home_espn} & {away_espn}")
                    team1_stats = process_team(home_api, return_data=True)
                    team2_stats = process_team(away_api, return_data=True)
                    compare_teams_and_predict_score(
                        team1_stats, team2_stats, home_api, away_api, date, time, league, country, résultats=résultats
                    )
                else:
                    if home_espn in teams_urls:
                        process_team(home_api)
                    if away_espn in teams_urls:
                        process_team(away_api)
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
        return 'W' if away_score > home_score else 'D' if home_score == away_score else 'L'
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

def analyze_weighted_trends(match_data, team_name, return_values=False):
    if len(match_data) < 6:
        print("\n⚠️ Pas assez de données pour la tendance pondérée.")
        if return_values:
            return 0.0, 0.0
        return
    # pondération croissante
    poids = [0.5, 0.6, 0.7, 1.0, 1.2, 1.5]
    scored, conceded = 0.0, 0.0
    total_poids = 0.0
    # On prend les 6 derniers matchs, le plus ancien d'abord
    data = match_data[-6:]
    for idx, (_, team1, team2, _, score, _) in enumerate(data):
        buts_m, buts_e, _ = extract_goals(team_name, score, team1, team2)
        if buts_m is not None and buts_e is not None:
            p = poids[idx]
            scored += buts_m * p
            conceded += buts_e * p
            total_poids += p
    avg_scored = scored / total_poids if total_poids else 0.0
    avg_conceded = conceded / total_poids if total_poids else 0.0

    print("\n📊 Tendance pondérée (poids croissants sur 6 matchs) :")
    print(f"   ⚽ Moyenne mobile buts marqués   : {avg_scored:.2f}")
    print(f"   🛡️ Moyenne mobile buts encaissés : {avg_conceded:.2f}")

    if return_values:
        return avg_scored, avg_conceded

def get_streak_bonus(recent_form):
    # Bonus pour victoires consécutives, malus pour défaites consécutives
    streak_bonus = 0
    streak_malus = 0
    count_win = 0
    count_lose = 0
    for r in recent_form:
        if r == 'W':
            count_win += 1
            if count_lose >= 2:
                streak_malus -= (count_lose - 1)
            count_lose = 0
        elif r == 'L':
            count_lose += 1
            if count_win >= 2:
                streak_bonus += (count_win - 1)
            count_win = 0
        else:
            if count_win >= 2:
                streak_bonus += (count_win - 1)
            if count_lose >= 2:
                streak_malus -= (count_lose - 1)
            count_win = 0
            count_lose = 0
    # Fin de série
    if count_win >= 2:
        streak_bonus += (count_win - 1)
    if count_lose >= 2:
        streak_malus -= (count_lose - 1)
    return streak_bonus + streak_malus

def get_form_points(recent_form):
    points_map = {'W': 3, 'D': 1, 'L': 0}
    total = sum(points_map.get(r, 0) for r in recent_form)
    ratio = total / (len(recent_form)*3) if recent_form else 0
    # Momentum bonus/malus
    momentum = get_streak_bonus(recent_form)
    return total, ratio, momentum

def scrape_team_data(team_name, action):
    espn_team_name = get_espn_name(team_name)
    url = teams_urls.get(espn_team_name, {}).get(action)
    if not url:
        print(f"URL non trouvée pour {espn_team_name} et action {action}.")
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
                result = get_match_result_for_team(espn_team_name, score, team1, team2)
                if result:
                    recent_form.append(result)
                buts_m, buts_e, domicile = extract_goals(espn_team_name, score, team1, team2)
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
        print(f"\n🗓️ {action.capitalize()} pour {espn_team_name} :")
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
        # Tendance pondérée améliorée
        avg_trend_scored, avg_trend_conceded = analyze_weighted_trends(valid_results, espn_team_name, return_values=True)
        return {
            "matches": valid_results,
            "moyenne_marques": total_marques / nb_matchs,
            "moyenne_encaisses": total_encaisses / nb_matchs,
            "recent_form": recent_form,
            "trend_scored": avg_trend_scored,
            "trend_conceded": avg_trend_conceded
        }
    except Exception as e:
        print(f"Erreur scraping {espn_team_name} ({action}) : {e}")
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
    # Amélioré : prend aussi en compte la capacité défensive
    if (
        pred_t1 >= 1.2 and pred_t2 >= 1.2 and
        t1['moyenne_encaisses'] >= 1.0 and
        t2['moyenne_encaisses'] >= 1.0
    ):
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

def compute_indice_forme(t, forme_adj, adj):
    # 0.4 * (buts marqués - encaissés) + 0.3 * forme + 0.3 * tendance
    return (
        0.4 * (t['moyenne_marques'] - t['moyenne_encaisses']) +
        0.3 * forme_adj +
        0.3 * (adj)
    )

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
    points1, ratio1, momentum1 = get_form_points(t1.get('recent_form', []))
    points2, ratio2, momentum2 = get_form_points(t2.get('recent_form', []))
    forme_adj1 = (ratio1 - 0.5) * 0.5 + 0.1 * momentum1
    forme_adj2 = (ratio2 - 0.5) * 0.5 + 0.1 * momentum2

    # Prédiction initiale
    pred_t1 = (t1['moyenne_marques'] + t2['moyenne_encaisses']) / 2
    pred_t2 = (t2['moyenne_marques'] + t1['moyenne_encaisses']) / 2
    pred_t1 += adj1*0.5 + forme_adj1
    pred_t2 += adj2*0.5 + forme_adj2
    pred_t1 = max(pred_t1, 0.1)
    pred_t2 = max(pred_t2, 0.1)
    # Normalisation offensive
    global_moyenne = (pred_t1 + pred_t2) / 2
    pred_t1 = (pred_t1 + global_moyenne) / 2
    pred_t2 = (pred_t2 + global_moyenne) / 2

    print(f"\n🛠️ Ajustements appliqués :")
    print(f"{name1} ➤ Tendance:{adj1:+.2f} | Forme:{forme_adj1:+.2f}")
    print(f"{name2} ➤ Tendance:{adj2:+.2f} | Forme:{forme_adj2:+.2f}")
    print(f"\n🔮 **Score estimé final** :")
    print(f"{name1} {pred_t1:.1f} - {pred_t2:.1f} {name2}")

    # Calcul de l'indice de forme combiné
    indice_forme_t1 = compute_indice_forme(t1, forme_adj1, adj1)
    indice_forme_t2 = compute_indice_forme(t2, forme_adj2, adj2)
    diff_indice_forme = abs(indice_forme_t1 - indice_forme_t2)
    print(f"\n📊 Indice de forme : {name1}: {indice_forme_t1:.2f} | {name2}: {indice_forme_t2:.2f} | Diff: {diff_indice_forme:.2f}")

    total_pred = pred_t1 + pred_t2
    print("\n🔎 Prédictions détaillées :")
    conf_total = confidence_total(total_pred)
    pred_safe = None
    conf_safe = 0

    defeats_t1 = count_defeats(t1.get('recent_form', []))
    defeats_t2 = count_defeats(t2.get('recent_form', []))
    # Règle prudence matchs équilibrés
    if diff_indice_forme < 0.3 and defeats_t1 >= 2 and defeats_t2 >= 2:
        print(f"👉 Prédiction : **⚠️ Match très équilibré, à éviter**")
        pred_safe = "⚠️ Match très équilibré, à éviter"
        conf_safe = 60
    else:
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

        diff = abs(indice_forme_t1 - indice_forme_t2)
        both_at_least_3_defeats = (defeats_t1 >= 3 and defeats_t2 >= 3)
        if indice_forme_t1 > indice_forme_t2:
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
        elif indice_forme_t2 > indice_forme_t1:
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

    print("\n📚 Note : Prédictions issues de la tendance pondérée, forme récente, séries, stats offensives/défensives et indice de forme combiné. La fiabilité (%) est une estimation statistique, non une certitude.")
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
    print(f"\n🧠 Analyse pour l'équipe : {get_espn_name(team_name)}")
    data = scrape_team_data(team_name, 'results')
    print("\n" + "-" * 60 + "\n")
    return data if return_data else None

def sauvegarder_prediction_json(predictions, date_str):
    chemin = f"prédiction-{date_str}-analyse-ia.json"
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(predictions, f, ensure_ascii=False, indent=2)
    print(f"✅ Prédictions sauvegardées dans : {chemin}")

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
    print("⚽️ Bienvenue dans l'analyse IA améliorée pour tous les matchs du jour (tendance pondérée, série dynamique, prudence sur matchs équilibrés, etc).\n")
    get_today_matches_filtered()
    print("\nMerci d'avoir utilisé le script IA ⚽️📊. À bientôt !")

if __name__ == "__main__":
    main()
