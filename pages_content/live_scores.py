import streamlit as st
from utils import load_scores, save_scores, load_teams, get_points
from data.players import PLAYERS

def show():
    st.markdown("## 📊 Live Scores")
    st.markdown("<div style='color:rgba(255,255,255,0.6);font-size:0.9rem;margin-bottom:1.5rem;'>Leaderboard updates automatically as positions are entered. Use the Admin panel to update scores.</div>", unsafe_allow_html=True)

    scores = load_scores()
    teams = load_teams()

    # Build drafted players set
    drafted = {}
    for tid, team in teams.items():
        for pick in team.get("picks", []):
            if pick:
                drafted[pick] = team.get("name", f"Team {tid}")

    if not scores:
        st.info("⛳ No scores yet. Scores will appear here once the tournament begins.")
        st.markdown("Use the **Admin** panel to enter player positions.")
        return

    # Sort by position
    scored_players = []
    for player, data in scores.items():
        pos = data.get("position")
        status = data.get("status", "active")
        to_par = data.get("to_par", "E")
        thru = data.get("thru", "")
        scored_players.append((player, pos, status, to_par, thru))

    scored_players.sort(key=lambda x: (x[1] or 999))

    # Table header
    st.markdown("""
<div style='display:grid;grid-template-columns:60px 1fr 80px 80px 80px 120px 80px;
gap:0.5rem;padding:0.5rem 0.75rem;background:rgba(26,71,42,0.8);
border-radius:8px 8px 0 0;border:1px solid rgba(201,168,76,0.3);'>
    <div style='font-size:0.75rem;color:#C9A84C;font-weight:600;'>POS</div>
    <div style='font-size:0.75rem;color:#C9A84C;font-weight:600;'>PLAYER</div>
    <div style='font-size:0.75rem;color:#C9A84C;font-weight:600;text-align:center;'>TO PAR</div>
    <div style='font-size:0.75rem;color:#C9A84C;font-weight:600;text-align:center;'>THRU</div>
    <div style='font-size:0.75rem;color:#C9A84C;font-weight:600;text-align:center;'>STATUS</div>
    <div style='font-size:0.75rem;color:#C9A84C;font-weight:600;text-align:center;'>DRAFTED BY</div>
    <div style='font-size:0.75rem;color:#C9A84C;font-weight:600;text-align:center;'>PTS</div>
</div>
""", unsafe_allow_html=True)

    for i, (player, pos, status, to_par, thru) in enumerate(scored_players):
        bg = "rgba(45,106,79,0.25)" if i % 2 == 0 else "rgba(26,71,42,0.4)"
        is_drafted = player in drafted
        drafted_by = drafted.get(player, "—")
        pts = get_points(pos) if status == "active" else 0

        if status == "cut":
            status_html = "<span style='color:#ff6b6b;font-size:0.8rem;'>CUT</span>"
            pos_display = "CUT"
            pts = 0
        elif status == "wd":
            status_html = "<span style='color:#ff6b6b;font-size:0.8rem;'>WD</span>"
            pos_display = "WD"
            pts = 0
        else:
            status_html = "<span style='color:#69db7c;font-size:0.8rem;'>Active</span>"
            pos_display = f"T{pos}" if pos else "—"

        player_style = "font-weight:700;color:#C9A84C;" if is_drafted else "color:#ffffff;"
        drafted_badge = f"<span style='font-size:0.78rem;color:#C9A84C;'>{drafted_by}</span>" if is_drafted else "<span style='color:rgba(255,255,255,0.3);font-size:0.78rem;'>—</span>"
        pts_badge = f"<span style='background:#C9A84C;color:#1A472A;font-weight:700;font-size:0.78rem;padding:1px 7px;border-radius:10px;'>{pts}</span>" if pts > 0 else "<span style='color:rgba(255,255,255,0.3);font-size:0.78rem;'>0</span>"

        st.markdown(f"""
<div style='display:grid;grid-template-columns:60px 1fr 80px 80px 80px 120px 80px;
gap:0.5rem;padding:0.5rem 0.75rem;background:{bg};
border-left:1px solid rgba(201,168,76,0.15);border-right:1px solid rgba(201,168,76,0.15);
border-bottom:1px solid rgba(201,168,76,0.1);'>
    <div style='font-size:0.85rem;color:rgba(255,255,255,0.7);'>{pos_display}</div>
    <div style='{player_style}font-size:0.88rem;'>{player}</div>
    <div style='font-size:0.85rem;text-align:center;color:{"#69db7c" if isinstance(to_par,str) and to_par.startswith("-") else "#ffffff"};'>{to_par}</div>
    <div style='font-size:0.85rem;text-align:center;color:rgba(255,255,255,0.6);'>{thru or "—"}</div>
    <div style='text-align:center;'>{status_html}</div>
    <div style='text-align:center;'>{drafted_badge}</div>
    <div style='text-align:center;'>{pts_badge}</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)
    st.caption("⛳ Scores updated manually. Refresh to see latest.")
