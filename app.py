import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date

st.set_page_config(
    page_title="🃏 जुआरी Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    background-color: #0a0a0a !important;
    color: #f0f0f0 !important;
    font-family: 'DM Mono', monospace !important;
}
[data-testid="stSidebar"] {
    background: #0f0f0f !important;
    border-right: 1px solid #2a0a0a !important;
}
[data-testid="stSidebar"] * { color: #f0f0f0 !important; }
[data-testid="stSidebarNav"] { display: none; }
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {
    background-color: #8b0000 !important;
}
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="select"] > div,
[data-testid="stSidebar"] .stDateInput input {
    background-color: #1a1a1a !important;
    border: 1px solid #8b0000 !important;
    color: #f0f0f0 !important;
}
.hero-title {
    text-align: center;
    font-family: 'Playfair Display', serif;
    font-size: 3.8rem;
    font-weight: 900;
    color: #ffffff;
    letter-spacing: 0.04em;
    line-height: 1.1;
    padding: 1.2rem 0 0.2rem;
    text-shadow: 0 0 40px rgba(180,0,0,0.6), 0 2px 4px rgba(0,0,0,0.8);
}
.hero-subtitle {
    text-align: center;
    font-family: 'DM Mono', monospace;
    font-size: 0.8rem;
    color: #666;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding-bottom: 1rem;
}
.suit-row {
    text-align: center;
    font-size: 1.4rem;
    letter-spacing: 0.3em;
    padding-bottom: 0.5rem;
    opacity: 0.7;
}
.red-divider {
    border: none;
    height: 1px;
    background: linear-gradient(to right, transparent, #8b0000, #cc0000, #8b0000, transparent);
    margin: 1rem 0 1.5rem;
}
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #141414 0%, #1a0a0a 100%) !important;
    border: 1px solid #2a0a0a !important;
    border-top: 2px solid #cc0000 !important;
    border-radius: 6px !important;
    padding: 1rem 1.2rem !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.03) !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #888 !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Playfair Display', serif !important;
    font-size: 1.6rem !important;
    color: #ffffff !important;
}
[data-testid="stMetricDelta"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.85rem !important;
}
.chart-card {
    background: linear-gradient(160deg, #111111 0%, #0d0505 100%);
    border: 1px solid #1f0a0a;
    border-top: 2px solid #8b0000;
    border-radius: 8px;
    padding: 1.2rem 1.4rem 0.8rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.02);
    margin-bottom: 1.2rem;
}
.chart-card-title {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #cc0000;
    margin-bottom: 0.6rem;
    border-bottom: 1px solid #1f0a0a;
    padding-bottom: 0.5rem;
}
.sidebar-heading {
    font-family: 'Playfair Display', serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #cc0000;
    margin-bottom: 0.3rem;
}
[data-testid="stButton"] button {
    background: linear-gradient(135deg, #8b0000, #cc0000) !important;
    color: white !important;
    border: none !important;
    border-radius: 4px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.1em !important;
    padding: 0.4rem 1rem !important;
    width: 100% !important;
    transition: opacity 0.2s !important;
}
[data-testid="stButton"] button:hover { opacity: 0.85 !important; }
[data-testid="stDataFrame"] {
    background: #0f0f0f !important;
    border: 1px solid #1f0a0a !important;
    border-radius: 6px !important;
}
[data-baseweb="select"] > div {
    background-color: #1a1a1a !important;
    border-color: #8b0000 !important;
    color: #f0f0f0 !important;
}
[data-testid="stExpander"] {
    background: #111 !important;
    border: 1px solid #1f0a0a !important;
    border-radius: 6px !important;
}
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #0a0a0a; }
::-webkit-scrollbar-thumb { background: #8b0000; border-radius: 2px; }
</style>
""", unsafe_allow_html=True)

# ── Month filter state (read once from query params) ──
try:
    month_active = st.query_params.get("month_filter", "0") == "1"
except:
    month_active = False

# ── Floating button ──
btn_emoji = "⏱️" if month_active else "🗓️"
btn_tooltip = "All time" if month_active else "This month"
next_val = "0" if month_active else "1"

st.markdown(f"""
<style>
#float-month-btn {{
    position: fixed;
    bottom: 2rem;
    right: 2rem;
    width: 58px;
    height: 58px;
    border-radius: 50%;
    background: linear-gradient(135deg, #8b0000, #cc0000);
    border: none;
    color: white;
    font-size: 26px;
    cursor: pointer;
    box-shadow: 0 4px 18px rgba(204,0,0,0.45);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
    transition: transform 0.2s, box-shadow 0.2s;
    line-height: 1;
}}
#float-month-btn:hover {{
    transform: scale(1.12);
    box-shadow: 0 6px 24px rgba(204,0,0,0.65);
}}
#float-month-tooltip {{
    position: fixed;
    bottom: 5.2rem;
    right: 1.2rem;
    background: #1a0a0a;
    border: 1px solid #8b0000;
    color: #f0f0f0;
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 0.25rem 0.6rem;
    border-radius: 4px;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.2s;
    white-space: nowrap;
    z-index: 9999;
}}
#float-month-btn:hover + #float-month-tooltip {{
    opacity: 1;
}}
</style>
<button id="float-month-btn" onclick="
    const u = new URL(window.location.href);
    u.searchParams.set('month_filter', '{next_val}');
    window.location.href = u.toString();
">{btn_emoji}</button>
<div id="float-month-tooltip">{btn_tooltip}</div>
""", unsafe_allow_html=True)

# ── Plotly dark template ──
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Mono, monospace", color="#aaa", size=11),
    margin=dict(l=10, r=10, t=10, b=10),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#aaa")),
    xaxis=dict(gridcolor="#1a1a1a", linecolor="#333", tickcolor="#333"),
    yaxis=dict(gridcolor="#1a1a1a", linecolor="#333", tickcolor="#333"),
)

# ── Data ──
SHEET_ID = "1N0f0momimoEEWxqmxSrthV3IxkQIMpxczoLIbHw5XsQ"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

@st.cache_data(ttl=300)
def load_data():
    df = pd.read_csv(CSV_URL)
    df.columns = df.columns.str.strip()
    df["Date"] = pd.to_datetime(df["Date"])
    df["P/L"] = pd.to_numeric(df["P/L"], errors="coerce")
    df["Buyin"] = pd.to_numeric(df["Buyin"], errors="coerce")
    df["Cashout"] = pd.to_numeric(df["Cashout"], errors="coerce")
    df = df.dropna(subset=["Name", "Date", "P/L"])
    return df

df = load_data()

# ── Sidebar filters ──
with st.sidebar:
    st.markdown('<div class="sidebar-heading">♠ Filters</div>', unsafe_allow_html=True)

    all_players = sorted(df["Name"].unique())
    all_dates = sorted(df["Date"].dt.date.unique())

    selected_players = st.multiselect("Players", all_players, default=all_players)

    date_range = st.date_input(
        "Date Range",
        value=(min(all_dates), max(all_dates)),
        min_value=min(all_dates),
        max_value=max(all_dates),
    )

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<hr style="border-color:#1f0a0a">', unsafe_allow_html=True)
    st.markdown(
        '<div style="font-size:0.65rem;color:#444;text-align:center;letter-spacing:0.1em">AUTO-REFRESHES EVERY 5 MIN</div>',
        unsafe_allow_html=True
    )

# ── Build df_f (apply filters once) ──
if month_active:
    # Month filter overrides the date range picker entirely
    today = date.today()
    month_start = date(today.year, today.month, 1)
    df_f = df[
        (df["Name"].isin(selected_players)) &
        (df["Date"].dt.date >= month_start) &
        (df["Date"].dt.date <= today)
    ]
    st.toast(f"📅 {today.strftime('%B %Y')} only", icon="🗓️")
else:
    if len(date_range) == 2:
        start, end = date_range
        df_f = df[
            (df["Name"].isin(selected_players)) &
            (df["Date"].dt.date >= start) &
            (df["Date"].dt.date <= end)
        ]
    else:
        df_f = df[df["Name"].isin(selected_players)]

# ── Apply month filter if active ──
if month_active:
    today = date.today()
    month_start = date(today.year, today.month, 1)
    df_f = df_f[df_f["Date"].dt.date >= month_start]
    st.toast(f"📅 {today.strftime('%B %Y')} only", icon="🗓️")

# ── Qualified players (always based on full dataset) ──
qualified = df.groupby("Name")["Date"].nunique()
qualified_players = qualified[qualified > 3].index
df_f = df_f[df_f["Name"].isin(qualified_players)]

# ── Hero Header ──
st.markdown('<div class="suit-row">♠ ♥ ♦ ♣</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">JUAARI DASHBOARD</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Gambling addiction tracker</div>', unsafe_allow_html=True)
st.markdown('<hr class="red-divider">', unsafe_allow_html=True)

# ── KPIs ──
total_pl = df_f.groupby("Name")["P/L"].sum()
sessions_per_player = df_f.groupby("Name")["Date"].nunique()
sessions_count = df_f["Date"].nunique()

biggest_winner = total_pl.idxmax() if not total_pl.empty else "N/A"
biggest_loser  = total_pl.idxmin() if not total_pl.empty else "N/A"

total_sessions = df_f["Date"].nunique()
full_attendance = [p for p in sessions_per_player.index if sessions_per_player[p] == total_sessions]
regulars_str = ", ".join(full_attendance) if full_attendance else "None"
if len(regulars_str) > 28:
    regulars_str = regulars_str[:25] + "…"

winner_val = total_pl.get(biggest_winner, 0)
loser_val  = total_pl.get(biggest_loser, 0)

def kpi_card(col, label, value, delta=None, delta_colour="#cc0000", delta_arrow="▼"):
    col.markdown(f"""
<div style="
    background: linear-gradient(135deg, #141414 0%, #1a0a0a 100%);
    border: 1px solid #2a0a0a;
    border-top: 2px solid #cc0000;
    border-radius: 6px;
    padding: 1rem 1.2rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.5);
">
    <div style="font-family:'DM Mono',monospace;font-size:0.7rem;letter-spacing:0.12em;text-transform:uppercase;color:#888">{label}</div>
    <div style="font-family:'Playfair Display',serif;font-size:1.6rem;color:#ffffff;margin:0.2rem 0">{value}</div>
    {f'<div style="font-family:DM Mono,monospace;font-size:0.85rem;color:{delta_colour}">{delta_arrow} {delta}</div>' if delta else ''}
</div>
""", unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)
kpi_card(k1, "♠ All Time GOAT",   biggest_winner, f"₹{abs(winner_val):,.0f}", delta_colour="#2ecc71", delta_arrow="▲")
kpi_card(k2, "♥ Biggest Spender", biggest_loser,  f"₹{abs(loser_val):,.0f}",  delta_colour="#cc0000", delta_arrow="▼")
kpi_card(k3, "♦ Session Count",   sessions_count)
kpi_card(k4, "♣ Table Regulars",  regulars_str)

st.markdown("<br>", unsafe_allow_html=True)

# ── Chart card wrapper ──
def chart_card(title, fig, key):
    st.markdown(f'<div class="chart-card"><div class="chart-card-title">{title}</div>', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, key=key)
    st.markdown("</div>", unsafe_allow_html=True)

# ── Cumulative P/L ──
with st.container():
    df_sorted = df_f.sort_values("Date")
    df_cum = (
        df_sorted.groupby(["Date", "Name"])["P/L"]
        .sum().groupby(level=1).cumsum().reset_index()
    )
    fig_line = px.line(
        df_cum, x="Date", y="P/L", color="Name", markers=True,
        color_discrete_sequence=["#3498db","#2ecc71","#f39c12","#9b59b6","#ff00ea","#e67e22","#e74c3c","#f1c40f","#1abc9c","#e74c3c"]
    )
    fig_line.update_layout(**PLOTLY_LAYOUT, yaxis_title="Cumulative P/L (₹)")
    fig_line.update_layout(legend=dict(orientation="h", y=-0.15, x=0, xanchor="left"))
    chart_card("♥ Cumulative P/L Over Time", fig_line, "line")

# ── Leaderboard + Session Wins ──
c3, c1 = st.columns(2)

with c1:
    leaderboard = total_pl.sort_values(ascending=False).reset_index()
    leaderboard.columns = ["Player", "Total P/L"]
    leaderboard["colour"] = leaderboard["Total P/L"].apply(lambda x: "#cc0000" if x >= 0 else "#4a0000")
    fig_bar = go.Figure(go.Bar(
        x=leaderboard["Player"],
        y=leaderboard["Total P/L"],
        marker_color=leaderboard["colour"],
        text=leaderboard["Total P/L"].apply(lambda x: f"₹{x:+.0f}"),
        textposition="outside",
        textfont=dict(color="#aaa", size=10),
    ))
    fig_bar.update_layout(**PLOTLY_LAYOUT, yaxis_title="P/L (₹)")
    chart_card("♠ All-Time P/L Leaderboard", fig_bar, "bar")

with c3:
    session_winners = df_f.loc[df_f.groupby("Date")["P/L"].idxmax()]["Name"]
    wins_count = session_winners.value_counts().reset_index()
    wins_count.columns = ["Player", "Sessions Won"]

    pr = (
        df_f.groupby("Name")["P/L"].max()
        .reset_index()
        .rename(columns={"Name": "Player", "P/L": "Best Session"})
    )

    combined = wins_count.merge(pr, on="Player") \
        .sort_values("Sessions Won", ascending=False) \
        .reset_index(drop=True)
    combined["Best Session"] = combined["Best Session"].apply(lambda x: f"₹{x:+,.0f}")

    def colour_combined(val):
        if isinstance(val, (int, float)) and val == combined["Sessions Won"].max():
            return "color: #cc0000; font-weight: bold"
        if isinstance(val, str) and val.startswith("₹"):
            return "color: #cc0000; font-weight: bold"
        return "color: #f0f0f0"

    st.markdown('<div class="chart-card"><div class="chart-card-title">♥ Session Wins & PR</div>', unsafe_allow_html=True)
    st.dataframe(
        combined.style.applymap(colour_combined, subset=["Sessions Won", "Best Session"]),
        use_container_width=True,
        hide_index=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ── Session Breakdown ──
st.markdown('<hr class="red-divider">', unsafe_allow_html=True)

sessions_list = sorted(df_f["Date"].dt.date.unique(), reverse=True)
col_sel, _ = st.columns([1, 2])
with col_sel:
    selected_session = st.selectbox("📅 Select a Session", sessions_list)

session_df = df_f[df_f["Date"].dt.date == selected_session][
    ["Name", "Buyin", "Cashout", "P/L"]
].sort_values("P/L", ascending=False).reset_index(drop=True)

def colour_pl(val):
    if val > 0: return "color: #cc0000; font-weight: bold"
    if val < 0: return "color: #660000; font-weight: bold"
    return "color: #555"

st.markdown(
    f'<div class="chart-card"><div class="chart-card-title">♠ Session Results — {selected_session}</div>',
    unsafe_allow_html=True
)
st.dataframe(
    session_df.style.applymap(colour_pl, subset=["P/L"]),
    use_container_width=True,
    hide_index=True,
)
st.markdown("</div>", unsafe_allow_html=True)