
import streamlit as st
import pandas as pd
import datetime

# Configuración inicial
st.set_page_config(page_title="SmartBuild Perú - Pro", layout="wide")

# --- Sidebar ---
st.sidebar.title("SmartBuild Pro")
st.sidebar.markdown("Versión Profesional - Estimador de Obras")

menu = st.sidebar.radio("Menú", ["Inicio", "Estimación", "Reporte", "Acerca de"])

# --- Funciones auxiliares ---
def calcular_estimacion(area, tipo_obra, materiales):
    base = 300 if tipo_obra == "Residencial" else 500
    mat_factor = 1.2 if materiales == "Premium" else 1
    return area * base * mat_factor

def generar_resumen(area, tipo_obra, materiales, total):
    return f"""
    Estimación de Construcción
    ---------------------------
    Tipo de Obra: {tipo_obra}
    Calidad de Materiales: {materiales}

    Área estimada: {area} m2
    Costo estimado total: S/. {total:,.2f}
    Fecha: {datetime.date.today()}
    """

# --- Inicio ---
if menu == "Inicio":
    st.title("SmartBuild Perú - Versión Pro")
    st.markdown("Estimador profesional de costos de construcción para el mercado peruano.")
    st.image("https://i.imgur.com/FE5ZpWQ.png", width=800)

# --- Estimación ---
elif menu == "Estimación":
    st.title("Estimación de Proyecto")
    col1, col2 = st.columns(2)

    with col1:
        area = st.number_input("Área construida (m2)", min_value=10, max_value=1000, value=100)
        tipo_obra = st.selectbox("Tipo de obra", ["Residencial", "Comercial"])
        materiales = st.selectbox("Calidad de materiales", ["Económico", "Premium"])

    total = calcular_estimacion(area, tipo_obra, materiales)

    st.subheader(f"Costo estimado: S/. {total:,.2f}")

    if st.button("Generar Resumen"):
        resumen = generar_resumen(area, tipo_obra, materiales, total)
        st.text_area("Resumen para exportar o copiar", resumen, height=250)

# --- Reporte ---
elif menu == "Reporte":
    st.title("Historial de estimaciones")
    st.info("En la versión gratuita, esta funcionalidad está desactivada.")

# --- Acerca de ---
elif menu == "Acerca de":
    st.title("Acerca del proyecto")
    st.markdown("""
    **SmartBuild Perú** es una herramienta creada para facilitar la planificación de proyectos de construcción
    en Perú. Inspirada por el trabajo de empresas como Build-Tech y ADR Technology.

    Diseñada para constructores, inversores y arquitectos que quieren una herramienta gratuita, visual y escalable.
    """)
