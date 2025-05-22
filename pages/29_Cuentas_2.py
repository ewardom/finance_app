import streamlit as st
import pandas as pd
from streamlit_card import card

st.set_page_config(
    page_title="Cuentas",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

import pandas as pd

# Estilos CSS
st.markdown("""
    <style>
        .card {
            display: flex;
            align-items: center;
            background-color: #ffffff;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
            border: 2px solid #ddd;
        }
        .logo {
            font-size: 30px;
            margin-right: 15px;
        }
        .info {
            flex-grow: 1;
        }
        .monto {
            font-weight: bold;
            text-align: right;
            font-size: 18px;
        }
    </style>
""", unsafe_allow_html=True)

# Datos de cuentas
cuentas = [
    {"logo": "🏦", "titulo": "Cuenta Bancaria", "monto": 1500.50},
    {"logo": "💳", "titulo": "Tarjeta de Crédito", "monto": -500.75},
    {"logo": "💰", "titulo": "Efectivo", "monto": 300.00},
]

# Datos de transacciones (ejemplo)
transacciones = pd.DataFrame([
    {"Cuenta": "Cuenta Bancaria", "Fecha": "2024-02-01", "Descripción": "Pago de luz", "Monto": -100.0},
    {"Cuenta": "Cuenta Bancaria", "Fecha": "2024-02-03", "Descripción": "Salario", "Monto": 2000.0},
    {"Cuenta": "Tarjeta de Crédito", "Fecha": "2024-02-05", "Descripción": "Compra en Amazon", "Monto": -300.0},
    {"Cuenta": "Tarjeta de Crédito", "Fecha": "2024-02-07", "Descripción": "Pago tarjeta", "Monto": 500.0},
    {"Cuenta": "Efectivo", "Fecha": "2024-02-10", "Descripción": "Cena", "Monto": -50.0},
])

# Dividir en dos columnas
col1, col2 = st.columns([1, 2])  # Ajusta la proporción según prefieras

# Columna Izquierda: Cards de Cuentas
with col1:
    st.subheader("Cuentas")
    cuenta_seleccionada = None  # Inicializar variable

    for cuenta in cuentas:
        # Crear la card con bordes
        card_html = f"""
            <div class="card" onclick="document.getElementById('{cuenta['titulo']}').click();">
                <div class="logo">{cuenta['logo']}</div>
                <div class="info">
                    <strong>{cuenta['titulo']}</strong>
                </div>
                <div class="monto">${cuenta['monto']:,.2f}</div>
            </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
        # Crear botón oculto para manejar la selección
        if st.button(f"Seleccionar {cuenta['titulo']}", key=cuenta["titulo"]):
            cuenta_seleccionada = cuenta["titulo"]

# Columna Derecha: Tabla de Transacciones Filtradas
with col2:
    st.subheader("Transacciones")
    
    if cuenta_seleccionada:
        st.write(f"Mostrando transacciones de: **{cuenta_seleccionada}**")
        df_filtrado = transacciones[transacciones["Cuenta"] == cuenta_seleccionada]
        st.dataframe(df_filtrado, hide_index=True)
    else:
        st.info("Selecciona una cuenta para ver las transacciones.")
