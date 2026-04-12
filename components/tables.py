import streamlit as st


def _colour_pl(val):
    if val > 0: return "color: #cc0000; font-weight: bold"
    if val < 0: return "color: #660000; font-weight: bold"
    return "color: #555"


def render_session_wins_and_pr(df_f):
    session_winners = df_f.loc[df_f.groupby("Date")["P/L"].idxmax()]["Name"]
    wins_count = session_winners.value_counts().reset_index()
    wins_count.columns = ["Player", "Sessions MVP"]

    pr = (
        df_f.groupby("Name")["P/L"].max()
        .reset_index()
        .rename(columns={"Name": "Player", "P/L": "Biggest Bag💰"})
    )

    combined = (
        wins_count.merge(pr, on="Player")
        .sort_values("Sessions MVP", ascending=False)
        .reset_index(drop=True)
    )
    combined = combined.rename(columns={"Sessions Won": "Sessions MVP", "Best Session": "Biggest Bag💰"})
    combined["Biggest Bag💰"] = combined["Biggest Bag💰"].apply(lambda x: f"₹{x:+,.0f}")

    def colour_combined(val):
        if isinstance(val, (int, float)) and val == combined["Sessions MVP"].max():
            return "color: #cc0000; font-weight: bold"
        if isinstance(val, str) and val.startswith("₹"):
            return "color: #cc0000; font-weight: bold"
        return "color: #888888"

    st.markdown('<div class="chart-card"><div class="chart-card-title">♥ Session Wins & PR</div>', unsafe_allow_html=True)
    st.dataframe(
        combined.style.applymap(colour_combined, subset=["Sessions MVP", "Biggest Bag💰"]),
        use_container_width=True, hide_index=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


def render_all_time_rankings(df_f):
    all_profits = (
        df_f[df_f["P/L"] > 0][["Name", "Date", "P/L"]]
        .sort_values("P/L", ascending=False)
        .reset_index(drop=True)
    )
    all_profits["Rank"] = ["#" + str(i + 1) for i in range(len(all_profits))]
    all_profits["Date"] = all_profits["Date"].dt.strftime("%d %b %Y")
    all_profits["P/L"]  = all_profits["P/L"].apply(lambda x: f"₹{x:+,.0f}")
    all_profits = all_profits[["Rank", "Name", "P/L", "Date"]]

    def colour_rank(val):
        if val == "#1": return "color: #FFD700; font-weight: bold"
        if val == "#2": return "color: #C0C0C0; font-weight: bold"
        if val == "#3": return "color: #CD7F32; font-weight: bold"
        return "color: #f0f0f0"

    st.markdown('<div class="chart-card"><div class="chart-card-title">♠ All-Time Profit Rankings</div>', unsafe_allow_html=True)
    st.dataframe(
        all_profits.style.applymap(colour_rank, subset=["Rank"]),
        use_container_width=True, hide_index=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


def render_session_results(df_f):
    st.markdown('<hr class="red-divider">', unsafe_allow_html=True)

    sessions_list = sorted(df_f["Date"].dt.date.unique(), reverse=True)
    col_sel, _ = st.columns([1, 2])
    with col_sel:
        selected_session = st.selectbox("📅 Select a Session", sessions_list)

    session_df = (
        df_f[df_f["Date"].dt.date == selected_session]
        [["Name", "Buyin", "Cashout", "P/L"]]
        .sort_values("P/L", ascending=False)
        .reset_index(drop=True)
    )

    st.markdown(
        f'<div class="chart-card"><div class="chart-card-title">♠ Session Results — {selected_session}</div>',
        unsafe_allow_html=True,
    )
    st.dataframe(
        session_df.style.applymap(_colour_pl, subset=["P/L"]),
        use_container_width=True, hide_index=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)
