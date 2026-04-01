SHEET_ID = "1N0f0momimoEEWxqmxSrthV3IxkQIMpxczoLIbHw5XsQ"
CSV_URL  = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Mono, monospace", color="#aaa", size=11),
    margin=dict(l=10, r=10, t=10, b=10),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#aaa")),
    xaxis=dict(gridcolor="#1a1a1a", linecolor="#333", tickcolor="#333"),
    yaxis=dict(gridcolor="#1a1a1a", linecolor="#333", tickcolor="#333"),
)

LINE_COLOURS = [
    "#3498db", "#2ecc71", "#f39c12", "#9b59b6",
    "#ff00ea", "#e67e22", "#e74c3c", "#f1c40f",
    "#1abc9c", "#e74c3c",
]

LOCATION_COORDS = {
    "London, UK":     {"lat": 51.5074,  "lon": -0.1278,  "label": "London 🇬🇧"},
    "Thane, IND":     {"lat": 19.2183,  "lon": 72.9781,  "label": "Mumbai 🇮🇳"},
    "Adelaide, AUS":  {"lat": -34.9285, "lon": 138.6007, "label": "Adelaide 🇦🇺"},
    "Hyderabad, IND": {"lat": 17.3850,  "lon": 78.4867,  "label": "Hyderabad 🇮🇳"},
}

LABEL_OFFSETS = {
    "London, UK":     (0, 12),
    "Thane, IND":     (-60, -5),
    "Hyderabad, IND": (0, 25),
    "Adelaide, AUS":  (0, 12),
}

MIN_SESSIONS = 3  # players need more than this many sessions to appear
