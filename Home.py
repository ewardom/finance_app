import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import os
import streamlit_antd_components as sac
import time
import plotly.express as px
import numpy as np
#df = pd.read_excel("MoneyCoach.xlsx")

st.set_page_config(
    page_title="Registro",
    page_icon="💲",
    layout="wide",
    initial_sidebar_state="auto",
)

def main():
    # Archivo donde se guardarán los datos
    transacciones_csv = "transacciones.csv"

    # Título de la app
    st.title("💰 Registro de movimientos")

    # Definir categorías dinámicamente
    categorias_gasto = ["Alimentación", "Transporte", "Entretenimiento", "Salud", "Otros"]
    categorias_ingreso = ["Salario", "Inversiones", "Regalos", "Ventas", "Otros"]
    cuentas = ["Plata", "Amex", "BBVA"]
    cuenta = cuentas
    # Selector de tipo de movimiento con `segmented_control`
    with st.expander('Registrar movimiento', icon=":material/add_circle:"): 
        tipo_movimiento = sac.segmented(
            items=[
                sac.SegmentedItem(icon=sac.AntIcon(name='MinusCircleOutlined', size=25)),
                sac.SegmentedItem(icon=sac.AntIcon(name='PlusCircleOutlined', size=25)),
                sac.SegmentedItem(icon=sac.AntIcon(name='RetweetOutlined', size=25)),
            ], index=0, align='center', disabled=False, return_index=True, use_container_width=True, divider=False,
        )
        # 🌟 Aquí comienza el formulario
        with st.form(key="form_movimiento", clear_on_submit=True):
            col_fecha_1, col_fecha_2, = st.columns([1,1])
            col_cat_1, col_cat_2, = st.columns([1,1])
            # Campos comunescols=st.columns(3)
            with col_fecha_1:
                fecha = st.date_input("Fecha del movimiento", format="DD/MM/YYYY",)
            with col_fecha_2:
                hora = st.time_input("Hora del movimiento")
            cantidad = st.number_input("Cantidad ($)", min_value=0.0, value=None, format="%.2f", placeholder="$ 0.00", step=1.00)
            cuenta = st.selectbox("Cuenta", cuenta)

            # Campos específicos según el tipo de movimiento
            if tipo_movimiento == 0:
                tipo_movimiento='Gasto'
                categoria = st.selectbox("Categoría", categorias_gasto)
                subcategoria = st.text_input("Subcategoría (opcional)")
                descripcion = st.text_area("Descripción")

            elif tipo_movimiento == 1:
                tipo_movimiento='Ingreso'
                with col_cat_1:
                    categoria = st.selectbox("Categoría", categorias_ingreso)
                with col_cat_2:
                    subcategoria = st.text_input("Subcategoría (opcional)")
                descripcion = st.text_area("Descripción")

            elif tipo_movimiento == 2:
                tipo_movimiento='Transferencia'
                sac.divider(icon=sac.AntIcon(name='RetweetOutlined', size=20), align='center', color='gray', size='xs')
                cuenta_destino = st.selectbox("Cuenta destino", cuentas)

            # Botón para guardar el movimiento (solo se ejecuta al hacer clic)
            submit = st.form_submit_button("Guardar movimiento")

    # ✅ Guardar los datos solo si el usuario presiona "Guardar movimiento"
    if submit:
        nuevo_movimiento = {
            "Fecha": [fecha],
            "Hora": [hora],
            "Cuenta": [cuenta],
            "Cantidad": [cantidad],
            "Tipo de Movimiento": [tipo_movimiento]
        }

        if tipo_movimiento in ["Gasto", "Ingreso"]:
            nuevo_movimiento["Categoría"] = [categoria]
            nuevo_movimiento["Subcategoría"] = [subcategoria]
            nuevo_movimiento["Descripción"] = [descripcion]
            df_nuevo = pd.DataFrame(nuevo_movimiento)

            # Verifica si el archivo existe y lo actualiza
            if os.path.exists(transacciones_csv):
                df = pd.read_csv(transacciones_csv)
                df = pd.concat([df, df_nuevo], ignore_index=True)
            else:
                df = df_nuevo

            df.to_csv(transacciones_csv, index=False)
            st.success("✅ Movimiento guardado exitosamente")

        elif tipo_movimiento == "Transferencia":
            if cuenta == cuenta_destino:
                st.error("❌ La cuenta origen es igual a la cuenta destino.")
            else:
                nuevo_movimiento["Cuenta Destino"] = [cuenta_destino]

                df_nuevo = pd.DataFrame(nuevo_movimiento)

                # Verifica si el archivo existe y lo actualiza
                if os.path.exists(transacciones_csv):
                    df = pd.read_csv(transacciones_csv)
                    df = pd.concat([df, df_nuevo], ignore_index=True)
                else:
                    df = df_nuevo

                df.to_csv(transacciones_csv, index=False)
                st.success("✅ Movimiento guardado exitosamente")

    df = pd.read_csv(transacciones_csv)
    
    columnas=st.columns([3,3,3,4])
    gastos = df[df['Tipo de Movimiento']=='Gasto']
    totalGastos=df[df['Tipo de Movimiento']=='Gasto']['Cantidad'].sum()
    totalIngresos=df[df['Tipo de Movimiento']=='Ingreso']['Cantidad'].sum()
    balanceTotal = totalIngresos - totalGastos

    with columnas[0]:
        st.metric('Gastos',f'{totalGastos:,.2f}', border=True) 
    with columnas[1]:
        st.metric('Ingresos',f'{totalIngresos:,.2f}', border=True) 
    with columnas[2]:
        st.metric('Balance',f'{balanceTotal:,.2f}', border=True) 
    
    with st.container():
        # Crear gráfico sunburst
        fig = px.sunburst(
            gastos,
            path=["Tipo de Movimiento", "Categoría", "Subcategoría"],
            values="Cantidad",
            title="Distribución de Gastos por Categoría y Subcategoría"
        )

        # Mostrar en Streamlit
        st.title("Gráfico de Gastos (Sunburst)")
        st.plotly_chart(fig, use_container_width=True)


    # Mostrar historial de movimientos
    st.header("Historial de Movimientos")
    if os.path.exists(transacciones_csv):
        df_movimientos = pd.read_csv(transacciones_csv)
        st.data_editor(df_movimientos, num_rows="dynamic")
    else:
        st.info("Aún no hay movimientos registrados.")        


if __name__== '__main__':
    main()