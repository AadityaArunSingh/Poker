# import streamlit as st
# import pandas as pd

# # Use your PUBLISHED CSV link here
# DATA_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1v.../pub?output=csv"

# # Pipeline: Read the CSV data into a DataFrame
# df = pd.read_csv(DATA_URL)

# st.title("Poker Data Test")

# # Display the actual data frame
# st.table(df)

# example/st_app.py

import streamlit as st
from streamlit_gsheets import GSheetsConnection

url = "https://docs.google.com/spreadsheets/d/1Gc3Wi1vpTP4g5rnWuaRJDZWycZHvKO7F2xCv1ZGo0oU/edit?usp=sharing"

conn = st.connection("gsheets", type=GSheetsConnection)

data = conn.read(spreadsheet=url, usecols=[0, 1])
st.dataframe(data)