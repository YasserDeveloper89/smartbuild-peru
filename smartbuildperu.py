
import streamlit as st
from fpdf import FPDF

st.set_page_config(page_title="SmartBuild Pro", layout="centered")

# --- Encabezado ---
st.title("SmartBuild Perú - Versión Pro Final")
st.markdown("Calculadora profesional de materiales y costos para obras")

# --- Datos de entrada ---
ubicaciones = {
    "Lima": 1200,
    "Arequipa": 1000,
    "Cusco": 950,
    "Trujillo": 1050
}

acabados = {
    "Básico": 1.0,
    "Intermedio": 1.2,
    "Premium": 1.5
}

st.header("Parámetros del Proyecto")
ubicacion = st.selectbox("Ubicación del proyecto", list(ubicaciones.keys()))
area = st.number_input("Área del proyecto (m²)", min_value=10.0, max_value=1000.0, value=100.0, step=10.0)
acabado = st.selectbox("Nivel de acabado", list(acabados.keys()))
pisos = st.slider("Número de pisos", 1, 5, 1)

# --- Cálculo de materiales estimados ---
def calcular_materiales(area_total):
    materiales = {
        "Cemento (bolsas)": round(area_total * 0.2, 2),  # aprox 0.2 bolsas por m²
        "Arena (m³)": round(area_total * 0.05, 2),
        "Grava (m³)": round(area_total * 0.04, 2),
        "Ladrillos (unidades)": round(area_total * 55),  # 55 ladrillos por m²
        "Acero (kg)": round(area_total * 7.5, 2)
    }
    return materiales

if "historial" not in st.session_state:
    st.session_state.historial = []

if st.button("Calcular presupuesto"):
    costo_base = ubicaciones[ubicacion]
    factor_acabado = acabados[acabado]
    area_total = area * pisos
    costo_total = costo_base * area_total * factor_acabado

    materiales = calcular_materiales(area_total)

    st.subheader("Resumen del proyecto")
    st.markdown(f"**Ubicación:** {ubicacion}")
    st.markdown(f"**Área total:** {area_total} m²")
    st.markdown(f"**Nivel de acabado:** {acabado}")
    st.markdown(f"**Pisos:** {pisos}")
    st.markdown(f"**Costo estimado:** S/. {costo_total:,.2f}")

    st.subheader("Materiales estimados:")
    for mat, cant in materiales.items():
        st.markdown(f"- {mat}: {cant}")

    st.session_state.historial.append((ubicacion, area, acabado, pisos, costo_total))

    # Exportar PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Resumen del Proyecto SmartBuild", ln=True, align="C")
    pdf.cell(200, 10, txt=f"Ubicación: {ubicacion}", ln=True)
    pdf.cell(200, 10, txt=f"Área Total: {area_total} m²", ln=True)
    pdf.cell(200, 10, txt=f"Acabado: {acabado}", ln=True)
    pdf.cell(200, 10, txt=f"Pisos: {pisos}", ln=True)
    pdf.cell(200, 10, txt=f"Costo Total: S/. {costo_total:,.2f}", ln=True)
    pdf.cell(200, 10, txt="Materiales estimados:", ln=True)
    for mat, cant in materiales.items():
        pdf.cell(200, 10, txt=f"- {mat}: {cant}", ln=True)

    pdf.output("/mnt/data/SmartBuild_Presupuesto.pdf")
    st.success("PDF generado exitosamente.")
    st.markdown("[Descargar PDF](sandbox:/mnt/data/SmartBuild_Presupuesto.pdf)", unsafe_allow_html=True)

# --- Historial ---
if st.session_state.historial:
    st.subheader("Historial de presupuestos")
    for i, h in enumerate(st.session_state.historial[::-1]):
        st.markdown(f"{i+1}. {h}")
