import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Cuentas Configuración",
    page_icon="🧾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Definir la ruta del archivo CSV
csv_file = "cuentas.csv"

# Columnas del modelo de datos
columns = ["nombre", "tipo", "limite_credito", "dia_pago", "dia_corte_inicio", "dia_corte_fin", "icono"]

# Si el archivo no existe, lo creamos con datos de ejemplo
if not os.path.exists(csv_file):
    data = {
        "nombre": ["Tarjeta de Crédito", "Cuenta de Débito", "Efectivo"],
        "tipo": ["Crédito", "Débito", "Efectivo"],
        "limite_credito": [5000, None, None],
        "dia_pago": [25, None, None],
        "dia_corte_inicio": [10, None, None],
        "dia_corte_fin": [15, None, None],
        "icono": ["<i class='fa fa-credit-card'></i>", "<i class='fa fa-university'></i>", "<i class='fa fa-money'></i>"]
    }
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(csv_file, index=False)
else:
    df = pd.read_csv(csv_file)

st.title("Configuración de Cuentas")

# Mostrar las cuentas actuales
st.subheader("Cuentas actuales")
st.dataframe(df)

# Formulario para agregar o editar una cuenta
st.subheader("Agregar/Editar Cuenta")
with st.form("cuenta_form"):
    nombre = st.text_input("Nombre de la cuenta")
    tipo = st.selectbox("Tipo de cuenta", ["Crédito", "Débito", "Efectivo"])
    
    # Para cuentas de crédito se muestran campos adicionales
    limite_credito = None
    dia_pago = None
    dia_corte_inicio = None
    dia_corte_fin = None
    if tipo == "Crédito":
        limite_credito = st.number_input("Límite de crédito", min_value=0, value=1000)
        dia_pago = st.number_input("Día de pago", min_value=1, max_value=31, value=25)
        dia_corte_inicio = st.number_input("Día de corte (inicio)", min_value=1, max_value=31, value=10)
        dia_corte_fin = st.number_input("Día de corte (fin)", min_value=1, max_value=31, value=15)
        
    icono = st.text_input("Icono (HTML o emoji)", value="💳")
    
    submitted = st.form_submit_button("Guardar")
    if submitted:
        # Crear el diccionario con los datos ingresados
        new_row = {
            "nombre": nombre,
            "tipo": tipo,
            "limite_credito": limite_credito,
            "dia_pago": dia_pago,
            "dia_corte_inicio": dia_corte_inicio,
            "dia_corte_fin": dia_corte_fin,
            "icono": icono,
        }
        # Agregar la nueva cuenta al DataFrame usando loc
        df.loc[len(df)] = new_row
        # Guardar el DataFrame actualizado en el CSV
        df.to_csv(csv_file, index=False)
        st.success("Cuenta guardada exitosamente!")
        st.rerun()
