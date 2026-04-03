import streamlit as st
from datetime import date

st.set_page_config(
    page_title="🃏 जुआरी Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Local imports ──────────────────────────────────────────────────────────────
from styles import CSS
from data import load_data, apply_filters, compute_kpis
from components.header import render_header
from components.kpis import render_kpis
from components.charts import render_cumulative_pl, render_leaderboard
from components.tables import render_session_wins_and_pr, render_session_results

# ── Styles ─────────────────────────────────────────────────────────────────────
st.markdown(CSS, unsafe_allow_html=True)

# ── Month filter state (read before any rendering) ─────────────────────────────
try:
    month_active = st.query_params.get("month_filter", "0") == "1"
except Exception:
    month_active = False

# ── Data ───────────────────────────────────────────────────────────────────────
df   = load_data()
df_f = apply_filters(df, month_active)

# Apply sidebar filters on top
all_players = sorted(df["Name"].unique())
selected_players = st.sidebar.multiselect("Players", all_players, default=all_players)
all_dates = sorted(df["Date"].dt.date.unique())
date_range = st.sidebar.date_input(
    "Date Range",
    value=(min(all_dates), max(all_dates)),
    min_value=min(all_dates),
    max_value=max(all_dates),
)
if len(date_range) == 2:
    start, end = date_range
    df_f = df_f[
        (df_f["Name"].isin(selected_players)) &
        (df_f["Date"].dt.date >= start) &
        (df_f["Date"].dt.date <= end)
    ]
else:
    df_f = df_f[df_f["Name"].isin(selected_players)]

kpis = compute_kpis(df_f)

if month_active:
    st.toast(f"📅 {date.today().strftime('%B %Y')} only", icon="🗓️")

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-heading">♠ Filters</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()
    st.markdown('<hr style="border-color:#1f0a0a">', unsafe_allow_html=True)
    st.markdown(
        '<div style="font-size:0.65rem;color:#444;text-align:center;letter-spacing:0.1em">AUTO-REFRESHES EVERY 5 MIN</div>',
        unsafe_allow_html=True,
    )

# ── Header ─────────────────────────────────────────────────────────────────────
render_header(month_active)

# ── KPIs ───────────────────────────────────────────────────────────────────────
render_kpis(kpis)

# ── Row 1: Cumulative P/L (full width) ─────────────────────────────────────────
with st.container():
    render_cumulative_pl(df_f)

# ── Row 2: Session Wins & PR | Leaderboard ─────────────────────────────────────
c_left, c_right = st.columns(2)
with c_left:
    render_session_wins_and_pr(df_f)
with c_right:
    render_leaderboard(kpis["total_pl"])

# ── Session Results ─────────────────────────────────────────────────────────────
render_session_results(df_f)
