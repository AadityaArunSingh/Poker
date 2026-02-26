import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="🃏 Poker Dashboard", layout="wide")

# ── Config ──────────────────────────────────────────────────────────────────
SHEET_ID = "1N0f0momimoEEWxqmxSrthV3IxkQIMpxczoLIbHw5XsQ"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# ── Load data ────────────────────────────────────────────────────────────────
@st.cache_data(ttl=300)  # refresh every 5 minutes
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

# ── Header ───────────────────────────────────────────────────────────────────
st.title("🃏 Poker Night Dashboard")
st.caption("Data auto-refreshes every 5 minutes from Google Sheets")

# Reload button
if st.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

st.divider()

# ── Filters ──────────────────────────────────────────────────────────────────
all_players = sorted(df["Name"].unique())
all_dates = sorted(df["Date"].dt.date.unique())

col_f1, col_f2 = st.columns(2)
with col_f1:
    selected_players = st.multiselect("Filter by Player", all_players, default=all_players)
with col_f2:
    date_range = st.date_input(
        "Date Range",
        value=(min(all_dates), max(all_dates)),
        min_value=min(all_dates),
        max_value=max(all_dates),
    )

# Apply filters
if len(date_range) == 2:
    start, end = date_range
    df_filtered = df[
        (df["Name"].isin(selected_players)) &
        (df["Date"].dt.date >= start) &
        (df["Date"].dt.date <= end)
    ]
else:
    df_filtered = df[df["Name"].isin(selected_players)]

st.divider()

# ── Top KPI cards ─────────────────────────────────────────────────────────────
total_pl = df_filtered.groupby("Name")["P/L"].sum()
biggest_winner = total_pl.idxmax() if not total_pl.empty else "N/A"
biggest_loser  = total_pl.idxmin() if not total_pl.empty else "N/A"
sessions = df_filtered["Date"].nunique()
total_sessions_per_player = df_filtered.groupby("Name")["Date"].nunique()
most_active = total_sessions_per_player.idxmax() if not total_sessions_per_player.empty else "N/A"

k1, k2, k3, k4 = st.columns(4)
k1.metric("🏆 Biggest Winner", biggest_winner, f"£{total_pl.get(biggest_winner, 0):+.0f}")
k2.metric("💸 Biggest Loser",  biggest_loser,  f"£{total_pl.get(biggest_loser, 0):+.0f}")
k3.metric("🎮 Sessions Tracked", sessions)
k4.metric("🔥 Most Active", most_active, f"{total_sessions_per_player.get(most_active, 0)} sessions")

st.divider()

# ── Charts row 1 ─────────────────────────────────────────────────────────────
c1, c2 = st.columns(2)

with c1:
    st.subheader("💰 All-Time P/L Leaderboard")
    leaderboard = total_pl.sort_values(ascending=False).reset_index()
    leaderboard.columns = ["Player", "Total P/L"]
    leaderboard["Colour"] = leaderboard["Total P/L"].apply(lambda x: "green" if x >= 0 else "red")
    fig_bar = px.bar(
        leaderboard, x="Player", y="Total P/L",
        color="Colour",
        color_discrete_map={"green": "#2ecc71", "red": "#e74c3c"},
        text="Total P/L",
    )
    fig_bar.update_traces(texttemplate="£%{text:.0f}", textposition="outside")
    fig_bar.update_layout(showlegend=False, yaxis_title="P/L (£)", xaxis_title="")
    st.plotly_chart(fig_bar, use_container_width=True)

with c2:
    st.subheader("📈 Cumulative P/L Over Time")
    df_sorted = df_filtered.sort_values("Date")
    df_cumulative = (
        df_sorted.groupby(["Date", "Name"])["P/L"]
        .sum()
        .groupby(level=1)
        .cumsum()
        .reset_index()
    )
    fig_line = px.line(
        df_cumulative, x="Date", y="P/L", color="Name",
        markers=True,
    )
    fig_line.update_layout(yaxis_title="Cumulative P/L (£)", xaxis_title="")
    st.plotly_chart(fig_line, use_container_width=True)

# ── Charts row 2 ─────────────────────────────────────────────────────────────
c3, c4 = st.columns(2)

with c3:
    st.subheader("🎯 Win Rate by Player")
    win_rate = (
        df_filtered.groupby("Name")["P/L"]
        .apply(lambda x: round((x > 0).sum() / len(x) * 100, 1))
        .reset_index()
    )
    win_rate.columns = ["Player", "Win Rate (%)"]
    win_rate = win_rate.sort_values("Win Rate (%)", ascending=False)
    fig_wr = px.bar(
        win_rate, x="Player", y="Win Rate (%)",
        color="Win Rate (%)",
        color_continuous_scale=["#e74c3c", "#f39c12", "#2ecc71"],
        text="Win Rate (%)",
    )
    fig_wr.update_traces(texttemplate="%{text}%", textposition="outside")
    fig_wr.update_layout(coloraxis_showscale=False, xaxis_title="")
    st.plotly_chart(fig_wr, use_container_width=True)

with c4:
    st.subheader("📅 P/L Per Session (Heatmap)")
    pivot = df_filtered.pivot_table(
        index="Name", columns=df_filtered["Date"].dt.strftime("%d %b"),
        values="P/L", aggfunc="sum"
    )
    fig_heat = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns.tolist(),
        y=pivot.index.tolist(),
        colorscale=[[0, "#e74c3c"], [0.5, "#2c2c2c"], [1, "#2ecc71"]],
        text=pivot.values,
        texttemplate="£%{text:.0f}",
        zmid=0,
    ))
    fig_heat.update_layout(xaxis_title="", yaxis_title="")
    st.plotly_chart(fig_heat, use_container_width=True)

st.divider()

# ── Session-by-session breakdown ─────────────────────────────────────────────
st.subheader("🗂️ Session-by-Session Breakdown")
sessions_list = sorted(df_filtered["Date"].dt.date.unique(), reverse=True)
selected_session = st.selectbox("Select a session", sessions_list)

session_df = df_filtered[df_filtered["Date"].dt.date == selected_session][
    ["Name", "Buyin", "Cashout", "P/L"]
].sort_values("P/L", ascending=False).reset_index(drop=True)

def colour_pl(val):
    colour = "#2ecc71" if val > 0 else ("#e74c3c" if val < 0 else "white")
    return f"color: {colour}; font-weight: bold"

st.dataframe(
    session_df.style.applymap(colour_pl, subset=["P/L"]),
    use_container_width=True,
    hide_index=True,
)

st.divider()

# ── Raw data table ────────────────────────────────────────────────────────────
with st.expander("📋 View Full Raw Data"):
    st.dataframe(df_filtered.sort_values("Date", ascending=False).reset_index(drop=True), use_container_width=True)
