import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List
import requests


class FootballDataConsolidator:
    """Classe pour consolider et nettoyer les données de matchs avec résultats réels"""

    FIELDS_TO_KEEP = {
        'match_info': ['id', 'fixture_id', 'HomeTeam', 'AwayTeam', 'date', 'league'],
        'stats': [
            'moyenne_marques', 'moyenne_encaisses', 'form_6', 'form_10',
            'total_points_6', 'total_points_10', 'serie_domicile', 'serie_exterieur',
            'buts_dom_marques', 'buts_dom_encaisses', 'buts_ext_marques', 'buts_ext_encaisses'
        ],
        'classement': [
            'classement_home', 'classement_away', 'points_classement_home', 'points_classement_away'
        ],
        'match_stats': [
            'Possession', 'Shots on Goal', 'Shot Attempts', 'Corner Kicks', 'Saves', 'Yellow Cards'
        ]
    }

    def __init__(self, source_dir: str = ".", output_file: str = "Analysesdata.json", api_key: str = ""):
        self.source_dir = Path(source_dir)
        self.output_file = Path(output_file)
        self.api_key = api_key

    def get_yesterday_filename(self) -> str:
        yesterday = datetime.now() - timedelta(days=1)
        return f"prédiction-{yesterday.strftime('%Y-%m-%d')}-analyse-ia.json"

    def convert_form_to_numeric(self, form_list: List[str]) -> List[int]:
        mapping = {'W': 1, 'L': -1, 'D': 0}
        return [mapping.get(result, 0) for result in form_list]

    def extract_possession(self, possession_str: str) -> float:
        try:
            return float(possession_str.strip('%')) / 100
        except (ValueError, AttributeError):
            return 0.0

    def clean_match_stats(self, stats: Dict) -> Dict:
        if not stats:
            return {}
        cleaned = {}
        for key in self.FIELDS_TO_KEEP['match_stats']:
            if key in stats:
                value = stats[key]
                if key == 'Possession' and isinstance(value, list) and len(value) == 2:
                    cleaned['possession_home'] = self.extract_possession(value[0])
                    cleaned['possession_away'] = self.extract_possession(value[1])
                elif isinstance(value, list) and len(value) == 2:
                    try:
                        cleaned[f"{key.lower().replace(' ', '_')}_home"] = int(value[0])
                        cleaned[f"{key.lower().replace(' ', '_')}_away"] = int(value[1])
                    except (ValueError, TypeError):
                        pass
        return cleaned

    def clean_last_matches(self, matches: List[Dict], max_matches: int = 10) -> List[Dict]:
        cleaned_matches = []
        for match in matches[:max_matches]:
            score = match.get('score', '0 - 0')
            try:
                parts = score.replace(' ', '').split('-')
                home_score, away_score = map(int, parts)
            except (ValueError, AttributeError):
                home_score, away_score = 0, 0
            cleaned_matches.append({
                'date': match.get('date', ''),
                'home_team': match.get('home_team', ''),
                'away_team': match.get('away_team', ''),
                'score_home': home_score,
                'score_away': away_score,
                'stats': self.clean_match_stats(match.get('stats', {}))
            })
        return cleaned_matches

    def clean_h2h(self, h2h_matches: List[Dict]) -> List[Dict]:
        cleaned_h2h = []
        for match in h2h_matches:
            score = match.get('score', '0 - 0')
            try:
                parts = score.replace(' ', '').split('-')
                home_score, away_score = map(int, parts)
            except (ValueError, AttributeError):
                home_score, away_score = 0, 0
            cleaned_h2h.append({
                'date': match.get('date', ''),
                'team1': match.get('team1', ''),
                'team2': match.get('team2', ''),
                'score_home': home_score,
                'score_away': away_score,
                'stats': self.clean_match_stats(match.get('stats', {}))
            })
        return cleaned_h2h

    def generate_predict_targets(self, halftime: dict, fulltime: dict) -> dict:
        def _calc_targets(score_home: int, score_away: int) -> dict:
            total_goals = score_home + score_away

            if score_home > score_away:
                res_1x2 = "1"
            elif score_home < score_away:
                res_1x2 = "2"
            else:
                res_1x2 = "X"

            if res_1x2 == "1":
                double_chance_valid = ["1X", "12"]
            elif res_1x2 == "2":
                double_chance_valid = ["X2", "12"]
            else:
                double_chance_valid = ["1X", "X2"]

            thresholds = [2, 2.5, 3, 3.5]
            over_under_valid = []
            for t in thresholds:
                if total_goals > t:
                    over_under_valid.append(f"over_{str(t).replace('.', '_')}")
                else:
                    over_under_valid.append(f"under_{str(t).replace('.', '_')}")

            btts_valid = ["yes"] if (score_home > 0 and score_away > 0) else ["no"]

            return {
                "1x2": [res_1x2],
                "double_chance": double_chance_valid,
                "over_under": over_under_valid,
                "btts": btts_valid
            }

        ht_home = halftime.get("home", 0)
        ht_away = halftime.get("away", 0)
        halftime_targets = _calc_targets(ht_home, ht_away)

        ft_home = fulltime.get("home", 0)
        ft_away = fulltime.get("away", 0)
        fulltime_targets = _calc_targets(ft_home, ft_away)

        return {
            "halftime": halftime_targets,
            "fulltime": fulltime_targets
        }

    def fetch_scores_from_api(self, fixture_id: int) -> dict:
        default = {
            "halftime": {"home": 0, "away": 0},
            "fulltime": {"home": 0, "away": 0},
            "status": ""
        }

        if not self.api_key:
            print("⚠️ Pas de clé API fournie. Scores par défaut (0-0).")
            return default

        url = f"https://v3.football.api-sports.io/fixtures?id={fixture_id}"
        headers = {"x-apisports-key": self.api_key}

        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code != 200:
                print(f"❌ Erreur API [{response.status_code}] pour fixture {fixture_id}")
                return default

            data = response.json()
            resp_list = data.get("response", [])
            if not resp_list:
                print(f"⚠️ Aucun résultat pour fixture {fixture_id}")
                return default

            item = resp_list[0]
            fixture = item.get("fixture", {})
            scores = item.get("score", {})

            halftime_home = scores.get("halftime", {}).get("home", 0)
            halftime_away = scores.get("halftime", {}).get("away", 0)
            fulltime_home = scores.get("fulltime", {}).get("home", 0)
            fulltime_away = scores.get("fulltime", {}).get("away", 0)
            status_long = fixture.get("status", {}).get("long", "")

            return {
                "halftime": {"home": int(halftime_home or 0), "away": int(halftime_away or 0)},
                "fulltime": {"home": int(fulltime_home or 0), "away": int(fulltime_away or 0)},
                "status": status_long
            }

        except Exception as e:
            print(f"❌ Erreur pour fixture {fixture_id}: {e}")
            return default

    def clean_prediction(self, prediction: Dict) -> Dict:
        cleaned = {}

        for field in self.FIELDS_TO_KEEP['match_info']:
            if field in prediction:
                cleaned[field] = prediction[field]

        for side in ['home', 'away']:
            stats = prediction.get(f"stats_{side}", {})
            cleaned[f'stats_{side}'] = {
                'moyenne_marques': stats.get('moyenne_marques', 0),
                'moyenne_encaisses': stats.get('moyenne_encaisses', 0),
                'form_6_numeric': self.convert_form_to_numeric(stats.get('form_6', [])),
                'form_10_numeric': self.convert_form_to_numeric(stats.get('form_10', [])),
                'total_points_6': stats.get('total_points_6', 0),
                'total_points_10': stats.get('total_points_10', 0),
                'buts_dom_marques': stats.get('buts_dom_marques', 0),
                'buts_dom_encaisses': stats.get('buts_dom_encaisses', 0),
                'buts_ext_marques': stats.get('buts_ext_marques', 0),
                'buts_ext_encaisses': stats.get('buts_ext_encaisses', 0)
            }

        for field in self.FIELDS_TO_KEEP['classement']:
            if field in prediction:
                cleaned[field] = prediction[field]

        cleaned['last_matches_home'] = self.clean_last_matches(prediction.get('last_matches_home', []))
        cleaned['last_matches_away'] = self.clean_last_matches(prediction.get('last_matches_away', []))
        cleaned['h2h'] = self.clean_h2h(prediction.get('confrontations_saison_derniere', []))

        fixture_id = prediction.get('fixture_id', 0)
        actual_scores = self.fetch_scores_from_api(fixture_id)
        cleaned['actual_scores'] = actual_scores

        halftime_scores = actual_scores.get('halftime', {})
        fulltime_scores = actual_scores.get('fulltime', {})
        cleaned['predict_targets'] = self.generate_predict_targets(halftime_scores, fulltime_scores)

        return cleaned

    def load_existing_data(self) -> List[Dict]:
        if not self.output_file.exists():
            return []
        try:
            with open(self.output_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('predictions', [])
        except Exception as e:
            print(f"⚠️ Erreur lecture {self.output_file}: {e}")
            return []

    def save_consolidated_data(self, predictions: List[Dict]):
        output = {
            'metadata': {
                'total_matches': len(predictions),
                'last_update': datetime.now().isoformat(),
                'description': 'Données consolidées pour entraînement RNN'
            },
            'predictions': predictions
        }
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"✅ Données sauvegardées dans {self.output_file}")

    def process_yesterday_file(self) -> bool:
        yesterday_file = self.source_dir / self.get_yesterday_filename()
        if not yesterday_file.exists():
            print(f"❌ Fichier introuvable: {yesterday_file}")
            return False

        with open(yesterday_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        raw_predictions = data.get('statistiques_brutes_avec_ia_hors_montecarlo', {}).get('details', [])
        if not raw_predictions:
            print("⚠️ Aucun match trouvé")
            return False

        cleaned_predictions = [self.clean_prediction(pred) for pred in raw_predictions]

        existing_data = self.load_existing_data()
        existing_ids = {pred.get('fixture_id') for pred in existing_data}
        new_predictions = [pred for pred in cleaned_predictions if pred.get('fixture_id') not in existing_ids]

        all_predictions = existing_data + new_predictions
        self.save_consolidated_data(all_predictions)
        return True


def main():
    print("=" * 60)
    print("🔄 CONSOLIDATION DES MATCHS FOOTBALL AVEC SCORES RÉELS")
    print("=" * 60)

    api_key = os.environ.get("API_FOOTBALL_KEY", "")
    consolidator = FootballDataConsolidator(source_dir=".", output_file="Analysesdata.json", api_key=api_key)
    success = consolidator.process_yesterday_file()

    if success:
        print("\n✅ Consolidation terminée avec succès!")
    else:
        print("\n❌ Échec de la consolidation")
    print("=" * 60)


if __name__ == "__main__":
    main()