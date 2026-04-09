import streamlit as st
from utils import load_scores, save_scores, load_teams, get_points
from espn_sync import fetch_espn_scores

def show():
    st.markdown("## 📊 Live Scores")

    # Auto-sync from ESPN on every page load
    with st.spinner("Fetching live scores from ESPN..."):
        espn_scores, message = fetch_espn_scores()

    if espn_scores:
        existing = load_scores()
        existing.update(espn_scores)
        save_scores(existing)
        st.caption(f"⛳ {message}")
    else:
        st.warning(f"Could not fetch live scores: {message}. Showing last saved scores.")

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
        st.info("⛳ No players drafted yet.")
        return

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

    # Header
    st.markdown("""
<div style='display:grid;grid-template-columns:55px 1fr 140px 90px 70px 70px;
gap:0.5rem;padding:0.6rem 1rem;
background:rgba(26,71,42,0.9);
border-radius:8px 8px 0 0;
border:1px solid rgba(201,168,76,0.4);
margin-top:0.5rem;'>
    <div style='font-size:0.75rem;color:#C9A84C;font-weight:700;'>POS</div>
    <div style='font-size:0.75rem;color:#C9A84C;font-weight:700;'>PLAYER</div>
    <div style='font-size:0.75rem;color:#C9A84C;font-weight:700;'>TEAM</div>
    <div style='font-size:0.75rem;color:#C9A84C;font-weight:700;text-align:center;'>SCORE</div>
    <div style='font-size:0.75rem;color:#C9A84C;font-weight:700;text-align:center;'>THRU</div>
    <div style='font-size:0.75rem;color:#C9A84C;font-weight:700;text-align:center;'>PTS</div>
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

        st.markdown(f"""
<div style='display:grid;grid-template-columns:55px 1fr 140px 90px 70px 70px;
gap:0.5rem;padding:0.65rem 1rem;background:{bg};
border-left:1px solid rgba(201,168,76,0.15);
border-right:1px solid rgba(201,168,76,0.15);
border-bottom:1px solid rgba(201,168,76,0.08);
align-items:center;'>
    <div style='font-size:0.85rem;color:rgba(255,255,255,0.65);'>{pos_display}</div>
    <div style='font-size:0.9rem;font-weight:700;color:#ffffff;'>{player}{status_indicator}</div>
    <div style='font-size:0.82rem;color:#C9A84C;'>{team_name}</div>
    <div style='font-size:1rem;font-weight:800;color:{score_color};text-align:center;'>{to_par}</div>
    <div style='font-size:0.85rem;color:rgba(255,255,255,0.5);text-align:center;'>{thru or "—"}</div>
    <div style='text-align:center;'>{pts_html}</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<div style='border:1px solid rgba(201,168,76,0.15);border-top:none;border-radius:0 0 8px 8px;height:8px;'></div>", unsafe_allow_html=True)

    cuts = sum(1 for p in scored if p[5] == "cut")
    col1, col2 = st.columns(2)
    col1.metric("Drafted Players", len(drafted_players))
    col2.metric("Missed Cut", cuts)

    if st.button("🔄 Refresh Scores"):
        st.rerun()
