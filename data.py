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
                home_score, away_score = map(int, score.split(' - '))
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
                home_score, away_score = map(int, score.split(' - '))
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

    def generate_predict_targets(self, score_home: int, score_away: int) -> dict:
        x1x2 = "1" if score_home > score_away else "2" if score_home < score_away else "X"
        over_under = "over_2.5" if (score_home + score_away) > 2.5 else "under_2.5"
        btts = "yes" if score_home > 0 and score_away > 0 else "no"
        double_chance = "1X" if score_home > score_away else "X2" if score_home < score_away else "12"
        return {
            "1x2": x1x2,
            "over_under": over_under,
            "btts": btts,
            "double_chance": double_chance
        }

    def fetch_scores_from_api(self, fixture_id: int) -> dict:
        """Récupère tous les matchs d'hier et filtre par fixture_id"""
        if not self.api_key:
            return {"halftime": "0-0", "fulltime": "0-0"}
        try:
            yesterday = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%d')
            url = f"https://v3.football.api-sports.io/fixtures?date={yesterday}"
            headers = {"x-apisports-key": self.api_key}
            response = requests.get(url, headers=headers, timeout=10)
            data = response.json().get("response", [])

            # Filtrage pour le fixture_id
            match = next((m for m in data if m.get("fixture", {}).get("id") == fixture_id), None)
            if not match:
                return {"halftime": "0-0", "fulltime": "0-0"}

            scores = match.get("score", {})
            return {
                "halftime": f"{scores.get('halftime', {}).get('home',0)}-{scores.get('halftime', {}).get('away',0)}",
                "fulltime": f"{scores.get('fulltime', {}).get('home',0)}-{scores.get('fulltime', {}).get('away',0)}"
            }
        except Exception as e:
            print(f"⚠️ Erreur API pour fixture {fixture_id}: {e}")
            return {"halftime": "0-0", "fulltime": "0-0"}

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
        home_score, away_score = map(int, actual_scores['fulltime'].split('-'))
        cleaned['predict_targets'] = self.generate_predict_targets(home_score, away_score)

        return cleaned

    def load_existing_data(self) -> List[Dict]:
        if not self.output_file.exists():
            return []
        try:
            with open(self.output_file, 'r', encoding='utf-8') as f:
                return json.load(f).get('predictions', [])
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
        print(f"📊 Total de matchs: {len(predictions)}")

    def process_yesterday_file(self) -> bool:
        yesterday_file = self.source_dir / self.get_yesterday_filename()
        if not yesterday_file.exists():
            print(f"❌ Fichier introuvable: {yesterday_file}")
            return False

        print(f"📂 Lecture du fichier: {yesterday_file}")
        try:
            with open(yesterday_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            raw_predictions = data.get('statistiques_brutes_avec_ia_hors_montecarlo', {}).get('details', [])
            if not raw_predictions:
                print("⚠️ Aucun match trouvé")
                return False

            print(f"🔍 {len(raw_predictions)} matchs trouvés")
            cleaned_predictions = [self.clean_prediction(pred) for pred in raw_predictions]

            existing_data = self.load_existing_data()
            existing_ids = {pred.get('fixture_id') for pred in existing_data}
            new_predictions = [pred for pred in cleaned_predictions if pred.get('fixture_id') not in existing_ids]

            if not new_predictions:
                print("ℹ️ Tous les matchs existent déjà dans Analysesdata.json")
                return True

            print(f"➕ Ajout de {len(new_predictions)} nouveaux matchs")
            all_predictions = existing_data + new_predictions
            self.save_consolidated_data(all_predictions)
            return True

        except Exception as e:
            print(f"❌ Erreur lors du traitement: {e}")
            return False

def main():
    print("="*60)
    print("🔄 CONSOLIDATION DES MATCHS FOOTBALL AVEC SCORES RÉELS")
    print("="*60)

    api_key = os.environ.get("API_FOOTBALL_KEY", "")
    consolidator = FootballDataConsolidator(source_dir=".", output_file="Analysesdata.json", api_key=api_key)
    success = consolidator.process_yesterday_file()

    if success:
        print("\n✅ Consolidation terminée avec succès!")
    else:
        print("\n❌ Échec de la consolidation")
    print("="*60)

if __name__ == "__main__":
    main()