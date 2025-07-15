import requests
from datetime import datetime
from bs4 import BeautifulSoup
import json
import subprocess
import math
import itertools
import os

API_KEY = '1933761904aae9724ca6497102b2e094'
api_headers = {
    'x-apisports-key': API_KEY
}

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
}


classement_ligue_mapping = {
    "Colombia": {"Primera A": "https://www.espn.com/soccer/standings/_/league/col.1"},
    "France": {"Ligue 1": "https://www.espn.com/soccer/standings/_/league/fra.1"},
    "Belgium": {"Jupiler Pro League": "https://www.espn.com/soccer/standings/_/league/bel.1"},
    "England": {
        "Premier League": "https://www.espn.com/soccer/standings/_/league/eng.1",
        "National League": "https://www.espn.com/soccer/standings/_/league/eng.4"
    },
    "Netherlands": {"Eredivisie": "https://www.espn.com/soccer/standings/_/league/ned.1"},
    "Portugal": {"Primeira Liga": "https://www.espn.com/soccer/standings/_/league/por.1"},
    "Spain": {"La Liga": "https://www.espn.com/soccer/standings/_/league/esp.1"},
    "Germany": {"Bundesliga": "https://www.espn.com/soccer/standings/_/league/ger.1"},
    "Austria": {"Bundesliga": "https://www.espn.com/soccer/standings/_/league/aut.1"},
    "Italy": {"Serie A": "https://www.espn.com/soccer/standings/_/league/ita.1"},
    "Brazil": {
        "Serie A": "https://www.espn.com/soccer/standings/_/league/bra.1",
        "Serie B": "https://www.espn.com/soccer/standings/_/league/bra.2"
    },
    "Turkey": {"Süper Lig": "https://www.espn.com/soccer/standings/_/league/tur.1"},
    "Mexico": {"Liga MX": "https://www.espn.com/soccer/standings/_/league/mex.1"},
    "USA": {"Major League Soccer": "https://www.espn.com/soccer/standings/_/league/usa.1"},
    "Japan": {"J1 League": "https://www.espn.com/soccer/standings/_/league/jpn.1"},
    "Saudi-Arabia": {"Pro League": "https://www.espn.com/soccer/standings/_/league/ksa.1"},
    "Switzerland": {"Super League": "https://www.espn.com/soccer/standings/_/league/sui.1"},
    "China": {"Super League": "https://www.espn.com/soccer/standings/_/league/chn.1"},
    "Russia": {"Premier League": "https://www.espn.com/soccer/standings/_/league/rus.1"},
    "Greece": {"Super League 1": "https://www.espn.com/soccer/standings/_/league/gre.1"},

    # ✅ Nouvelles ligues ajoutées
    "Chile": {"Primera División": "https://www.espn.com/soccer/standings/_/league/chi.1"},
    "Peru": {"Primera División": "https://www.espn.com/soccer/standings/_/league/per.1"},
    "Sweden": {"Allsvenskan": "https://www.espn.com/soccer/standings/_/league/swe.1"},
    "Argentina": {"Primera Nacional": "https://www.espn.com/soccer/standings/_/league/arg.2"},
    "Paraguay": {"Division Profesional": "https://www.espn.com/soccer/standings/_/league/par.1"},
    "Venezuela": {"Primera División": "https://www.espn.com/soccer/standings/_/league/ven.1"},
    "Romania": {"Liga I": "https://www.espn.com/soccer/standings/_/league/rou.1"}
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
    "Atlético-MG": {
    "results": "https://www.espn.com/soccer/team/results/_/id/7632/atletico-mg"
  },
  "Bahia": {
    "results": "https://www.espn.com/soccer/team/results/_/id/9967/bahia"
  },
  "Botafogo": {
    "results": "https://www.espn.com/soccer/team/results/_/id/6086/botafogo"
  },
  "Ceará": {
    "results": "https://www.espn.com/soccer/team/results/_/id/9969/ceara"
  },
  "Corinthians": {
    "results": "https://www.espn.com/soccer/team/results/_/id/874/corinthians"
  },
  "Cruzeiro": {
    "results": "https://www.espn.com/soccer/team/results/_/id/2022/cruzeiro"
  },
  "Flamengo": {
    "results": "https://www.espn.com/soccer/team/results/_/id/819/flamengo"
  },
  "Fluminense": {
    "results": "https://www.espn.com/soccer/team/results/_/id/3445/fluminense"
  },
  "Fortaleza": {
    "results": "https://www.espn.com/soccer/team/results/_/id/6272/fortaleza"
  },
  "Grêmio": {
    "results": "https://www.espn.com/soccer/team/results/_/id/6273/gremio"
  },
  "Internacional": {
    "results": "https://www.espn.com/soccer/team/results/_/id/1936/internacional"
  },
  "Juventude": {
    "results": "https://www.espn.com/soccer/team/results/_/id/6270/juventude"
  },
  "Mirassol": {
    "results": "https://www.espn.com/soccer/team/results/_/id/9169/mirassol"
  },
  "Palmeiras": {
    "results": "https://www.espn.com/soccer/team/results/_/id/2029/palmeiras"
  },
  "Red Bull Bragantino": {
    "results": "https://www.espn.com/soccer/team/results/_/id/6079/red-bull-bragantino"
  },
  "Santos": {
    "results": "https://www.espn.com/soccer/team/results/_/id/2674/santos"
  },
  "São Paulo": {
    "results": "https://www.espn.com/soccer/team/results/_/id/2026/sao-paulo"
  },
  "Vasco da Gama": {
    "results": "https://www.espn.com/soccer/team/results/_/id/3454/vasco-da-gama"
  },
  "Vitória": {
    "results": "https://www.espn.com/soccer/team/results/_/id/3457/vitoria"
  },
  "Sport": {
    "results": "https://www.espn.com/soccer/team/results/_/id/7635/sport"
  },
  "AFC Bournemouth": {
        "results": "https://www.espn.com/football/team/results/_/id/349/afc-bournemouth"
    },
    "Arsenal": {
        "results": "https://www.espn.com/football/team/results/_/id/359/arsenal"
    },
    "Aston Villa": {
        "results": "https://www.espn.com/football/team/results/_/id/362/aston-villa"
    },
    "Brentford": {
        "results": "https://www.espn.com/football/team/results/_/id/337/brentford"
    },
    "Brighton & Hove Albion": {
        "results": "https://www.espn.com/football/team/results/_/id/331/brighton-hove-albion"
    },
    "Chelsea": {
        "results": "https://www.espn.com/football/team/results/_/id/363/chelsea"
    },
    "Crystal Palace": {
        "results": "https://www.espn.com/football/team/results/_/id/384/crystal-palace"
    },
    "Everton": {
        "results": "https://www.espn.com/football/team/results/_/id/368/everton"
    },
    "Fulham": {
        "results": "https://www.espn.com/football/team/results/_/id/370/fulham"
    },
    "Ipswich Town": {
        "results": "https://www.espn.com/football/team/results/_/id/373/ipswich-town"
    },
    "Leicester City": {
        "results": "https://www.espn.com/football/team/results/_/id/375/leicester-city"
    },
    "Liverpool": {
        "results": "https://www.espn.com/football/team/results/_/id/364/liverpool"
    },
    "Manchester City": {
        "results": "https://www.espn.com/football/team/results/_/id/382/manchester-city"
    },
    "Manchester United": {
        "results": "https://www.espn.com/football/team/results/_/id/360/manchester-united"
    },
    "Newcastle United": {
        "results": "https://www.espn.com/football/team/results/_/id/361/newcastle-united"
    },
    "Nottingham Forest": {
        "results": "https://www.espn.com/football/team/results/_/id/393/nottingham-forest"
    },
    "Southampton": {
        "results": "https://www.espn.com/football/team/results/_/id/376/southampton"
    },
    "Tottenham Hotspur": {
        "results": "https://www.espn.com/football/team/results/_/id/367/tottenham-hotspur"
    },
    "West Ham United": {
        "results": "https://www.espn.com/football/team/results/_/id/371/west-ham-united"
    },
    "Wolverhampton Wanderers": {
        "results": "https://www.espn.com/football/team/results/_/id/380/wolverhampton-wanderers"
    },
    "Alavés": {
        "results": "https://www.espn.com/football/team/results/_/id/96/alaves"
    },
    "Athletic Club": {
        "results": "https://www.espn.com/football/team/results/_/id/93/athletic-club"
    },
    "Atlético Madrid": {
        "results": "https://www.espn.com/football/team/results/_/id/1068/atletico-madrid"
    },
    "Barcelona": {
        "results": "https://www.espn.com/football/team/results/_/id/83/barcelona"
    },
    "Celta Vigo": {
        "results": "https://www.espn.com/football/team/results/_/id/85/celta-vigo"
    },
    "Espanyol": {
        "results": "https://www.espn.com/football/team/results/_/id/88/espanyol"
    },
    "Getafe": {
        "results": "https://www.espn.com/football/team/results/_/id/2922/getafe"
    },
    "Girona": {
        "results": "https://www.espn.com/football/team/results/_/id/9812/girona"
    },
    "Las Palmas": {
        "results": "https://www.espn.com/football/team/results/_/id/98/las-palmas"
    },
    "Leganés": {
        "results": "https://www.espn.com/football/team/results/_/id/17534/leganes"
    },
    "Mallorca": {
        "results": "https://www.espn.com/football/team/results/_/id/84/mallorca"
    },
    "Osasuna": {
        "results": "https://www.espn.com/football/team/results/_/id/97/osasuna"
    },
    "Rayo Vallecano": {
        "results": "https://www.espn.com/football/team/results/_/id/101/rayo-vallecano"
    },
    "Real Betis": {
        "results": "https://www.espn.com/football/team/results/_/id/244/real-betis"
    },
    "Real Madrid": {
        "results": "https://www.espn.com/football/team/results/_/id/86/real-madrid"
    },
    "Real Sociedad": {
        "results": "https://www.espn.com/football/team/results/_/id/89/real-sociedad"
    },
    "Real Valladolid": {
        "results": "https://www.espn.com/football/team/results/_/id/95/real-valladolid"
    },
    "Sevilla": {
        "results": "https://www.espn.com/football/team/results/_/id/243/sevilla"
    },
    "Valencia": {
        "results": "https://www.espn.com/football/team/results/_/id/94/valencia"
    },
    "Villarreal": {
        "results": "https://www.espn.com/football/team/results/_/id/102/villarreal"
    },
    "AC Milan": {
        "results": "https://www.espn.com/football/team/results/_/id/103/ac-milan"
    },
    "AS Roma": {
        "results": "https://www.espn.com/football/team/results/_/id/104/as-roma"
    },
    "Atalanta": {
        "results": "https://www.espn.com/football/team/results/_/id/105/atalanta"
    },
    "Bologna": {
        "results": "https://www.espn.com/football/team/results/_/id/107/bologna"
    },
    "Cagliari": {
        "results": "https://www.espn.com/football/team/results/_/id/2925/cagliari"
    },
    "Como": {
        "results": "https://www.espn.com/football/team/results/_/id/2572/como"
    },
    "Cremonese": {
        "results": "https://www.espn.com/football/team/results/_/id/4050/cremonese"
    },
    "Fiorentina": {
        "results": "https://www.espn.com/football/team/results/_/id/109/fiorentina"
    },
    "Genoa": {
        "results": "https://www.espn.com/football/team/results/_/id/3263/genoa"
    },
    "Hellas Verona": {
        "results": "https://www.espn.com/football/team/results/_/id/119/hellas-verona"
    },
    "Internazionale": {
        "results": "https://www.espn.com/football/team/results/_/id/110/internazionale"
    },
    "Juventus": {
        "results": "https://www.espn.com/football/team/results/_/id/111/juventus"
    },
    "Lazio": {
        "results": "https://www.espn.com/football/team/results/_/id/112/lazio"
    },
    "Lecce": {
        "results": "https://www.espn.com/football/team/results/_/id/113/lecce"
    },
    "Napoli": {
        "results": "https://www.espn.com/football/team/results/_/id/114/napoli"
    },
    "Parma": {
        "results": "https://www.espn.com/football/team/results/_/id/115/parma"
    },
    "Pisa": {
        "results": "https://www.espn.com/football/team/results/_/id/3956/pisa"
    },
    "Sassuolo": {
        "results": "https://www.espn.com/football/team/results/_/id/3997/sassuolo"
    },
    "Torino": {
        "results": "https://www.espn.com/football/team/results/_/id/239/torino"
    },
    "Udinese": {
        "results": "https://www.espn.com/football/team/results/_/id/118/udinese"
    },
    "1. FC Heidenheim 1846": {
        "results": "https://www.espn.com/football/team/results/_/id/6418/1-fc-heidenheim-1846"
    },
    "1. FC Union Berlin": {
        "results": "https://www.espn.com/football/team/results/_/id/598/1-fc-union-berlin"
    },
    "Bayer Leverkusen": {
        "results": "https://www.espn.com/football/team/results/_/id/131/bayer-leverkusen"
    },
    "Bayern Munich": {
        "results": "https://www.espn.com/football/team/results/_/id/132/bayern-munich"
    },
    "Borussia Dortmund": {
        "results": "https://www.espn.com/football/team/results/_/id/124/borussia-dortmund"
    },
    "Borussia Mönchengladbach": {
        "results": "https://www.espn.com/football/team/results/_/id/268/borussia-monchengladbach"
    },
    "Eintracht Frankfurt": {
        "results": "https://www.espn.com/football/team/results/_/id/125/eintracht-frankfurt"
    },
    "FC Augsburg": {
        "results": "https://www.espn.com/football/team/results/_/id/3841/fc-augsburg"
    },
    "Holstein Kiel": {
        "results": "https://www.espn.com/football/team/results/_/id/7884/holstein-kiel"
    },
    "Mainz": {
        "results": "https://www.espn.com/football/team/results/_/id/2950/mainz"
    },
    "RB Leipzig": {
        "results": "https://www.espn.com/football/team/results/_/id/11420/rb-leipzig"
    },
    "SC Freiburg": {
        "results": "https://www.espn.com/football/team/results/_/id/126/sc-freiburg"
    },
    "St. Pauli": {
        "results": "https://www.espn.com/football/team/results/_/id/270/st-pauli"
    },
    "TSG Hoffenheim": {
        "results": "https://www.espn.com/football/team/results/_/id/7911/tsg-hoffenheim"
    },
    "VfB Stuttgart": {
        "results": "https://www.espn.com/football/team/results/_/id/134/vfb-stuttgart"
    },
    "VfL Bochum": {
        "results": "https://www.espn.com/football/team/results/_/id/121/vfl-bochum"
    },
    "VfL Wolfsburg": {
        "results": "https://www.espn.com/football/team/results/_/id/138/vfl-wolfsburg"
    },
    "Werder Bremen": {
        "results": "https://www.espn.com/football/team/results/_/id/137/werder-bremen"
    },
    "AJ Auxerre": {
        "results": "https://www.espn.com/football/team/results/_/id/172/aj-auxerre"
    },
    "AS Monaco": {
        "results": "https://www.espn.com/football/team/results/_/id/174/as-monaco"
    },
    "Angers": {
        "results": "https://www.espn.com/football/team/results/_/id/7868/angers"
    },
    "Brest": {
        "results": "https://www.espn.com/football/team/results/_/id/6997/brest"
    },
    "Le Havre AC": {
        "results": "https://www.espn.com/football/team/results/_/id/3236/le-havre-ac"
    },
    "Lens": {
        "results": "https://www.espn.com/football/team/results/_/id/175/lens"
    },
    "Lille": {
        "results": "https://www.espn.com/football/team/results/_/id/166/lille"
    },
    "Lyon": {
        "results": "https://www.espn.com/football/team/results/_/id/167/lyon"
    },
    "Marseille": {
        "results": "https://www.espn.com/football/team/results/_/id/176/marseille"
    },
    "Montpellier": {
        "results": "https://www.espn.com/football/team/results/_/id/274/montpellier"
    },
    "Nantes": {
        "results": "https://www.espn.com/football/team/results/_/id/165/nantes"
    },
    "Nice": {
        "results": "https://www.espn.com/football/team/results/_/id/2502/nice"
    },
    "Paris Saint-Germain": {
        "results": "https://www.espn.com/football/team/results/_/id/160/paris-saint-germain"
    },
    "Saint-Étienne": {
        "results": "https://www.espn.com/football/team/results/_/id/178/saint-etienne"
    },
    "Stade Rennais": {
        "results": "https://www.espn.com/football/team/results/_/id/169/stade-rennais"
    },
    "Stade de Reims": {
        "results": "https://www.espn.com/football/team/results/_/id/3243/stade-de-reims"
    },
    "Strasbourg": {
        "results": "https://www.espn.com/football/team/results/_/id/180/strasbourg"
    },
    "Toulouse": {
        "results": "https://www.espn.com/football/team/results/_/id/179/toulouse"
    },
    "Atlanta United FC": {
        "results": "https://www.espn.com/football/team/results/_/id/18418/atlanta-united-fc"
    },
    "Austin FC": {
        "results": "https://www.espn.com/football/team/results/_/id/20906/austin-fc"
    },
    "CF Montréal": {
        "results": "https://www.espn.com/football/team/results/_/id/9720/cf-montreal"
    },
    "Charlotte FC": {
        "results": "https://www.espn.com/football/team/results/_/id/21300/charlotte-fc"
    },
    "Chicago Fire FC": {
        "results": "https://www.espn.com/football/team/results/_/id/182/chicago-fire-fc"
    },
    "Colorado Rapids": {
        "results": "https://www.espn.com/football/team/results/_/id/184/colorado-rapids"
    },
    "Columbus Crew": {
        "results": "https://www.espn.com/football/team/results/_/id/183/columbus-crew"
    },
    "D.C. United": {
        "results": "https://www.espn.com/football/team/results/_/id/193/dc-united"
    },
    "FC Cincinnati": {
        "results": "https://www.espn.com/football/team/results/_/id/18267/fc-cincinnati"
    },
    "FC Dallas": {
        "results": "https://www.espn.com/football/team/results/_/id/185/fc-dallas"
    },
    "Houston Dynamo FC": {
        "results": "https://www.espn.com/football/team/results/_/id/6077/houston-dynamo-fc"
    },
    "Inter Miami CF": {
        "results": "https://www.espn.com/football/team/results/_/id/20232/inter-miami-cf"
    },
    "LA Galaxy": {
        "results": "https://www.espn.com/football/team/results/_/id/187/la-galaxy"
    },
    "LAFC": {
        "results": "https://www.espn.com/football/team/results/_/id/18966/lafc"
    },
    "Minnesota United FC": {
        "results": "https://www.espn.com/football/team/results/_/id/17362/minnesota-united-fc"
    },
    "Nashville SC": {
        "results": "https://www.espn.com/football/team/results/_/id/18986/nashville-sc"
    },
    "New England Revolution": {
        "results": "https://www.espn.com/football/team/results/_/id/189/new-england-revolution"
    },
    "New York City FC": {
        "results": "https://www.espn.com/football/team/results/_/id/17606/new-york-city-fc"
    },
    "New York Red Bulls": {
        "results": "https://www.espn.com/football/team/results/_/id/190/new-york-red-bulls"
    },
    "Orlando City SC": {
        "results": "https://www.espn.com/football/team/results/_/id/12011/orlando-city-sc"
    },
    "Philadelphia Union": {
        "results": "https://www.espn.com/football/team/results/_/id/10739/philadelphia-union"
    },
    "Portland Timbers": {
        "results": "https://www.espn.com/football/team/results/_/id/9723/portland-timbers"
    },
    "Real Salt Lake": {
        "results": "https://www.espn.com/football/team/results/_/id/4771/real-salt-lake"
    },
    "San Diego FC": {
        "results": "https://www.espn.com/football/team/results/_/id/22529/san-diego-fc"
    },
    "San Jose Earthquakes": {
        "results": "https://www.espn.com/football/team/results/_/id/191/san-jose-earthquakes"
    },
    "Seattle Sounders FC": {
        "results": "https://www.espn.com/football/team/results/_/id/9726/seattle-sounders-fc"
    },
    "Sporting Kansas City": {
        "results": "https://www.espn.com/football/team/results/_/id/186/sporting-kansas-city"
    },
    "St. Louis CITY SC": {
        "results": "https://www.espn.com/football/team/results/_/id/21812/st-louis-city-sc"
    },
    "Toronto FC": {
        "results": "https://www.espn.com/football/team/results/_/id/7318/toronto-fc"
    },
    "Vancouver Whitecaps": {
        "results": "https://www.espn.com/football/team/results/_/id/9727/vancouver-whitecaps"
    },
    "América": {
        "results": "https://www.espn.com/football/team/results/_/id/227/america"
    },
    "Atlas": {
        "results": "https://www.espn.com/football/team/results/_/id/216/atlas"
    },
    "Atlético de San Luis": {
        "results": "https://www.espn.com/football/team/results/_/id/15720/atletico-de-san-luis"
    },
    "Cruz Azul": {
        "results": "https://www.espn.com/football/team/results/_/id/218/cruz-azul"
    },
    "FC Juarez": {
        "results": "https://www.espn.com/football/team/results/_/id/17851/fc-juarez"
    },
    "Guadalajara": {
        "results": "https://www.espn.com/football/team/results/_/id/219/guadalajara"
    },
    "León": {
        "results": "https://www.espn.com/football/team/results/_/id/228/leon"
    },
    "Mazatlán FC": {
        "results": "https://www.espn.com/football/team/results/_/id/20702/mazatlan-fc"
    },
    "Monterrey": {
        "results": "https://www.espn.com/football/team/results/_/id/220/monterrey"
    },
    "Necaxa": {
        "results": "https://www.espn.com/football/team/results/_/id/229/necaxa"
    },
    "Pachuca": {
        "results": "https://www.espn.com/football/team/results/_/id/234/pachuca"
    },
    "Puebla": {
        "results": "https://www.espn.com/football/team/results/_/id/231/puebla"
    },
    "Pumas UNAM": {
        "results": "https://www.espn.com/football/team/results/_/id/233/pumas-unam"
    },
    "Querétaro": {
        "results": "https://www.espn.com/football/team/results/_/id/222/queretaro"
    },
    "Santos": {
        "results": "https://www.espn.com/football/team/results/_/id/225/santos"
    },
    "Tigres UANL": {
        "results": "https://www.espn.com/football/team/results/_/id/232/tigres-uanl"
    },
    "Tijuana": {
        "results": "https://www.espn.com/football/team/results/_/id/10125/tijuana"
    },
    "Toluca": {
        "results": "https://www.espn.com/football/team/results/_/id/223/toluca"
    },
    "AZ Alkmaar": {
        "results": "https://www.espn.com/football/team/results/_/id/140/az-alkmaar"
    },
    "Ajax Amsterdam": {
        "results": "https://www.espn.com/football/team/results/_/id/139/ajax-amsterdam"
    },
    "Almere City": {
        "results": "https://www.espn.com/football/team/results/_/id/5291/almere-city"
    },
    "FC Groningen": {
        "results": "https://www.espn.com/football/team/results/_/id/145/fc-groningen"
    },
    "FC Twente": {
        "results": "https://www.espn.com/football/team/results/_/id/152/fc-twente"
    },
    "FC Utrecht": {
        "results": "https://www.espn.com/football/team/results/_/id/153/fc-utrecht"
    },
    "Feyenoord Rotterdam": {
        "results": "https://www.espn.com/football/team/results/_/id/142/feyenoord-rotterdam"
    },
    "Fortuna Sittard": {
        "results": "https://www.espn.com/football/team/results/_/id/143/fortuna-sittard"
    },
    "Go Ahead Eagles": {
        "results": "https://www.espn.com/football/team/results/_/id/3706/go-ahead-eagles"
    },
    "Heerenveen": {
        "results": "https://www.espn.com/football/team/results/_/id/146/heerenveen"
    },
    "Heracles Almelo": {
        "results": "https://www.espn.com/football/team/results/_/id/3708/heracles-almelo"
    },
    "NAC Breda": {
        "results": "https://www.espn.com/football/team/results/_/id/141/nac-breda"
    },
    "NEC Nijmegen": {
        "results": "https://www.espn.com/football/team/results/_/id/147/nec-nijmegen"
    },
    "PEC Zwolle": {
        "results": "https://www.espn.com/football/team/results/_/id/2565/pec-zwolle"
    },
    "PSV Eindhoven": {
        "results": "https://www.espn.com/football/team/results/_/id/148/psv-eindhoven"
    },
    "RKC Waalwijk": {
        "results": "https://www.espn.com/football/team/results/_/id/155/rkc-waalwijk"
    },
    "Sparta Rotterdam": {
        "results": "https://www.espn.com/football/team/results/_/id/151/sparta-rotterdam"
    },
    "Willem II": {
        "results": "https://www.espn.com/football/team/results/_/id/156/willem-ii"
    },
    "AVS": {
        "results": "https://www.espn.com/football/team/results/_/id/22064/avs"
    },
    "Arouca": {
        "results": "https://www.espn.com/football/team/results/_/id/15784/arouca"
    },
    "Benfica": {
        "results": "https://www.espn.com/football/team/results/_/id/1929/benfica"
    },
    "Boavista": {
        "results": "https://www.espn.com/football/team/results/_/id/2256/boavista"
    },
    "Braga": {
        "results": "https://www.espn.com/football/team/results/_/id/2994/braga"
    },
    "C.D. Nacional": {
        "results": "https://www.espn.com/football/team/results/_/id/3472/cd-nacional"
    },
    "Casa Pia": {
        "results": "https://www.espn.com/football/team/results/_/id/21581/casa-pia"
    },
    "Estoril": {
        "results": "https://www.espn.com/football/team/results/_/id/12216/estoril"
    },
    "Estrela": {
        "results": "https://www.espn.com/football/team/results/_/id/21610/estrela"
    },
    "FC Famalicao": {
        "results": "https://www.espn.com/football/team/results/_/id/12698/fc-famalicao"
    },
    "FC Porto": {
        "results": "https://www.espn.com/football/team/results/_/id/437/fc-porto"
    },
    "Gil Vicente": {
        "results": "https://www.espn.com/football/team/results/_/id/3699/gil-vicente"
    },
    "Guimaraes": {
        "results": "https://www.espn.com/football/team/results/_/id/5309/guimaraes"
    },
    "Moreirense": {
        "results": "https://www.espn.com/football/team/results/_/id/3696/moreirense"
    },
    "Rio Ave": {
        "results": "https://www.espn.com/football/team/results/_/id/3822/rio-ave"
    },
    "SC Farense": {
        "results": "https://www.espn.com/football/team/results/_/id/20740/sc-farense"
    },
    "Santa Clara": {
        "results": "https://www.espn.com/football/team/results/_/id/12215/santa-clara"
    },
    "Sporting CP": {
        "results": "https://www.espn.com/football/team/results/_/id/2250/sporting-cp"
    },
    "Al Ahli": {
        "results": "https://www.espn.com/football/team/results/_/id/8346/al-ahli"
    },
    "Al Ettifaq": {
        "results": "https://www.espn.com/football/team/results/_/id/8363/al-ettifaq"
    },
    "Al Fateh": {
        "results": "https://www.espn.com/football/team/results/_/id/13033/al-fateh"
    },
    "Al Fayha": {
        "results": "https://www.espn.com/football/team/results/_/id/21827/al-fayha"
    },
    "Al Hilal": {
        "results": "https://www.espn.com/football/team/results/_/id/929/al-hilal"
    },
    "Al Ittihad": {
        "results": "https://www.espn.com/football/team/results/_/id/2276/al-ittihad"
    },
    "Al Khaleej": {
        "results": "https://www.espn.com/football/team/results/_/id/21829/al-khaleej"
    },
    "Al Kholood": {
        "results": "https://www.espn.com/football/team/results/_/id/22028/al-kholood"
    },
    "Al Nassr": {
        "results": "https://www.espn.com/football/team/results/_/id/817/al-nassr"
    },
    "Al Okhdood": {
        "results": "https://www.espn.com/football/team/results/_/id/21966/al-okhdood"
    },
    "Al Orobah": {
        "results": "https://www.espn.com/football/team/results/_/id/22029/al-orobah"
    },
    "Al Qadsiah": {
        "results": "https://www.espn.com/football/team/results/_/id/22022/al-qadsiah"
    },
    "Al Raed": {
        "results": "https://www.espn.com/football/team/results/_/id/21834/al-raed"
    },
    "Al Riyadh": {
        "results": "https://www.espn.com/football/team/results/_/id/21965/al-riyadh"
    },
    "Al Shabab": {
        "results": "https://www.espn.com/football/team/results/_/id/793/al-shabab"
    },
    "Al Taawoun": {
        "results": "https://www.espn.com/football/team/results/_/id/18459/al-taawoun"
    },
    "Al Wehda": {
        "results": "https://www.espn.com/football/team/results/_/id/21835/al-wehda"
    },
    "Damac": {
        "results": "https://www.espn.com/football/team/results/_/id/21828/damac"
    },
    "Beijing Guoan": {
        "results": "https://www.espn.com/football/team/results/_/id/2052/beijing-guoan"
    },
    "Changchun Yatai": {
        "results": "https://www.espn.com/football/team/results/_/id/8225/changchun-yatai"
    },
    "Chengdu Rongcheng": {
        "results": "https://www.espn.com/football/team/results/_/id/21355/chengdu-rongcheng"
    },
    "Dalian Yingbo": {
        "results": "https://www.espn.com/football/team/results/_/id/22537/dalian-yingbo"
    },
    "Henan Songshan Longmen": {
        "results": "https://www.espn.com/football/team/results/_/id/8240/henan-songshan-longmen"
    },
    "Meizhou Hakka": {
        "results": "https://www.espn.com/football/team/results/_/id/21507/meizhou-hakka"
    },
    "Qingdao Hainiu": {
        "results": "https://www.espn.com/football/team/results/_/id/21910/qingdao-hainiu"
    },
    "Qingdao West Coast": {
        "results": "https://www.espn.com/football/team/results/_/id/22198/qingdao-west-coast"
    },
    "Shandong Taishan": {
        "results": "https://www.espn.com/football/team/results/_/id/7521/shandong-taishan"
    },
    "Shanghai Port": {
        "results": "https://www.espn.com/football/team/results/_/id/15515/shanghai-port"
    },
    "Shanghai Shenhua": {
        "results": "https://www.espn.com/football/team/results/_/id/977/shanghai-shenhua"
    },
    "Shenzhen Xinpengcheng": {
        "results": "https://www.espn.com/football/team/results/_/id/22199/shenzhen-xinpengcheng"
    },
    "Tianjin Jinmen Tiger": {
        "results": "https://www.espn.com/football/team/results/_/id/8239/tianjin-jinmen-tiger"
    },
    "Wuhan Three Towns": {
        "results": "https://www.espn.com/football/team/results/_/id/21506/wuhan-three-towns"
    },
    "Yunnan Yukun": {
        "results": "https://www.espn.com/football/team/results/_/id/22536/yunnan-yukun"
    },
    "Zhejiang Professional FC": {
        "results": "https://www.espn.com/football/team/results/_/id/18203/zhejiang-professional-fc"
    },
    "Albirex Niigata": {
        "results": "https://www.espn.com/football/team/results/_/id/7113/albirex-niigata"
    },
    "Avispa Fukuoka": {
        "results": "https://www.espn.com/football/team/results/_/id/7107/avispa-fukuoka"
    },
    "Cerezo Osaka": {
        "results": "https://www.espn.com/football/team/results/_/id/7109/cerezo-osaka"
    },
    "FC Tokyo": {
        "results": "https://www.espn.com/football/team/results/_/id/3384/fc-tokyo"
    },
    "Fagiano Okayama": {
        "results": "https://www.espn.com/football/team/results/_/id/22522/fagiano-okayama"
    },
    "Gamba Osaka": {
        "results": "https://www.espn.com/football/team/results/_/id/7102/gamba-osaka"
    },
    "Kashima Antlers": {
        "results": "https://www.espn.com/football/team/results/_/id/7115/kashima-antlers"
    },
    "Kashiwa Reysol": {
        "results": "https://www.espn.com/football/team/results/_/id/7476/kashiwa-reysol"
    },
    "Kawasaki Frontale": {
        "results": "https://www.espn.com/football/team/results/_/id/7112/kawasaki-frontale"
    },
    "Kyoto Sanga": {
        "results": "https://www.espn.com/football/team/results/_/id/21361/kyoto-sanga"
    },
    "Machida Zelvia": {
        "results": "https://www.espn.com/football/team/results/_/id/22167/machida-zelvia"
    },
    "Nagoya Grampus": {
        "results": "https://www.espn.com/football/team/results/_/id/7108/nagoya-grampus"
    },
    "Sanfrecce Hiroshima": {
        "results": "https://www.espn.com/football/team/results/_/id/7114/sanfrecce-hiroshima"
    },
    "Shimizu S-Pulse": {
        "results": "https://www.espn.com/football/team/results/_/id/7104/shimizu-s-pulse"
    },
    "Shonan Bellmare": {
        "results": "https://www.espn.com/football/team/results/_/id/6902/shonan-bellmare"
    },
    "Tokyo Verdy 1969": {
        "results": "https://www.espn.com/football/team/results/_/id/3393/tokyo-verdy-1969"
    },
    "Urawa Red Diamonds": {
        "results": "https://www.espn.com/football/team/results/_/id/3385/urawa-red-diamonds"
    },
    "Vissel Kobe": {
        "results": "https://www.espn.com/football/team/results/_/id/7477/vissel-kobe"
    },
    "Yokohama F. Marinos": {
        "results": "https://www.espn.com/football/team/results/_/id/7116/yokohama-f-marinos"
    },
    "Yokohama FC": {
        "results": "https://www.espn.com/football/team/results/_/id/7145/yokohama-fc"
    },
    "Beitar Jerusalem": {
        "results": "https://www.espn.com/football/team/results/_/id/5218/beitar-jerusalem"
    },
    "Bnei Sakhnin": {
        "results": "https://www.espn.com/football/team/results/_/id/8329/bnei-sakhnin"
    },
    "Hapoel Be'er": {
        "results": "https://www.espn.com/football/team/results/_/id/13083/hapoel-beer"
    },
    "Hapoel Hadera": {
        "results": "https://www.espn.com/football/team/results/_/id/19255/hapoel-hadera"
    },
    "Hapoel Haifa": {
        "results": "https://www.espn.com/football/team/results/_/id/9577/hapoel-haifa"
    },
    "Hapoel Jerusalem": {
        "results": "https://www.espn.com/football/team/results/_/id/20970/hapoel-jerusalem"
    },
    "Hapoel Kiryat Shmona": {
        "results": "https://www.espn.com/football/team/results/_/id/8327/hapoel-kiryat-shmona"
    },
    "Ironi Tiberias": {
        "results": "https://www.espn.com/football/team/results/_/id/22311/ironi-tiberias"
    },
    "Maccabi Haifa": {
        "results": "https://www.espn.com/football/team/results/_/id/611/maccabi-haifa"
    },
    "Maccabi Netanya": {
        "results": "https://www.espn.com/football/team/results/_/id/5945/maccabi-netanya"
    },
    "Maccabi Petah-Tikva": {
        "results": "https://www.espn.com/football/team/results/_/id/2983/maccabi-petah-tikva"
    },
    "Maccabi Raina": {
        "results": "https://www.espn.com/football/team/results/_/id/21517/maccabi-raina"
    },
    "Maccabi Tel-Aviv": {
        "results": "https://www.espn.com/football/team/results/_/id/524/maccabi-tel-aviv"
    },
    "Moadon Sport Ashdod": {
        "results": "https://www.espn.com/football/team/results/_/id/5269/moadon-sport-ashdod"
    },
    "AEK Athens": {
        "results": "https://www.espn.com/football/team/results/_/id/887/aek-athens"
    },
    "Aris": {
        "results": "https://www.espn.com/football/team/results/_/id/11553/aris"
    },
    "Asteras Tripoli": {
        "results": "https://www.espn.com/football/team/results/_/id/8354/asteras-tripoli"
    },
    "Athens Kallithea": {
        "results": "https://www.espn.com/football/team/results/_/id/22325/athens-kallithea"
    },
    "Atromitos": {
        "results": "https://www.espn.com/football/team/results/_/id/6790/atromitos"
    },
    "Lamia": {
        "results": "https://www.espn.com/football/team/results/_/id/18814/lamia"
    },
    "Levadiakos": {
        "results": "https://www.espn.com/football/team/results/_/id/5276/levadiakos"
    },
    "OFI Crete": {
        "results": "https://www.espn.com/football/team/results/_/id/1010/ofi-crete"
    },
    "Olympiacos": {
        "results": "https://www.espn.com/football/team/results/_/id/435/olympiacos"
    },
    "PAOK Salonika": {
        "results": "https://www.espn.com/football/team/results/_/id/605/paok-salonika"
    },
    "Panathinaikos": {
        "results": "https://www.espn.com/football/team/results/_/id/443/panathinaikos"
    },
    "Panetolikos": {
        "results": "https://www.espn.com/football/team/results/_/id/11431/panetolikos"
    },
    "Panserraikos FC": {
        "results": "https://www.espn.com/football/team/results/_/id/21970/panserraikos-fc"
    },
    "Volos NFC": {
        "results": "https://www.espn.com/football/team/results/_/id/20043/volos-nfc"
    },
    "Anderlecht": {
        "results": "https://www.espn.com/football/team/results/_/id/441/anderlecht"
    },
    "Antwerp": {
        "results": "https://www.espn.com/football/team/results/_/id/17544/antwerp"
    },
    "Beerschot": {
        "results": "https://www.espn.com/football/team/results/_/id/991/beerschot"
    },
    "Cercle Brugge KSV": {
        "results": "https://www.espn.com/football/team/results/_/id/3610/cercle-brugge-ksv"
    },
    "Club Brugge": {
        "results": "https://www.espn.com/football/team/results/_/id/570/club-brugge"
    },
    "Dender": {
        "results": "https://www.espn.com/football/team/results/_/id/7878/dender"
    },
    "KAA Gent": {
        "results": "https://www.espn.com/football/team/results/_/id/3611/kaa-gent"
    },
    "KV Kortrijk": {
        "results": "https://www.espn.com/football/team/results/_/id/5786/kv-kortrijk"
    },
    "KV Mechelen": {
        "results": "https://www.espn.com/football/team/results/_/id/7879/kv-mechelen"
    },
    "KVC Westerlo": {
        "results": "https://www.espn.com/football/team/results/_/id/606/kvc-westerlo"
    },
    "Oud-Heverlee Leuven": {
        "results": "https://www.espn.com/football/team/results/_/id/5579/oud-heverlee-leuven"
    },
    "Racing Genk": {
        "results": "https://www.espn.com/football/team/results/_/id/938/racing-genk"
    },
    "Royal Charleroi SC": {
        "results": "https://www.espn.com/football/team/results/_/id/3616/royal-charleroi-sc"
    },
    "Sint-Truidense": {
        "results": "https://www.espn.com/football/team/results/_/id/936/sint-truidense"
    },
    "Standard Liege": {
        "results": "https://www.espn.com/football/team/results/_/id/559/standard-liege"
    },
    "Union St.-Gilloise": {
        "results": "https://www.espn.com/football/team/results/_/id/5807/union-st-gilloise"
    },
    "Akhmat Grozny": {
        "results": "https://www.espn.com/football/team/results/_/id/2991/akhmat-grozny"
    },
    "Akron Tolyatti": {
        "results": "https://www.espn.com/football/team/results/_/id/22271/akron-tolyatti"
    },
    "CSKA Moscow": {
        "results": "https://www.espn.com/football/team/results/_/id/1963/cska-moscow"
    },
    "Dinamo Moscow": {
        "results": "https://www.espn.com/football/team/results/_/id/596/dinamo-moscow"
    },
    "Dynamo Makhachkala": {
        "results": "https://www.espn.com/football/team/results/_/id/22300/dynamo-makhachkala"
    },
    "FC Khimki": {
        "results": "https://www.espn.com/football/team/results/_/id/7424/fc-khimki"
    },
    "Fakel Voronezh": {
        "results": "https://www.espn.com/football/team/results/_/id/21539/fakel-voronezh"
    },
    "Gazovik Orenburg": {
        "results": "https://www.espn.com/football/team/results/_/id/18285/gazovik-orenburg"
    },
    "Krasnodar": {
        "results": "https://www.espn.com/football/team/results/_/id/11336/krasnodar"
    },
    "Krylia Sovetov": {
        "results": "https://www.espn.com/football/team/results/_/id/3850/krylia-sovetov"
    },
    "Lokomotiv Moscow": {
        "results": "https://www.espn.com/football/team/results/_/id/442/lokomotiv-moscow"
    },
    "Nizhny Novgorod": {
        "results": "https://www.espn.com/football/team/results/_/id/13150/nizhny-novgorod"
    },
    "Rostov": {
        "results": "https://www.espn.com/football/team/results/_/id/3852/rostov"
    },
    "Rubin Kazan": {
        "results": "https://www.espn.com/football/team/results/_/id/3851/rubin-kazan"
    },
    "Spartak Moscow": {
        "results": "https://www.espn.com/football/team/results/_/id/1941/spartak-moscow"
    },
    "Zenit St Petersburg": {
        "results": "https://www.espn.com/football/team/results/_/id/2533/zenit-st-petersburg"
    },
    "FC Basel": {
        "results": "https://www.espn.com/football/team/results/_/id/989/fc-basel"
    },
    "FC Lugano": {
        "results": "https://www.espn.com/football/team/results/_/id/7672/fc-lugano"
    },
    "FC Luzern": {
        "results": "https://www.espn.com/football/team/results/_/id/7640/fc-luzern"
    },
    "FC Sion": {
        "results": "https://www.espn.com/football/team/results/_/id/3076/fc-sion"
    },
    "FC Zürich": {
        "results": "https://www.espn.com/football/team/results/_/id/3019/fc-zurich"
    },
    "Grasshoppers": {
        "results": "https://www.espn.com/football/team/results/_/id/492/grasshoppers"
    },
    "Lausanne Sports": {
        "results": "https://www.espn.com/football/team/results/_/id/11551/lausanne-sports"
    },
    "Servette": {
        "results": "https://www.espn.com/football/team/results/_/id/20032/servette"
    },
    "St. Gallen": {
        "results": "https://www.espn.com/football/team/results/_/id/557/st-gallen"
    },
    "Winterthur": {
        "results": "https://www.espn.com/football/team/results/_/id/20996/winterthur"
    },
    "Young Boys": {
        "results": "https://www.espn.com/football/team/results/_/id/2722/young-boys"
    },
    "Yverdon": {
        "results": "https://www.espn.com/football/team/results/_/id/21538/yverdon"
    },
    "Adana Demirspor": {
        "results": "https://www.espn.com/football/team/results/_/id/20765/adana-demirspor"
    },
    "Alanyaspor": {
        "results": "https://www.espn.com/football/team/results/_/id/9078/alanyaspor"
    },
    "Antalyaspor": {
        "results": "https://www.espn.com/football/team/results/_/id/3794/antalyaspor"
    },
    "Besiktas": {
        "results": "https://www.espn.com/football/team/results/_/id/1895/besiktas"
    },
    "Bodrum FK": {
        "results": "https://www.espn.com/football/team/results/_/id/22321/bodrum-fk"
    },
    "Caykur Rizespor": {
        "results": "https://www.espn.com/football/team/results/_/id/7656/caykur-rizespor"
    },
    "Eyupspor": {
        "results": "https://www.espn.com/football/team/results/_/id/20729/eyupspor"
    },
    "Fenerbahce": {
        "results": "https://www.espn.com/football/team/results/_/id/436/fenerbahce"
    },
    "Galatasaray": {
        "results": "https://www.espn.com/football/team/results/_/id/432/galatasaray"
    },
    "Gaziantep FK": {
        "results": "https://www.espn.com/football/team/results/_/id/20070/gaziantep-fk"
    },
    "Goztepe": {
        "results": "https://www.espn.com/football/team/results/_/id/789/goztepe"
    },
    "Hatayspor": {
        "results": "https://www.espn.com/football/team/results/_/id/20737/hatayspor"
    },
    "Istanbul Basaksehir": {
        "results": "https://www.espn.com/football/team/results/_/id/7914/istanbul-basaksehir"
    },
    "Kasimpasa": {
        "results": "https://www.espn.com/football/team/results/_/id/6870/kasimpasa"
    },
    "Kayserispor": {
        "results": "https://www.espn.com/football/team/results/_/id/3643/kayserispor"
    },
    "Konyaspor": {
        "results": "https://www.espn.com/football/team/results/_/id/7648/konyaspor"
    },
    "Samsunspor": {
        "results": "https://www.espn.com/football/team/results/_/id/11429/samsunspor"
    },
    "Sivasspor": {
        "results": "https://www.espn.com/football/team/results/_/id/3691/sivasspor"
    },
    "Trabzonspor": {
        "results": "https://www.espn.com/football/team/results/_/id/997/trabzonspor"
    },
    "Alianza FC": {
            "results": "https://www.espn.com/football/team/results/_/id/9761/alianza-fc"
        },
        "América de Cali": {
            "results": "https://www.espn.com/football/team/results/_/id/8109/america-de-cali"
        },
        "Atlético Junior": {
            "results": "https://www.espn.com/football/team/results/_/id/4815/atletico-junior"
        },
        "Atlético Nacional": {
            "results": "https://www.espn.com/football/team/results/_/id/5264/atletico-nacional"
        },
        "Boyacá Chicó": {
            "results": "https://www.espn.com/football/team/results/_/id/5480/boyaca-chico"
        },
        "Bucaramanga": {
            "results": "https://www.espn.com/football/team/results/_/id/6137/bucaramanga"
        },
        "Deportes Tolima": {
            "results": "https://www.espn.com/football/team/results/_/id/5489/deportes-tolima"
        },
        "Deportivo Cali": {
            "results": "https://www.espn.com/football/team/results/_/id/2672/deportivo-cali"
        },
        "Deportivo Pasto": {
            "results": "https://www.espn.com/football/team/results/_/id/5485/deportivo-pasto"
        },
        "Deportivo Pereira": {
            "results": "https://www.espn.com/football/team/results/_/id/5486/deportivo-pereira"
        },
        "Envigado": {
            "results": "https://www.espn.com/football/team/results/_/id/5481/envigado"
        },
        "Fortaleza CEIF": {
            "results": "https://www.espn.com/football/team/results/_/id/4928/fortaleza-ceif"
        },
        "Independiente Medellín": {
            "results": "https://www.espn.com/football/team/results/_/id/2690/independiente-medellin"
        },
        "Independiente Santa Fe": {
            "results": "https://www.espn.com/football/team/results/_/id/5488/independiente-santa-fe"
        },
        "La Equidad": {
            "results": "https://www.espn.com/football/team/results/_/id/7445/la-equidad"
        },
        "Llaneros": {
            "results": "https://www.espn.com/football/team/results/_/id/7915/llaneros"
        },
        "Millonarios": {
            "results": "https://www.espn.com/football/team/results/_/id/5484/millonarios"
        },
        "Once Caldas": {
            "results": "https://www.espn.com/football/team/results/_/id/2919/once-caldas"
        },
        "Unión Magdalena": {
            "results": "https://www.espn.com/football/team/results/_/id/17374/union-magdalena"
        },
        "Águilas Doradas": {
            "results": "https://www.espn.com/football/team/results/_/id/9762/aguilas-doradas"
        },
        "Amazonas": {
            "results": "https://africa.espn.com/football/team/results/_/id/21888/amazonas"
        },
        "America Mineiro": {
            "results": "https://africa.espn.com/football/team/results/_/id/6154/america-mineiro"
        },
        "Athletic": {
            "results": "https://africa.espn.com/football/team/results/_/id/20851/athletic"
        },
        "Athletico Paranaense": {
            "results": "https://africa.espn.com/football/team/results/_/id/3458/athletico-paranaense"
        },
        "Atletico Goianiense": {
            "results": "https://africa.espn.com/football/team/results/_/id/10357/atletico-goianiense"
        },
        "Avai": {
            "results": "https://africa.espn.com/football/team/results/_/id/9966/avai"
        },
        "Botafogo Sp": {
            "results": "https://africa.espn.com/football/team/results/_/id/10281/botafogo-sp"
        },
        "Crb": {
            "results": "https://africa.espn.com/football/team/results/_/id/9970/crb"
        },
        "Chapecoense": {
            "results": "https://africa.espn.com/football/team/results/_/id/9318/chapecoense"
        },
        "Coritiba": {
            "results": "https://africa.espn.com/football/team/results/_/id/3456/coritiba"
        },
        "Criciuma": {
            "results": "https://africa.espn.com/football/team/results/_/id/9971/criciuma"
        },
        "Cuiaba": {
            "results": "https://africa.espn.com/football/team/results/_/id/17313/cuiaba"
        },
        "Ferroviaria": {
            "results": "https://africa.espn.com/football/team/results/_/id/18126/ferroviaria"
        },
        "Goias": {
            "results": "https://africa.espn.com/football/team/results/_/id/3395/goias"
        },
        "Novorizontino": {
            "results": "https://africa.espn.com/football/team/results/_/id/18127/novorizontino"
        },
        "Operario PR": {
            "results": "https://africa.espn.com/football/team/results/_/id/18187/operario-pr"
        },
        "Paysandu": {
            "results": "https://africa.espn.com/football/team/results/_/id/15424/paysandu"
        },
        "Remo": {
            "results": "https://africa.espn.com/football/team/results/_/id/4936/remo"
        },
        "Vila Nova": {
            "results": "https://africa.espn.com/football/team/results/_/id/9973/vila-nova"
        },
        "Volta Redonda": {
            "results": "https://africa.espn.com/football/team/results/_/id/4806/volta-redonda"
        },
        "Audax Italiano": {
            "results": "https://africa.espn.com/football/team/results/_/id/4138/audax-italiano"
        },
        "Cobresal": {
            "results": "https://africa.espn.com/football/team/results/_/id/4133/cobresal"
        },
        "Colo Colo": {
            "results": "https://africa.espn.com/football/team/results/_/id/2688/colo-colo"
        },
        "Coquimbo Unido": {
            "results": "https://africa.espn.com/football/team/results/_/id/8186/coquimbo-unido"
        },
        "Deportes Iquique": {
            "results": "https://africa.espn.com/football/team/results/_/id/10142/deportes-iquique"
        },
        "Deportes Limache": {
            "results": "https://africa.espn.com/football/team/results/_/id/19195/deportes-limache"
        },
        "Everton Cd": {
            "results": "https://africa.espn.com/football/team/results/_/id/4129/everton-cd"
        },
        "Huachipato": {
            "results": "https://africa.espn.com/football/team/results/_/id/4134/huachipato"
        },
        "La Serena": {
            "results": "https://africa.espn.com/football/team/results/_/id/4137/la-serena"
        },
        "Ohiggins": {
            "results": "https://africa.espn.com/football/team/results/_/id/6072/ohiggins"
        },
        "Palestino": {
            "results": "https://africa.espn.com/football/team/results/_/id/4422/palestino"
        },
        "Universidad Catolica": {
            "results": "https://africa.espn.com/football/team/results/_/id/885/universidad-catolica"
        },
        "Universidad De Chile": {
            "results": "https://africa.espn.com/football/team/results/_/id/4139/universidad-de-chile"
        },
        "Union Espanola": {
            "results": "https://africa.espn.com/football/team/results/_/id/4132/union-espanola"
        },
        "Union La Calera": {
            "results": "https://africa.espn.com/football/team/results/_/id/10144/union-la-calera"
        },
        "Nublense": {
            "results": "https://africa.espn.com/football/team/results/_/id/7427/nublense"
        },
        "ADT": {
            "results": "https://africa.espn.com/football/team/results/_/id/21314/adt"
        },
        "Alianza Atletico": {
            "results": "https://africa.espn.com/football/team/results/_/id/5267/alianza-atletico"
        },
        "Alianza Lima": {
            "results": "https://africa.espn.com/football/team/results/_/id/2680/alianza-lima"
        },
        "Alianza Universidad": {
            "results": "https://africa.espn.com/football/team/results/_/id/19432/alianza-universidad"
        },
        "Atletico Grau": {
            "results": "https://africa.espn.com/football/team/results/_/id/20293/atletico-grau"
        },
        "Ayacucho Fc": {
            "results": "https://africa.espn.com/football/team/results/_/id/10116/ayacucho-fc"
        },
        "Cienciano Del Cusco": {
            "results": "https://africa.espn.com/football/team/results/_/id/3372/cienciano-del-cusco"
        },
        "Comerciantes Unidos": {
            "results": "https://africa.espn.com/football/team/results/_/id/18153/comerciantes-unidos"
        },
        "Cusco Fc": {
            "results": "https://africa.espn.com/football/team/results/_/id/11995/cusco-fc"
        },
        "Deportivo Binacional": {
            "results": "https://africa.espn.com/football/team/results/_/id/18985/deportivo-binacional"
        },
        "Deportivo Garcilaso": {
            "results": "https://africa.espn.com/football/team/results/_/id/21819/deportivo-garcilaso"
        },
        "Juan Pablo Ii": {
            "results": "https://africa.espn.com/football/team/results/_/id/22534/juan-pablo-ii"
        },
        "Los Chankas": {
            "results": "https://africa.espn.com/football/team/results/_/id/22168/los-chankas"
        },
        "Melgar": {
            "results": "https://africa.espn.com/football/team/results/_/id/7312/melgar"
        },
        "Sport Boys": {
            "results": "https://africa.espn.com/football/team/results/_/id/5570/sport-boys"
        },
        "Sport Huancayo": {
            "results": "https://africa.espn.com/football/team/results/_/id/10318/sport-huancayo"
        },
        "Sporting Cristal": {
            "results": "https://africa.espn.com/football/team/results/_/id/2673/sporting-cristal"
        },
        "Utc": {
            "results": "https://africa.espn.com/football/team/results/_/id/10122/utc"
        },
        "Universitario": {
            "results": "https://africa.espn.com/football/team/results/_/id/2685/universitario"
        },
        "Austria Vienna": {
            "results": "https://africa.espn.com/football/team/results/_/id/1382/austria-vienna"
        },
        "Fc Blau Weiß Linz": {
            "results": "https://africa.espn.com/football/team/results/_/id/21950/fc-blau-weiß-linz"
        },
        "Grazer Ak": {
            "results": "https://africa.espn.com/football/team/results/_/id/21846/grazer-ak"
        },
        "Lask Linz": {
            "results": "https://africa.espn.com/football/team/results/_/id/4411/lask-linz"
        },
        "Rb Salzburg": {
            "results": "https://africa.espn.com/football/team/results/_/id/2790/rb-salzburg"
        },
        "Rapid Vienna": {
            "results": "https://africa.espn.com/football/team/results/_/id/519/rapid-vienna"
        },
        "Sc Rheindorf Altach": {
            "results": "https://africa.espn.com/football/team/results/_/id/4405/sc-rheindorf-altach"
        },
        "Sk Sturm Graz": {
            "results": "https://africa.espn.com/football/team/results/_/id/3746/sk-sturm-graz"
        },
        "Sv Josko Ried": {
            "results": "https://africa.espn.com/football/team/results/_/id/3759/sv-josko-ried"
        },
        "Tsv Hartberg": {
            "results": "https://africa.espn.com/football/team/results/_/id/6907/tsv-hartberg"
        },
        "Wsg Swarovski Tirol": {
            "results": "https://africa.espn.com/football/team/results/_/id/18794/wsg-swarovski-tirol"
        },
        "Wolfsberger": {
            "results": "https://africa.espn.com/football/team/results/_/id/13294/wolfsberger"
        },
        "Aik": {
            "results": "https://africa.espn.com/football/team/results/_/id/994/aik"
        },
        "Bk Hacken": {
            "results": "https://africa.espn.com/football/team/results/_/id/7834/bk-hacken"
        },
        "Degerfors If": {
            "results": "https://africa.espn.com/football/team/results/_/id/20856/degerfors-if"
        },
        "Djurgarden": {
            "results": "https://africa.espn.com/football/team/results/_/id/2339/djurgarden"
        },
        "Gais": {
            "results": "https://africa.espn.com/football/team/results/_/id/8222/gais"
        },
        "Halmstads Bk": {
            "results": "https://africa.espn.com/football/team/results/_/id/3017/halmstads-bk"
        },
        "Hammarby If": {
            "results": "https://africa.espn.com/football/team/results/_/id/2495/hammarby-if"
        },
        "If Brommapojkarna": {
            "results": "https://africa.espn.com/football/team/results/_/id/8221/if-brommapojkarna"
        },
        "If Elfsborg": {
            "results": "https://africa.espn.com/football/team/results/_/id/529/if-elfsborg"
        },
        "Ifk Goteborg": {
            "results": "https://africa.espn.com/football/team/results/_/id/2556/ifk-goteborg"
        },
        "Ifk Norrkoping": {
            "results": "https://africa.espn.com/football/team/results/_/id/8544/ifk-norrkoping"
        },
        "Ifk Varnamo": {
            "results": "https://africa.espn.com/football/team/results/_/id/21382/ifk-varnamo"
        },
        "Ik Sirius": {
            "results": "https://africa.espn.com/football/team/results/_/id/8547/ik-sirius"
        },
        "Malmo Ff": {
            "results": "https://africa.espn.com/football/team/results/_/id/2720/malmo-ff"
        },
        "Mjallby Aif": {
            "results": "https://africa.espn.com/football/team/results/_/id/20301/mjallby-aif"
        },
        "Osters If": {
            "results": "https://africa.espn.com/football/team/results/_/id/2936/osters-if"
        },
        "Agropecuario": {
            "results": "https://africa.espn.com/football/team/results/_/id/13913/agropecuario"
        },
        "All Boys": {
            "results": "https://africa.espn.com/football/team/results/_/id/9786/all-boys"
        },
        "Almagro": {
            "results": "https://africa.espn.com/football/team/results/_/id/2/almagro"
        },
        "Almirante Brown": {
            "results": "https://africa.espn.com/football/team/results/_/id/9740/almirante-brown"
        },
        "Alvarado Mar Del Plata": {
            "results": "https://africa.espn.com/football/team/results/_/id/19143/alvarado-mar-del-plata"
        },
        "Arsenal Sarandi": {
            "results": "https://africa.espn.com/football/team/results/_/id/2635/arsenal-sarandi"
        },
        "Atlanta": {
            "results": "https://africa.espn.com/football/team/results/_/id/10146/atlanta"
        },
        "Central Norte": {
            "results": "https://africa.espn.com/football/team/results/_/id/11993/central-norte"
        },
        "Chacarita Juniors": {
            "results": "https://africa.espn.com/football/team/results/_/id/6/chacarita-juniors"
        },
        "Chaco For Ever": {
            "results": "https://africa.espn.com/football/team/results/_/id/11963/chaco-for-ever"
        },
        "Colegiales": {
            "results": "https://africa.espn.com/football/team/results/_/id/10149/colegiales"
        },
        "Colon Santa Fe": {
            "results": "https://africa.espn.com/football/team/results/_/id/7/colon-santa-fe"
        },
        "Defensores Unidos": {
            "results": "https://africa.espn.com/football/team/results/_/id/17697/defensores-unidos"
        },
        "Defensores De Belgrano": {
            "results": "https://africa.espn.com/football/team/results/_/id/10151/defensores-de-belgrano"
        },
        "Deportivo Madryn": {
            "results": "https://africa.espn.com/football/team/results/_/id/18260/deportivo-madryn"
        },
        "Deportivo Maipu": {
            "results": "https://africa.espn.com/football/team/results/_/id/11978/deportivo-maipu"
        },
        "Deportivo Moron": {
            "results": "https://africa.espn.com/football/team/results/_/id/10154/deportivo-moron"
        },
        "Estudiantes Buenos Aires": {
            "results": "https://africa.espn.com/football/team/results/_/id/17352/estudiantes-buenos-aires"
        },
        "Estudiantes De Rio Cuarto": {
            "results": "https://africa.espn.com/football/team/results/_/id/19685/estudiantes-de-rio-cuarto"
        },
        "Ferro Carril Oeste": {
            "results": "https://africa.espn.com/football/team/results/_/id/9743/ferro-carril-oeste"
        },
        "Gimnasia Mendoza": {
            "results": "https://africa.espn.com/football/team/results/_/id/11972/gimnasia-mendoza"
        },
        "Gimnasia Y Esgrima Jujuy": {
            "results": "https://africa.espn.com/football/team/results/_/id/5263/gimnasia-y-esgrima-jujuy"
        },
        "Gimnasia Y Tiro Salta": {
            "results": "https://africa.espn.com/football/team/results/_/id/10743/gimnasia-y-tiro-salta"
        },
        "Guemes": {
            "results": "https://africa.espn.com/football/team/results/_/id/18284/guemes"
        },
        "Los Andes": {
            "results": "https://africa.espn.com/football/team/results/_/id/13/los-andes"
        },
        "Mitre Santiago Del Estero": {
            "results": "https://africa.espn.com/football/team/results/_/id/11990/mitre-santiago-del-estero"
        },
        "Nueva Chicago": {
            "results": "https://africa.espn.com/football/team/results/_/id/236/nueva-chicago"
        },
        "Patronato": {
            "results": "https://africa.espn.com/football/team/results/_/id/10374/patronato"
        },
        "Quilmes": {
            "results": "https://africa.espn.com/football/team/results/_/id/2741/quilmes"
        },
        "Racing Cordoba": {
            "results": "https://africa.espn.com/football/team/results/_/id/19145/racing-cordoba"
        },
        "San Martin Tucuman": {
            "results": "https://africa.espn.com/football/team/results/_/id/17814/san-martin-tucuman"
        },
        "San Miguel": {
            "results": "https://africa.espn.com/football/team/results/_/id/10058/san-miguel"
        },
        "San Telmo": {
            "results": "https://africa.espn.com/football/team/results/_/id/10157/san-telmo"
        },
        "Talleres": {
            "results": "https://africa.espn.com/football/team/results/_/id/10161/talleres"
        },
        "Temperley": {
            "results": "https://africa.espn.com/football/team/results/_/id/10162/temperley"
        },
        "Tristan Suarez": {
            "results": "https://africa.espn.com/football/team/results/_/id/10163/tristan-suarez"
        },
        "2 de Mayo": {
            "results": "https://africa.espn.com/football/team/results/_/id/6097/2-de-mayo"
        },
        "Cerro Porteno": {
            "results": "https://africa.espn.com/football/team/results/_/id/2671/cerro-porteno"
        },
        "Club Atletico Tembetary": {
            "results": "https://africa.espn.com/football/team/results/_/id/22518/club-atletico-tembetary"
        },
        "Deportivo Recoleta": {
            "results": "https://africa.espn.com/football/team/results/_/id/22517/deportivo-recoleta"
        },
        "General Caballero JLM": {
            "results": "https://africa.espn.com/football/team/results/_/id/21316/general-caballero-jlm"
        },
        "Guarani": {
            "results": "https://africa.espn.com/football/team/results/_/id/7385/guarani"
        },
        "Libertad": {
            "results": "https://africa.espn.com/football/team/results/_/id/2670/libertad"
        },
        "Nacional": {
            "results": "https://africa.espn.com/football/team/results/_/id/5584/nacional"
        },
        "Olimpia": {
            "results": "https://africa.espn.com/football/team/results/_/id/2675/olimpia"
        },
        "Sportivo Ameliano": {
            "results": "https://africa.espn.com/football/team/results/_/id/21313/sportivo-ameliano"
        },
        "Sportivo Luqueño": {
            "results": "https://africa.espn.com/football/team/results/_/id/5583/sportivo-luqueno"
        },
        "Trinidense": {
            "results": "https://africa.espn.com/football/team/results/_/id/7466/trinidense"
        },
        "Academia Anzoategui": {
            "results": "https://africa.espn.com/football/team/results/_/id/13783/academia-anzoategui"
        },
        "Academia Puerto Cabello": {
            "results": "https://africa.espn.com/football/team/results/_/id/18995/academia-puerto-cabello"
        },
        "Carabobo": {
            "results": "https://africa.espn.com/football/team/results/_/id/6037/carabobo"
        },
        "Caracas Fc": {
            "results": "https://africa.espn.com/football/team/results/_/id/4811/caracas-fc"
        },
        "Deportivo La Guaira": {
            "results": "https://africa.espn.com/football/team/results/_/id/17090/deportivo-la-guaira"
        },
        "Deportivo Rayo Zuliano": {
            "results": "https://africa.espn.com/football/team/results/_/id/21850/deportivo-rayo-zuliano"
        },
        "Deportivo Tachira": {
            "results": "https://africa.espn.com/football/team/results/_/id/4818/deportivo-tachira"
        },
        "Estudiantes De Merida": {
            "results": "https://africa.espn.com/football/team/results/_/id/6038/estudiantes-de-merida"
        },
        "Metropolitanos Fc": {
            "results": "https://africa.espn.com/football/team/results/_/id/13481/metropolitanos-fc"
        },
        "Monagas Sc": {
            "results": "https://africa.espn.com/football/team/results/_/id/6041/monagas-sc"
        },
        "Portuguesa": {
            "results": "https://africa.espn.com/football/team/results/_/id/6762/portuguesa"
        },
        "Universidad Central": {
            "results": "https://africa.espn.com/football/team/results/_/id/10094/universidad-central"
        },
        "Yaracuyanos": {
            "results": "https://africa.espn.com/football/team/results/_/id/10096/yaracuyanos"
        },
        "Zamora": {
            "results": "https://africa.espn.com/football/team/results/_/id/6763/zamora"
        },
        "Cfr Cluj Napoca": {
            "results": "https://africa.espn.com/football/team/results/_/id/5260/cfr-cluj-napoca"
        },
        "Csu Craiova": {
            "results": "https://africa.espn.com/football/team/results/_/id/8089/csu-craiova"
        },
        "Csikszereda": {
            "results": "https://africa.espn.com/football/team/results/_/id/21032/csikszereda"
        },
        "Dinamo Bucuresti": {
            "results": "https://africa.espn.com/football/team/results/_/id/2496/dinamo-bucuresti"
        },
        "Fc Arges": {
            "results": "https://africa.espn.com/football/team/results/_/id/20725/fc-arges"
        },
        "Fc Botosani": {
            "results": "https://africa.espn.com/football/team/results/_/id/9682/fc-botosani"
        },
        "Fc Farul Constanta": {
            "results": "https://africa.espn.com/football/team/results/_/id/6731/fc-farul-constanta"
        },
        "Fcsb": {
            "results": "https://africa.espn.com/football/team/results/_/id/484/fcsb"
        },
        "Hermannstadt": {
            "results": "https://africa.espn.com/football/team/results/_/id/19265/hermannstadt"
        },
        "Metaloglobus": {
            "results": "https://africa.espn.com/football/team/results/_/id/130880/metaloglobus"
        },
        "Otelul Galati": {
            "results": "https://africa.espn.com/football/team/results/_/id/2942/otelul-galati"
        },
        "Petrolul Ploiesti": {
            "results": "https://africa.espn.com/football/team/results/_/id/12603/petrolul-ploiesti"
        },
        "Rapid Bucuresti": {
            "results": "https://africa.espn.com/football/team/results/_/id/545/rapid-bucuresti"
        },
        "Uta Arad": {
            "results": "https://africa.espn.com/football/team/results/_/id/6912/uta-arad"
        },
        "Unirea Slobozia": {
            "results": "https://africa.espn.com/football/team/results/_/id/22314/unirea-slobozia"
        },
        "Universitatea Cluj": {
            "results": "https://africa.espn.com/football/team/results/_/id/8091/universitatea-cluj"
        },
        "Beitar Jerusalem": {
            "results": "https://africa.espn.com/football/team/results/_/id/5218/beitar-jerusalem"
        },
        "Bnei Sakhnin": {
            "results": "https://africa.espn.com/football/team/results/_/id/8329/bnei-sakhnin"
        },
        "Hapoel Beer": {
            "results": "https://africa.espn.com/football/team/results/_/id/13083/hapoel-beer"
        },
        "Hapoel Hadera": {
            "results": "https://africa.espn.com/football/team/results/_/id/19255/hapoel-hadera"
        },
        "Hapoel Haifa": {
            "results": "https://africa.espn.com/football/team/results/_/id/9577/hapoel-haifa"
        },
        "Hapoel Jerusalem": {
            "results": "https://africa.espn.com/football/team/results/_/id/20970/hapoel-jerusalem"
        },
        "Hapoel Kiryat Shmona": {
            "results": "https://africa.espn.com/football/team/results/_/id/8327/hapoel-kiryat-shmona"
        },
        "Ironi Tiberias": {
            "results": "https://africa.espn.com/football/team/results/_/id/22311/ironi-tiberias"
        },
        "Maccabi Haifa": {
            "results": "https://africa.espn.com/football/team/results/_/id/611/maccabi-haifa"
        },
        "Maccabi Netanya": {
            "results": "https://africa.espn.com/football/team/results/_/id/5945/maccabi-netanya"
        },
        "Maccabi Petah Tikva": {
            "results": "https://africa.espn.com/football/team/results/_/id/2983/maccabi-petah-tikva"
        },
        "Maccabi Raina": {
            "results": "https://africa.espn.com/football/team/results/_/id/21517/maccabi-raina"
        },
        "Maccabi Tel Aviv": {
            "results": "https://africa.espn.com/football/team/results/_/id/524/maccabi-tel-aviv"
        },
        "Moadon Sport Ashdod": {
            "results": "https://africa.espn.com/football/team/results/_/id/5269/moadon-sport-ashdod"
        },
        "Afc Fylde": {
            "results": "https://africa.espn.com/football/team/results/_/id/13884/afc-fylde"
        },
        "Aldershot Town": {
            "results": "https://africa.espn.com/football/team/results/_/id/632/aldershot-town"
        },
        "Altrincham": {
            "results": "https://africa.espn.com/football/team/results/_/id/633/altrincham"
        },
        "Barnet": {
            "results": "https://africa.espn.com/football/team/results/_/id/280/barnet"
        },
        "Boston United": {
            "results": "https://africa.espn.com/football/team/results/_/id/3256/boston-united"
        },
        "Braintree Town": {
            "results": "https://africa.espn.com/football/team/results/_/id/3828/braintree-town"
        },
        "Dagenham Redbridge": {
            "results": "https://africa.espn.com/football/team/results/_/id/275/dagenham-redbridge"
        },
        "Eastleigh": {
            "results": "https://africa.espn.com/football/team/results/_/id/3897/eastleigh"
        },
        "Ebbsfleet United": {
            "results": "https://africa.espn.com/football/team/results/_/id/640/ebbsfleet-united"
        },
        "Fc Halifax Town": {
            "results": "https://africa.espn.com/football/team/results/_/id/312/fc-halifax-town"
        },
        "Forest Green Rovers": {
            "results": "https://africa.espn.com/football/team/results/_/id/282/forest-green-rovers"
        },
        "Gateshead": {
            "results": "https://africa.espn.com/football/team/results/_/id/3138/gateshead"
        },
        "Hartlepool United": {
            "results": "https://africa.espn.com/football/team/results/_/id/323/hartlepool-united"
        },
        "Maidenhead United": {
            "results": "https://africa.espn.com/football/team/results/_/id/7156/maidenhead-united"
        },
        "Oldham Athletic": {
            "results": "https://africa.espn.com/football/team/results/_/id/332/oldham-athletic"
        },
        "Rochdale": {
            "results": "https://africa.espn.com/football/team/results/_/id/303/rochdale"
        },
        "Solihull Moors": {
            "results": "https://africa.espn.com/football/team/results/_/id/13061/solihull-moors"
        },
        "Southend United": {
            "results": "https://africa.espn.com/football/team/results/_/id/310/southend-united"
        },
        "Sutton United": {
            "results": "https://africa.espn.com/football/team/results/_/id/3231/sutton-united"
        },
        "Tamworth": {
            "results": "https://africa.espn.com/football/team/results/_/id/645/tamworth"
        },
        "Wealdstone": {
            "results": "https://africa.espn.com/football/team/results/_/id/3887/wealdstone"
        },
        "Woking": {
            "results": "https://africa.espn.com/football/team/results/_/id/290/woking"
        },
        "Yeovil Town": {
            "results": "https://africa.espn.com/football/team/results/_/id/284/yeovil-town"
        },
        "York City": {
            "results": "https://africa.espn.com/football/team/results/_/id/315/york-city"
        },
        "Aek Athens": {
            "results": "https://africa.espn.com/football/team/results/_/id/887/aek-athens"
        },
        "Aris": {
            "results": "https://africa.espn.com/football/team/results/_/id/11553/aris"
        },
        "Asteras Tripoli": {
            "results": "https://africa.espn.com/football/team/results/_/id/8354/asteras-tripoli"
        },
        "Athens Kallithea": {
            "results": "https://africa.espn.com/football/team/results/_/id/22325/athens-kallithea"
        },
        "Atromitos": {
            "results": "https://africa.espn.com/football/team/results/_/id/6790/atromitos"
        },
        "Lamia": {
            "results": "https://africa.espn.com/football/team/results/_/id/18814/lamia"
        },
        "Levadiakos": {
            "results": "https://africa.espn.com/football/team/results/_/id/5276/levadiakos"
        },
        "Ofi Crete": {
            "results": "https://africa.espn.com/football/team/results/_/id/1010/ofi-crete"
        },
        "Olympiacos": {
            "results": "https://africa.espn.com/football/team/results/_/id/435/olympiacos"
        },
        "Paok Salonika": {
            "results": "https://africa.espn.com/football/team/results/_/id/605/paok-salonika"
        },
        "Panathinaikos": {
            "results": "https://africa.espn.com/football/team/results/_/id/443/panathinaikos"
        },
        "Panetolikos": {
            "results": "https://africa.espn.com/football/team/results/_/id/11431/panetolikos"
        },
        "Panserraikos Fc": {
            "results": "https://africa.espn.com/football/team/results/_/id/21970/panserraikos-fc"
        },
        "Volos Nfc": {
            "results": "https://africa.espn.com/football/team/results/_/id/20043/volos-nfc"
        }
    # Ajoutez d'autres équipes si besoin
}
headers = {'User-Agent': 'Mozilla/5.0'}

PREDICTIONS = []
COMBINED_PREDICTIONS = []
FAILED_TEAMS = set()
IGNORED_ZERO_FORM_TEAMS = []
COUNTRY_TRANSLATION_CACHE = {}

# Récupération des deux clés Groq via les variables d'environnement
groq_keys = list(filter(None, [
    os.environ.get("GROQ_API_KEY"),
    os.environ.get("GROQ_API_KEY1")
]))

# Création d'un itérateur infini qui tourne entre les deux
GROQ_KEY_CYCLE = itertools.cycle(groq_keys)

DEFENSE_ADJUST_METHOD = "asym"

# 🔧 Classe réutilisable de scraping de classement
class ClassementScraper:
    def __init__(self, url):
        self.url = url
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.teams_positions = {}

    def scrape_table(self):
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            rows = soup.find_all('tr', class_='Table__TR')

            for row in rows:
                pos_tag = row.find('span', class_='team-position')
                team_tag = row.find('span', class_='hide-mobile')
                if pos_tag and team_tag:
                    position = int(pos_tag.text.strip())
                    team_name = team_tag.text.strip()
                    self.teams_positions[team_name.lower()] = (position, team_name)

        except Exception as e:
            print(f"❌ Erreur scraping classement : {e}")

    def get_position(self, team_query):
        for key, (position, full_name) in self.teams_positions.items():
            if team_query.lower() in key:
                return position, full_name
        return None, None

# 🧠 Fonction utilitaire get_team_classement_position
def get_team_classement_position(country, league, team_name):
    url = classement_ligue_mapping.get(country, {}).get(league)
    if not url:
        return None, None
    scraper = ClassementScraper(url)
    scraper.scrape_table()
    return scraper.get_position(team_name)

# ----------- ✅ NOUVEAU PROMPT & FONCTION IA -----------
def generate_ai_analysis(pred_obj, t1, t2, adj1, adj2, forme1, forme2, bonus, facteur, method, bonus_serie_domicile=0.0, bonus_serie_exterieur=0.0):
    prompt = f"""
Match : {pred_obj['HomeTeam']} vs {pred_obj['AwayTeam']}
Date : {pred_obj['date']}
Compétition : {pred_obj['league']}
Classement actuel :
- {pred_obj['HomeTeam']} : {pred_obj.get('classement_home', 'N/A')}ᵉ
- {pred_obj['AwayTeam']} : {pred_obj.get('classement_away', 'N/A')}ᵉ

Score estimé : {pred_obj['score_prediction']} par le système de base

📊 Statistiques :
- Moy. buts marqués : {t1['moyenne_marques']:.2f} ({t1['nom']}), {t2['moyenne_marques']:.2f} ({t2['nom']})
- Moy. encaissés : {t1['moyenne_encaisses']:.2f} / {t2['moyenne_encaisses']:.2f}
- Tendance pondérée : {t1['trend_scored']:.2f}-{t1['trend_conceded']:.2f} / {t2['trend_scored']:.2f}-{t2['trend_conceded']:.2f}
- Forme récente : {t1['recent_form']} vs {t2['recent_form']}
- Série à domicile : {'-'.join(t1.get('serie_domicile', [])) or 'N/A'}
- Série à l'extérieur : {'-'.join(t2.get('serie_exterieur', [])) or 'N/A'}
- Bonus série domicile/ext. : {bonus_serie_domicile:+.2f} / {bonus_serie_exterieur:+.2f}
- Ajustement forme & tendance : {forme1:+.2f} / {adj1:+.2f} ({t1['nom']}), {forme2:+.2f} / {adj2:+.2f} ({t2['nom']})
- Bonus défenses faibles : {'Oui' if bonus > 0 else 'Non'}
- Facteur offensif : x{facteur:.2f}
- Méthode d'ajustement défensif : {method}

📈 Probabilités Poisson :
- Victoire {pred_obj['HomeTeam']}: {pred_obj['poisson_probabilities']['win1']}%
- Nul : {pred_obj['poisson_probabilities']['draw']}%
- Victoire {pred_obj['AwayTeam']}: {pred_obj['poisson_probabilities']['win2']}%
- Over 1.5 : {pred_obj['poisson_probabilities']['over15']}%
- Under 3.5 : {pred_obj['poisson_probabilities']['under35']}%
- Les deux marquent : {pred_obj['poisson_probabilities']['btts']}%

🎯 Tâche :
Tu dois proposer **la prédiction la plus sûre possible** à partir de ces données(rien en dehors des données du prompt) et réponds stricte en français même ton raisonnement en français ne fais rien en anglais.  
❌ Ignore totalement la prédiction précédente et les probabilités poisson .  
✅ Choisis **une seule prédiction finale**, parmi cette liste :
 
- Victoire équipe 1
- Victoire ou nul équipe 1
- Victoire équipe 2
- Victoire ou nul équipe 2
- Les deux équipes marquent
- +1.5 buts
- -3.5 buts

⚠️ **Ce match sera utilisé dans un pari combiné.**
💡 Ton objectif est de **minimiser les risques de perte**, même si la cote est plus basse.  
🧠 Analyse les forces/faiblesses, les formes, les buts, le contexte et les probabilités pour choisir **la meilleure option de sécurité**.

Réponds en **français**, de manière **claire, directe et justifiée**.Jamais autre langue que le français.
"""
    selected_key = next(GROQ_KEY_CYCLE)
    headers = {
        "Authorization": f"Bearer {selected_key}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "deepseek-r1-distill-llama-70b",
        "messages": [
            {"role": "system", "content": "Tu es un expert français en analyse de données sportives et paris. Tu disposes de toutes les statistiques détaillées du match pour faire la meilleure prédiction possible."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 3000
    }
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=body
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        return content
    except Exception as e:
        print(f"❌ Erreur IA Groq : {e}")
        return "Erreur IA - Données insuffisantes pour l'analyse"
# ----------- ✅ FIN NOUVEAU PROMPT & IA -----------

def choisir_methode_ajustement(t1, t2):
    ecart_def = abs(t1['moyenne_encaisses'] - t2['moyenne_encaisses'])
    if ecart_def >= 0.6:
        return "asym"
    else:
        return "continuous"

def poisson_pmf(k, lmbda):
    return math.exp(-lmbda) * (lmbda ** k) / math.factorial(k)

def poisson_score_probabilities(lmbda_home, lmbda_away, max_goals=5):
    probabilities = {}
    for home_goals in range(0, max_goals + 1):
        for away_goals in range(0, max_goals + 1):
            prob = poisson_pmf(home_goals, lmbda_home) * poisson_pmf(away_goals, lmbda_away)
            probabilities[(home_goals, away_goals)] = prob
    residual_home = 1 - sum(poisson_pmf(i, lmbda_home) for i in range(0, max_goals + 1))
    residual_away = 1 - sum(poisson_pmf(i, lmbda_away) for i in range(0, max_goals + 1))
    if residual_home > 0 or residual_away > 0:
        probabilities[(max_goals, max_goals)] += residual_home * residual_away
    return probabilities

def poisson_issues(probabilities):
    win1 = sum(p for (h, a), p in probabilities.items() if h > a)
    win2 = sum(p for (h, a), p in probabilities.items() if h < a)
    draw = sum(p for (h, a), p in probabilities.items() if h == a)
    over15 = sum(p for (h, a), p in probabilities.items() if h + a > 1)
    over25 = sum(p for (h, a), p in probabilities.items() if h + a > 2)
    under35 = sum(p for (h, a), p in probabilities.items() if h + a < 4)
    btts = sum(p for (h, a), p in probabilities.items() if h > 0 and a > 0)
    return {
        "win1": win1,
        "draw": draw,
        "win2": win2,
        "over15": over15,
        "over25": over25,
        "under35": under35,
        "btts": btts
    }

def get_top_poisson_scores(lmbda_home, lmbda_away, name1, name2, max_goals=5, n_top=5):
    probabilities = poisson_score_probabilities(lmbda_home, lmbda_away, max_goals)
    sorted_probs = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)[:n_top]
    top_scores = []
    for (h, a), p in sorted_probs:
        top_scores.append({
            "score": f"{name1} {h}-{a} {name2}",
            "probability": round(p * 100, 2)
        })
    return top_scores

def print_poisson_probabilities(lmbda_home, lmbda_away, name1, name2, max_goals=5, n_top=5):
    probabilities = poisson_score_probabilities(lmbda_home, lmbda_away, max_goals=max_goals)
    sorted_probs = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)[:n_top]
    print("\n📊 Scores les plus probables (modèle Poisson):")
    for (h, a), p in sorted_probs:
        print(f"Score {name1} {h}-{a} {name2} : {p*100:.2f}%")
    issues = poisson_issues(probabilities)
    print(f"\n✅ Probabilités Poisson cumulées :")
    print(f"Victoire {name1}: {issues['win1']*100:.2f}%")
    print(f"Match nul   : {issues['draw']*100:.2f}%")
    print(f"Victoire {name2}: {issues['win2']*100:.2f}%")
    print(f"+1.5 buts : {issues['over15']*100:.2f}%")
    print(f"+2.5 buts : {issues['over25']*100:.2f}%")
    print(f"-3.5 buts : {issues['under35']*100:.2f}%")
    print(f"Les deux équipes marquent : {issues['btts']*100:.2f}%")
    return probabilities, issues

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
                home_espn = get_espn_name(home_api)
                away_espn = get_espn_name(away_api)
                if home_espn in teams_urls and away_espn in teams_urls:
                    print(f"\n🔎 Analyse automatique pour : {home_espn} & {away_espn}")
                    team1_stats = process_team(home_api, return_data=True)
                    team2_stats = process_team(away_api, return_data=True)
                    if team1_stats: team1_stats['nom'] = home_espn
                    if team2_stats: team2_stats['nom'] = away_espn
                    compare_teams_and_predict_score(
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
        if résultats:
            sauvegarder_prediction_json_complete(résultats, [], today)
            fichier = f"prédiction-{today}-analyse-ia.json"
            git_commit_and_push(fichier)
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

def analyze_weighted_trends(match_data, team_name, return_values=False):
    if len(match_data) < 6:
        print("\n⚠️ Pas assez de données pour la tendance pondérée.")
        if return_values:
            return 0.0, 0.0
        return
    poids = [0.5, 0.6, 0.7, 1.0, 1.2, 1.5]
    scored, conceded = 0.0, 0.0
    total_poids = 0.0
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
    if count_win >= 2:
        streak_bonus += (count_win - 1)
    if count_lose >= 2:
        streak_malus -= (count_lose - 1)
    return streak_bonus + streak_malus

def calcul_ajustement_automatique_serie(serie):
    """
    Calcule un ajustement automatique en fonction des plus longues séries de victoires/défaites.
    Bonus max = +0.5 | Malus max = -0.5
    """
    if not serie:
        return 0.0

    streak = 0
    current = None
    max_wins = 0
    max_losses = 0

    for r in serie:
        if r == current:
            streak += 1
        else:
            current = r
            streak = 1

        if r == 'W':
            max_wins = max(max_wins, streak)
        elif r == 'L':
            max_losses = max(max_losses, streak)

    bonus = 0.05 * max_wins   # ex: 4 victoires = +0.20
    malus = -0.05 * max_losses  # ex: 3 défaites = -0.15

    bonus = min(bonus, 0.5)
    malus = max(malus, -0.5)

    return bonus + malus

def get_form_points(recent_form):
    points_map = {'W': 3, 'D': 1, 'L': 0}
    total = sum(points_map.get(r, 0) for r in recent_form)
    ratio = total / (len(recent_form)*3) if recent_form else 0
    momentum = get_streak_bonus(recent_form)
    return total, ratio, momentum

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
        valid_results = []
        recent_form = []
        buts_dom_marques = 0
        buts_dom_encaisses = 0
        buts_ext_marques = 0
        buts_ext_encaisses = 0

        # 🏗️ Initialisation des séries domicile/extérieur
        serie_domicile = []
        serie_exterieur = []

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

                    # 🔄 Ajout dans la bonne série
                    is_home = (team1 == espn_team_name)
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
            if len(valid_results) >= 6:
                break
        nb_matchs = len(valid_results)
        if nb_matchs == 0:
            print("Aucun match trouvé.")
            FAILED_TEAMS.add(team_name)
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
        avg_trend_scored, avg_trend_conceded = analyze_weighted_trends(valid_results, espn_team_name, return_values=True)

        # 💡 BONUS : Affichage des séries
        print(f"🏠 Série domicile : {'-'.join(serie_domicile)}")
        print(f"✈️ Série extérieur : {'-'.join(serie_exterieur)}")

        return {
            "matches": valid_results,
            "moyenne_marques": total_marques / nb_matchs,
            "moyenne_encaisses": total_encaisses / nb_matchs,
            "recent_form": recent_form,
            "trend_scored": avg_trend_scored,
            "trend_conceded": avg_trend_conceded,
            "serie_domicile": serie_domicile,
            "serie_exterieur": serie_exterieur
        }
    except Exception as e:
        print(f"Erreur scraping {espn_team_name} ({action}) : {e}")
        FAILED_TEAMS.add(team_name)
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
    return (
        0.4 * (t['moyenne_marques'] - t['moyenne_encaisses']) +
        0.3 * forme_adj +
        0.3 * (adj)
    )

def apply_weak_defense_bonus(pred_t1, pred_t2, t1, t2):
    SEUIL_DEFENSE_FAIBLE = 1.5
    nom1 = t1.get('nom', 'Équipe 1')
    nom2 = t2.get('nom', 'Équipe 2')
    defense_faible_t1 = t1['moyenne_encaisses'] >= SEUIL_DEFENSE_FAIBLE
    defense_faible_t2 = t2['moyenne_encaisses'] >= SEUIL_DEFENSE_FAIBLE
    bonus_applied = 0

    if defense_faible_t1 and defense_faible_t2:
        bonus = 0.3
        pred_t1 += bonus
        pred_t2 += bonus
        bonus_applied = bonus
        print(f"🚨 Bonus défenses faibles appliqué : +{bonus} but pour chaque équipe ({nom1}, {nom2})")
    elif defense_faible_t1:
        bonus = 0.2
        pred_t2 += bonus
        bonus_applied = bonus
        print(f"🚨 Bonus défense faible {nom1} : +{bonus} but pour {nom2}")
    elif defense_faible_t2:
        bonus = 0.2
        pred_t1 += bonus
        bonus_applied = bonus
        print(f"🚨 Bonus défense faible {nom2} : +{bonus} but pour {nom1}")

    return pred_t1, pred_t2, bonus_applied

def calculate_match_offensive_factor(t1, t2):
    moyenne_encaisse_combinee = (t1['moyenne_encaisses'] + t2['moyenne_encaisses']) / 2
    if moyenne_encaisse_combinee >= 2.0:
        facteur = 1.4
        print(f"🔥 Match à fort potentiel offensif (facteur: {facteur})")
    elif moyenne_encaisse_combinee >= 1.5:
        facteur = 1.2
        print(f"⚡ Match avec potentiel offensif modéré (facteur: {facteur})")
    elif moyenne_encaisse_combinee >= 1.0:
        facteur = 1.1
        print(f"📈 Match équilibré offensivement (facteur: {facteur})")
    else:
        facteur = 1.0
        print(f"🛡️ Match défensif attendu (facteur: {facteur})")
    return facteur

def is_undefeated_home(team, team_name):
    last_matches = team.get('matches', [])
    count = 0
    for m in last_matches:
        is_home = (m[1] == team_name)
        res = get_match_result_for_team(team_name, m[4], m[1], m[2])
        if is_home and res in ('W', 'D'):
            count += 1
        if count >= 3:
            return True
    return False

def has_no_home_defeat(team, team_name):
    last_matches = team.get('matches', [])[:6]
    for m in last_matches:
        is_home = (m[1] == team_name)
        res = get_match_result_for_team(team_name, m[4], m[1], m[2])
        if is_home and res == 'L':
            return False
    return True

def has_no_away_win_in_5(team, team_name):
    last_matches = team.get('matches', [])[:5]
    count = 0
    for m in last_matches:
        is_away = (m[2] == team_name)
        res = get_match_result_for_team(team_name, m[4], m[1], m[2])
        if is_away and res == 'W':
            return False
        if is_away:
            count += 1
        if count >= 5:
            break
    return count == 5

def away_wins_count(team, team_name):
    last_matches = team.get('matches', [])[:6]
    count = 0
    for m in last_matches:
        is_away = (m[2] == team_name)
        res = get_match_result_for_team(team_name, m[4], m[1], m[2])
        if is_away and res == 'W':
            count += 1
    return count

def has_two_games_no_goal(team, team_name):
    matches = team.get('matches', [])[:2]
    for m in matches:
        buts, _, _ = extract_goals(team_name, m[4], m[1], m[2])
        if buts and buts > 0:
            return False
    return len(matches) == 2

def determine_optimal_prediction(pred_t1, pred_t2, t1, t2, name1, name2, indice_forme_t1, indice_forme_t2, defeats_t1, defeats_t2, adj1, adj2, forme_adj1, forme_adj2):
    total_pred = pred_t1 + pred_t2
    diff_indice_forme = abs(indice_forme_t1 - indice_forme_t2)
    both_at_least_3_defeats = (defeats_t1 >= 3 and defeats_t2 >= 3)

    if both_at_least_3_defeats and diff_indice_forme < 1.2:
        print("🛑 Blocage : match trop instable, aucune prédiction proposée.")
        return "⚠️ Trop de défaites récentes, match instable à éviter", 55

    predictions_candidates = []

    conf_total = confidence_total(total_pred)
    if total_pred >= 2.8:
        predictions_candidates.append({
            "prediction": "+1.5 buts",
            "confidence": conf_total,
            "type": "total"
        })
    elif total_pred <= 2.3:
        predictions_candidates.append({
            "prediction": "-3.5 buts",
            "confidence": conf_total,
            "type": "total"
        })
    else:
        predictions_candidates.append({
            "prediction": "+1.5 buts",
            "confidence": conf_total,
            "type": "total"
        })

    conf_btts = confidence_btts(pred_t1, pred_t2, t1, t2)
    if conf_btts > 0:
        if not (has_two_games_no_goal(t1, name1) or has_two_games_no_goal(t2, name2)):
            predictions_candidates.append({
                "prediction": "Les deux équipes marquent",
                "confidence": conf_btts,
                "type": "btts"
            })

    if diff_indice_forme < 0.3 and defeats_t1 >= 2 and defeats_t2 >= 2:
        predictions_candidates.append({
            "prediction": "⚠️ Match très équilibré, à éviter",
            "confidence": 60,
            "type": "avoid"
        })
    else:
        if indice_forme_t1 > indice_forme_t2:
            conf_draw = confidence_win_or_draw(diff_indice_forme, adj1, forme_adj1)
            conf_vic = confidence_victory(diff_indice_forme, adj1, forme_adj1)

            if 0.1 < diff_indice_forme < 0.7:
                victoire_pred = f"Victoire ou nul {name1}"
                conf_pred = conf_draw
            elif diff_indice_forme >= 1.0 and not both_at_least_3_defeats:
                victoire_pred = f"Victoire {name1}"
                conf_pred = conf_vic
            elif diff_indice_forme >= 1.0 and both_at_least_3_defeats:
                victoire_pred = f"Victoire ou nul {name1}"
                conf_pred = conf_draw
            else:
                victoire_pred = None
                conf_pred = 0

            if victoire_pred and victoire_pred == f"Victoire {name1}" and name1 != name2:
                if is_undefeated_home(t1, name1):
                    victoire_pred = f"Victoire ou nul {name1}"
                    conf_pred = min(conf_pred, 75)
                elif has_no_away_win_in_5(t1, name1):
                    victoire_pred = f"Victoire ou nul {name1}"
                    conf_pred = min(conf_pred, 75)

            if victoire_pred and conf_pred > 0:
                predictions_candidates.append({
                    "prediction": victoire_pred,
                    "confidence": conf_pred,
                    "type": "victory"
                })

        elif indice_forme_t2 > indice_forme_t1:
            conf_draw = confidence_win_or_draw(diff_indice_forme, adj2, forme_adj2)
            conf_vic = confidence_victory(diff_indice_forme, adj2, forme_adj2)

            if 0.1 < diff_indice_forme < 0.7:
                victoire_pred = f"Victoire ou nul {name2}"
                conf_pred = conf_draw
            elif diff_indice_forme >= 1.0 and not both_at_least_3_defeats:
                victoire_pred = f"Victoire {name2}"
                conf_pred = conf_vic
            elif diff_indice_forme >= 1.0 and both_at_least_3_defeats:
                victoire_pred = f"Victoire ou nul {name2}"
                conf_pred = conf_draw
            else:
                victoire_pred = None
                conf_pred = 0

            if victoire_pred and victoire_pred == f"Victoire {name2}" and name1 != name2:
                if is_undefeated_home(t1, name1):
                    victoire_pred = f"Victoire ou nul {name2}"
                    conf_pred = min(conf_pred, 75)
                elif has_no_away_win_in_5(t2, name2):
                    victoire_pred = f"Victoire ou nul {name2}"
                    conf_pred = min(conf_pred, 75)

            if victoire_pred and conf_pred > 0:
                predictions_candidates.append({
                    "prediction": victoire_pred,
                    "confidence": conf_pred,
                    "type": "victory"
                })

    if predictions_candidates:
        best_prediction = max(predictions_candidates, key=lambda x: x['confidence'])
        return best_prediction["prediction"], best_prediction["confidence"]
    else:
        return None, 0

def calculate_defensive_reduction(avg_conceded):
    if avg_conceded >= 1.0:
        return 0.0
    return round((1.0 - avg_conceded) * 0.3, 3)

def apply_defensive_adjustment(pred_t1, pred_t2, t1, t2, name1, name2):
    if DEFENSE_ADJUST_METHOD == "asym":
        defense_threshold = 0.9
        if t1['moyenne_encaisses'] < defense_threshold and t2['moyenne_encaisses'] >= defense_threshold:
            reduction_pct = 0.20
            print(f"🛡️ {name1} a une défense solide ➤ réduction de 20% sur le score estimé de {name2}")
            pred_t2 *= (1 - reduction_pct)
        elif t2['moyenne_encaisses'] < defense_threshold and t1['moyenne_encaisses'] >= defense_threshold:
            reduction_pct = 0.20
            print(f"🛡️ {name2} a une défense solide ➤ réduction de 20% sur le score estimé de {name1}")
            pred_t1 *= (1 - reduction_pct)
        elif t1['moyenne_encaisses'] < defense_threshold and t2['moyenne_encaisses'] < defense_threshold:
            print(f"🛡️ Les deux équipes ont une défense solide ➤ réduction de 15% sur chaque score")
            pred_t1 *= 0.85
            pred_t2 *= 0.85
    elif DEFENSE_ADJUST_METHOD == "continuous":
        reduction_pct_t1 = calculate_defensive_reduction(t1['moyenne_encaisses'])
        reduction_pct_t2 = calculate_defensive_reduction(t2['moyenne_encaisses'])
        if reduction_pct_t1 > 0:
            print(f"🛡️ Réduction continue appliquée ➤ {name2} réduit de {int(reduction_pct_t1 * 100)}%")
            pred_t2 *= (1 - reduction_pct_t1)
        if reduction_pct_t2 > 0:
            print(f"🛡️ Réduction continue appliquée ➤ {name1} réduit de {int(reduction_pct_t2 * 100)}%")
            pred_t1 *= (1 - reduction_pct_t2)
    return pred_t1, pred_t2

def compare_teams_and_predict_score(
    t1, t2, name1, name2, match_date="N/A", match_time="N/A",
    league="N/A", country="N/A", logo_home=None, logo_away=None, résultats=None
):
    if not t1 or not t2:
        print("⚠️ Données insuffisantes pour la comparaison.")
        return

    # Vérifier si une équipe a une forme récente totalement vide (0 point)
    points1, _, _ = get_form_points(t1.get('recent_form', []))
    points2, _, _ = get_form_points(t2.get('recent_form', []))

    if points1 == 0:
        print(f"🚫 {name1} a une forme totalement vide (0 point), match ignoré.")
        IGNORED_ZERO_FORM_TEAMS.append(name1)
        return
    if points2 == 0:
        print(f"🚫 {name2} a une forme totalement vide (0 point), match ignoré.")
        IGNORED_ZERO_FORM_TEAMS.append(name2)
        return

    # 🏆 Récupération classement des équipes
    pos_home, nom_classement_home = get_team_classement_position(country, league, name1)
    pos_away, nom_classement_away = get_team_classement_position(country, league, name2)

    if pos_home:
        print(f"📌 Classement de {nom_classement_home} : {pos_home}ᵉ")
    if pos_away:
        print(f"📌 Classement de {nom_classement_away} : {pos_away}ᵉ")

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

    # 🎯 Ajustement automatique selon les séries domicile / extérieur
    bonus_serie_domicile = calcul_ajustement_automatique_serie(t1.get('serie_domicile', []))
    bonus_serie_exterieur = calcul_ajustement_automatique_serie(t2.get('serie_exterieur', []))

    forme_adj1 += bonus_serie_domicile
    forme_adj2 += bonus_serie_exterieur

    print(f"🏠 Bonus série domicile ({name1}) : {bonus_serie_domicile:+.2f}")
    print(f"✈️ Bonus série extérieur ({name2}) : {bonus_serie_exterieur:+.2f}")

    pred_t1_initial = (t1['moyenne_marques'] + t2['moyenne_encaisses']) / 2
    pred_t2_initial = (t2['moyenne_marques'] + t1['moyenne_encaisses']) / 2
    pred_t1_initial += adj1*0.5 + forme_adj1
    pred_t2_initial += adj2*0.5 + forme_adj2

    pred_t1, pred_t2, bonus_defense = apply_weak_defense_bonus(pred_t1_initial, pred_t2_initial, t1, t2)
    facteur_offensif = calculate_match_offensive_factor(t1, t2)
    pred_t1 *= facteur_offensif
    pred_t2 *= facteur_offensif

    global DEFENSE_ADJUST_METHOD
    DEFENSE_ADJUST_METHOD = choisir_methode_ajustement(t1, t2)
    print(f"🧠 Méthode d'ajustement défensif choisie : {DEFENSE_ADJUST_METHOD}")

    pred_t1_before_defensive = pred_t1
    pred_t2_before_defensive = pred_t2

    pred_t1, pred_t2 = apply_defensive_adjustment(pred_t1, pred_t2, t1, t2, name1, name2)

    defensive_reduction_applied = (pred_t1 != pred_t1_before_defensive) or (pred_t2 != pred_t2_before_defensive)

    pred_t1 = max(pred_t1, 0.1)
    pred_t2 = max(pred_t2, 0.1)

    print(f"\n🛠️ Ajustements appliqués :")
    print(f"{name1} ➤ Tendance:{adj1:+.2f} | Forme:{forme_adj1:+.2f}")
    print(f"{name2} ➤ Tendance:{adj2:+.2f} | Forme:{forme_adj2:+.2f}")
    print(f"Facteur offensif appliqué : x{facteur_offensif:.2f}")

    if defensive_reduction_applied:
        print(f"Score avant réduction défensive : {name1} {pred_t1_before_defensive:.1f} - {pred_t2_before_defensive:.1f} {name2}")
        print(f"Score après réduction défensive : {name1} {pred_t1:.1f} - {pred_t2:.1f} {name2}")

    print(f"\n🔮 **Score estimé final** :")
    print(f"{name1} {pred_t1:.1f} - {pred_t2:.1f} {name2}")

    poisson_probs, poisson_issues_dict = print_poisson_probabilities(pred_t1, pred_t2, name1, name2, max_goals=5, n_top=5)
    poisson_top_scores = get_top_poisson_scores(pred_t1, pred_t2, name1, name2, max_goals=5, n_top=5)

    indice_forme_t1 = compute_indice_forme(t1, forme_adj1, adj1)
    indice_forme_t2 = compute_indice_forme(t2, forme_adj2, adj2)
    diff_indice_forme = abs(indice_forme_t1 - indice_forme_t2)
    defeats_t1 = count_defeats(t1.get('recent_form', []))
    defeats_t2 = count_defeats(t2.get('recent_form', []))

    print(f"\n📊 Indice de forme : {name1}: {indice_forme_t1:.2f} | {name2}: {indice_forme_t2:.2f} | Diff: {diff_indice_forme:.2f}")

    pred_safe = None
    conf_safe = 0

    if defensive_reduction_applied:
        print(f"\n🔄 Vérification de cohérence après réduction défensive...")

        pred_before, conf_before = determine_optimal_prediction(
            pred_t1_before_defensive, pred_t2_before_defensive, t1, t2, name1, name2,
            indice_forme_t1, indice_forme_t2, defeats_t1, defeats_t2, adj1, adj2, forme_adj1, forme_adj2
        )
        pred_after, conf_after = determine_optimal_prediction(
            pred_t1, pred_t2, t1, t2, name1, name2,
            indice_forme_t1, indice_forme_t2, defeats_t1, defeats_t2, adj1, adj2, forme_adj1, forme_adj2
        )

        if pred_before != pred_after:
            print(f"⚠️ Changement de prédiction dû à la réduction défensive :")
            print(f"   • Avant réduction : {pred_before} (Confiance: {conf_before}%)")
            print(f"   • Après réduction : {pred_after} (Confiance: {conf_after}%)")
            print(f"   • Prédiction finale retenue : {pred_after}")

        pred_safe = pred_after
        conf_safe = conf_after
    else:
        pred_safe, conf_safe = determine_optimal_prediction(
            pred_t1, pred_t2, t1, t2, name1, name2,
            indice_forme_t1, indice_forme_t2, defeats_t1, defeats_t2, adj1, adj2, forme_adj1, forme_adj2
        )

    print("\n🔎 Prédictions détaillées :")

    if pred_safe == "+1.5 buts":
        poisson_conf = int(poisson_issues_dict["over15"] * 100)
        print(f"🔁 Ajustement Poisson : confiance over1.5 = {poisson_conf}%")
        conf_safe = (conf_safe + poisson_conf) // 2
    elif pred_safe == "+2.5 buts":
        poisson_conf = int(poisson_issues_dict["over25"] * 100)
        print(f"🔁 Ajustement Poisson : confiance over2.5 = {poisson_conf}%")
        conf_safe = (conf_safe + poisson_conf) // 2
    elif pred_safe == "-3.5 buts":
        poisson_conf = int(poisson_issues_dict["under35"] * 100)
        print(f"🔁 Ajustement Poisson : confiance under3.5 = {poisson_conf}%")
        conf_safe = (conf_safe + poisson_conf) // 2
    elif pred_safe == "Les deux équipes marquent":
        poisson_conf = int(poisson_issues_dict["btts"] * 100)
        print(f"🔁 Ajustement Poisson : confiance BTTS = {poisson_conf}%")
        conf_safe = (conf_safe + poisson_conf) // 2
    elif pred_safe and pred_safe.startswith("Victoire ") and not pred_safe.endswith("nul"):
        if name1 in pred_safe:
            poisson_conf = int(poisson_issues_dict["win1"] * 100)
            print(f"🔁 Ajustement Poisson : confiance victoire {name1} = {poisson_conf}%")
            conf_safe = (conf_safe + poisson_conf) // 2
        elif name2 in pred_safe:
            poisson_conf = int(poisson_issues_dict["win2"] * 100)
            print(f"🔁 Ajustement Poisson : confiance victoire {name2} = {poisson_conf}%")
            conf_safe = (conf_safe + poisson_conf) // 2
    elif pred_safe and pred_safe.startswith("Victoire ou nul "):
        if name1 in pred_safe:
            poisson_conf = int((poisson_issues_dict["win1"] + poisson_issues_dict["draw"]) * 100)
            print(f"🔁 Ajustement Poisson : confiance 1X = {poisson_conf}%")
            conf_safe = (conf_safe + poisson_conf) // 2
        elif name2 in pred_safe:
            poisson_conf = int((poisson_issues_dict["win2"] + poisson_issues_dict["draw"]) * 100)
            print(f"🔁 Ajustement Poisson : confiance X2 = {poisson_conf}%")
            conf_safe = (conf_safe + poisson_conf) // 2

    print(f"👉 Prédiction finale : **{pred_safe}** (Confiance : {conf_safe}%)")

    print("\n📚 Note : Prédictions issues de la tendance pondérée, forme récente, séries, stats offensives/défensives, indice de forme combiné, bonus défenses faibles, facteur offensif, **ajustement automatique après réduction défensive** et **ajustement probabilités Poisson**. La fiabilité (%) est une estimation statistique, non une certitude.")

    if pred_safe and conf_safe:
        prediction_obj = {
            "id": len(PREDICTIONS) + 1,
            "HomeTeam": name1,
            "AwayTeam": name2,
            "confidence": conf_safe,
            "date": format_date_fr(match_date, match_time),
            "league": f"{country} - {league}",
            "prediction": pred_safe,
            "type": "single",
            "score_prediction": f"{pred_t1:.1f} - {pred_t2:.1f}",
            "defensive_reduction_applied": defensive_reduction_applied,
            "score_before_reduction": f"{pred_t1_before_defensive:.1f} - {pred_t2_before_defensive:.1f}" if defensive_reduction_applied else None,
            "poisson_probabilities": {
                "win1": round(poisson_issues_dict["win1"] * 100, 2),
                "draw": round(poisson_issues_dict["draw"] * 100, 2),
                "win2": round(poisson_issues_dict["win2"] * 100, 2),
                "over15": round(poisson_issues_dict["over15"] * 100, 2),
                "over25": round(poisson_issues_dict["over25"] * 100, 2),
                "under35": round(poisson_issues_dict["under35"] * 100, 2),
                "btts": round(poisson_issues_dict["btts"] * 100, 2)
            },
            "poisson_top_scores": poisson_top_scores,
            "logo_home": logo_home,
            "logo_away": logo_away,
            "bonus_serie_domicile": bonus_serie_domicile,
            "bonus_serie_exterieur": bonus_serie_exterieur,
            "classement_home": pos_home,
            "classement_away": pos_away,
            "nom_classement_home": nom_classement_home,
            "nom_classement_away": nom_classement_away
        }

        # ✅ NOUVEL APPEL IA SELON DEMANDE avec bonus séries :
        prediction_obj["analyse_ia"] = generate_ai_analysis(
            prediction_obj, t1, t2, adj1, adj2, forme_adj1, forme_adj2,
            bonus_defense, facteur_offensif, DEFENSE_ADJUST_METHOD, 
            bonus_serie_domicile, bonus_serie_exterieur
        )

        PREDICTIONS.append(prediction_obj)
        if résultats is not None:
            résultats.append(prediction_obj)

def process_team(team_name, return_data=False):
    print(f"\n🧠 Analyse pour l'équipe : {get_espn_name(team_name)}")
    data = scrape_team_data(team_name, 'results')
    print("\n" + "-" * 60 + "\n")
    return data if return_data else None

def generate_combined_predictions(predictions):
    print("\n🔗 Génération des prédictions combinées...")

    def pred_eligible(pred):
        if pred['prediction'] == "Les deux équipes marquent":
            return pred['confidence'] >= 70
        return pred['confidence'] >= 80

    eligible_preds = [p for p in predictions if pred_eligible(p)]

    def get_match_id(pred):
        return (pred['HomeTeam'], pred['AwayTeam'], pred['date'])

    match_ids = [get_match_id(p) for p in eligible_preds]
    num_matches = len(eligible_preds)

    if num_matches < 2:
        print("⚠️ Pas assez de prédictions éligibles pour combiner.")
        return

    combinable_sizes = []
    if num_matches == 2:
        combinable_sizes = [2]
    elif num_matches == 3:
        combinable_sizes = [2, 3]
    elif num_matches == 4:
        combinable_sizes = [3, 4]
    else:
        combinable_sizes = [3, num_matches] if num_matches > 4 else []

    if num_matches > 4:
        combinable_sizes = [3, num_matches]

    all_combos = []
    for combo_size in combinable_sizes:
        combos = []
        for combo in itertools.combinations(eligible_preds, combo_size):
            match_set = set()
            for p in combo:
                mid = get_match_id(p)
                if mid in match_set:
                    break
                match_set.add(mid)
            else:
                combos.append(combo)
        all_combos.extend(combos)

    limited_combos = []
    for combo_size in combinable_sizes:
        combos = [c for c in all_combos if len(c) == combo_size]
        max_combos = 10 if combo_size == 2 else 5 if combo_size == 3 else 2
        limited_combos.extend(combos[:max_combos])

    for combo in limited_combos:
        combined_confidence = 1.0
        for pred in combo:
            combined_confidence *= (pred['confidence'] / 100.0)
        combined_confidence_percent = round(combined_confidence * 100, 2)
        combo_name = f"Combiné IA {len(combo)} matchs"

        combo_description = {
            "nombre_evenements": len(combo),
            "événements": [
                {
                    "match": f"{p['HomeTeam']} - {p['AwayTeam']}",
                    "prédiction": p['prediction'],
                    "ligue": p['league']
                } for p in combo
            ]
        }

        combined_pred = {
            "id": len(COMBINED_PREDICTIONS) + 1,
            "name": combo_name,
            "description": combo_description,
            "matches": [
                {
                    "match": f"{p['HomeTeam']} vs {p['AwayTeam']}",
                    "prediction": p['prediction'],
                    "individual_confidence": p['confidence'],
                    "country_fr": p['league'],
                    "league": p['league']
                } for p in combo
            ],
            "combined_confidence": combined_confidence_percent,
            "type": "combined_ia",
            "size": len(combo),
            "estimated_odds": round(1 / combined_confidence, 2) if combined_confidence > 0 else 0
        }
        COMBINED_PREDICTIONS.append(combined_pred)
    COMBINED_PREDICTIONS.sort(key=lambda x: x['combined_confidence'], reverse=True)
    print(f"✅ {len(COMBINED_PREDICTIONS)} combinés IA générés.")
    print("\n🏆 Top 5 des meilleurs combinés IA :")
    for i, combo in enumerate(COMBINED_PREDICTIONS[:5], 1):
        descr = combo['description']
        if isinstance(descr, dict):
            resume = " | ".join([f"{e['match']} : {e['ligue']}" for e in descr['événements']])
        else:
            resume = descr
        print(f"{i}. {combo['name']} - Confiance: {combo['combined_confidence']}% - Cote estimée: {combo['estimated_odds']}")
        print(f"   {resume[:100]}{'...' if len(resume) > 100 else ''}")

def sauvegarder_prediction_json_complete(predictions_simples, predictions_combinees, date_str):
    safest_bets = [p for p in predictions_simples if p['confidence'] >= 85]
    ia_singles_premium = [p for p in predictions_simples if p['confidence'] >= 80]
    details_filtered = [p for p in predictions_simples if p['confidence'] < 80]
    total_predictions = len(details_filtered)
    high_confidence_count = len([p for p in details_filtered if p['confidence'] >= 80])
    medium_confidence_count = len([p for p in details_filtered if 60 <= p['confidence'] < 80])
    low_confidence_count = len([p for p in details_filtered if p['confidence'] < 60])
    avg_confidence = round(
        sum(p['confidence'] for p in details_filtered) / total_predictions, 2
    ) if total_predictions > 0 else 0

    prediction_types = {}
    for pred in details_filtered:
        pred_type = pred['prediction']
        if pred_type not in prediction_types:
            prediction_types[pred_type] = []
        prediction_types[pred_type].append(pred)

    for p in predictions_simples:
        p['country_fr'] = p['league']

    data_complete = {
        "metadata": {
            "date_generation": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "date_matchs": date_str,
            "version_algorithme": "3.7 - Poisson + IA Singles Premium + Combinés IA + scores Poisson + IA Enrichie + Bonus Séries Auto + Classements",
            "total_predictions_simples": total_predictions,
            "statistiques": {
                "confiance_moyenne": avg_confidence,
                "haute_confiance_80plus": high_confidence_count,
                "moyenne_confiance_60_79": medium_confidence_count,
                "faible_confiance_moins_60": low_confidence_count
            }
        },
        "predictions_simples": {
            "count": total_predictions,
            "details": details_filtered,
            "par_type": prediction_types
        },
        "ia_singles_premium": {
            "count": len(ia_singles_premium),
            "details": ia_singles_premium
        },
        "recommandations": {
            "safest_bets": safest_bets
        }
    }
    chemin = f"prédiction-{date_str}-analyse-ia.json"
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(data_complete, f, ensure_ascii=False, indent=2)
    print(f"✅ Prédictions complètes sauvegardées dans : {chemin}")
    print(f"📊 Total: {total_predictions} prédictions simples")
    print(f"📈 Confiance moyenne: {avg_confidence}%")

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
        subprocess.run(["git", "commit", "-m", f"📊 Prédictions IA du {datetime.now().strftime('%Y-%m-%d')} - Version 3.7 IA Enrichie + Bonus Séries Automatiques + Classements"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("✅ Prédictions poussées avec succès sur GitHub.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur Git : {e}")

def main():
    print("⚽️ Bienvenue dans l'analyse IA v3.7 : Poisson, Singles Premium, combinés IA, IA enrichie + Bonus Séries Automatiques + Classements !")
    print("🔬 Nouvelles fonctionnalités: Analyse IA avec TOUTES les données contextuelles + ajustement automatique selon séries domicile/extérieur + classements")
    print("🧠 L'IA LLaMA 3 dispose maintenant de l'intégralité du contexte pour optimiser les prédictions")
    print("🎯 Bonus automatiques selon les plus longues séries de victoires/défaites à domicile et à l'extérieur")
    print("🏆 Intégration des classements des équipes dans les analyses")
    print("🛑 Filtrage automatique des équipes avec forme nulle (0 point)")
    print("📊 Analyse complète des matchs du jour avec recommandations...\n")
    get_today_matches_filtered()
    print(f"\n📋 Résumé de la session:")
    print(f"   🎯 {len(PREDICTIONS)} prédictions simples générées")
    print(f"   🔗 {len(COMBINED_PREDICTIONS)} combinés IA créés")
    if IGNORED_ZERO_FORM_TEAMS:
        print(f"   🚫 {len(set(IGNORED_ZERO_FORM_TEAMS))} équipes ignorées pour forme nulle")
    if COMBINED_PREDICTIONS:
        print(f"\n🏆 Meilleur combiné IA:")
        best = COMBINED_PREDICTIONS[0]
        print(f"   {best['name']} - Confiance: {best['combined_confidence']}%")
        print(f"   Cote estimée: {best['estimated_odds']}")
    print("\n✨ Merci d'avoir utilisé le script IA v3.7 ⚽️📊🧠🏆. Bonne chance avec vos paris ! 🍀")

if __name__ == "__main__":
    main()
