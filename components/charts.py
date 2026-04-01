import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium

from config import PLOTLY_LAYOUT, LINE_COLOURS, LOCATION_COORDS, LABEL_OFFSETS


# ── Helper ────────────────────────────────────────────────────────────────────

def _card(title: str, fig, key: str):
    st.markdown(f'<div class="chart-card"><div class="chart-card-title">{title}</div>', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, key=key)
    st.markdown("</div>", unsafe_allow_html=True)


# ── Charts ────────────────────────────────────────────────────────────────────

def render_cumulative_pl(df_f):
    df_sorted = df_f.sort_values("Date")
    df_cum = (
        df_sorted.groupby(["Date", "Name"])["P/L"]
        .sum().groupby(level=1).cumsum().reset_index()
    )
    fig = px.line(df_cum, x="Date", y="P/L", color="Name",
                  markers=True, color_discrete_sequence=LINE_COLOURS)
    fig.update_layout(**PLOTLY_LAYOUT, yaxis_title="Cumulative P/L (₹)")
    fig.update_layout(legend=dict(orientation="h", y=-0.15, x=0, xanchor="left"))
    _card("♥ Cumulative P/L Over Time", fig, "line")


def render_leaderboard(total_pl):
    leaderboard = total_pl.sort_values(ascending=False).reset_index()
    leaderboard.columns = ["Player", "Total P/L"]
    leaderboard["colour"] = leaderboard["Total P/L"].apply(lambda x: "#cc0000" if x >= 0 else "#4a0000")
    fig = go.Figure(go.Bar(
        x=leaderboard["Player"],
        y=leaderboard["Total P/L"],
        marker_color=leaderboard["colour"],
        text=leaderboard["Total P/L"].apply(lambda x: f"₹{x:+.0f}"),
        textposition="outside",
        textfont=dict(color="#aaa", size=10),
    ))
    fig.update_layout(**PLOTLY_LAYOUT, yaxis_title="P/L (₹)")
    _card("♠ All-Time P/L Leaderboard", fig, "bar")


# def render_greed_radar(df_f):
#     all_p = sorted(df_f["Name"].unique())

#     greed = df_f.groupby(["Name", "Date"])["Buyin"].sum().reset_index()
#     greed["Units"] = greed["Buyin"] / 200
#     avg_units     = greed.groupby("Name")["Units"].mean().reindex(all_p, fill_value=0)
#     total_cashout = df_f.groupby("Name")["Cashout"].sum().reindex(all_p, fill_value=0)

#     max_cashout   = total_cashout.max() or 1
#     cashout_scaled = (total_cashout / max_cashout * 100).round(1)

#     MAX_RINGS = 4
#     ring_data = [
#         [round((r / MAX_RINGS * 100), 1) if avg_units[p] >= r else 0 for p in all_p]
#         for r in range(1, MAX_RINGS + 1)
#     ]
#     ring1, ring2, ring3, ring4 = ring_data

#     labels           = all_p
#     cashout_vals     = [float(cashout_scaled[p]) for p in all_p]
#     avg_units_list   = [round(float(avg_units[p]), 1) for p in all_p]
#     cashout_raw_list = [int(total_cashout[p]) for p in all_p]

#     st.markdown('<div class="chart-card"><div class="chart-card-title">♦ Greed vs Reward</div>', unsafe_allow_html=True)
#     components.html(f"""
# <!DOCTYPE html><html><head>
# <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
# <style>
#   body {{ background:transparent; margin:0; display:flex; justify-content:center; align-items:center; }}
#   #tooltip {{
#     position:absolute; background:#111; border-top:2px solid #cc0000; color:#f0f0f0;
#     font-family:monospace; font-size:11px; padding:8px 12px; border-radius:4px;
#     pointer-events:none; display:none; white-space:nowrap; z-index:99;
#   }}
# </style></head><body>
# <div style="position:relative;width:420px;height:420px;">
#   <canvas id="radar"></canvas><div id="tooltip"></div>
# </div>
# <script>
#   const labels={labels}; const cashout={cashout_vals};
#   const ring1={ring1}; const ring2={ring2}; const ring3={ring3}; const ring4={ring4};
#   const avgUnits={avg_units_list}; const cashoutRaw={cashout_raw_list};
#   let rotation=0;
#   const chart=new Chart(document.getElementById("radar").getContext("2d"),{{
#     type:"radar",
#     data:{{labels,datasets:[
#       {{label:"Avg 4× Buy-in",data:ring4,borderColor:"rgba(255,255,255,0.9)",backgroundColor:"rgba(255,255,255,0.03)",borderWidth:2,pointRadius:0,order:4}},
#       {{label:"Avg 3× Buy-in",data:ring3,borderColor:"rgba(255,255,255,0.65)",backgroundColor:"rgba(255,255,255,0.04)",borderWidth:2,pointRadius:0,order:3}},
#       {{label:"Avg 2× Buy-in",data:ring2,borderColor:"rgba(255,255,255,0.4)",backgroundColor:"rgba(255,255,255,0.06)",borderWidth:2,pointRadius:0,order:2}},
#       {{label:"Avg 1× Buy-in",data:ring1,borderColor:"rgba(255,255,255,0.2)",backgroundColor:"rgba(255,255,255,0.08)",borderWidth:2,pointRadius:0,order:1}},
#       {{label:"Cashout",data:cashout,borderColor:"#cc0000",backgroundColor:"rgba(204,0,0,0.15)",borderWidth:2.5,pointBackgroundColor:"#cc0000",pointRadius:4,order:0}},
#     ]}},
#     options:{{
#       animation:false, responsive:true, maintainAspectRatio:true,
#       plugins:{{
#         legend:{{position:"bottom",labels:{{color:"#666",font:{{family:"monospace",size:10}},boxWidth:12}}}},
#         tooltip:{{enabled:false}},
#       }},
#       scales:{{r:{{startAngle:0,min:0,max:100,ticks:{{display:false}},grid:{{color:"#222"}},angleLines:{{color:"#333"}},pointLabels:{{color:"#ddd",font:{{family:"monospace",size:12}}}}}}}}
#     }}
#   }});
#   (function rotate(){{ rotation=(rotation+0.15)%360; chart.options.scales.r.startAngle=rotation; chart.update("none"); requestAnimationFrame(rotate); }})();
#   const canvas=document.getElementById("radar"), tooltip=document.getElementById("tooltip");
#   canvas.addEventListener("mousemove",(e)=>{{
#     const pts=chart.getElementsAtEventForMode(e,"point",{{intersect:true}},false);
#     if(pts.length>0){{
#       const i=pts[0].index;
#       tooltip.style.display="block"; tooltip.style.left=(e.offsetX+14)+"px"; tooltip.style.top=(e.offsetY-10)+"px";
#       tooltip.innerHTML="<b style='color:#cc0000'>"+labels[i]+"</b><br>Avg buy-ins: "+avgUnits[i]+"×<br>Total cashout: ₹"+cashoutRaw[i].toLocaleString();
#     }} else {{ tooltip.style.display="none"; }}
#   }});
#   canvas.addEventListener("mouseleave",()=>{{ tooltip.style.display="none"; }});
# </script></body></html>
# """, height=480)
#     st.markdown("</div>", unsafe_allow_html=True)


# def render_map(df_f):
#     if "Location" in df_f.columns:
#         player_loc_df = df_f.groupby(["Location", "Name"])["P/L"].sum().reset_index()
#     else:
#         player_loc_df = __import__("pandas").DataFrame(columns=["Location", "Name", "P/L"])

#     fmap = folium.Map(location=[20, 20], zoom_start=2, tiles="CartoDB dark_matter")

#     for loc_key, coords in LOCATION_COORDS.items():
#         players_here = player_loc_df[player_loc_df["Location"] == loc_key]
#         if players_here.empty:
#             player_rows = "<i style='color:#555'>No data</i>"
#         else:
#             rows = []
#             for _, p in players_here.sort_values("P/L", ascending=False).iterrows():
#                 colour = "#cc0000" if p["P/L"] >= 0 else "#ff6666"
#                 sign   = "+" if p["P/L"] >= 0 else ""
#                 rows.append(
#                     f'<tr><td style="padding:2px 8px 2px 0;color:#ddd">{p["Name"]}</td>'
#                     f'<td style="color:{colour};font-weight:bold">{sign}₹{p["P/L"]:.0f}</td></tr>'
#                 )
#             player_rows = "<table style='border-collapse:collapse'>" + "".join(rows) + "</table>"

#         popup_html = f"""<div style="font-family:monospace;background:#111;color:#f0f0f0;
#             padding:10px 12px;border-radius:6px;min-width:180px;border-top:2px solid #cc0000">
#             <b style="color:#cc0000;font-size:13px">{coords["label"]}</b><br><br>{player_rows}</div>"""

#         folium.Marker(
#             location=[coords["lat"], coords["lon"]],
#             popup=folium.Popup(popup_html, max_width=250),
#             tooltip=coords["label"],
#             icon=folium.DivIcon(
#                 html=f'<div style="font-family:monospace;font-size:11px;color:#fff;background:#cc0000;'
#                      f'padding:3px 7px;border-radius:3px;white-space:nowrap;'
#                      f'box-shadow:0 2px 6px rgba(0,0,0,0.6)">{coords["label"]}</div>',
#                 icon_size=(120, 24),
#                 icon_anchor=LABEL_OFFSETS.get(loc_key, (0, 12)),
#             )
#         ).add_to(fmap)

#     st.markdown('<div class="chart-card"><div class="chart-card-title">♣ Where the Gamblers Are</div>', unsafe_allow_html=True)
#     st_folium(fmap, use_container_width=True, height=320, returned_objects=[])
#     st.markdown("</div>", unsafe_allow_html=True)
