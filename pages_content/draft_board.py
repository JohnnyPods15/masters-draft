import streamlit as st
from utils import load_teams, load_draft, generate_snake_order

def show():
    st.markdown("## 📋 Draft Board")
    st.markdown("Snake draft order — 8 teams, 5 rounds, 5 picks each.")

    teams = load_teams()
    draft = load_draft()
    order = draft.get("order", generate_snake_order())
    current_pick = draft.get("current_pick", 0)

    rounds = 5
    num_teams = 8
    total_picks = rounds * num_teams

    # Header row — team names in order 1-8
    cols = st.columns([1.2] + [1.5] * num_teams)
    cols[0].markdown("<div style='font-size:0.8rem;color:rgba(255,255,255,0.5);padding:0.4rem 0;'>ROUND</div>", unsafe_allow_html=True)
    for i in range(num_teams):
        team_id = str(i + 1)
        name = teams.get(team_id, {}).get("name", f"Team {i+1}")
        short = name[:10] + "…" if len(name) > 10 else name
        cols[i+1].markdown(f"<div style='font-size:0.78rem;color:#C9A84C;font-weight:600;text-align:center;padding:0.4rem 0;'>{short}</div>", unsafe_allow_html=True)

    st.markdown("<hr style='border-color:rgba(201,168,76,0.2);margin:0.25rem 0 0.75rem 0;'>", unsafe_allow_html=True)

    for r in range(rounds):
        cols = st.columns([1.2] + [1.5] * num_teams)
        cols[0].markdown(f"<div style='font-size:0.85rem;color:rgba(255,255,255,0.6);padding:0.5rem 0.25rem;font-weight:600;'>R{r+1}</div>", unsafe_allow_html=True)

        # For each team column, find what pick slot they occupy this round
        for team_idx in range(num_teams):
            team_id = str(team_idx + 1)
            # Find the global pick index for this team in this round
            global_pick = r * num_teams + order[r * num_teams:r * num_teams + num_teams].index(team_idx + 1)
            
            picks = teams.get(team_id, {}).get("picks", [])
            # picks are stored in draft order, find which round index this team picked in
            round_pick_index = sum(1 for p in order[:global_pick] if p == team_idx + 1)
            player = picks[round_pick_index] if round_pick_index < len(picks) and picks[round_pick_index] else None

            is_on_clock = global_pick == current_pick and current_pick < total_picks

            if player:
                bg = "rgba(201,168,76,0.15)"
                border = "1px solid rgba(201,168,76,0.4)"
                text_color = "#ffffff"
                label = player
            elif is_on_clock:
                bg = "rgba(201,168,76,0.25)"
                border = "2px solid #C9A84C"
                text_color = "#C9A84C"
                label = "🕐 On Clock"
            else:
                bg = "rgba(26,71,42,0.3)"
                border = "1px dashed rgba(255,255,255,0.1)"
                text_color = "rgba(255,255,255,0.2)"
                label = "—"

            # Show pick number in snake order as subtitle
            snake_pos = order[global_pick]
            cols[team_idx + 1].markdown(
                f"""<div style='background:{bg};border:{border};border-radius:6px;
                padding:0.4rem 0.5rem;text-align:center;font-size:0.78rem;
                color:{text_color};min-height:2.2rem;display:flex;align-items:center;
                justify-content:center;margin:0.1rem;'>{label}</div>""",
                unsafe_allow_html=True
            )

        st.markdown("<div style='margin-bottom:0.4rem;'></div>", unsafe_allow_html=True)

    # Current pick indicator
    if current_pick < total_picks:
        team_on_clock = order[current_pick]
        team_name = teams.get(str(team_on_clock), {}).get("name", f"Team {team_on_clock}")
        round_num = current_pick // num_teams + 1
        pick_num = current_pick % num_teams + 1
        st.markdown(f"""
<div style='background:rgba(201,168,76,0.15);border:1px solid #C9A84C;border-radius:8px;
padding:1rem 1.5rem;margin-top:1.5rem;text-align:center;'>
    <div style='font-size:0.8rem;color:rgba(255,255,255,0.6);letter-spacing:0.1em;text-transform:uppercase;'>Now Picking</div>
    <div style='font-size:1.4rem;font-weight:700;color:#C9A84C;margin:0.3rem 0;'>{team_name}</div>
    <div style='font-size:0.85rem;color:rgba(255,255,255,0.5);'>Round {round_num} · Pick {pick_num} of 8</div>
</div>
""", unsafe_allow_html=True)
    else:
        st.success("✅ Draft complete! All 40 picks have been made.")
