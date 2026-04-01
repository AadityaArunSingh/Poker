import pandas as pd
import streamlit as st
from datetime import date
from config import CSV_URL, MIN_SESSIONS


@st.cache_data(ttl=300)
def load_data() -> pd.DataFrame:
    df = pd.read_csv(CSV_URL)
    df.columns = df.columns.str.strip()
    df["Date"]    = pd.to_datetime(df["Date"])
    df["P/L"]     = pd.to_numeric(df["P/L"],     errors="coerce")
    df["Buyin"]   = pd.to_numeric(df["Buyin"],   errors="coerce")
    df["Cashout"] = pd.to_numeric(df["Cashout"], errors="coerce")
    df = df.dropna(subset=["Name", "Date", "P/L"])
    return df


def apply_filters(df: pd.DataFrame, month_active: bool) -> pd.DataFrame:
    """Apply month filter and qualified player filter."""
    if month_active:
        today       = date.today()
        month_start = date(today.year, today.month, 1)
        df_f = df[(df["Date"].dt.date >= month_start) & (df["Date"].dt.date <= today)]
    else:
        df_f = df.copy()

    # Only keep players with enough sessions in the full dataset
    qualified         = df.groupby("Name")["Date"].nunique()
    qualified_players = qualified[qualified > MIN_SESSIONS].index
    df_f              = df_f[df_f["Name"].isin(qualified_players)]
    return df_f


def compute_kpis(df_f: pd.DataFrame) -> dict:
    """Return all KPI values as a dict."""
    total_pl           = df_f.groupby("Name")["P/L"].sum()
    sessions_per_player = df_f.groupby("Name")["Date"].nunique()
    sessions_count     = df_f["Date"].nunique()

    biggest_winner = total_pl.idxmax() if not total_pl.empty else "N/A"
    biggest_loser  = total_pl.idxmin() if not total_pl.empty else "N/A"

    full_attendance = [
        p for p in sessions_per_player.index
        if sessions_per_player[p] == sessions_count
    ]
    regulars_str = ", ".join(full_attendance) if full_attendance else "None"
    if len(regulars_str) > 28:
        regulars_str = regulars_str[:25] + "…"

    return {
        "total_pl":           total_pl,
        "sessions_per_player": sessions_per_player,
        "sessions_count":     sessions_count,
        "biggest_winner":     biggest_winner,
        "biggest_loser":      biggest_loser,
        "winner_val":         total_pl.get(biggest_winner, 0),
        "loser_val":          total_pl.get(biggest_loser,  0),
        "regulars_str":       regulars_str,
    }
