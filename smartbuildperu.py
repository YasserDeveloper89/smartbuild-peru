import streamlit as st
from fpdf import FPDF
import io

st.set_page_config(page_title="SmartBuild Perú", layout="centered")
st.title("SmartBuild Perú - Calculadora de Presupuesto")

if "historial" not in st.session_state:
    st.session_state.historial = []

st.subheader("Datos del proyecto")

ubicacion = st.selectbox("Ubicación del terreno", ["Lima", "Cusco", "Arequipa", "Trujillo"])
area = st.number_input("Área del terreno (m²)", min_value=10.0, max_value=1000.0, step=1.0)
acabado = st.selectbox("Tipo de acabado", ["Económico", "Estándar", "Premium"])
pisos = st.slider("Número de pisos", min_value=1, max_value=5)

precios_m2 = {
    "Económico": 450,
    "Estándar": 700,
    "Premium": 1100
}

materiales_base = {
    "Arena (m³)": 0.05,
    "Cemento (bolsas)": 0.5,
    "Ladrillo (unidades)": 30,
    "Hierro (kg)": 5
}

if st.button("Calcular presupuesto"):
    precio_m2 = precios_m2[acabado]
    costo_total = precio_m2 * area * pisos
    materiales = {mat: round(cantidad * area * pisos, 2) for mat, cantidad in materiales_base.items()}

    st.success(f"Presupuesto estimado: S/ {costo_total:,.2f}")
    st.subheader("Materiales estimados")
    for mat, cant in materiales.items():
        st.write(f"- {mat}: {cant}")

    # Guardar historial
    st.session_state.historial.append((ubicacion, area, acabado, pisos, costo_total))

    # Crear PDF en memoria
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "SmartBuild Perú - Presupuesto", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, f"Ubicación: {ubicacion}", ln=True)
    pdf.cell(200, 10, f"Área: {area} m²", ln=True)
    pdf.cell(200, 10, f"Acabado: {acabado}", ln=True)
    pdf.cell(200, 10, f"Pisos: {pisos}", ln=True)
    pdf.cell(200, 10, f"Costo Total: S/ {costo_total:,.2f}", ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, "Materiales estimados:", ln=True)
    for mat, cant in materiales.items():
        pdf.cell(200, 10, f"- {mat}: {cant}", ln=True)

    pdf_buffer = io.BytesIO()
    pdf.output(pdf_buffer)
    st.download_button(
        label="Descargar PDF",
        data=pdf_buffer.getvalue(),
        file_name="presupuesto_smartbuild.pdf",
        mime="application/pdf"
    )

# Mostrar historial
if st.session_state.historial:
    st.subheader("Historial de presupuestos")
    for i, item in enumerate(st.session_state.historial, 1):
        ubic, ar, ac, pi, costo = item
        st.text(f"{i}. {ubic} | {ar} m² | {ac} | {pi} pisos => S/ {costo:,.2f}")
