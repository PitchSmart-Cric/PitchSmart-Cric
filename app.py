import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import json
from datetime import datetime

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PitchSmart | IPL 2026",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
    --navy:   #0D1B2A;
    --blue:   #1A3A5C;
    --accent: #F4A227;
    --green:  #2ECC71;
    --red:    #E74C3C;
    --card:   #111E2E;
    --border: #1E3A5F;
    --text:   #E8EDF2;
    --muted:  #7A90A8;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--navy);
    color: var(--text);
}

.stApp { background-color: var(--navy); }

/* Hide streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem 3rem; max-width: 1400px; }

/* ── Hero banner ── */
.hero {
    background: linear-gradient(135deg, #0D1B2A 0%, #1A3A5C 50%, #0D1B2A 100%);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(244,162,39,0.15) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3rem;
    letter-spacing: 3px;
    color: var(--accent);
    margin: 0;
    line-height: 1;
}
.hero-sub {
    font-size: 0.95rem;
    color: var(--muted);
    margin-top: 0.3rem;
    letter-spacing: 1px;
    text-transform: uppercase;
}
.hero-badge {
    display: inline-block;
    background: rgba(244,162,39,0.15);
    border: 1px solid var(--accent);
    color: var(--accent);
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 1px;
    padding: 0.2rem 0.7rem;
    border-radius: 20px;
    margin-top: 0.8rem;
    text-transform: uppercase;
}

/* ── Cards ── */
.card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
}
.card-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.1rem;
    letter-spacing: 2px;
    color: var(--accent);
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--border);
}

/* ── KPI tiles ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0.75rem;
}
.kpi {
    background: linear-gradient(135deg, #111E2E, #162840);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.9rem 1rem;
    text-align: center;
}
.kpi-value {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.8rem;
    color: var(--accent);
    line-height: 1;
}
.kpi-label {
    font-size: 0.7rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 0.2rem;
}

/* ── Points table ── */
.pt-row {
    display: flex;
    align-items: center;
    padding: 0.55rem 0.75rem;
    border-radius: 8px;
    margin-bottom: 0.3rem;
    font-size: 0.88rem;
    transition: background 0.2s;
}
.pt-row:hover { background: rgba(255,255,255,0.04); }
.pt-rank {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: var(--muted);
    width: 24px;
}
.pt-team {
    font-weight: 600;
    flex: 1;
    color: var(--text);
}
.pt-stat {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    width: 32px;
    text-align: center;
    color: var(--muted);
}
.pt-pts {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1rem;
    width: 36px;
    text-align: center;
    color: var(--accent);
}
.pt-nrr {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    width: 52px;
    text-align: right;
}
.pt-hdr {
    display: flex;
    padding: 0.3rem 0.75rem;
    font-size: 0.68rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 0.3rem;
}
.qualify { border-left: 3px solid var(--green); }
.danger  { border-left: 3px solid var(--red); }
.nrr-pos { color: var(--green); }
.nrr-neg { color: var(--red); }

/* ── Form badges ── */
.form-badge {
    display: inline-block;
    width: 22px; height: 22px;
    border-radius: 50%;
    font-size: 0.65rem;
    font-weight: 700;
    line-height: 22px;
    text-align: center;
    margin-right: 2px;
}
.fb-w { background: var(--green); color: #fff; }
.fb-l { background: var(--red);   color: #fff; }
.fb-n { background: #555;         color: #fff; }

/* ── Team table ── */
.team-tbl { width: 100%; border-collapse: collapse; font-size: 0.82rem; }
.team-tbl th {
    background: #162840;
    color: var(--muted);
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 0.5rem 0.75rem;
    text-align: center;
    font-weight: 500;
}
.team-tbl td {
    padding: 0.55rem 0.75rem;
    text-align: center;
    border-bottom: 1px solid rgba(30,58,95,0.5);
    color: var(--text);
}
.team-tbl tr:hover td { background: rgba(255,255,255,0.03); }
.team-name { font-weight: 700; text-align: left !important; color: var(--accent); }
.hot  { color: #F4A227; font-weight: 700; }
.ok   { color: #2ECC71; font-weight: 600; }
.cold { color: #E74C3C; font-weight: 600; }

/* ── Playoff predictor ── */
.pp-row {
    display: flex;
    align-items: center;
    padding: 0.5rem 0.75rem;
    border-radius: 8px;
    margin-bottom: 0.3rem;
    font-size: 0.85rem;
}
.pp-team { font-weight: 600; flex: 1; }
.pp-pts  { font-family: 'JetBrains Mono', monospace; width: 40px; text-align: center; }
.pp-proj { font-family: 'Bebas Neue', sans-serif; font-size: 1rem; width: 40px; text-align: center; color: var(--accent); }
.pp-qual {
    font-size: 0.72rem;
    font-weight: 700;
    padding: 0.15rem 0.5rem;
    border-radius: 20px;
    letter-spacing: 0.5px;
}
.pp-yes { background: rgba(46,204,113,0.15); color: var(--green); border: 1px solid var(--green); }
.pp-no  { background: rgba(231,76,60,0.15);  color: var(--red);   border: 1px solid var(--red); }

/* ── Outcome tiles ── */
.outcome-grid { display: grid; grid-template-columns: repeat(2,1fr); gap: 0.75rem; }
.outcome-tile {
    background: #162840;
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
}
.outcome-val {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.5rem;
    line-height: 1;
}
.outcome-lbl { font-size: 0.7rem; color: var(--muted); text-transform: uppercase; letter-spacing: 1px; margin-top: 0.2rem; }

/* ── PitchSmart AI ── */
.ai-box {
    background: linear-gradient(135deg, #0D1B2A, #162840);
    border: 1px solid var(--accent);
    border-radius: 12px;
    padding: 1.5rem;
}
.ai-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.4rem;
    letter-spacing: 3px;
    color: var(--accent);
    margin-bottom: 0.3rem;
}
.ai-sub { font-size: 0.8rem; color: var(--muted); margin-bottom: 1rem; }
.ai-response {
    background: #0D1B2A;
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.25rem;
    font-size: 0.9rem;
    line-height: 1.7;
    color: var(--text);
    white-space: pre-wrap;
    min-height: 80px;
}
.ai-quick-btn {
    display: inline-block;
    background: rgba(244,162,39,0.1);
    border: 1px solid rgba(244,162,39,0.3);
    color: var(--accent);
    font-size: 0.75rem;
    padding: 0.3rem 0.75rem;
    border-radius: 20px;
    margin: 0.2rem;
    cursor: pointer;
}

/* ── Nav tabs ── */
div[data-testid="stHorizontalBlock"] { gap: 1rem; }
.stButton button {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    border-radius: 8px !important;
    transition: all 0.2s !important;
}
.stButton button:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
}
.stTextInput input, .stTextArea textarea {
    background: #0D1B2A !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(244,162,39,0.15) !important;
}
div[data-testid="stSelectbox"] > div {
    background: #0D1B2A !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
}
</style>
""", unsafe_allow_html=True)

# ── Load data ──────────────────────────────────────────────────────────────────
EXCEL_FILE = "IPL Teams Runs & Wickets 2026.xlsm"

@st.cache_data
def load_data():
    try:
        rs   = pd.read_excel(EXCEL_FILE, sheet_name="Regular Season", header=None, engine="openpyxl")
        an   = pd.read_excel(EXCEL_FILE, sheet_name="Analytics",      header=None, engine="openpyxl")
        dash = pd.read_excel(EXCEL_FILE, sheet_name="Dashboard",      header=None, engine="openpyxl")
        return rs, an, dash
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None, None, None

rs, an, dash = load_data()

# ── Parse standings — wins/losses from RS, NRR from Dashboard col L rows 34-43 ─
def get_standings(rs, dash):
    if rs is None:
        return pd.DataFrame()

    teams_info = {
        "CSK":  (1,  7,  33),
        "MI":   (8,  14, 34),
        "GT":   (15, 21, 35),
        "RCB":  (22, 28, 36),
        "RR":   (29, 35, 37),
        "DC":   (36, 42, 38),
        "PBKS": (43, 49, 39),
        "LSG":  (50, 56, 40),
        "KKR":  (57, 63, 41),
        "SRH":  (64, 70, 42),
    }

    rows = []
    for team, (opp_col, res_col, dash_row) in teams_info.items():
        try:
            res_data = rs.iloc[3:17, res_col]
            wins   = int((res_data == "Win").sum())
            losses = int((res_data == "Loss").sum())
            nr     = int((res_data == "NR").sum())
            played = wins + losses
            pts    = wins * 2 + nr

            # Read real NRR from Dashboard sheet col L (index 11), rows 34-43 (0-indexed: 33-42)
            nrr = 0.0
            if dash is not None:
                try:
                    nrr = float(pd.to_numeric(dash.iloc[dash_row, 11], errors="coerce") or 0)
                except:
                    nrr = 0.0

            rows.append({
                "Team": team, "P": played, "W": wins, "L": losses,
                "NR": nr, "Pts": pts, "NRR": round(nrr, 3),
            })
        except Exception as e:
            pass

    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.sort_values(["Pts", "NRR"], ascending=[False, False]).reset_index(drop=True)
        df.insert(0, "Rank", range(1, len(df) + 1))
    return df

# ── Parse team batting stats from Analytics sheet ─────────────────────────────
# Analytics sheet structure (0-indexed rows):
# Row 4 = headers, Rows 5-14 = team data for Home/Away section (CSK=row4, MI=row5...)
# Row 18 = headers for Boundary section, Rows 19-28 = team data
# Row 32 = headers for Form Guide, Rows 33-42 = team data
def get_team_stats(rs, an):
    if rs is None:
        return pd.DataFrame()

    teams_order = ["CSK","MI","GT","RCB","RR","DC","PBKS","LSG","KKR","SRH"]
    # From Analytics screenshot row 19-28 (0-indexed: 18-27):
    # Col A=Team(0), B=Total Runs(1), C=Total 4s(2), D=Total 6s(3),
    # E=Runs from 4s(4), F=Runs from 6s(5), G=Boundary Runs(6),
    # H=Boundary%(7), I=Extras(8), J=Extras/Game(9), K=Avg Runs/Game(10), L=Strike Rate(11)

    rows = []
    teams_info = {
        "CSK":  (1, 7),
        "MI":   (8, 14),
        "GT":   (15, 21),
        "RCB":  (22, 28),
        "RR":   (29, 35),
        "DC":   (36, 42),
        "PBKS": (43, 49),
        "LSG":  (50, 56),
        "KKR":  (57, 63),
        "SRH":  (64, 70),
    }

    for ti, team in enumerate(teams_order):
        try:
            opp_col, res_col = teams_info[team]
            runs_col   = opp_col + 1
            wkts_col   = opp_col + 2
            fours_col  = opp_col + 3
            sixes_col  = opp_col + 4
            extras_col = opp_col + 5

            res_data    = rs.iloc[3:17, res_col]
            runs_data   = pd.to_numeric(rs.iloc[3:17, runs_col],   errors="coerce")
            wkts_data   = pd.to_numeric(rs.iloc[3:17, wkts_col],   errors="coerce")
            fours_data  = pd.to_numeric(rs.iloc[3:17, fours_col],  errors="coerce")
            sixes_data  = pd.to_numeric(rs.iloc[3:17, sixes_col],  errors="coerce")
            extras_data = pd.to_numeric(rs.iloc[3:17, extras_col], errors="coerce")

            wins   = int((res_data == "Win").sum())
            losses = int((res_data == "Loss").sum())
            played = wins + losses

            total_runs   = runs_data.sum()
            total_wkts   = wkts_data.sum()
            total_fours  = fours_data.sum()
            total_sixes  = sixes_data.sum()
            total_extras = extras_data.sum()

            avg_runs  = round(total_runs / played, 1) if played > 0 else 0
            bdry_runs = total_fours * 4 + total_sixes * 6
            bdry_pct  = round(bdry_runs / total_runs * 100, 1) if total_runs > 0 else 0
            win_pct   = round(wins / played * 100, 1) if played > 0 else 0

            # Last 5 results for form
            results = res_data.dropna().tolist()
            last5   = results[-5:] if len(results) >= 5 else results
            form_wins = last5.count("Win")
            if form_wins >= 4:   trend = "🔥 Hot"
            elif form_wins >= 3: trend = "✅ Good"
            elif form_wins >= 2: trend = "⚠️ Average"
            else:                trend = "❌ Poor"

            rows.append({
                "Team": team, "Runs": int(total_runs), "Wickets": int(total_wkts),
                "4s": int(total_fours), "6s": int(total_sixes),
                "Extras": int(total_extras), "Avg Runs": avg_runs,
                "Bdry%": bdry_pct, "Win%": win_pct,
                "Form": trend, "Played": played, "Wins": wins,
                "Last5": last5,
            })
        except Exception as e:
            pass
    return pd.DataFrame(rows)

# ── Season totals ──────────────────────────────────────────────────────────────
def get_season_totals(rs):
    totals = {}
    if rs is None:
        return totals
    try:
        # Sum runs/4s/6s/extras across all 10 teams from match rows (3-16, 0-indexed)
        # Runs cols: C=2, J=9, Q=16, X=23, AE=30, AL=37, AS=44, AZ=51, BG=58, BN=65
        run_cols    = [2,  9,  16, 23, 30, 37, 44, 51, 58, 65]
        wkt_cols    = [3,  10, 17, 24, 31, 38, 45, 52, 59, 66]
        four_cols   = [4,  11, 18, 25, 32, 39, 46, 53, 60, 67]
        six_cols    = [5,  12, 19, 26, 33, 40, 47, 54, 61, 68]
        extras_cols = [6,  13, 20, 27, 34, 41, 48, 55, 62, 69]
        res_cols    = [7,  14, 21, 28, 35, 42, 49, 56, 63, 70]

        all_runs   = sum(pd.to_numeric(rs.iloc[3:17, c], errors="coerce").sum() for c in run_cols)
        all_wkts   = sum(pd.to_numeric(rs.iloc[3:17, c], errors="coerce").sum() for c in wkt_cols)
        all_fours  = sum(pd.to_numeric(rs.iloc[3:17, c], errors="coerce").sum() for c in four_cols)
        all_sixes  = sum(pd.to_numeric(rs.iloc[3:17, c], errors="coerce").sum() for c in six_cols)
        all_extras = sum(pd.to_numeric(rs.iloc[3:17, c], errors="coerce").sum() for c in extras_cols)

        # Count total games played
        total_games = sum(
            int((rs.iloc[3:17, c] == "Win").sum()) + int((rs.iloc[3:17, c] == "Loss").sum())
            for c in res_cols
        ) // 2  # divide by 2 since each game counted twice

        totals["Total Runs"]    = int(all_runs)
        totals["Total Wickets"] = int(all_wkts)
        totals["Total 4s"]      = int(all_fours)
        totals["Total 6s"]      = int(all_sixes)
        totals["Total Extras"]  = int(all_extras)
        totals["Boundary Runs"] = int(all_fours * 4 + all_sixes * 6)
        totals["Avg Runs/Game"] = round(all_runs / (total_games * 2), 1) if total_games > 0 else 0
        totals["Avg Wkts/Game"] = round(all_wkts / (total_games * 2), 1) if total_games > 0 else 0
    except Exception as e:
        pass
    return totals

# ── PitchSmart AI ──────────────────────────────────────────────────────────────
def ask_pitchsmart(question, standings_df, team_stats_df, totals, api_key):
    context = "You are PitchSmart, an expert IPL 2026 cricket analyst AI. Answer in a friendly, confident and insightful way. Keep responses concise but analytical.\n\n"
    context += "CURRENT STANDINGS:\n"
    for _, r in standings_df.iterrows():
        context += f"Rank {r['Rank']}: {r['Team']} | P:{r['P']} W:{r['W']} L:{r['L']} Pts:{r['Pts']} NRR:{r['NRR']:.3f}\n"
    context += "\nSEASON STATS:\n"
    for k, v in totals.items():
        context += f"{k}: {v}\n"
    context += "\nTEAM PERFORMANCE:\n"
    for _, r in team_stats_df.iterrows():
        context += f"{r['Team']}: Runs={r['Runs']} Win%={r['Win%']}% Form={r['Form']} Avg={r['Avg Runs']}\n"
    context += f"\nUSER QUESTION: {question}"

    body = {"contents": [{"parts": [{"text": context}]}]}
    url  = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    try:
        resp = requests.post(url, json=body, timeout=30)
        data = resp.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"⚠️ Could not reach PitchSmart. Check your API key. Error: {e}"

# ── Load everything ────────────────────────────────────────────────────────────
standings  = get_standings(rs, dash)
team_stats = get_team_stats(rs, an)
totals     = get_season_totals(rs)

# ── HERO ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-title">🏏 PitchSmart</div>
    <div class="hero-sub">IPL 2026 · Live Season Intelligence</div>
</div>
""", unsafe_allow_html=True)

# ── Navigation tabs ────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🤖 PitchSmart AI", "📊 Dashboard", "📈 Team Analytics"])

# ════════════════════════════════════════════════════════════════════════════════
# TAB 1 — PITCHSMART AI
# ════════════════════════════════════════════════════════════════════════════════
with tab1:
    # Load API key from Streamlit secrets or sidebar fallback
    api_key = ""
    try:
        api_key = st.secrets["GEMINI_KEY"]
    except:
        pass

    if not api_key:
        with st.sidebar:
            st.markdown("### ⚙️ PitchSmart Settings")
            api_key_input = st.text_input(
                "Gemini API Key",
                type="password",
                placeholder="Paste your Gemini API key...",
                help="Get a free key at aistudio.google.com",
                key="api_key_stored"
            )
            if api_key_input:
                st.session_state["gemini_key"] = api_key_input
                st.success("API key saved ✅")
        api_key = st.session_state.get("gemini_key", "")

    st.markdown('<div class="ai-box">', unsafe_allow_html=True)
    st.markdown("""
    <div class="ai-title">🤖 PITCHSMART</div>
    <div class="ai-sub">Your IPL 2026 cricket analyst — ask anything about the season</div>
    """, unsafe_allow_html=True)

    st.markdown("**Quick questions:**")
    quick_cols = st.columns(4)
    quick_questions = [
        "Which team is most likely to win IPL 2026?",
        "Who is in the best form right now?",
        "Which teams are in danger of missing playoffs?",
        "Compare the top 2 teams in detail",
    ]
    quick_selected = None
    for i, (col, q) in enumerate(zip(quick_cols, quick_questions)):
        with col:
            if st.button(q[:30] + "...", key=f"quick_{i}"):
                quick_selected = q

    question = st.text_area(
        "Your question",
        value=quick_selected if quick_selected else "",
        placeholder="e.g. Which team has the best batting lineup? Who should I watch in the next match?",
        height=80,
        label_visibility="collapsed"
    )

    if st.button("⚡ Ask PitchSmart", type="primary", use_container_width=False):
        if not api_key:
            st.error("Please enter your Gemini API key above.")
        elif not question:
            st.error("Please type a question first!")
        else:
            with st.spinner("PitchSmart is analysing the data..."):
                response = ask_pitchsmart(question, standings, team_stats, totals, api_key)
                st.session_state["last_response"] = response
                st.session_state["last_question"] = question

    if "last_response" in st.session_state:
        st.markdown(f"""
        <div style="margin-top:1rem">
            <p style="font-size:0.75rem;color:#7A90A8;margin-bottom:0.5rem">
                💬 Q: <em>{st.session_state.get('last_question','')}</em>
            </p>
            <div class="ai-response">{st.session_state['last_response']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    if "history" not in st.session_state:
        st.session_state["history"] = []
    if "last_response" in st.session_state and st.session_state.get("last_question"):
        entry = {"time": datetime.now().strftime("%H:%M"), "q": st.session_state["last_question"]}
        if entry not in st.session_state["history"]:
            st.session_state["history"].insert(0, entry)

    if st.session_state.get("history"):
        st.markdown('<div class="card" style="margin-top:1rem"><div class="card-title">🕐 QUESTION HISTORY</div>', unsafe_allow_html=True)
        for h in st.session_state["history"][:5]:
            st.markdown(f'<p style="font-size:0.8rem;color:#7A90A8;margin:0.2rem 0"><span style="color:#F4A227">{h["time"]}</span> — {h["q"]}</p>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# TAB 2 — DASHBOARD
# ════════════════════════════════════════════════════════════════════════════════
with tab2:
    col_left, col_mid, col_right = st.columns([1.2, 1.5, 1])

    # ── Points Table ──────────────────────────────────────────────────────────
    with col_left:
        st.markdown('<div class="card"><div class="card-title">📊 POINTS TABLE</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="pt-hdr">
            <span style="width:24px">#</span>
            <span style="flex:1">Team</span>
            <span style="width:32px;text-align:center">P</span>
            <span style="width:32px;text-align:center">W</span>
            <span style="width:32px;text-align:center">L</span>
            <span style="width:36px;text-align:center">Pts</span>
            <span style="width:52px;text-align:right">NRR</span>
        </div>
        """, unsafe_allow_html=True)

        for _, row in standings.iterrows():
            rank     = int(row["Rank"])
            cls      = "qualify" if rank <= 4 else ("danger" if rank >= 8 else "")
            nrr_cls  = "nrr-pos" if row["NRR"] >= 0 else "nrr-neg"
            nrr_sign = "+" if row["NRR"] >= 0 else ""
            st.markdown(f"""
            <div class="pt-row {cls}">
                <span class="pt-rank">{rank}</span>
                <span class="pt-team">{row['Team']}</span>
                <span class="pt-stat">{row['P']}</span>
                <span class="pt-stat">{row['W']}</span>
                <span class="pt-stat">{row['L']}</span>
                <span class="pt-pts">{row['Pts']}</span>
                <span class="pt-nrr {nrr_cls}">{nrr_sign}{row['NRR']:.3f}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<p style="font-size:0.7rem;color:#7A90A8;margin-top:0.5rem">🟢 Top 4 qualify &nbsp; 🔴 Danger zone</p></div>', unsafe_allow_html=True)

    # ── KPIs + Outcomes ───────────────────────────────────────────────────────
    with col_mid:
        st.markdown('<div class="card"><div class="card-title">📈 SEASON STATISTICS</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="kpi-grid">
            <div class="kpi"><div class="kpi-value">{totals.get('Total Runs', 'N/A'):,}</div><div class="kpi-label">Total Runs</div></div>
            <div class="kpi"><div class="kpi-value">{totals.get('Total Wickets', 'N/A')}</div><div class="kpi-label">Wickets</div></div>
            <div class="kpi"><div class="kpi-value">{totals.get('Total 4s', 'N/A')}</div><div class="kpi-label">Fours</div></div>
            <div class="kpi"><div class="kpi-value">{totals.get('Total 6s', 'N/A')}</div><div class="kpi-label">Sixes</div></div>
            <div class="kpi"><div class="kpi-value">{totals.get('Avg Runs/Game', 'N/A')}</div><div class="kpi-label">Avg Runs/Game</div></div>
            <div class="kpi"><div class="kpi-value">{totals.get('Avg Wkts/Game', 'N/A')}</div><div class="kpi-label">Avg Wkts/Game</div></div>
        </div>
        </div>
        """, unsafe_allow_html=True)

        # Charts
        if not team_stats.empty:
            st.markdown('<div class="card"><div class="card-title">📊 RUNS BY TEAM</div>', unsafe_allow_html=True)
            fig = px.bar(
                team_stats.sort_values("Runs", ascending=True),
                x="Runs", y="Team", orientation="h",
                color="Runs",
                color_continuous_scale=["#1A3A5C", "#F4A227"],
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font_color="#E8EDF2", margin=dict(l=0, r=0, t=0, b=0),
                height=280, coloraxis_showscale=False,
                xaxis=dict(gridcolor="#1E3A5F", tickfont=dict(size=10)),
                yaxis=dict(gridcolor="rgba(0,0,0,0)", tickfont=dict(size=11, color="#F4A227")),
            )
            fig.update_traces(marker_line_width=0)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # ── Playoff Predictor ─────────────────────────────────────────────────────
    with col_right:
        st.markdown('<div class="card"><div class="card-title">🎪 PLAYOFF PREDICTOR</div></div>', unsafe_allow_html=True)

        pp_rows = ""
        for _, row in standings.iterrows():
            rank = int(row["Rank"])
            proj = round(row["Pts"] / row["P"] * 14) if row["P"] > 0 else 0
            qual_cls = "pp-yes" if rank <= 4 else "pp-no"
            qual_txt = "✅ IN" if rank <= 4 else "❌ OUT"
            row_bg = "rgba(46,204,113,0.05)" if rank <= 4 else "rgba(231,76,60,0.05)"
            border = "3px solid #2ECC71" if rank <= 4 else "3px solid #E74C3C"
            pp_rows += f"""
            <tr style="background:{row_bg};border-bottom:1px solid #1E3A5F;border-left:{border}">
                <td style="padding:0.55rem 0.75rem;font-weight:700;color:#E8EDF2">{row['Team']}</td>
                <td style="padding:0.55rem 0.75rem;text-align:center;font-family:monospace;color:#7A90A8">{row['Pts']}</td>
                <td style="padding:0.55rem 0.75rem;text-align:center;font-weight:700;font-size:1rem;color:#F4A227">{proj}</td>
                <td style="padding:0.55rem 0.75rem;text-align:center">
                    <span style="font-size:0.72rem;font-weight:700;padding:0.2rem 0.5rem;border-radius:20px;{'background:rgba(46,204,113,0.15);color:#2ECC71;border:1px solid #2ECC71' if rank <= 4 else 'background:rgba(231,76,60,0.15);color:#E74C3C;border:1px solid #E74C3C'}">{qual_txt}</span>
                </td>
            </tr>"""

        pp_table = f"""
        <div style="background:#111E2E;border:1px solid #1E3A5F;border-radius:10px;overflow:hidden;margin-bottom:0.5rem">
        <table style="width:100%;border-collapse:collapse;font-size:0.85rem;font-family:sans-serif">
        <thead><tr style="background:#162840">
            <th style="padding:0.5rem 0.75rem;text-align:left;color:#7A90A8;font-size:0.65rem;text-transform:uppercase;letter-spacing:1px;font-weight:500">Team</th>
            <th style="padding:0.5rem 0.75rem;text-align:center;color:#7A90A8;font-size:0.65rem;text-transform:uppercase;letter-spacing:1px;font-weight:500">Points</th>
            <th style="padding:0.5rem 0.75rem;text-align:center;color:#7A90A8;font-size:0.65rem;text-transform:uppercase;letter-spacing:1px;font-weight:500">Proj Pts</th>
            <th style="padding:0.5rem 0.75rem;text-align:center;color:#7A90A8;font-size:0.65rem;text-transform:uppercase;letter-spacing:1px;font-weight:500">Status</th>
        </tr></thead>
        <tbody>{pp_rows}</tbody>
        </table></div>
        <p style="font-size:0.7rem;color:#7A90A8;margin:0">Proj = projected final points based on current form</p>
        """
        st.markdown(pp_table, unsafe_allow_html=True)

        # NRR Chart
        if not standings.empty:
            st.markdown('<div class="card"><div class="card-title">📉 NRR COMPARISON</div>', unsafe_allow_html=True)
            nrr_df  = standings.sort_values("NRR", ascending=True)
            colors  = ["#E74C3C" if x < 0 else "#2ECC71" for x in nrr_df["NRR"]]
            fig2 = go.Figure(go.Bar(
                x=nrr_df["NRR"], y=nrr_df["Team"],
                orientation="h", marker_color=colors,
            ))
            fig2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font_color="#E8EDF2", margin=dict(l=0, r=0, t=0, b=0),
                height=250,
                xaxis=dict(gridcolor="#1E3A5F", tickfont=dict(size=9), zeroline=True, zerolinecolor="#7A90A8"),
                yaxis=dict(gridcolor="rgba(0,0,0,0)", tickfont=dict(size=10)),
            )
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# TAB 3 — TEAM ANALYTICS
# ════════════════════════════════════════════════════════════════════════════════
with tab3:
    if team_stats.empty:
        st.warning("Could not load team data. Check your Excel file.")
    else:
        st.markdown('<div class="card"><div class="card-title">🏏 TEAM PERFORMANCE & FORM GUIDE</div></div>', unsafe_allow_html=True)

        # Build full self-contained HTML table
        rows_html = ""
        for i, (_, r) in enumerate(team_stats.iterrows()):
            row_bg = "#111E2E" if i % 2 == 0 else "#0D1B2A"
            if "Hot" in r["Form"]:
                form_color = "#F4A227"; form_bg = "rgba(244,162,39,0.15)"
            elif "Good" in r["Form"]:
                form_color = "#2ECC71"; form_bg = "rgba(46,204,113,0.15)"
            elif "Average" in r["Form"]:
                form_color = "#F39C12"; form_bg = "rgba(243,156,18,0.15)"
            else:
                form_color = "#E74C3C"; form_bg = "rgba(231,76,60,0.15)"

            win_val = float(r["Win%"])
            win_color = "#2ECC71" if win_val >= 60 else ("#F39C12" if win_val >= 40 else "#E74C3C")

            rows_html += f"""<tr style="background:{row_bg};border-bottom:1px solid #1E3A5F">
                <td style="padding:0.6rem 0.75rem;font-weight:700;color:#F4A227">{r['Team']}</td>
                <td style="padding:0.6rem 0.75rem;text-align:center;color:#E8EDF2">{r['Runs']:,}</td>
                <td style="padding:0.6rem 0.75rem;text-align:center;color:#E8EDF2">{r['Avg Runs']}</td>
                <td style="padding:0.6rem 0.75rem;text-align:center;color:#E8EDF2">{r['4s']}</td>
                <td style="padding:0.6rem 0.75rem;text-align:center;color:#E8EDF2">{r['6s']}</td>
                <td style="padding:0.6rem 0.75rem;text-align:center;color:#E8EDF2">{r['Bdry%']}%</td>
                <td style="padding:0.6rem 0.75rem;text-align:center;font-weight:700;color:{win_color}">{r['Win%']}%</td>
                <td style="padding:0.6rem 0.75rem;text-align:center;font-weight:700;color:{form_color};background:{form_bg}">{r['Form']}</td>
            </tr>"""

        full_table = f"""
        <div style="background:#111E2E;border:1px solid #1E3A5F;border-radius:10px;overflow:hidden;margin-bottom:1rem">
        <table style="width:100%;border-collapse:collapse;font-size:0.85rem;font-family:sans-serif">
        <thead><tr style="background:#162840">
            <th style="padding:0.6rem 0.75rem;text-align:left;color:#7A90A8;font-size:0.68rem;text-transform:uppercase;letter-spacing:1px;font-weight:500">Team</th>
            <th style="padding:0.6rem 0.75rem;text-align:center;color:#7A90A8;font-size:0.68rem;text-transform:uppercase;letter-spacing:1px;font-weight:500">Runs</th>
            <th style="padding:0.6rem 0.75rem;text-align:center;color:#7A90A8;font-size:0.68rem;text-transform:uppercase;letter-spacing:1px;font-weight:500">Avg Runs</th>
            <th style="padding:0.6rem 0.75rem;text-align:center;color:#7A90A8;font-size:0.68rem;text-transform:uppercase;letter-spacing:1px;font-weight:500">4s</th>
            <th style="padding:0.6rem 0.75rem;text-align:center;color:#7A90A8;font-size:0.68rem;text-transform:uppercase;letter-spacing:1px;font-weight:500">6s</th>
            <th style="padding:0.6rem 0.75rem;text-align:center;color:#7A90A8;font-size:0.68rem;text-transform:uppercase;letter-spacing:1px;font-weight:500">Bdry%</th>
            <th style="padding:0.6rem 0.75rem;text-align:center;color:#7A90A8;font-size:0.68rem;text-transform:uppercase;letter-spacing:1px;font-weight:500">Win%</th>
            <th style="padding:0.6rem 0.75rem;text-align:center;color:#7A90A8;font-size:0.68rem;text-transform:uppercase;letter-spacing:1px;font-weight:500">Form</th>
        </tr></thead>
        <tbody>{rows_html}</tbody>
        </table></div>"""

        st.markdown(full_table, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown('<div class="card"><div class="card-title">🎯 BOUNDARY % BY TEAM</div>', unsafe_allow_html=True)
            fig3 = px.bar(
                team_stats.sort_values("Bdry%", ascending=False),
                x="Team", y="Bdry%",
                color="Bdry%",
                color_continuous_scale=["#1A3A5C", "#F4A227"],
            )
            fig3.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font_color="#E8EDF2", margin=dict(l=0, r=0, t=10, b=0),
                height=280, coloraxis_showscale=False,
                xaxis=dict(gridcolor="rgba(0,0,0,0)"),
                yaxis=dict(gridcolor="#1E3A5F", ticksuffix="%"),
            )
            st.plotly_chart(fig3, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_b:
            st.markdown('<div class="card"><div class="card-title">💥 SIXES BY TEAM</div>', unsafe_allow_html=True)
            fig4 = px.bar(
                team_stats.sort_values("6s", ascending=False),
                x="Team", y="6s",
                color="6s",
                color_continuous_scale=["#1A3A5C", "#E74C3C"],
            )
            fig4.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font_color="#E8EDF2", margin=dict(l=0, r=0, t=10, b=0),
                height=280, coloraxis_showscale=False,
                xaxis=dict(gridcolor="rgba(0,0,0,0)"),
                yaxis=dict(gridcolor="#1E3A5F"),
            )
            st.plotly_chart(fig4, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
