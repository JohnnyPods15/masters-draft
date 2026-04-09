import streamlit as st
from utils import load_teams, load_scores, save_scores, calc_team_score, get_points
from espn_sync import fetch_espn_scores

def show():
    st.markdown("## 🏆 Leaderboard")

    # Auto-sync scores from ESPN
    espn_scores, _ = fetch_espn_scores()
    if espn_scores:
        existing = load_scores()
        existing.update(espn_scores)
        save_scores(existing)

    teams = load_teams()
    scores = load_scores()

    results = []
    for team_id, team in teams.items():
        name = team.get("name", f"Team {team_id}")
        picks = team.get("picks", [])
        total, pick_scores = calc_team_score(picks, scores)
        results.append({
            "team_id": team_id,
            "name": name,
            "picks": picks,
            "total": total,
            "pick_scores": pick_scores,
        })

    results.sort(key=lambda x: x["total"], reverse=True)

    rank_icons = {1: "🥇", 2: "🥈", 3: "🥉"}

    for rank, r in enumerate(results, 1):
        icon = rank_icons.get(rank, f"#{rank}")
        border_style = "card-gold" if rank == 1 else "card"

        picks_html = ""
        for i, pick in enumerate(r["picks"]):
            if pick:
                ps = r["pick_scores"][i] if i < len(r["pick_scores"]) else None
                pts_label = f'<span class="points-badge-green">{ps} pts</span>' if ps is not None else ""
                # Get position
                pos_str = ""
                if pick in scores:
                    pos = scores[pick].get("position")
                    status = scores[pick].get("status", "active")
                    if status == "cut":
                        pos_str = " · <span style='color:#ff6b6b;font-size:0.8rem'>CUT</span>"
                    elif status == "wd":
                        pos_str = " · <span style='color:#ff6b6b;font-size:0.8rem'>WD</span>"
                    elif pos:
                        pos_str = f" · <span style='color:rgba(255,255,255,0.5);font-size:0.8rem'>T{pos}</span>"
                picks_html += f'<div class="pick-slot">Pick {i+1}: <b>{pick}</b>{pos_str} {pts_label}</div>'
            else:
                picks_html += f'<div class="pick-slot-empty">Pick {i+1}: Not yet drafted</div>'

        st.markdown(f"""
<div class="{border_style}">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem;">
        <div>
            <span style="font-size:1.5rem; margin-right:0.5rem;">{icon}</span>
            <span style="font-family:'Playfair Display',serif; font-size:1.3rem; font-weight:700; color:#{'C9A84C' if rank==1 else 'ffffff'};">{r['name']}</span>
        </div>
        <div style="text-align:right;">
            <div style="font-size:2rem; font-weight:700; color:#C9A84C;">{r['total']}</div>
            <div style="font-size:0.75rem; color:rgba(255,255,255,0.5);">POINTS</div>
        </div>
    </div>
    {picks_html}
</div>
""", unsafe_allow_html=True)

    if not any(r["total"] > 0 for r in results):
        st.info("⛳ Scores will appear here once the tournament begins and scores are updated.")

    st.markdown("---")
    st.markdown("""
<div style='font-size:0.8rem; color:rgba(255,255,255,0.4); text-align:center;'>
Best 3 of 5 picks count toward your score
</div>
""", unsafe_allow_html=True)
