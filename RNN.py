import json
import numpy as np
import os
from pathlib import Path
from typing import Dict, Any, List, Tuple
from sklearn.preprocessing import StandardScaler

# ---------- CONFIG ----------
DATA_PATH = Path("Analysesdata.json")
LOOKBACK = 6
FUSION_STRATEGY = "concat_pair"
SAVE_PREFIX = "hist_seq"
INCLUDE_TEAM_ONEHOT = True
# ---------------------------

HIST_MATCH_STATS_KEYS = [
    "possession_home", "possession_away",
    "shots_on_goal_home", "shots_on_goal_away",
    "shot_attempts_home", "shot_attempts_away",
    "corner_kicks_home", "corner_kicks_away",
    "saves_home", "saves_away",
    "yellow_cards_home", "yellow_cards_away",
    "classement_home", "classement_away",
    "points_classement_home", "points_classement_away"
]

CATEGORICAL_FEATURES = ["HomeTeam", "AwayTeam", "league"]

# ---------- UTILITAIRES ----------
def load_json(path: Path) -> Dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        return json.load(f)

def safe_float(x, default=0.0):
    try:
        return float(x)
    except Exception:
        return float(default)

def get_last_matches_list(match_obj: Dict[str, Any], side: str) -> List[Dict[str, Any]]:
    return match_obj.get(f"last_matches_{side}", []) or []

def build_team_onehot_maps(predictions: List[Dict[str, Any]]) -> Dict[str, List[str]]:
    maps = {}
    for cat in CATEGORICAL_FEATURES:
        vals = []
        for m in predictions:
            v = m.get(cat, "")
            if v not in vals:
                vals.append(v)
        maps[cat] = vals
    return maps

# ---------- VECTEURS ----------
def build_timestep_vector(home_entry: Dict[str, Any], away_entry: Dict[str, Any],
                          perspective: str, team_onehots: Dict[str, List[str]],
                          include_onehot: bool) -> Tuple[np.ndarray, List[str]]:
    feat, names = [], []

    def extract_from_entry(entry, team_role):
        if entry is None:
            return {k: 0.0 for k in HIST_MATCH_STATS_KEYS + ["score_home", "score_away", "result_view", "was_home"]}
        stats = entry.get("stats", {}) or {}
        out = {}
        for k in HIST_MATCH_STATS_KEYS:
            if k in stats:
                out[k] = safe_float(stats.get(k, 0.0))
            else:
                out[k] = safe_float(entry.get(k, 0.0))
        sh = safe_float(entry.get("score_home", 0))
        sa = safe_float(entry.get("score_away", 0))
        out["score_home"] = sh
        out["score_away"] = sa
        out["was_home"] = 1.0 if team_role == "home_entry" else 0.0
        out["result_view"] = 1.0 if (sh > sa if team_role == "home_entry" else sa > sh) else (0.0 if sh == sa else -1.0)
        return out

    home_feats = extract_from_entry(home_entry, "home_entry")
    away_feats = extract_from_entry(away_entry, "away_entry")

    for k in sorted(home_feats.keys()):
        feat.append(float(home_feats[k]))
        names.append(f"home_{k}")
    for k in sorted(away_feats.keys()):
        feat.append(float(away_feats[k]))
        names.append(f"away_{k}")

    feat.extend([1.0 if perspective == "home" else 0.0, 1.0 if perspective == "away" else 0.0])
    names.extend(["perspective_is_home", "perspective_is_away"])

    if include_onehot and team_onehots:
        for cat in CATEGORICAL_FEATURES:
            for c in team_onehots.get(cat, []):
                feat.append(0.0)
                names.append(f"{cat}={c}")

    return np.array(feat, dtype=np.float32), names

# ---------- CIBLES ----------
def target_builder(match: Dict[str, Any]) -> List[float]:
    """
    Convertit les cibles en un vecteur numérique unique :
    [1x2, double_chance, over_under, btts]
    """
    targets = match.get("predict_targets", {})
    ft = targets.get("fulltime", {})

    t1x2 = ft.get("1x2", [None])[0]
    tdc = ft.get("double_chance", [None])[0]
    tou = ft.get("over_under", [None])[0]
    tbtts = ft.get("btts", [None])[0]

    def encode(val):
        if val is None:
            return 0.0
        if isinstance(val, str):
            if val in ["1", "1X", "X1"]:
                return 1.0
            if val in ["X2", "2X", "2"]:
                return 2.0
            if val.lower() in ["over", "oui", "yes"]:
                return 1.0
            if val.lower() in ["under", "non", "no"]:
                return 0.0
        try:
            return float(val)
        except:
            return 0.0

    return [encode(t1x2), encode(tdc), encode(tou), encode(tbtts)]

# ---------- ASSEMBLAGE ----------
def assemble_sequences(data: Dict[str, Any], lookback=LOOKBACK,
                       fusion=FUSION_STRATEGY, include_onehot=INCLUDE_TEAM_ONEHOT):
    preds = data.get("predictions", [])
    team_maps = build_team_onehot_maps(preds) if include_onehot else {}
    seq_list, ids, targets_list, feature_names_global = [], [], [], None
    all_timesteps = []

    for match in preds:
        fid = match.get("fixture_id")
        if not fid:
            continue
        hist_home = get_last_matches_list(match, "home")[:lookback]
        hist_away = get_last_matches_list(match, "away")[:lookback]

        def pad(lst): return lst + [None]*(lookback - len(lst)) if len(lst) < lookback else lst[:lookback]
        hist_home, hist_away = pad(hist_home), pad(hist_away)

        timesteps, names_for_timestep = [], None
        for i in range(lookback):
            vec, names = build_timestep_vector(hist_home[i], hist_away[i],
                                               perspective="home",
                                               team_onehots=team_maps,
                                               include_onehot=include_onehot)
            timesteps.append(vec)
            if names_for_timestep is None:
                names_for_timestep = names

        seq = np.stack(timesteps, axis=0)
        if include_onehot and team_maps:
            for t in range(seq.shape[0]):
                for cat in CATEGORICAL_FEATURES:
                    for c in team_maps[cat]:
                        val = 1.0 if match.get(cat, "") == c else 0.0
                        try:
                            pos = names_for_timestep.index(f"{cat}={c}")
                            seq[t, pos] = val
                        except ValueError:
                            pass

        all_timesteps.append(seq)
        seq_list.append(seq)
        ids.append(fid)
        targets_list.append(target_builder(match))
        if feature_names_global is None:
            feature_names_global = names_for_timestep

    seq_len = seq_list[0].shape[0]
    n_feats = seq_list[0].shape[1]
    all_flat = np.concatenate([s.reshape(-1, n_feats) for s in all_timesteps], axis=0)
    cat_indices = [i for i, n in enumerate(feature_names_global)
                   if any(n.startswith(cat+"=") for cat in CATEGORICAL_FEATURES)]
    num_indices = [i for i in range(n_feats) if i not in cat_indices]

    scaler = StandardScaler()
    if num_indices:
        scaler.fit(all_flat[:, num_indices])

    X_array = np.stack(seq_list, axis=0)
    for i in range(X_array.shape[0]):
        for j in num_indices:
            X_array[i, :, j] = (X_array[i, :, j] - scaler.mean_[num_indices.index(j)]) / (scaler.scale_[num_indices.index(j)] + 1e-9)

    y_array = np.array(targets_list, dtype=np.float32)
    return X_array.astype(np.float32), y_array, feature_names_global, ids

# ---------- FUSION/ÉCRASEMENT ----------
def merge_with_existing(X_new, y_new, ids_new, feature_names, prefix=SAVE_PREFIX):
    X_path, y_path, id_path = f"{prefix}_X.npy", f"{prefix}_y.npy", f"{prefix}_ids.npy"

    # Si les fichiers existent mais sont vides → on les écrase
    if all(os.path.exists(p) for p in [X_path, y_path, id_path]):
        if os.path.getsize(X_path) == 0 or os.path.getsize(y_path) == 0 or os.path.getsize(id_path) == 0:
            print("⚠️ Fichiers vides détectés → réinitialisation.")
            os.remove(X_path)
            os.remove(y_path)
            os.remove(id_path)

    files_exist = all(os.path.exists(p) for p in [X_path, y_path, id_path])

    if files_exist:
        ids_old = np.load(id_path, allow_pickle=True).tolist()
        new_indices = [i for i, fid in enumerate(ids_new) if fid not in ids_old]
        if not new_indices:
            print("Aucune nouvelle donnée à ajouter.")
            return
        X_old = np.load(X_path)
        y_old = np.load(y_path)
        X_combined = np.concatenate([X_old, X_new[new_indices]], axis=0)
        y_combined = np.concatenate([y_old, y_new[new_indices]], axis=0)
        ids_combined = ids_old + [ids_new[i] for i in new_indices]
    else:
        X_combined, y_combined, ids_combined = X_new, y_new, ids_new

    np.save(X_path, X_combined)
    np.save(y_path, y_combined)
    np.save(id_path, np.array(ids_combined))
    with open(f"{prefix}_feature_names.txt", "w", encoding="utf-8") as f:
        for n in feature_names:
            f.write(n + "\n")

    print(f"✅ Fichiers mis à jour ({len(ids_combined)} séquences totales)")
    print(f"→ X.shape = {X_combined.shape}, y.shape = {y_combined.shape}")

# ---------- MAIN ----------
def main():
    data = load_json(DATA_PATH)
    X, y, feature_names, ids = assemble_sequences(data)
    merge_with_existing(X, y, ids, feature_names)
    print("Exemple cible (y[0]):", y[0])

if __name__ == "__main__":
    main()