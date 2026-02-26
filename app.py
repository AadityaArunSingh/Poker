import streamlit as st
import pandas as pd

data = 'https://docs.google.com/spreadsheets/d/1N0f0momimoEEWxqmxSrthV3IxkQIMpxczoLIbHw5XsQ/edit?usp=sharing'

df = pd.read_csv(data)

st.table(data=df)