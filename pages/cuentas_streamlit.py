import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Cuentas",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

archivo_csv = "transacciones.csv"
df_transacciones = pd.read_csv(
    archivo_csv, 
    dtype={"Cuenta": "string", "Descripción": "string"}, 
    parse_dates=["Fecha"]
)
df_transacciones["Fecha"] = pd.to_datetime(df_transacciones["Fecha"])

cuentas = ["Todas las cuentas"] + list(df_transacciones["Cuenta"].unique())

if "cuenta_seleccionada" not in st.session_state:
    st.session_state["cuenta_seleccionada"] = "Todas las cuentas"

def get_balance(cuenta):
    if cuenta == "Todas las cuentas":
        return df_transacciones["Cantidad"].sum()
    else:
        return df_transacciones.loc[df_transacciones["Cuenta"] == cuenta, "Cantidad"].sum()

col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("Cuentas")
    for cuenta in cuentas:
        balance = get_balance(cuenta)
        label = f"💰 {cuenta} ({balance})"
        if st.button(label):
            st.session_state["cuenta_seleccionada"] = cuenta

with col2:
    selected = st.session_state["cuenta_seleccionada"]
    st.subheader(f"Transacciones de {selected} (Balance: {get_balance(selected)})")
    
    with st.expander("🔍 Filtros avanzados"):
        min_fecha, max_fecha = df_transacciones["Fecha"].min(), df_transacciones["Fecha"].max()
        fecha_inicio, fecha_fin = st.date_input(
            "📅 Rango de fechas", 
            [min_fecha.date(), max_fecha.date()], 
            min_value=min_fecha.date(), 
            max_value=max_fecha.date()
        )
        busqueda = st.text_input("🔎 Buscar en la descripción", "")
    
    fecha_inicio = pd.to_datetime(fecha_inicio)
    fecha_fin = pd.to_datetime(fecha_fin)
    
    if selected == "Todas las cuentas":
        df_filtrado = df_transacciones
    else:
        df_filtrado = df_transacciones[df_transacciones["Cuenta"] == selected]
    
    df_filtrado = df_filtrado[
        (df_filtrado["Fecha"] >= fecha_inicio) & 
        (df_filtrado["Fecha"] <= fecha_fin)
    ]
    
    if busqueda:
        df_filtrado = df_filtrado[df_filtrado["Descripción"].str.contains(busqueda, case=False, na=False)]
    
    st.dataframe(df_filtrado, hide_index=True)
