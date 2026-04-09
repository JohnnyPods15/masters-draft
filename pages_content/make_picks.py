import streamlit as st
from utils import load_teams, save_teams, load_draft, save_draft, get_drafted_players
from data.players import PLAYERS

def show():
    st.markdown("## ✏️ Make Your Picks")

    teams = load_teams()
    draft = load_draft()
    order = draft.get("order", [])
    current_pick = draft.get("current_pick", 0)
    num_teams = 8
    total_picks = 40

    # Who's on the clock
    if current_pick >= total_picks:
        st.success("✅ The draft is complete!")
        return

    team_on_clock = order[current_pick]
    team_id = str(team_on_clock)
    team_name = teams.get(team_id, {}).get("name", f"Team {team_on_clock}")
    round_num = current_pick // num_teams + 1
    pick_num = current_pick % num_teams + 1

    st.markdown(f"""
<div style='background:rgba(201,168,76,0.15);border:2px solid #C9A84C;border-radius:10px;
padding:1.25rem 1.5rem;margin-bottom:1.5rem;text-align:center;'>
    <div style='font-size:0.8rem;color:rgba(255,255,255,0.6);letter-spacing:0.12em;text-transform:uppercase;'>Now On The Clock</div>
    <div style='font-family:"Playfair Display",serif;font-size:1.8rem;color:#C9A84C;font-weight:700;margin:0.3rem 0;'>{team_name}</div>
    <div style='font-size:0.85rem;color:rgba(255,255,255,0.5);'>Round {round_num} · Overall Pick #{current_pick + 1}</div>
</div>
""", unsafe_allow_html=True)

    drafted = get_drafted_players()
    available = [p for p in PLAYERS if p not in drafted]

    st.markdown("### Select a Player")
    selected = st.selectbox(
        "Available players",
        ["— Choose a player —"] + available,
        label_visibility="collapsed"
    )

    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("✅ Confirm Pick", use_container_width=True):
            if selected == "— Choose a player —":
                st.error("Please select a player first.")
            else:
                picks = teams[team_id].get("picks", [])
                picks.append(selected)
                teams[team_id]["picks"] = picks
                save_teams(teams)

                draft["current_pick"] = current_pick + 1
                save_draft(draft)

                st.success(f"✅ {team_name} selected **{selected}**!")
                st.rerun()

    st.markdown("---")

    # Show all teams' current picks
    st.markdown("### All Team Picks")
    cols = st.columns(2)
    for idx, (tid, team) in enumerate(teams.items()):
        with cols[idx % 2]:
            name = team.get("name", f"Team {tid}")
            picks = team.get("picks", [])
            picks_html = ""
            for i in range(5):
                if i < len(picks) and picks[i]:
                    picks_html += f"<div style='font-size:0.85rem;padding:0.2rem 0;'>Pick {i+1}: <b>{picks[i]}</b></div>"
                else:
                    picks_html += f"<div style='font-size:0.85rem;color:rgba(255,255,255,0.3);padding:0.2rem 0;'>Pick {i+1}: —</div>"
            st.markdown(f"""
<div style='background:rgba(45,106,79,0.3);border:1px solid rgba(201,168,76,0.2);
border-radius:8px;padding:0.9rem 1.1rem;margin-bottom:0.75rem;'>
    <div style='font-weight:700;color:#C9A84C;margin-bottom:0.5rem;'>{name}</div>
    {picks_html}
</div>
""", unsafe_allow_html=True)
