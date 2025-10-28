#!/usr/bin/env python3
"""
Script de consolidation des fichiers de prédiction quotidiens
Récupère le fichier d'hier, nettoie les données et les ajoute à Analysesdata.json
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any


class FootballDataConsolidator:
    """Classe pour consolider et nettoyer les données de prédiction"""
    
    # Champs à conserver pour l'entraînement du RNN
    FIELDS_TO_KEEP = {
        'match_info': [
            'id', 'fixture_id', 'HomeTeam', 'AwayTeam', 'date', 'league'
        ],
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
        ],
        'predictions': [
            'prediction_principale', 'confiance_pourcentage', 'scores_probables'
        ],
        'probabilities': [
            '1x2', 'over_under', 'btts', 'double_chance', 'buts_moyens_simules'
        ]
    }
    
    def __init__(self, source_dir: str = ".", output_file: str = "Analysesdata.json"):
        """
        Initialise le consolidateur
        
        Args:
            source_dir: Répertoire contenant les fichiers de prédiction
            output_file: Nom du fichier de sortie consolidé
        """
        self.source_dir = Path(source_dir)
        self.output_file = Path(output_file)
        
    def get_yesterday_filename(self) -> str:
        """Génère le nom du fichier d'hier"""
        yesterday = datetime.now() - timedelta(days=1)
        return f"prédiction-{yesterday.strftime('%Y-%m-%d')}-analyse-ia.json"
    
    def convert_form_to_numeric(self, form_list: List[str]) -> List[int]:
        """
        Convertit la forme ['W', 'L', 'D'] en valeurs numériques [1, -1, 0]
        
        Args:
            form_list: Liste de résultats (W/L/D)
            
        Returns:
            Liste de valeurs numériques
        """
        mapping = {'W': 1, 'L': -1, 'D': 0}
        return [mapping.get(result, 0) for result in form_list]
    
    def extract_possession(self, possession_str: str) -> float:
        """
        Convertit '58.8%' en 0.588
        
        Args:
            possession_str: String de possession avec %
            
        Returns:
            Valeur décimale
        """
        try:
            return float(possession_str.strip('%')) / 100
        except (ValueError, AttributeError):
            return 0.0
    
    def clean_match_stats(self, stats: Dict) -> Dict:
        """
        Nettoie et normalise les statistiques d'un match
        
        Args:
            stats: Dictionnaire des statistiques brutes
            
        Returns:
            Dictionnaire nettoyé
        """
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
        """
        Nettoie l'historique des matchs récents
        
        Args:
            matches: Liste des matchs récents
            max_matches: Nombre maximum de matchs à conserver
            
        Returns:
            Liste nettoyée et limitée
        """
        cleaned_matches = []
        
        for match in matches[:max_matches]:
            score = match.get('score', '0 - 0')
            try:
                home_score, away_score = map(int, score.split(' - '))
            except (ValueError, AttributeError):
                home_score, away_score = 0, 0
            
            cleaned_match = {
                'date': match.get('date', ''),
                'home_team': match.get('home_team', ''),
                'away_team': match.get('away_team', ''),
                'score_home': home_score,
                'score_away': away_score,
                'stats': self.clean_match_stats(match.get('stats', {}))
            }
            cleaned_matches.append(cleaned_match)
        
        return cleaned_matches
    
    def clean_h2h(self, h2h_matches: List[Dict]) -> List[Dict]:
        """
        Nettoie les confrontations directes
        
        Args:
            h2h_matches: Liste des matchs H2H
            
        Returns:
            Liste nettoyée
        """
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
    
    def clean_prediction(self, prediction: Dict) -> Dict:
        """
        Nettoie une prédiction complète
        
        Args:
            prediction: Dictionnaire de prédiction brut
            
        Returns:
            Dictionnaire nettoyé
        """
        cleaned = {}
        
        # Informations du match
        for field in self.FIELDS_TO_KEEP['match_info']:
            if field in prediction:
                cleaned[field] = prediction[field]
        
        # Statistiques home
        stats_home = prediction.get('stats_home', {})
        cleaned['stats_home'] = {
            'moyenne_marques': stats_home.get('moyenne_marques', 0),
            'moyenne_encaisses': stats_home.get('moyenne_encaisses', 0),
            'form_6_numeric': self.convert_form_to_numeric(stats_home.get('form_6', [])),
            'form_10_numeric': self.convert_form_to_numeric(stats_home.get('form_10', [])),
            'total_points_6': stats_home.get('total_points_6', 0),
            'total_points_10': stats_home.get('total_points_10', 0),
            'buts_dom_marques': stats_home.get('buts_dom_marques', 0),
            'buts_dom_encaisses': stats_home.get('buts_dom_encaisses', 0),
            'buts_ext_marques': stats_home.get('buts_ext_marques', 0),
            'buts_ext_encaisses': stats_home.get('buts_ext_encaisses', 0)
        }
        
        # Statistiques away
        stats_away = prediction.get('stats_away', {})
        cleaned['stats_away'] = {
            'moyenne_marques': stats_away.get('moyenne_marques', 0),
            'moyenne_encaisses': stats_away.get('moyenne_encaisses', 0),
            'form_6_numeric': self.convert_form_to_numeric(stats_away.get('form_6', [])),
            'form_10_numeric': self.convert_form_to_numeric(stats_away.get('form_10', [])),
            'total_points_6': stats_away.get('total_points_6', 0),
            'total_points_10': stats_away.get('total_points_10', 0),
            'buts_dom_marques': stats_away.get('buts_dom_marques', 0),
            'buts_dom_encaisses': stats_away.get('buts_dom_encaisses', 0),
            'buts_ext_marques': stats_away.get('buts_ext_marques', 0),
            'buts_ext_encaisses': stats_away.get('buts_ext_encaisses', 0)
        }
        
        # Classement
        for field in self.FIELDS_TO_KEEP['classement']:
            if field in prediction:
                cleaned[field] = prediction[field]
        
        # Matchs récents
        cleaned['last_matches_home'] = self.clean_last_matches(
            prediction.get('last_matches_home', [])
        )
        cleaned['last_matches_away'] = self.clean_last_matches(
            prediction.get('last_matches_away', [])
        )
        
        # Confrontations directes
        cleaned['h2h'] = self.clean_h2h(
            prediction.get('confrontations_saison_derniere', [])
        )
        
        # Probabilités Monte-Carlo
        probs = prediction.get('Probabilites', {})
        cleaned['probabilites'] = {
            '1x2': probs.get('1x2', {}),
            'over_under': probs.get('over_under', {}),
            'btts': probs.get('btts', {}),
            'double_chance': probs.get('double_chance', {}),
            'buts_moyens_simules': probs.get('buts_moyens_simules', {})
        }
        
        # Prédictions
        for field in self.FIELDS_TO_KEEP['predictions']:
            if field in prediction:
                cleaned[field] = prediction[field]
        
        return cleaned
    
    def load_existing_data(self) -> List[Dict]:
        """
        Charge les données existantes depuis Analysesdata.json
        
        Returns:
            Liste des données existantes ou liste vide
        """
        if not self.output_file.exists():
            return []
        
        try:
            with open(self.output_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('predictions', [])
        except (json.JSONDecodeError, IOError) as e:
            print(f"⚠️ Erreur lors de la lecture de {self.output_file}: {e}")
            return []
    
    def save_consolidated_data(self, predictions: List[Dict]):
        """
        Sauvegarde les données consolidées
        
        Args:
            predictions: Liste des prédictions à sauvegarder
        """
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
        """
        Traite le fichier d'hier et l'ajoute aux données consolidées
        
        Returns:
            True si le traitement a réussi, False sinon
        """
        yesterday_file = self.source_dir / self.get_yesterday_filename()
        
        if not yesterday_file.exists():
            print(f"❌ Fichier introuvable: {yesterday_file}")
            return False
        
        print(f"📂 Lecture du fichier: {yesterday_file}")
        
        try:
            # Charger le fichier d'hier
            with open(yesterday_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extraire les prédictions
            raw_predictions = data.get('statistiques_brutes_avec_ia_hors_montecarlo', {}).get('details', [])
            
            if not raw_predictions:
                print("⚠️ Aucune prédiction trouvée dans le fichier")
                return False
            
            print(f"🔍 {len(raw_predictions)} prédictions trouvées")
            
            # Nettoyer les prédictions
            cleaned_predictions = [self.clean_prediction(pred) for pred in raw_predictions]
            
            # Charger les données existantes
            existing_data = self.load_existing_data()
            
            # Vérifier les doublons par fixture_id
            existing_ids = {pred.get('fixture_id') for pred in existing_data}
            new_predictions = [
                pred for pred in cleaned_predictions 
                if pred.get('fixture_id') not in existing_ids
            ]
            
            if not new_predictions:
                print("ℹ️ Toutes les prédictions existent déjà dans Analysesdata.json")
                return True
            
            print(f"➕ Ajout de {len(new_predictions)} nouvelles prédictions")
            
            # Fusionner et sauvegarder
            all_predictions = existing_data + new_predictions
            self.save_consolidated_data(all_predictions)
            
            return True
            
        except (json.JSONDecodeError, IOError) as e:
            print(f"❌ Erreur lors du traitement: {e}")
            return False


def main():
    """Fonction principale"""
    print("=" * 60)
    print("🔄 CONSOLIDATION DES PRÉDICTIONS FOOTBALL")
    print("=" * 60)
    
    # Créer le consolidateur
    consolidator = FootballDataConsolidator(
        source_dir=".",  # Répertoire courant
        output_file="Analysesdata.json"
    )
    
    # Traiter le fichier d'hier
    success = consolidator.process_yesterday_file()
    
    if success:
        print("\n✅ Consolidation terminée avec succès!")
    else:
        print("\n❌ Échec de la consolidation")
    
    print("=" * 60)


if __name__ == "__main__":
    main()