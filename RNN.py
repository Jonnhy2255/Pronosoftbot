import json
import numpy as np
from pathlib import Path
from collections import defaultdict
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from typing import List, Dict, Any, Tuple

CONFIGURATION

DATA_PATH = Path("data.json")
LOOKBACK = 6          # longueur temporelle (nombre de matchs à empiler). Ajustez.
STEP = 1              # pas glissant pour générer les séquences
PAD_VALUE = 0.0       # valeur pour padding
SAVE_PREFIX = "seq_output"

Choisir quelles caractéristiques extraires de chaque match/historique.

On construit les features à partir des blocs : stats_home, stats_away, classement, points, dernier match (aggregate), etc.

NUMERIC_FEATURES = [
# stats_home
"stats_home.moyenne_marques",
"stats_home.moyenne_encaisses",
"stats_home.total_points_6",
"stats_home.total_points_10",
"stats_home.buts_dom_marques",
"stats_home.buts_dom_encaisses",
"stats_home.buts_ext_marques",
"stats_home.buts_ext_encaisses",
# stats_away
"stats_away.moyenne_marques",
"stats_away.moyenne_encaisses",
"stats_away.total_points_6",
"stats_away.total_points_10",
"stats_away.buts_dom_marques",
"stats_away.buts_dom_encaisses",
"stats_away.buts_ext_marques",
"stats_away.buts_ext_encaisses",
# classement / points
"classement_home",
"classement_away",
"points_classement_home",
"points_classement_away",
]

Catégories simples à one-hot (teams, league)

CATEGORICAL_FEATURES = [
"HomeTeam",
"AwayTeam",
"league",
]

Quel target voulez-vous ? Exemple inclus: prédire résultat fulltime 1x2 (actual_scores.fulltime)

Le target_builder doit renvoyer un vecteur numpy pour chaque exemple.

def target_builder(match: Dict[str, Any]) -> np.ndarray:
"""
Construire la cible pour un match donné.
Ici: 1x2 fulltime encodé en one-hot [home_win, draw, away_win]
Vous pouvez modifier pour btts, over/under, ou multi-task.
"""
ft = match.get("actual_scores", {}).get("fulltime", {})
if not ft:
# si absent, renvoyer un vecteur neutre (ici [0,0,0]) -> exclure plus tard si nécessaire
return np.array([0, 0, 0], dtype=np.float32)
home = ft.get("home", 0)
away = ft.get("away", 0)
if home > away:
return np.array([1, 0, 0], dtype=np.float32)
elif home == away:
return np.array([0, 1, 0], dtype=np.float32)
else:
return np.array([0, 0, 1], dtype=np.float32)

###########################

Fonctions utilitaires

###########################

def load_json(path: Path) -> Dict[str, Any]:
with path.open(encoding="utf-8") as f:
return json.load(f)

def get_by_path(d: Dict[str, Any], path: str, default=None):
"""Accéder à la clé imbriquée 'a.b.c' dans un dict en retournant default si absent."""
parts = path.split(".")
cur = d
for p in parts:
if isinstance(cur, dict) and p in cur:
cur = cur[p]
else:
return default
return cur

def aggregate_last_matches_stats(last_matches: List[Dict[str, Any]], prefix: str = "") -> Dict[str, float]:
"""
Calcule des agrégats simples sur une liste de derniers matchs:
moyenne possession, moyenne shots_on_goal (home/away selon perspective), buts moyen, etc.
On retourne des features préfixées.
Important: last_matches est la liste complète de "last_matches_home" ou "last_matches_away",
il faut être cohérent avec la perspective (ex: pour équipe à domicile, last_matches_home contient matchs où
l'équipe était à domicile).
"""
if not last_matches:
return {}
agg = defaultdict(list)
for m in last_matches:
stats = m.get("stats", {})
# on collecte quelques stats si présentes
for key in ("possession_home", "possession_away",
"shots_on_goal_home", "shots_on_goal_away",
"shot_attempts_home", "shot_attempts_away",
"corner_kicks_home", "corner_kicks_away",
"saves_home", "saves_away",
"yellow_cards_home", "yellow_cards_away"):
if key in stats:
agg[key].append(float(stats[key]))

# créer features: moyenne et écart-type pour quelques clés si disponibles  
out = {}  
for k, vals in agg.items():  
    vals = np.array(vals, dtype=np.float32)  
    out[f"{prefix}{k}_mean"] = float(vals.mean())  
    out[f"{prefix}{k}_std"] = float(vals.std())  
    out[f"{prefix}{k}_count"] = int(len(vals))  
return out

def build_feature_vector(match: Dict[str, Any],
team_encoders: Dict[str, OneHotEncoder],
categorical_maps: Dict[str, List[str]]) -> Tuple[np.ndarray, List[str]]:
"""
Construit le vecteur de caractéristiques pour un match donné (sans historique temporel explicite).
Il contient:
- NUMERIC_FEATURES extraits,
- agrégats des derniers matches (home/away),
- encodage one-hot des catégories (HomeTeam, AwayTeam, league).
Retourne (vector, feature_names_list).
"""
feat = []
names = []

# Numerics (extraction directe, valeur 0 si manquante)  
for p in NUMERIC_FEATURES:  
    v = get_by_path(match, p, 0.0)  
    try:  
        fv = float(v) if v is not None else 0.0  
    except Exception:  
        fv = 0.0  
    feat.append(fv)  
    names.append(p)  

# Aggregats des derniers matches (home perspective)  
agg_home = aggregate_last_matches_stats(match.get("last_matches_home", []), prefix="home_")  
agg_away = aggregate_last_matches_stats(match.get("last_matches_away", []), prefix="away_")  
# Joindre clés de manière déterministe  
for k in sorted(set(list(agg_home.keys()) + list(agg_away.keys()))):  
    # si absent, mettre 0  
    feat.append(float(agg_home.get(k, 0.0)))  
    names.append(k)  
    feat.append(float(agg_away.get(k, 0.0)))  
    names.append("paired_"+k)  # pour garder trace de l'origine  
    # Note: cela double certaines features ; vous pouvez fusionner/adapter  

# Catégories: one-hot encodées via OneHotEncoder pour consistance  
for cat in CATEGORICAL_FEATURES:  
    val = match.get(cat, "")  
    # encoder via mapping list pour créer one-hot  
    categories = categorical_maps.get(cat, [])  
    one_hot = [1.0 if val == c else 0.0 for c in categories]  
    feat.extend(one_hot)  
    for c in categories:  
        names.append(f"{cat}={c}")  

return np.array(feat, dtype=np.float32), names

###########################

Pipeline principal

###########################

def build_category_maps(predictions: List[Dict[str, Any]]) -> Dict[str, List[str]]:
"""Trouver toutes les valeurs uniques pour chaque champ catégoriel (utile pour one-hot)."""
maps = {}
for cat in CATEGORICAL_FEATURES:
vals = []
for m in predictions:
v = m.get(cat, "")
if v not in vals:
vals.append(v)
maps[cat] = vals
return maps

def build_matrix_and_sequences(data: Dict[str, Any],
lookback: int = LOOKBACK,
step: int = STEP) -> Tuple[np.ndarray, np.ndarray, List[str]]:
"""
Transforme chaque entrée 'prediction' en une séquence (historique) de longueur lookback.
Ici on considère la donnée fournie comme une position temporelle par match (chaque objet représente un
match avec son historique). Pour former des séquences, on peut :
- utiliser les listes last_matches_{home,away} pour construire une séquence interne,
- ou considérer la liste globale data['predictions'] triée par date et former des fenêtres.
Dans ce script nous construisons des séquences par match en utilisant :
- pour chaque match, on extrait un vecteur "instantané" (features courantes/agrégats des n derniers matchs)
- puis on génère séquences glissantes à partir de la liste des vecteurs instants triés par date.
"""
preds = data.get("predictions", [])
# Trier par date si possible (simple tri lexicographique sur la string ISO-fr utilisée)
# NOTE: ici les dates sont en français "28 octobre 2025 ..." donc tri alphabétique peut être insuffisant.
# Nous utilisons l'ordre tel que fourni dans le fichier.
predictions = preds

# Construire les maps catégorielles  
cat_maps = build_category_maps(predictions)  

# Construire vecteurs instantanés  
features = []  
names = None  
for m in predictions:  
    vec, names = build_feature_vector(m, team_encoders={}, categorical_maps=cat_maps)  
    features.append(vec)  
features = np.stack(features, axis=0) if features else np.zeros((0, 0), dtype=np.float32)  

# Normalisation des features numériques : utiliser StandardScaler  
scaler = StandardScaler()  
if features.shape[0] > 0:  
    features = scaler.fit_transform(features)  

# Construire targets  
targets = [target_builder(m) for m in predictions]  
targets = np.stack(targets, axis=0) if targets else np.zeros((0, 0), dtype=np.float32)  

# Générer séquences glissantes  
X_seqs = []  
y_seqs = []  
n = features.shape[0]  
for start in range(0, n - lookback + 1, step):  
    end = start + lookback  
    seq = features[start:end]           # shape (lookback, n_features)  
    # choisir target : prédire le match à la fin de la fenêtre (cas classique)  
    target = targets[end - 1]  
    # Optionnel : ignorer si target neutre (par ex [0,0,0]) -> ici on garde tout  
    X_seqs.append(seq)  
    y_seqs.append(target)  

if len(X_seqs) == 0:  
    # si moins de lookback matches, on peut faire padding pour obtenir au moins un exemple  
    # construire un exemple avec padding à gauche  
    seq = np.zeros((lookback, features.shape[1]), dtype=np.float32)  
    pad_len = lookback - n  
    if n > 0:  
        seq[pad_len:, :] = features  
    else:  
        # pas de données  
        pass  
    X_seqs.append(seq)  
    # target : dernier match si existe sinon zeros  
    if n > 0:  
        y_seqs.append(targets[-1])  
    else:  
        y_seqs.append(np.zeros_like(targets[0]) if targets.shape[0] > 0 else np.zeros((3,), dtype=np.float32))  

X = np.stack(X_seqs, axis=0).astype(np.float32)  # (n_samples, lookback, n_features)  
y = np.stack(y_seqs, axis=0).astype(np.float32)  # (n_samples, n_targets)  

return X, y, names

def save_numpy_arrays(X: np.ndarray, y: np.ndarray, prefix: str = SAVE_PREFIX, task_name: str = "1x2_fulltime"):
np.save(f"{prefix}_X.npy", X)
np.save(f"{prefix}y{task_name}.npy", y)
print(f"Sauvegardé : {prefix}_X.npy (shape {X.shape}), {prefix}y{task_name}.npy (shape {y.shape})")

###########################

Main

###########################

def main():
data = load_json(DATA_PATH)
X, y, feature_names = build_matrix_and_sequences(data, lookback=LOOKBACK, step=STEP)

print("Forme X:", X.shape)  
print("Forme y:", y.shape)  
print("Nombre de features par timestep:", (X.shape[2] if X.ndim == 3 else 0))  
if feature_names:  
    print("Exemples de noms de features (début):", feature_names[:30])  

save_numpy_arrays(X, y, prefix=SAVE_PREFIX, task_name="1x2_fulltime")  

# Exemple rapide : charger dans Keras  
try:  
    from tensorflow.keras.models import Sequential  
    from tensorflow.keras.layers import LSTM, Dense, Masking  
    n_timesteps = X.shape[1]  
    n_features = X.shape[2]  
    n_targets = y.shape[1]  
    model = Sequential([  
        Masking(mask_value=PAD_VALUE, input_shape=(n_timesteps, n_features)),  
        LSTM(64, return_sequences=False),  
        Dense(n_targets, activation='softmax')  
    ])  
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])  
    print("Modèle Keras exemple prêt (non entraîné). Vous pouvez entraîner avec model.fit(X, y, ...)")  
except Exception:  
    pass

if name == "main":
main()