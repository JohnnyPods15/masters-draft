# ⛳ The Masters Draft — Streamlit App

## Setup & Deploy

### Local Testing
```bash
pip install streamlit
streamlit run app.py
```

### Deploy to Streamlit Community Cloud (free)
1. Push this folder to a GitHub repo
2. Go to share.streamlit.io
3. Connect your GitHub repo
4. Set main file path: `app.py`
5. Deploy — get a shareable link instantly

## How to Use

### Before the Draft
1. Go to **Admin** → enter password: `augusta2025`
2. Set all 10 team names under **Team Names**
3. Share the link with your friends

### During the Draft
1. Each person goes to **Make Picks** when it's their turn
2. Select their player and hit Confirm Pick
3. **Draft Board** shows all picks in snake order

### During the Tournament
1. Admin goes to **Update Scores** once or twice a day
2. Enter each drafted player's current position
3. **Leaderboard** auto-updates with points

## Scoring
- 🏆 Winner: 10 pts
- Top 5: 7 pts
- Top 10: 5 pts
- Top 20: 3 pts
- Top 30: 1 pt
- Missed Cut: 0 pts
- **Best 3 of 5 picks count**

## Admin Password
Default: `augusta2025`
Change it in `utils.py` → `ADMIN_PASSWORD`
