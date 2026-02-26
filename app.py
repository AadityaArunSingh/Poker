import streamlit as str
import pandas as pd

data = 'https://docs.google.com/spreadsheets/d/1N0f0momimoEEWxqmxSrthV3IxkQIMpxczoLIbHw5XsQ/edit?usp=sharing'

df = pd.read_csv(data)

str.table(data=df, border=True)