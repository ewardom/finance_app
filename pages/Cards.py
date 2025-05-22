import streamlit as st
import pandas as pd
import streamlit_antd_components as sac

# Datos de ejemplo para cuentas
data = [
    {"logo": "🔵", "title": "Cuenta 1", "balance": "$1,200"},
    {"logo": "🟢", "title": "Cuenta 2", "balance": "$2,500"},
    {"logo": "🟠", "title": "Cuenta 3", "balance": "$3,750"},
    {"logo": "🟣", "title": "Cuenta 4", "balance": "$4,820"},
    {"logo": "🔴", "title": "Cuenta 5", "balance": "$5,940"},
    {"logo": "🟡", "title": "Cuenta 6", "balance": "$6,100"},
    {"logo": "🔷", "title": "Cuenta 7", "balance": "$7,350"},
    {"logo": "🔶", "title": "Cuenta 8", "balance": "$8,720"},
]

# Datos para el DataFrame
df = pd.DataFrame([
    ["Cuenta 1", "Ingreso", 1200, "Salario"],
    ["Cuenta 2", "Gasto", -500, "Renta"],
    ["Cuenta 3", "Ingreso", 3750, "Freelance"],
    ["Cuenta 4", "Gasto", -100, "Comida"],
    ["Cuenta 5", "Ingreso", 5940, "Proyecto"],
    ["Cuenta 6", "Gasto", -200, "Transporte"]
], columns=["Cuenta", "Tipo", "Monto", "Descripción"])

# Inicializar el índice de la página en la sesión
if "page_index" not in st.session_state:
    st.session_state.page_index = 0

# Paginación
items_per_page = 3
total_pages = (len(data) - 1) // items_per_page + 1

col1, col2, col3, col4, col5 = st.columns([1, 2, 6, 2, 1])

# Botón de retroceso
with col1:
    if st.button("◀", key="prev") and st.session_state.page_index > 0:
        st.session_state.page_index -= 1

# Título en el centro
with col3:
    st.markdown("### 📑 Cuentas")

# Botón de avance
with col5:
    if st.button("▶", key="next") and st.session_state.page_index < total_pages - 1:
        st.session_state.page_index += 1

# Obtener las cuentas visibles en la página actual
start_idx = st.session_state.page_index * items_per_page
end_idx = start_idx + items_per_page
visible_accounts = data[start_idx:end_idx]

# Estilos CSS mejorados para que el contenido se mantenga dentro de las tarjetas
st.markdown("""
    <style>
        .card {
            border: 2px solid #ddd;
            border-radius: 10px;
            padding: 15px;
            background-color: #2a2a2a;
            text-align: center;
            height: 140px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        .title {
            font-size: 20px;
            font-weight: bold;
            color: white;
        }
        .balance {
            font-size: 16px;
            color: #cfcfcf;
        }
    </style>
""", unsafe_allow_html=True)

# Mostrar las cuentas en una fila de 3 columnas
columns = st.columns(3)
for col, account in zip(columns, visible_accounts):
    with col:
        st.markdown(
            f"""
            <div class="card">
                <div style="font-size: 30px;">{account['logo']}</div>
                <div class="title">{account['title']}</div>
                <div class="balance">💰 {account['balance']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        # Botón "Ver" FUERA de la tarjeta
        if st.button("Filtrar", key=f"ver_{account['title']}"):
            st.success(f"Seleccionaste {account['title']}")

# Tabla de movimientos debajo

sac.divider(icon=sac.BsIcon(name='credit-card', size=20), align='center', color='gray')
st.markdown("### 📊 Movimientos de cuentas")
st.dataframe(df, use_container_width=True)