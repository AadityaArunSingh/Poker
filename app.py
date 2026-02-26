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
import pandas as pd
# from streamlit_gsheets import GSheetsConnection

# url = "https://docs.google.com/spreadsheets/d/1N0f0momimoEEWxqmxSrthV3IxkQIMpxczoLIbHw5XsQ/edit?usp=sharing"

# conn = st.connection("gsheets", type=GSheetsConnection)

# data = conn.read(spreadsheet=url, worksheet="0")
df = pd.read_csv('/Users/aadityasingh/Developer/Coding/Poker/poker.csv')
st.dataframe(df)