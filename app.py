import streamlit as st

st.set_page_config(
    page_title="The Masters Draft",
    page_icon="⛳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.main-header {
    background: linear-gradient(135deg, #1A472A 0%, #2D6A4F 100%);
    padding: 2rem 2.5rem;
    border-radius: 12px;
    margin-bottom: 2rem;
    text-align: center;
    border: 1px solid rgba(201,168,76,0.3);
}
.main-header h1 {
    font-family: 'Playfair Display', serif;
    font-size: 2.8rem;
    color: #C9A84C;
    margin: 0;
    letter-spacing: 0.02em;
}
.main-header p {
    color: rgba(255,255,255,0.7);
    font-size: 0.95rem;
    margin: 0.5rem 0 0 0;
    letter-spacing: 0.15em;
    text-transform: uppercase;
}

.card {
    background: rgba(45,106,79,0.4);
    border: 1px solid rgba(201,168,76,0.2);
    border-radius: 10px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
}
.card-gold {
    background: rgba(201,168,76,0.15);
    border: 1px solid rgba(201,168,76,0.5);
    border-radius: 10px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
}

.rank-1 { color: #C9A84C; font-size: 1.4rem; }
.rank-2 { color: #C0C0C0; font-size: 1.2rem; }
.rank-3 { color: #CD7F32; font-size: 1.1rem; }

.points-badge {
    display: inline-block;
    background: #C9A84C;
    color: #1A472A;
    font-weight: 700;
    font-size: 0.85rem;
    padding: 2px 10px;
    border-radius: 12px;
}
.points-badge-green {
    display: inline-block;
    background: #2D6A4F;
    color: #C9A84C;
    font-weight: 600;
    font-size: 0.8rem;
    padding: 2px 8px;
    border-radius: 12px;
    border: 1px solid rgba(201,168,76,0.4);
}

.stButton > button {
    background: linear-gradient(135deg, #C9A84C, #b8943d) !important;
    color: #1A472A !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 6px !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #d4b483, #C9A84C) !important;
}

.pick-slot {
    background: rgba(26,71,42,0.6);
    border: 1px solid rgba(201,168,76,0.2);
    border-radius: 8px;
    padding: 0.6rem 1rem;
    margin: 0.3rem 0;
    font-size: 0.9rem;
}
.pick-slot-empty {
    background: rgba(26,71,42,0.2);
    border: 1px dashed rgba(201,168,76,0.2);
    border-radius: 8px;
    padding: 0.6rem 1rem;
    margin: 0.3rem 0;
    font-size: 0.9rem;
    color: rgba(255,255,255,0.3);
    font-style: italic;
}

.divider {
    border: none;
    border-top: 1px solid rgba(201,168,76,0.2);
    margin: 1.5rem 0;
}

.nav-item {
    padding: 0.5rem 0;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1A472A 0%, #133520 100%) !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>⛳ The Masters Draft</h1>
    <p>Augusta National · 2026 · Fantasy Golf</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("## Navigation")
page = st.sidebar.radio(
    "",
    ["🏆 Leaderboard", "📋 Draft Board", "✏️ Make Picks", "📊 Live Scores", "🔧 Admin"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='font-size:0.78rem; color:rgba(255,255,255,0.45); padding: 0.5rem 0;'>
<b style='color:rgba(201,168,76,0.7)'>Scoring System</b><br>
🏆 Winner · 10 pts<br>
Top 5 · 7 pts<br>
Top 10 · 5 pts<br>
Top 20 · 3 pts<br>
Top 30 · 1 pt<br>
Missed Cut · 0 pts<br><br>
<i>Best 3 of 5 picks count</i>
</div>
""", unsafe_allow_html=True)

if page == "🏆 Leaderboard":
    from pages_content import leaderboard
    leaderboard.show()
elif page == "📋 Draft Board":
    from pages_content import draft_board
    draft_board.show()
elif page == "✏️ Make Picks":
    from pages_content import make_picks
    make_picks.show()
elif page == "📊 Live Scores":
    from pages_content import live_scores
    live_scores.show()
elif page == "🔧 Admin":
    from pages_content import admin
    admin.show()
