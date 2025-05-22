import streamlit as st
import pandas as pd
from streamlit_card import card

#st.title("Transacciones")
archivo_csv = "transacciones.csv"

st.set_page_config(
    page_title="Transacciones",
    page_icon="🧾",
    layout="wide",
    initial_sidebar_state="expanded",
)

df = pd.read_csv(archivo_csv)
st.dataframe(df)