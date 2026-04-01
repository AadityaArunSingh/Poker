import streamlit as st


def _kpi_card(col, label: str, value, delta: str = None,
              delta_colour: str = "#cc0000", delta_arrow: str = "▼"):
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


def render_kpis(kpis: dict):
    k1, k2, k3, k4 = st.columns(4)
    _kpi_card(k1, "♠ All Time GOAT",   kpis["biggest_winner"], f"₹{abs(kpis['winner_val']):,.0f}", delta_colour="#2ecc71", delta_arrow="▲")
    _kpi_card(k2, "♥ Biggest Spender", kpis["biggest_loser"],  f"₹{abs(kpis['loser_val']):,.0f}",  delta_colour="#cc0000", delta_arrow="▼")
    _kpi_card(k3, "♦ Session Count",   kpis["sessions_count"])
    _kpi_card(k4, "♣ Table Regulars",  kpis["regulars_str"])
    st.markdown("<br>", unsafe_allow_html=True)
