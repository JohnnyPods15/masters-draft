import requests

ESPN_URL = "https://site.api.espn.com/apis/site/v2/sports/golf/pga/scoreboard"

def fetch_espn_scores():
    """
    Fetch live Masters leaderboard from ESPN's unofficial API.
    Returns a dict of {player_name: {position, to_par, thru, status}} or None on failure.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        resp = requests.get(ESPN_URL, headers=headers, timeout=10)
        if resp.status_code != 200:
            return None, f"ESPN returned status {resp.status_code}"

        data = resp.json()
        events = data.get("events", [])
        if not events:
            return None, "No events found in ESPN data — tournament may not be active yet."

        # Find the Masters
        masters_event = None
        for event in events:
            name = event.get("name", "").lower()
            if "masters" in name:
                masters_event = event
                break

        # If no Masters found, use first event
        if not masters_event:
            if events:
                masters_event = events[0]
            else:
                return None, "No golf events currently available on ESPN."

        competitions = masters_event.get("competitions", [])
        if not competitions:
            return None, "No competition data found."

        competition = competitions[0]
        competitors = competition.get("competitors", [])

        scores = {}
        for comp in competitors:
            athlete = comp.get("athlete", {})
            name = athlete.get("displayName", "")
            if not name:
                continue

            status_obj = comp.get("status", {})
            status_type = status_obj.get("type", {}).get("name", "").lower()

            # Position
            pos_str = comp.get("order", None)
            try:
                position = int(pos_str) if pos_str else None
            except:
                position = None

            # To par score
            linescores = comp.get("linescores", [])
            score_value = comp.get("score", "E")

            # Thru
            thru = status_obj.get("displayValue", "")

            # Status
            if "cut" in status_type or comp.get("status", {}).get("type", {}).get("description", "").lower() == "cut":
                status = "cut"
            elif "withdraw" in status_type or "wd" in status_type:
                status = "wd"
            else:
                status = "active"

            # Format to par
            try:
                par_val = int(score_value)
                if par_val > 0:
                    to_par = f"+{par_val}"
                elif par_val == 0:
                    to_par = "E"
                else:
                    to_par = str(par_val)
            except:
                to_par = str(score_value) if score_value else "E"

            scores[name] = {
                "position": position,
                "to_par": to_par,
                "thru": thru,
                "status": status,
            }

        if not scores:
            return None, "Could not parse player data from ESPN response."

        return scores, f"Successfully synced {len(scores)} players from ESPN."

    except requests.exceptions.Timeout:
        return None, "ESPN request timed out. Try again."
    except requests.exceptions.ConnectionError:
        return None, "Could not connect to ESPN. Check your internet connection."
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"
