import json
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = "data"
TEAMS_FILE = os.path.join(DATA_DIR, "teams.json")
SCORES_FILE = os.path.join(DATA_DIR, "scores.json")
DRAFT_FILE = os.path.join(DATA_DIR, "draft.json")

ADMIN_PASSWORD = "augusta2025"

POINTS_SYSTEM = {
    1: 10,   # Winner
    2: 7, 3: 7, 4: 7, 5: 7,       # Top 5
    6: 5, 7: 5, 8: 5, 9: 5, 10: 5, # Top 10
}
for i in range(11, 21):
    POINTS_SYSTEM[i] = 3   # Top 20
for i in range(21, 31):
    POINTS_SYSTEM[i] = 1   # Top 30

def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)

def load_json(filepath, default):
    ensure_data_dir()
    if os.path.exists(filepath):
        try:
            with open(filepath, "r") as f:
                return json.load(f)
        except:
            return default
    return default

def save_json(filepath, data):
    ensure_data_dir()
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)

def load_teams():
    default = {str(i): {"name": f"Team {i}", "picks": []} for i in range(1, 9)}
    return load_json(TEAMS_FILE, default)

def save_teams(teams):
    save_json(TEAMS_FILE, teams)

def load_scores():
    return load_json(SCORES_FILE, {})

def save_scores(scores):
    save_json(SCORES_FILE, scores)

def load_draft():
    default = {"drafted": [], "order": generate_snake_order(), "current_pick": 0}
    return load_json(DRAFT_FILE, default)

def save_draft(draft):
    save_json(DRAFT_FILE, draft)

def generate_snake_order():
    order = []
    for r in range(5):
        if r % 2 == 0:
            order.extend(range(1, 9))
        else:
            order.extend(range(8, 0, -1))
    return order

def get_points(position):
    if position is None:
        return 0
    return POINTS_SYSTEM.get(position, 0)

def calc_team_score(picks, scores):
    pick_scores = []
    for player in picks:
        if player and player in scores:
            pos = scores[player].get("position")
            status = scores[player].get("status", "active")
            if status in ("cut", "wd"):
                pick_scores.append(0)
            else:
                pick_scores.append(get_points(pos))
        else:
            pick_scores.append(None)
    valid = [s for s in pick_scores if s is not None]
    total = sum(valid)
    return total, pick_scores

def get_drafted_players():
    teams = load_teams()
    drafted = set()
    for t in teams.values():
        for p in t.get("picks", []):
            if p:
                drafted.add(p)
    return drafted
