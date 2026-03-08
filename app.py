import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="🃏 जुआरी Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Mono:wght@400;500&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    background-color: #0a0a0a !important;
    color: #f0f0f0 !important;
    font-family: 'DM Mono', monospace !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0f0f0f !important;
    border-right: 1px solid #2a0a0a !important;
}
[data-testid="stSidebar"] * {
    color: #f0f0f0 !important;
}
[data-testid="stSidebarNav"] { display: none; }

/* ── Sidebar widgets ── */
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {
    background-color: #8b0000 !important;
}
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="select"] > div,
[data-testid="stSidebar"] .stDateInput input {
    background-color: #1a1a1a !important;
    border: 1px solid #8b0000 !important;
    color: #f0f0f0 !important;
}

/* ── Hero title ── */
.hero-title {
    text-align: center;
    font-family: 'Playfair Display', serif;
    font-size: 3.8rem;
    font-weight: 900;
    color: #ffffff;
    letter-spacing: 0.04em;
    line-height: 1.1;
    padding: 1.2rem 0 0.2rem;
    text-shadow: 0 0 40px rgba(180, 0, 0, 0.6), 0 2px 4px rgba(0,0,0,0.8);
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

/* ── Divider ── */
.red-divider {
    border: none;
    height: 1px;
    background: linear-gradient(to right, transparent, #8b0000, #cc0000, #8b0000, transparent);
    margin: 1rem 0 1.5rem;
}

/* ── Metric cards ── */
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

/* ── Chart cards ── */
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

/* ── Sidebar filter heading ── */
.sidebar-heading {
    font-family: 'Playfair Display', serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #cc0000;
    margin-bottom: 0.3rem;
}
.sidebar-sub {
    font-size: 0.68rem;
    color: #555;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
}

/* ── Refresh button ── */
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

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    background: #0f0f0f !important;
    border: 1px solid #1f0a0a !important;
    border-radius: 6px !important;
}

/* ── Selectbox ── */
[data-baseweb="select"] > div {
    background-color: #1a1a1a !important;
    border-color: #8b0000 !important;
    color: #f0f0f0 !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: #111 !important;
    border: 1px solid #1f0a0a !important;
    border-radius: 6px !important;
}

/* scrollbar */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #0a0a0a; }
::-webkit-scrollbar-thumb { background: #8b0000; border-radius: 2px; }
</style>
""", unsafe_allow_html=True)

# Dark template
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Mono, monospace", color="#aaa", size=11),
    margin=dict(l=10, r=10, t=10, b=10),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#aaa")),
    xaxis=dict(gridcolor="#1a1a1a", linecolor="#333", tickcolor="#333"),
    yaxis=dict(gridcolor="#1a1a1a", linecolor="#333", tickcolor="#333"),
)

# Config
SHEET_ID = "1N0f0momimoEEWxqmxSrthV3IxkQIMpxczoLIbHw5XsQ"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# Data loading
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

# filters
with st.sidebar:
    st.markdown('<div class="sidebar-heading">♠ Filters</div>', unsafe_allow_html=True)
    # st.markdown('<div class="sidebar-sub">Adjust your view</div>', unsafe_allow_html=True)

    all_players = sorted(df["Name"].unique())
    all_dates = sorted(df["Date"].dt.date.unique())

    selected_players = st.multiselect(
        "Players",
        all_players,
        default=all_players,
    )

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

# apply filters 
if len(date_range) == 2:
    start, end = date_range
    df_f = df[
        (df["Name"].isin(selected_players)) &
        (df["Date"].dt.date >= start) &
        (df["Date"].dt.date <= end)
    ]
else:
    df_f = df[df["Name"].isin(selected_players)]

if len(date_range) == 2:
    start, end = date_range
    df_f = df[
        (df["Name"].isin(selected_players)) &
        (df["Date"].dt.date >= start) &
        (df["Date"].dt.date <= end)
    ]
else:
    df_f = df[df["Name"].isin(selected_players)]

# Only show players with more than 5 sessions in charts
qualified = df_f.groupby("Name")["Date"].nunique()
qualified_players = qualified[qualified > 3].index
df_f = df_f[df_f["Name"].isin(qualified_players)]

# Hero Header
st.markdown('<div class="suit-row">♠ ♥ ♦ ♣</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">JUAARI DASHBOARD</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Gambling addiction tracker</div>', unsafe_allow_html=True)
st.markdown('<hr class="red-divider">', unsafe_allow_html=True)

# KPI
total_pl = df_f.groupby("Name")["P/L"].sum()
sessions_per_player = df_f.groupby("Name")["Date"].nunique()
sessions_count = df_f["Date"].nunique()

biggest_winner = total_pl.idxmax() if not total_pl.empty else "N/A"
biggest_loser  = total_pl.idxmin() if not total_pl.empty else "N/A"
most_active    = sessions_per_player.idxmax() if not sessions_per_player.empty else "N/A"

# Players who attended every session
total_sessions = df_f["Date"].nunique()
full_attendance = [
    p for p in sessions_per_player.index
    if sessions_per_player[p] == total_sessions
]
regulars_str = ", ".join(full_attendance) if full_attendance else "None"
# Truncate if too long
if len(regulars_str) > 28:
    regulars_str = regulars_str[:25] + "…"

k1, k2, k3, k4 = st.columns(4)
k1.metric("♠ All Time GOAT",    biggest_winner, f"₹{total_pl.get(biggest_winner, 0):+.0f}")
k2.metric("♥ Biggest Spender",  biggest_loser,  float(total_pl.get(biggest_loser, 0)),  delta_color="inverse")
k3.metric("♦ Session Count",    sessions_count)
k4.metric("♣ Table Regulars",   regulars_str)

st.markdown("<br>", unsafe_allow_html=True)

# wrapper for plotly viz inside a card
def chart_card(title, fig, key):
    st.markdown(f'<div class="chart-card"><div class="chart-card-title">{title}</div>', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, key=key)
    st.markdown("</div>", unsafe_allow_html=True)

# charts on row 1
c1, c2 = st.columns(2)

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

with c2:
    df_sorted = df_f.sort_values("Date")
    df_cum = (
        df_sorted.groupby(["Date", "Name"])["P/L"]
        .sum().groupby(level=1).cumsum().reset_index()
    )
    fig_line = px.line(
    df_cum, x="Date", y="P/L", color="Name", markers=True,
    color_discrete_sequence=["#3498db","#2ecc71","#f39c12","#9b59b6","#ff00ea","#e67e22","#e74c3c","#f1c40f"]
    )
    fig_line.update_layout(**PLOTLY_LAYOUT, yaxis_title="Cumulative P/L (₹)")
    fig_line.update_layout(legend=dict(orientation="h", y=-0.25, x=0, xanchor="left"))
    chart_card("♥ Cumulative P/L Over Time", fig_line, "line")

# charts on row 2
c3, c4 = st.columns(2)

# with c3:
#     all_p = sorted(df_f["Name"].unique())

#     # Average buy-in units per player across all sessions
#     greed = df_f.groupby(["Name", "Date"])["Buyin"].sum().reset_index()
#     greed["Units"] = greed["Buyin"] / 200
#     avg_units = greed.groupby("Name")["Units"].mean().reindex(all_p, fill_value=0)

#     # Total cashout per player
#     total_cashout = df_f.groupby("Name")["Cashout"].sum().reindex(all_p, fill_value=0)

#     # Normalise cashout to 0–100
#     max_cashout = total_cashout.max() or 1
#     cashout_scaled = (total_cashout / max_cashout * 100).round(1)

#     # Each ring represents one buy-in level (1×, 2×, 3×, 4×)
#     # A player contributes to ring N only if their avg >= N
#     MAX_RINGS = 4
#     theta = all_p + [all_p[0]]

#     fig_radar = go.Figure()

#     # Draw rings from outermost (4) to innermost (1) so inner rings render on top
#     ring_styles = {
#         4: dict(color="rgba(255,255,255,0.9)", fill="rgba(255,255,255,0.03)", width=2),
#         3: dict(color="rgba(255,255,255,0.7)", fill="rgba(255,255,255,0.05)", width=2),
#         2: dict(color="rgba(255,255,255,0.5)", fill="rgba(255,255,255,0.07)", width=2),
#         1: dict(color="rgba(255,255,255,0.3)", fill="rgba(255,255,255,0.10)", width=2),
#     }

#     for ring in range(MAX_RINGS, 0, -1):
#         # Player reaches this ring only if avg buy-ins >= ring level
#         r_vals = [
#             (ring / MAX_RINGS * 100) if avg_units[p] >= ring else 0
#             for p in all_p
#         ]
#         r_closed = r_vals + [r_vals[0]]
#         style = ring_styles[ring]
#         fig_radar.add_trace(go.Scatterpolar(
#             r=r_closed,
#             theta=theta,
#             fill="toself",
#             fillcolor=style["fill"],
#             line=dict(color=style["color"], width=style["width"]),
#             name=f"Avg {ring}× Buy-in",
#             hovertemplate=(
#                 "<b>%{theta}</b><br>"
#                 f"Reached {ring}× avg buy-in<extra></extra>"
#             ),
#         ))

#     # Red polygon — Cashout on top
#     cashout_r = list(cashout_scaled) + [cashout_scaled.iloc[0]]
#     fig_radar.add_trace(go.Scatterpolar(
#         r=cashout_r,
#         theta=theta,
#         fill="toself",
#         fillcolor="rgba(204,0,0,0.15)",
#         line=dict(color="#cc0000", width=2),
#         name="Cashout",
#     ))

#     # Invisible markers for clean per-player hover
#     fig_radar.add_trace(go.Scatterpolar(
#         r=list(cashout_scaled),
#         theta=all_p,
#         mode="markers",
#         marker=dict(size=8, color="#cc0000", opacity=0.8),
#         showlegend=False,
#         customdata=[
#             [f"{avg_units[p]:.1f}×", f"₹{total_cashout[p]:,.0f}"]
#             for p in all_p
#         ],
#         hovertemplate=(
#             "<b>%{theta}</b><br>"
#             "Avg buy-ins: %{customdata[0]}<br>"
#             "Total cashout: %{customdata[1]}"
#             "<extra></extra>"
#         ),
#     ))

#     fig_radar.update_layout(
#         **PLOTLY_LAYOUT,
#         polar=dict(
#             bgcolor="rgba(0,0,0,0)",
#             radialaxis=dict(
#                 visible=True,
#                 range=[0, 100],
#                 showticklabels=False,
#                 gridcolor="#222",
#                 linecolor="#333",
#             ),
#             angularaxis=dict(
#                 tickfont=dict(size=12, color="#ddd"),
#                 gridcolor="#1a1a1a",
#                 linecolor="#333",
#             ),
#         ),
#     )
#     fig_radar.update_layout(legend=dict(
#         orientation="h", y=-0.15, x=0.5, xanchor="center",
#         font=dict(color="#aaa", size=10),
#         bgcolor="rgba(0,0,0,0)",
#     ))
#     chart_card("♦ Greed vs Reward", fig_radar, "radar")

with c3:
    import streamlit.components.v1 as components

    all_p = sorted(df_f["Name"].unique())

    # Average buy-in units per player
    greed = df_f.groupby(["Name", "Date"])["Buyin"].sum().reset_index()
    greed["Units"] = greed["Buyin"] / 200
    avg_units = greed.groupby("Name")["Units"].mean().reindex(all_p, fill_value=0)

    # Total cashout per player
    total_cashout = df_f.groupby("Name")["Cashout"].sum().reindex(all_p, fill_value=0)

    # Normalise cashout to 0–100
    max_cashout = total_cashout.max() or 1
    cashout_scaled = (total_cashout / max_cashout * 100).round(1)

    # Build ring data — 4 rings, player reaches ring N if avg >= N
    MAX_RINGS = 4
    ring_data = []
    for ring in range(1, MAX_RINGS + 1):
        ring_data.append([
            round((ring / MAX_RINGS * 100), 1) if avg_units[p] >= ring else 0
            for p in all_p
        ])

    # Pass data to JS
    labels        = all_p
    cashout_vals  = [float(cashout_scaled[p]) for p in all_p]
    ring1, ring2, ring3, ring4 = ring_data

    # Hover info as parallel arrays
    avg_units_list    = [round(float(avg_units[p]), 1) for p in all_p]
    cashout_raw_list  = [int(total_cashout[p]) for p in all_p]

    st.markdown('<div class="chart-card"><div class="chart-card-title">♦ Greed vs Reward</div>', unsafe_allow_html=True)
    components.html(f"""
<!DOCTYPE html>
<html>
<head>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<style>
  body {{
    background: transparent;
    margin: 0;
    display: flex;
    justify-content: center;
    align-items: center;
  }}
  canvas {{ max-width: 100%; }}
  #tooltip {{
    position: absolute;
    background: #111;
    border-top: 2px solid #cc0000;
    color: #f0f0f0;
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    padding: 8px 12px;
    border-radius: 4px;
    pointer-events: none;
    display: none;
    white-space: nowrap;
    z-index: 99;
  }}
</style>
</head>
<body>
<div style="position:relative;width:420px;height:420px;">
  <canvas id="radar"></canvas>
  <div id="tooltip"></div>
</div>
<script>
  const labels       = {labels};
  const cashout      = {cashout_vals};
  const ring1        = {ring1};
  const ring2        = {ring2};
  const ring3        = {ring3};
  const ring4        = {ring4};
  const avgUnits     = {avg_units_list};
  const cashoutRaw   = {cashout_raw_list};

  let rotation = 0;

  const data = {{
    labels: labels,
    datasets: [
      {{
        label: "Avg 4× Buy-in",
        data: ring4,
        borderColor: "rgba(255,255,255,0.9)",
        backgroundColor: "rgba(255,255,255,0.03)",
        borderWidth: 2,
        pointRadius: 0,
        order: 4,
      }},
      {{
        label: "Avg 3× Buy-in",
        data: ring3,
        borderColor: "rgba(255,255,255,0.65)",
        backgroundColor: "rgba(255,255,255,0.04)",
        borderWidth: 2,
        pointRadius: 0,
        order: 3,
      }},
      {{
        label: "Avg 2× Buy-in",
        data: ring2,
        borderColor: "rgba(255,255,255,0.4)",
        backgroundColor: "rgba(255,255,255,0.06)",
        borderWidth: 2,
        pointRadius: 0,
        order: 2,
      }},
      {{
        label: "Avg 1× Buy-in",
        data: ring1,
        borderColor: "rgba(255,255,255,0.2)",
        backgroundColor: "rgba(255,255,255,0.08)",
        borderWidth: 2,
        pointRadius: 0,
        order: 1,
      }},
      {{
        label: "Cashout",
        data: cashout,
        borderColor: "#cc0000",
        backgroundColor: "rgba(204,0,0,0.15)",
        borderWidth: 2.5,
        pointBackgroundColor: "#cc0000",
        pointRadius: 4,
        order: 0,
      }},
    ]
  }};

  const config = {{
    type: "radar",
    data: data,
    options: {{
      animation: false,
      responsive: true,
      maintainAspectRatio: true,
      plugins: {{
        legend: {{
          position: "bottom",
          labels: {{
            color: "#666",
            font: {{ family: "monospace", size: 10 }},
            boxWidth: 12,
            filter: (item) => item.text !== "",
          }}
        }},
        tooltip: {{ enabled: false }},
      }},
      scales: {{
        r: {{
          startAngle: 0,
          min: 0,
          max: 100,
          ticks: {{ display: false, stepSize: 25 }},
          grid: {{ color: "#222" }},
          angleLines: {{ color: "#333" }},
          pointLabels: {{
            color: "#ddd",
            font: {{ family: "monospace", size: 12 }},
          }},
        }}
      }}
    }}
  }};

  const ctx = document.getElementById("radar").getContext("2d");
  const chart = new Chart(ctx, config);

  // Smooth rotation
  function rotate() {{
    rotation = (rotation + 0.15) % 360;
    chart.options.scales.r.startAngle = rotation;
    chart.update("none");
    requestAnimationFrame(rotate);
  }}
  rotate();

  // Custom tooltip on hover
  const canvas = document.getElementById("radar");
  const tooltip = document.getElementById("tooltip");

  canvas.addEventListener("mousemove", (e) => {{
    const points = chart.getElementsAtEventForMode(e, "point", {{ intersect: true }}, false);
    if (points.length > 0) {{
      const idx = points[0].index;
      tooltip.style.display = "block";
      tooltip.style.left = (e.offsetX + 14) + "px";
      tooltip.style.top  = (e.offsetY - 10) + "px";
      tooltip.innerHTML  =
        "<b style='color:#cc0000'>" + labels[idx] + "</b><br>" +
        "Avg buy-ins: " + avgUnits[idx] + "×<br>" +
        "Total cashout: ₹" + cashoutRaw[idx].toLocaleString();
    }} else {{
      tooltip.style.display = "none";
    }}
  }});
  canvas.addEventListener("mouseleave", () => {{ tooltip.style.display = "none"; }});
</script>
</body>
</html>
""", height=480)
    st.markdown("</div>", unsafe_allow_html=True)

with c4:
    # World bubble map — Folium
    LOCATION_COORDS = {
        "London, UK":    {"lat": 51.5074,  "lon": -0.1278,  "label": "London 🇬🇧"},
        "Thane, IND":    {"lat": 19.2183,  "lon": 72.9781,  "label": "Mumbai 🇮🇳"},
        "Adelaide, AUS": {"lat": -34.9285, "lon": 138.6007, "label": "Adelaide 🇦🇺"},
    }

    # Group by location + player to get P/L per person per location
    if "Location" in df_f.columns:
        player_loc_df = df_f.groupby(["Location", "Name"])["P/L"].sum().reset_index()
    else:
        player_loc_df = pd.DataFrame(columns=["Location", "Name", "P/L"])

    fmap = folium.Map(
        location=[20, 20],
        zoom_start=2,
        tiles="CartoDB dark_matter",
    )

    for loc_key, coords in LOCATION_COORDS.items():
        players_here = player_loc_df[player_loc_df["Location"] == loc_key]

        # Build the player list HTML rows
        if players_here.empty:
            player_rows = "<i style='color:#555'>No data</i>"
        else:
            rows = []
            for _, p in players_here.sort_values("P/L", ascending=False).iterrows():
                colour = "#cc0000" if p["P/L"] >= 0 else "#ff6666"
                sign = "+" if p["P/L"] >= 0 else ""
                rows.append(
                    f'<tr><td style="padding:2px 8px 2px 0;color:#ddd">{p["Name"]}</td>' +
                    f'<td style="color:{colour};font-weight:bold">{sign}₹{p["P/L"]:.0f}</td></tr>'
                )
            player_rows = "<table style='border-collapse:collapse'>" + "".join(rows) + "</table>"

        popup_html = f"""
        <div style="font-family:monospace;background:#111;color:#f0f0f0;padding:10px 12px;border-radius:6px;min-width:180px;border-top:2px solid #cc0000">
            <b style="color:#cc0000;font-size:13px">{coords["label"]}</b><br><br>
            {player_rows}
        </div>"""

        folium.Marker(
            location=[coords["lat"], coords["lon"]],
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=coords["label"],
            icon=folium.DivIcon(
                html=f"""<div style="
                    font-family:monospace;
                    font-size:11px;
                    color:#fff;
                    background:#cc0000;
                    padding:3px 7px;
                    border-radius:3px;
                    white-space:nowrap;
                    box-shadow:0 2px 6px rgba(0,0,0,0.6);
                ">{coords["label"]}</div>""",
                icon_size=(120, 24),
                icon_anchor=(0, 12),
            )
        ).add_to(fmap)

    st.markdown('<div class="chart-card"><div class="chart-card-title">♣ Where the Gamblers Are</div>', unsafe_allow_html=True)
    st_folium(fmap, use_container_width=True, height=320, returned_objects=[])
    st.markdown("</div>", unsafe_allow_html=True)

# sesh breakdown
st.markdown('<hr class="red-divider">', unsafe_allow_html=True)

sessions_list = sorted(df_f["Date"].dt.date.unique(), reverse=True)
col_sel, _ = st.columns([1, 2])
with col_sel:
    selected_session = st.selectbox("📅 Select a Session", sessions_list)

session_df = df_f[df_f["Date"].dt.date == selected_session][
    ["Name", "Buyin", "Cashout", "P/L"]
].sort_values("P/L", ascending=False).reset_index(drop=True)

def colour_pl(val):
    if val > 0:  return "color: #cc0000; font-weight: bold"
    if val < 0:  return "color: #660000; font-weight: bold"
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

# raw
# with st.expander("📋 Full Raw Data"):
#     st.dataframe(df_f.sort_values("Date", ascending=False).reset_index(drop=True), use_container_width=True)

