import streamlit as st
import pandas as pd

# Estilos CSS mejorados
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
            cursor: pointer;
            transition: all 0.3s ease-in-out;
        }
        .card:hover {
            border-color: #007BFF;
            box-shadow: 4px 4px 10px rgba(0,123,255,0.2);
            transform: scale(1.02);
        }
        .selected {
            border-color: #007BFF !important;
            background-color: rgba(0,123,255,0.1);
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

# Inicializar el estado de la cuenta seleccionada
if "cuenta_seleccionada" not in st.session_state:
    st.session_state.cuenta_seleccionada = None

# Dividir en dos columnas
col1, col2 = st.columns([1, 2])  # Ajusta el tamaño de las columnas

# Columna Izquierda: Cards de Cuentas
with col1:
    st.subheader("Cuentas")

    for cuenta in cuentas:
        cuenta_id = cuenta["titulo"]

        # Resaltar si la cuenta está seleccionada
        selected_class = "selected" if st.session_state.cuenta_seleccionada == cuenta_id else ""

        # Crear la card con estilos
        card_html = f"""
            <div class="card {selected_class}" onclick="window.location.href='?selected={cuenta_id}'">
                <div class="logo">{cuenta['logo']}</div>
                <div class="info">
                    <strong>{cuenta['titulo']}</strong>
                </div>
                <div class="monto">${cuenta['monto']:,.2f}</div>
            </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

        # Capturar el clic en la card
        if st.query_params.get("selected") == cuenta_id:
            st.session_state.cuenta_seleccionada = cuenta_id

# Columna Derecha: Tabla de Transacciones Filtradas
with col2:
    st.subheader("Transacciones")
    
    if st.session_state.cuenta_seleccionada:
        st.write(f"Mostrando transacciones de: **{st.session_state.cuenta_seleccionada}**")
        df_filtrado = transacciones[transacciones["Cuenta"] == st.session_state.cuenta_seleccionada]
        st.dataframe(df_filtrado, hide_index=True)
    else:
        st.info("Selecciona una cuenta para ver las transacciones.")