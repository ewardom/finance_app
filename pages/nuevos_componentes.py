import streamlit as st
import streamlit_antd_components as sac
from st_ant_statistic import st_ant_statistic
import pandas as pd

st.set_page_config(
    page_title="Transacciones",
    page_icon="🧾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Crear tabs y obtener el tab seleccionado
selected_tab = sac.tabs([
    sac.TabsItem(label='Apple', tag="10"),
    sac.TabsItem(label='Google', icon='google'),
    sac.TabsItem(label='GitHub', icon='github'),
    sac.TabsItem(label='Disabled', disabled=True),
], align='center')

# Mostrar el tab seleccionado
st.write(f"Seleccionaste: {selected_tab}")

# Asignar acciones según el tab seleccionado
if selected_tab == "Apple":
    st.success("Seleccionaste Apple 🍏")
elif selected_tab == "Google":
    st.info("Seleccionaste Google 🔍")
elif selected_tab == "GitHub":
    st.warning("Seleccionaste GitHub 🐙")

# Crear DataFrame de muestra
data = {
    "Cuenta": ["Plata", "AMEX", "BBVA", "Simplicity", "Costco"],
    "Balance": [1200.50, 3450.75, 980.20, 2540.00, 620.80],
}
df = pd.DataFrame(data)

st.title("💰 Lista de Cuentas")

# Mostrar cada cuenta con su balance y un botón de detalles
for index, row in df.iterrows():
    col1, col2, col3= st.columns([3, 1, 1])  # División: 3/4 para la info y 1/4 para el botón

    with col1:
        st_ant_statistic(
            title=row["Cuenta"],
            value=row["Balance"],
            prefix="<i class='fa fa-money' aria-hidden='true'></i>",
            precision=2,
            loadingAnimation=True,
            loadingDuration=1,
            decimalSeperator=",",
            key=f"ant_statistic_{index}",
        )

    with col2:
        if st.button("Ver detalles", key=f"button_{index}"):
            st.session_state["selected_account"] = row["Cuenta"]
            st.session_state["selected_balance"] = row["Balance"]

# Mostrar detalles si se ha seleccionado una cuenta
if "selected_account" in st.session_state:
    st.subheader(f"Detalles de {st.session_state['selected_account']}")
    st.write(f"**Balance:** ${st.session_state['selected_balance']:,.2f}")