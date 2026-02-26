import streamlit as st
import pandas as pd

# Use your PUBLISHED CSV link here
DATA_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1v.../pub?output=csv"

# Pipeline: Read the CSV data into a DataFrame
df = pd.read_csv(DATA_URL)

st.title("Poker Data Test")

# Display the actual data frame
st.table(df)