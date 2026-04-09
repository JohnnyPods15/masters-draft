import streamlit as st
from utils import (load_teams, save_teams, load_scores, save_scores,
                   load_draft, save_draft, generate_snake_order, ADMIN_PASSWORD)
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.players import PLAYERS

def show():
    st.markdown("## 🔧 Admin Panel")

    if "admin_auth" not in st.session_state:
        st.session_state.admin_auth = False

    if not st.session_state.admin_auth:
        st.markdown("Enter the admin password to continue.")
        pwd = st.text_input("Password", type="password")
        if st.button("Login"):
            if pwd == ADMIN_PASSWORD:
                st.session_state.admin_auth = True
                st.rerun()
            else:
                st.error("Incorrect password.")
        return

    st.success("✅ Logged in as Commissioner")
    if st.button("Logout"):
        st.session_state.admin_auth = False
        st.rerun()

    st.markdown("---")
    tab1, tab2, tab3, tab4 = st.tabs(["👥 Team Names", "✏️ Edit Picks", "📊 Update Scores", "⚙️ Draft Settings"])

    # ── TAB 1: TEAM NAMES ──
    with tab1:
        st.markdown("### Set Team Names")
        teams = load_teams()
        updated = {}
        cols = st.columns(2)
        for i, (tid, team) in enumerate(teams.items()):
            with cols[i % 2]:
                new_name = st.text_input(f"Team {tid}", value=team.get("name", f"Team {tid}"), key=f"name_{tid}")
                updated[tid] = new_name
        if st.button("💾 Save Team Names", use_container_width=True):
            for tid, name in updated.items():
                teams[tid]["name"] = name
            save_teams(teams)
            st.success("Team names saved!")
            st.rerun()

    # ── TAB 2: EDIT PICKS ──
    with tab2:
        st.markdown("### Edit Any Team's Picks")
        teams = load_teams()
        drafted_by_others = {}

        team_options = {team.get("name", f"Team {tid}"): tid for tid, team in teams.items()}
        selected_team_name = st.selectbox("Select team to edit", list(team_options.keys()))
        tid = team_options[selected_team_name]
        team = teams[tid]
        current_picks = team.get("picks", ["", "", "", "", ""])
        while len(current_picks) < 5:
            current_picks.append("")

        # All drafted players except this team's own picks
        all_drafted = set()
        for other_tid, other_team in teams.items():
            if other_tid != tid:
                for p in other_team.get("picks", []):
                    if p:
                        all_drafted.add(p)

        new_picks = []
        for i in range(5):
            own_pick = current_picks[i] if i < len(current_picks) else ""
            available = ["— None —"] + [p for p in PLAYERS if p not in all_drafted or p == own_pick]
            default_idx = available.index(own_pick) if own_pick in available else 0
            pick = st.selectbox(f"Pick {i+1}", available, index=default_idx, key=f"edit_{tid}_{i}")
            new_picks.append("" if pick == "— None —" else pick)

        if st.button("💾 Save Picks", use_container_width=True):
            teams[tid]["picks"] = new_picks
            save_teams(teams)
            st.success(f"Picks saved for {selected_team_name}!")
            st.rerun()

    # ── TAB 3: UPDATE SCORES ──
    with tab3:
        st.markdown("### Update Player Positions")
        st.markdown("<div style='font-size:0.85rem;color:rgba(255,255,255,0.6);margin-bottom:1rem;'>Enter current leaderboard positions. Only need to enter players who have been drafted.</div>", unsafe_allow_html=True)

        scores = load_scores()
        teams = load_teams()

        # Get drafted players
        drafted_players = []
        for team in teams.values():
            for p in team.get("picks", []):
                if p and p not in drafted_players:
                    drafted_players.append(p)

        if not drafted_players:
            st.info("No players have been drafted yet.")
        else:
            st.markdown("**Drafted Players — Update Positions**")
            updated_scores = dict(scores)

            for player in sorted(drafted_players):
                current = scores.get(player, {})
                cols = st.columns([2, 1, 1, 1, 1])
                cols[0].markdown(f"<div style='padding-top:0.5rem;font-weight:600;'>{player}</div>", unsafe_allow_html=True)
                pos = cols[1].number_input("Pos", min_value=1, max_value=100,
                    value=current.get("position", 1), key=f"pos_{player}", label_visibility="collapsed")
                to_par = cols[2].text_input("To Par", value=current.get("to_par", "E"),
                    key=f"par_{player}", label_visibility="collapsed")
                thru = cols[3].text_input("Thru", value=current.get("thru", ""),
                    key=f"thru_{player}", placeholder="F or hole#", label_visibility="collapsed")
                status = cols[4].selectbox("Status", ["active", "cut", "wd"],
                    index=["active","cut","wd"].index(current.get("status","active")),
                    key=f"status_{player}", label_visibility="collapsed")
                updated_scores[player] = {
                    "position": pos,
                    "to_par": to_par,
                    "thru": thru,
                    "status": status
                }

        st.markdown("---")
        st.markdown("**Add any other player**")
        other_player = st.selectbox("Player", ["— Select —"] + PLAYERS, key="other_player")
        if other_player != "— Select —":
            c1, c2, c3, c4 = st.columns(4)
            op_pos = c1.number_input("Position", min_value=1, max_value=100, value=scores.get(other_player, {}).get("position", 1), key="op_pos")
            op_par = c2.text_input("To Par", value=scores.get(other_player, {}).get("to_par", "E"), key="op_par")
            op_thru = c3.text_input("Thru", value=scores.get(other_player, {}).get("thru", ""), key="op_thru")
            op_status = c4.selectbox("Status", ["active","cut","wd"], key="op_status")
            if st.button("Add Player"):
                updated_scores[other_player] = {"position": op_pos, "to_par": op_par, "thru": op_thru, "status": op_status}
                save_scores(updated_scores)
                st.success(f"Added {other_player}")
                st.rerun()

        if st.button("💾 Save All Scores", use_container_width=True, type="primary"):
            save_scores(updated_scores)
            st.success("Scores saved! Leaderboard updated.")
            st.rerun()

    # ── TAB 4: DRAFT SETTINGS ──
    with tab4:
        st.markdown("### Draft Settings")
        draft = load_draft()
        current_pick = draft.get("current_pick", 0)

        st.markdown(f"**Current pick:** #{current_pick + 1} of 50")

        new_pick = st.number_input("Set current pick number (1–50)", min_value=1, max_value=50, value=current_pick + 1)
        if st.button("Update Pick Position"):
            draft["current_pick"] = new_pick - 1
            save_draft(draft)
            st.success(f"Draft position set to pick #{new_pick}")

        st.markdown("---")
        st.markdown("**⚠️ Danger Zone**")
        if st.button("🔄 Reset Entire Draft", type="secondary"):
            confirm = st.session_state.get("confirm_reset", False)
            st.session_state.confirm_reset = True
            st.warning("Click again to confirm full reset.")

        if st.session_state.get("confirm_reset", False):
            if st.button("☠️ YES — Reset Everything"):
                teams = load_teams()
                for tid in teams:
                    teams[tid]["picks"] = []
                save_teams(teams)
                save_draft({"drafted": [], "order": generate_snake_order(), "current_pick": 0})
                save_scores({})
                st.session_state.confirm_reset = False
                st.success("Draft has been reset.")
                st.rerun()
