import streamlit as st
from utils import load_scores, load_teams, get_points

def show():
    st.markdown("## 📊 Live Scores")
    st.markdown("<div style='color:rgba(255,255,255,0.6);font-size:0.9rem;margin-bottom:1.5rem;'>Live scores for all drafted players. Admin syncs from ESPN during the tournament.</div>", unsafe_allow_html=True)

    scores = load_scores()
    teams = load_teams()

    # Build lookup: player -> team name
    player_to_team = {}
    for tid, team in teams.items():
        for pick in team.get("picks", []):
            if pick:
                player_to_team[pick] = team.get("name", f"Team {tid}")

    drafted_players = list(player_to_team.keys())

    if not drafted_players:
        st.info("⛳ No players drafted yet. Complete the draft first.")
        return

    if not scores:
        st.info("⛳ Scores will appear here once the tournament begins and ESPN sync runs.")
        scored = [(p, player_to_team[p], None, "E", "", "active") for p in drafted_players]
    else:
        scored = []
        for player in drafted_players:
            team_name = player_to_team[player]
            data = scores.get(player, {})
            position = data.get("position", None)
            to_par = data.get("to_par", "E")
            thru = data.get("thru", "")
            status = data.get("status", "active")
            scored.append((player, team_name, position, to_par, thru, status))

        scored.sort(key=lambda x: (x[2] is None, x[2] or 999))

    # Header row
    st.markdown("""
<div style='display:grid;grid-template-columns:55px 1fr 140px 90px 70px 70px;
gap:0.5rem;padding:0.6rem 1rem;
background:rgba(26,71,42,0.9);
border-radius:8px 8px 0 0;
border:1px solid rgba(201,168,76,0.4);
margin-top:0.5rem;'>
    <div style='font-size:0.75rem;color:#C9A84C;font-weight:700;letter-spacing:0.08em;'>POS</div>
    <div style='font-size:0.75rem;color:#C9A84C;font-weight:700;letter-spacing:0.08em;'>PLAYER</div>
    <div style='font-size:0.75rem;color:#C9A84C;font-weight:700;letter-spacing:0.08em;'>TEAM</div>
    <div style='font-size:0.75rem;color:#C9A84C;font-weight:700;letter-spacing:0.08em;text-align:center;'>SCORE</div>
    <div style='font-size:0.75rem;color:#C9A84C;font-weight:700;letter-spacing:0.08em;text-align:center;'>THRU</div>
    <div style='font-size:0.75rem;color:#C9A84C;font-weight:700;letter-spacing:0.08em;text-align:center;'>PTS</div>
</div>
""", unsafe_allow_html=True)

    for i, (player, team_name, position, to_par, thru, status) in enumerate(scored):
        bg = "rgba(45,106,79,0.25)" if i % 2 == 0 else "rgba(26,71,42,0.5)"

        if status == "cut":
            pos_display = "CUT"
            score_color = "#ff6b6b"
            pts = 0
            status_indicator = "<span style='font-size:0.7rem;color:#ff6b6b;margin-left:4px;'>CUT</span>"
        elif status == "wd":
            pos_display = "WD"
            score_color = "#ff6b6b"
            pts = 0
            status_indicator = "<span style='font-size:0.7rem;color:#ff6b6b;margin-left:4px;'>WD</span>"
        else:
            pos_display = f"T{position}" if position else "—"
            pts = get_points(position) if position else 0
            status_indicator = ""
            if isinstance(to_par, str) and to_par.startswith("-"):
                score_color = "#69db7c"
            elif to_par == "E":
                score_color = "#ffffff"
            else:
                score_color = "#ff9999"

        if pts >= 10:
            pts_html = f"<span style='background:#C9A84C;color:#1A472A;font-weight:800;font-size:0.82rem;padding:2px 9px;border-radius:10px;'>{pts}</span>"
        elif pts > 0:
            pts_html = f"<span style='background:rgba(201,168,76,0.3);color:#C9A84C;font-weight:700;font-size:0.82rem;padding:2px 9px;border-radius:10px;border:1px solid rgba(201,168,76,0.4);'>{pts}</span>"
        else:
            pts_html = f"<span style='color:rgba(255,255,255,0.25);font-size:0.82rem;'>0</span>"

        thru_display = thru if thru else "—"

        st.markdown(f"""
<div style='display:grid;grid-template-columns:55px 1fr 140px 90px 70px 70px;
gap:0.5rem;padding:0.65rem 1rem;background:{bg};
border-left:1px solid rgba(201,168,76,0.15);
border-right:1px solid rgba(201,168,76,0.15);
border-bottom:1px solid rgba(201,168,76,0.08);
align-items:center;'>
    <div style='font-size:0.85rem;color:rgba(255,255,255,0.65);font-weight:500;'>{pos_display}</div>
    <div style='font-size:0.9rem;font-weight:700;color:#ffffff;'>{player}{status_indicator}</div>
    <div style='font-size:0.82rem;color:#C9A84C;font-weight:500;'>{team_name}</div>
    <div style='font-size:1rem;font-weight:800;color:{score_color};text-align:center;'>{to_par}</div>
    <div style='font-size:0.85rem;color:rgba(255,255,255,0.5);text-align:center;'>{thru_display}</div>
    <div style='text-align:center;'>{pts_html}</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<div style='border:1px solid rgba(201,168,76,0.15);border-top:none;border-radius:0 0 8px 8px;height:8px;background:rgba(26,71,42,0.3);'></div>", unsafe_allow_html=True)

    st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
    cuts = sum(1 for p in scored if p[5] == "cut")
    total_pts_possible = sum(get_points(p[2]) for p in scored if p[2] and p[5] == "active")

    col1, col2, col3 = st.columns(3)
    col1.metric("Drafted Players", len(drafted_players))
    col2.metric("Missed Cut", cuts)
    col3.metric("Points in Play", total_pts_possible)

    st.caption("⛳ Scores updated via ESPN Sync in Admin panel. Green = under par · Red = over par")
