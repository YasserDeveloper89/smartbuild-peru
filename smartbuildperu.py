import streamlit as st
from fpdf import FPDF
import datetime

st.set_page_config(page_title="SmartBuild Perú", layout="centered")

st.title("SmartBuild Perú - Estimación de Presupuesto")

# Datos de entrada
ubicacion = st.selectbox("Ubicación", ["Lima"])
zona = st.selectbox("Zona o distrito", ["Miraflores", "San Isidro", "San Borja", "Comas", "Villa El Salvador", "Surco", "La Molina", "Ate", "Centro de Lima"])

tipo_construccion = st.selectbox("Tipo de construcción", [
    "Vivienda unifamiliar",
    "Edificio multifamiliar",
    "Local comercial",
    "Oficina",
    "Almacén"
])

area = st.number_input("Área del terreno (m²)", min_value=10.0, max_value=1000.0, value=100.0, step=10.0)
pisos = st.number_input("Cantidad de pisos", min_value=1, max_value=10, value=1)
acabado = st.selectbox("Tipo de acabado", ["Económico", "Estándar", "Premium"])

# Costos base referenciales por zona (S/ por m²)
costos_zona = {
    "Miraflores": 1200,
    "San Isidro": 1300,
    "San Borja": 1100,
    "Surco": 1000,
    "La Molina": 950,
    "Ate": 800,
    "Centro de Lima": 900,
    "Comas": 700,
    "Villa El Salvador": 680
}

multiplicador = {"Económico": 1.0, "Estándar": 1.25, "Premium": 1.5}

if st.button("Calcular presupuesto"):

    costo_m2 = costos_zona[zona] * multiplicador[acabado]
    total = costo_m2 * area * pisos

    # Estimación materiales
    cemento = round(area * pisos * 0.2, 1)     # bolsas
    arena = round(area * pisos * 0.15, 1)      # m³
    fierro = round(area * pisos * 10, 1)       # kg
    ladrillo = round(area * pisos * 120, 1)    # unidades

    # Duración estimada (simplificada)
    meses = round((area * pisos) / 300, 1)
    if meses < 1:
        duracion_texto = "menos de 1 mes"
    else:
        duracion_texto = f"{meses} meses"

    st.success(f"Presupuesto estimado: S/ {total:,.2f}")
    st.markdown(f"**Duración estimada de la obra:** {duracion_texto}")
    
    st.subheader("Materiales estimados")
    st.write(f"- Cemento: {cemento} bolsas")
    st.write(f"- Arena: {arena} m³")
    st.write(f"- Fierro: {fierro} kg")
    st.write(f"- Ladrillo: {ladrillo} unidades")

    # Generar PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, "Presupuesto de Construcción - SmartBuild Perú", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, f"Fecha: {datetime.datetime.now().strftime('%d/%m/%Y')}", ln=True)
    pdf.cell(200, 10, f"Ubicación: {ubicacion} - {zona}", ln=True)
    pdf.cell(200, 10, f"Tipo de construcción: {tipo_construccion}", ln=True)
    pdf.cell(200, 10, f"Área: {area} m²", ln=True)
    pdf.cell(200, 10, f"Pisos: {pisos}", ln=True)
    pdf.cell(200, 10, f"Acabado: {acabado}", ln=True)
    pdf.cell(200, 10, f"Duración estimada: {duracion_texto}", ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, f"Presupuesto estimado: S/ {total:,.2f}", ln=True)
    pdf.ln(10)
    pdf.cell(200, 10, "Materiales estimados:", ln=True)
    pdf.cell(200, 10, f"- Cemento: {cemento} bolsas", ln=True)
    pdf.cell(200, 10, f"- Arena: {arena} m³", ln=True)
    pdf.cell(200, 10, f"- Fierro: {fierro} kg", ln=True)
    pdf.cell(200, 10, f"- Ladrillo: {ladrillo} unidades", ln=True)

    # Convertir PDF a bytes
    pdf_bytes = pdf.output(dest='S').encode('latin1')

    st.download_button(
        label="Descargar presupuesto en PDF",
        data=pdf_bytes,
        file_name="presupuesto_smartbuild.pdf",
        mime="application/pdf"
)
