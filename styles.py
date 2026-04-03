CSS = """
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

[data-testid="stToggle"] p {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #888 !important;
}

::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #0a0a0a; }
::-webkit-scrollbar-thumb { background: #8b0000; border-radius: 2px; }
</style>
/* ── Mobile (iPhone) ── */
@media (max-width: 768px) {

    /* Title */
    .hero-title {
        font-size: 2rem !important;
        letter-spacing: 0.02em !important;
    }
    .hero-subtitle {
        font-size: 0.65rem !important;
    }

    /* KPIs — stack 2x2, centre everything */
    [data-testid="stHorizontalBlock"] {
        flex-wrap: wrap !important;
    }
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
        min-width: 45% !important;
        flex: 1 1 45% !important;
    }
    [data-testid="stMetric"] {
        text-align: center !important;
    }

    /* Charts — give them breathing room */
    [data-testid="stPlotlyChart"] {
        min-height: 300px !important;
    }

    /* Prevent horizontal overflow everywhere */
    .main .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        overflow-x: hidden !important;
    }
}

"""
