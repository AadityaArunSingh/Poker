import streamlit as st
from datetime import date

st.set_page_config(
    page_title="🃏 जुआरी Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from styles import CSS
from data import load_data, apply_filters, compute_kpis
from components.header import render_header
from components.kpis import render_kpis
from components.charts import render_cumulative_pl, render_leaderboard
from components.tables import render_session_wins_and_pr, render_session_results

st.markdown(CSS, unsafe_allow_html=True)

# ── One-time popup per session ────────────────────────────────────────────────
if "popup_dismissed" not in st.session_state:
    st.session_state.popup_dismissed = False

if not st.session_state.popup_dismissed:
    st.markdown("""
    <div id="popup-overlay" style="
        position:fixed; top:0; left:0; width:100vw; height:100vh;
        background:rgba(0,0,0,0.85); z-index:99999;
        display:flex; align-items:center; justify-content:center;
    ">
        <div style="
            background:linear-gradient(160deg,#111111,#0d0505);
            border:1px solid #1f0a0a; border-top:3px solid #cc0000;
            border-radius:10px; padding:2.5rem 3rem; max-width:420px;
            text-align:center; box-shadow:0 20px 60px rgba(0,0,0,0.8);
        ">
            <div style="font-size:2.5rem; margin-bottom:1rem">🎰</div>
            <div style="font-family:'Playfair Display',serif;font-size:1.6rem;
                color:#ffffff;font-weight:900;margin-bottom:0.5rem">
                Free Buy-in Wheel
            </div>
            <div style="font-family:'DM Mono',monospace;font-size:0.75rem;
                color:#666;letter-spacing:0.1em;text-transform:uppercase;
                margin-bottom:1.5rem">
                Play 5+ sessions this month · Win ₹200
            </div>
            <div style="font-family:'DM Mono',monospace;font-size:0.8rem;
                color:#aaa;margin-bottom:2rem;line-height:1.6">
                Every month, the highest profit player spins the wheel.<br>
                Whoever it lands on gets a free ₹200 buy-in. 🃏
            </div>
            <div style="display:flex;gap:1rem;justify-content:center">
                <a href="/wheel" target="_self" style="
                    background:linear-gradient(135deg,#8b0000,#cc0000);
                    color:white; text-decoration:none;
                    font-family:'DM Mono',monospace;
                    font-size:0.75rem;letter-spacing:0.1em;
                    text-transform:uppercase;
                    padding:0.7rem 1.5rem; border-radius:4px;
                    box-shadow:0 4px 16px rgba(204,0,0,0.4);
                ">Spin the Wheel 🎡</a>
                <button onclick="document.getElementById('popup-overlay').style.display='none'"
                style="
                    background:transparent; color:#555;
                    border:1px solid #2a0a0a; border-radius:4px;
                    font-family:'DM Mono',monospace;
                    font-size:0.75rem;letter-spacing:0.1em;
                    text-transform:uppercase;
                    padding:0.7rem 1.5rem; cursor:pointer;
                ">Maybe Later</button>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.session_state.popup_dismissed = True

# ── Read state before anything renders ────────────────────────────────────────
try:
    month_active = st.query_params.get("month_filter", "0") == "1"
except Exception:
    month_active = False

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-heading">♠ Filters</div>', unsafe_allow_html=True)

    df_raw = load_data()
    all_players = sorted(df_raw["Name"].unique())
    selected_players = st.multiselect("Players", all_players, default=all_players)
    all_dates = sorted(df_raw["Date"].dt.date.unique())
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
    btn_label = "📅 This Month Only ✓" if month_active else "📅 This Month Only"
    if st.button(btn_label, key="month_toggle"):
        new_val = "0" if month_active else "1"
        st.query_params["month_filter"] = new_val
        st.rerun()

    st.markdown('<hr style="border-color:#1f0a0a">', unsafe_allow_html=True)
    st.markdown(
        '<div style="font-size:0.65rem;color:#444;text-align:center;letter-spacing:0.1em">AUTO-REFRESHES EVERY 5 MIN</div>',
        unsafe_allow_html=True,
    )

# ── Data ──────────────────────────────────────────────────────────────────────
df   = load_data()
df_f = apply_filters(df, month_active)

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

# ── Header ────────────────────────────────────────────────────────────────────
render_header()

# ── KPIs ──────────────────────────────────────────────────────────────────────
render_kpis(kpis)

# ── Row 1: Cumulative P/L full width ──────────────────────────────────────────
with st.container():
    render_cumulative_pl(df_f)

# ── Row 2: Session Wins & PR | Leaderboard ────────────────────────────────────
c_left, c_right = st.columns(2)
with c_left:
    render_session_wins_and_pr(df_f)
with c_right:
    render_leaderboard(kpis["total_pl"])

# ── Session Results ───────────────────────────────────────────────────────────
render_session_results(df_f)