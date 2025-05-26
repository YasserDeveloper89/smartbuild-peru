import streamlit as st
from fpdf import FPDF
from io import BytesIO

st.set_page_config(page_title="SmartBuild Perú PRO", layout="centered")

st.title("SmartBuild Perú - Calculadora Profesional de Presupuesto")

# Opciones de entrada
ubicacion = st.selectbox("Ubicación del proyecto", ["Lima", "Arequipa", "Cusco", "Trujillo", "Piura"])
area = st.number_input("Área del terreno (m²)", min_value=10.0, step=1.0)
pisos = st.slider("Número de pisos", min_value=1, max_value=5, value=1)
acabado = st.selectbox("Tipo de acabado", ["Económico", "Estándar", "Premium"])

# Costos base por m² según tipo de acabado
costos_base = {
    "Económico": 350,
    "Estándar": 550,
    "Premium": 800
}

materiales = {
    "Cemento (bolsas)": 0.2 * area * pisos,
    "Arena (m³)": 0.1 * area * pisos,
    "Fierro (kg)": 5 * area * pisos,
    "Ladrillos (unidades)": 130 * area * pisos,
    "Mano de obra (S/)": 150 * area * pisos
}

costo_total = costos_base[acabado] * area * pisos

if st.button("Calcular presupuesto"):
    st.subheader("Resumen del presupuesto")
    st.markdown(f"- **Ubicación:** {ubicacion}")
    st.markdown(f"- **Área:** {area} m²")
    st.markdown(f"- **Pisos:** {pisos}")
    st.markdown(f"- **Tipo de acabado:** {acabado}")
    st.markdown(f"- **Costo estimado total:** S/ {costo_total:,.2f}")

    st.subheader("Materiales estimados")
    for mat, cantidad in materiales.items():
        unidad = "S/" if "Mano de obra" in mat else ""
        st.markdown(f"- {mat}: {unidad}{cantidad:,.2f}")

    # Crear PDF en memoria
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Presupuesto de Construcción - SmartBuild Perú", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.ln(5)
    pdf.cell(0, 10, f"Ubicación: {ubicacion}", ln=True)
    pdf.cell(0, 10, f"Área: {area} m²", ln=True)
    pdf.cell(0, 10, f"Pisos: {pisos}", ln=True)
    pdf.cell(0, 10, f"Tipo de acabado: {acabado}", ln=True)
    pdf.cell(0, 10, f"Costo estimado total: S/ {costo_total:,.2f}", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Materiales estimados", ln=True)
    pdf.set_font("Arial", size=12)
    for mat, cantidad in materiales.items():
        unidad = "S/" if "Mano de obra" in mat else ""
        pdf.cell(0, 10, f"{mat}: {unidad}{cantidad:,.2f}", ln=True)

    # Guardar en memoria para descarga
    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)

    st.download_button(
        label="Descargar PDF del presupuesto",
        data=pdf_buffer,
        file_name="presupuesto_smartbuild_peru.pdf",
        mime="application/pdf"
    )
