import streamlit as st
from fpdf import FPDF
import datetime

# Configuración de la página
st.set_page_config(page_title="SmartBuild Perú", layout="centered")

st.title("SmartBuild Perú - Estimación de Presupuesto")

# Base de datos de zonas con precios por m² (aproximados y personalizables)
zonas = {
    "Lima - Miraflores": 1300,
    "Lima - San Isidro": 1350,
    "Lima - San Borja": 1250,
    "Lima - Surco": 1200,
    "Lima - La Molina": 1150,
    "Lima - Jesús María": 1100,
    "Lima - Pueblo Libre": 1000,
    "Lima - Comas": 850,
    "Lima - Villa El Salvador": 800,
    "Lima - Ate": 900,
    "Arequipa - Cayma": 950,
    "Cusco - Centro": 900,
    "Trujillo - Urb. Primavera": 870,
    "Otro": 800
}

acabados = {
    "Económico": 1.0,
    "Estándar": 1.3,
    "Premium": 1.7
}

tipos_construccion = [
    "Vivienda unifamiliar",
    "Edificio multifamiliar",
    "Local comercial",
    "Oficina",
    "Almacén"
]

# Inputs
zona = st.selectbox("Zona / Distrito", list(zonas.keys()))
tipo_construccion = st.selectbox("Tipo de construcción", tipos_construccion)
area = st.number_input("Área construida (m²)", min_value=10.0, max_value=1000.0, value=100.0, step=10.0)
pisos = st.number_input("Cantidad de pisos", min_value=1, max_value=5, value=1)
acabado = st.selectbox("Tipo de acabado", list(acabados.keys()))

if st.button("Calcular presupuesto"):

    # Cálculo del presupuesto
    base_m2 = zonas[zona]
    factor_acabado = acabados[acabado]
    costo_m2 = base_m2 * factor_acabado
    total = costo_m2 * area * pisos

    # Materiales estimados (valores de referencia)
    cemento = round(area * pisos * 0.22, 1)
    arena = round(area * pisos * 0.18, 1)
    fierro = round(area * pisos * 11, 1)
    ladrillo = round(area * pisos * 125, 1)

    # Duración estimada
    duracion_meses = round((area * pisos) / 300, 1)

    st.success(f"Presupuesto estimado: S/ {total:,.2f}")
    st.subheader("Materiales estimados")
    st.write(f"- Cemento: {cemento} bolsas")
    st.write(f"- Arena: {arena} m³")
    st.write(f"- Fierro: {fierro} kg")
    st.write(f"- Ladrillo: {ladrillo} unidades")
    st.write(f"- Duración estimada de la obra: {duracion_meses} meses")

    # Generar PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, "Presupuesto SmartBuild Perú", ln=True, align="C")
    pdf.ln(5)
    pdf.cell(200, 10, f"Fecha: {datetime.date.today().strftime('%d/%m/%Y')}", ln=True)
    pdf.cell(200, 10, f"Zona: {zona}", ln=True)
    pdf.cell(200, 10, f"Tipo de construcción: {tipo_construccion}", ln=True)
    pdf.cell(200, 10, f"Área: {area} m²", ln=True)
    pdf.cell(200, 10, f"Pisos: {pisos}", ln=True)
    pdf.cell(200, 10, f"Acabado: {acabado}", ln=True)
    pdf.cell(200, 10, f"Presupuesto estimado: S/ {total:,.2f}", ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, "Materiales estimados:", ln=True)
    pdf.cell(200, 10, f"- Cemento: {cemento} bolsas", ln=True)
    pdf.cell(200, 10, f"- Arena: {arena} m³", ln=True)
    pdf.cell(200, 10, f"- Fierro: {fierro} kg", ln=True)
    pdf.cell(200, 10, f"- Ladrillo: {ladrillo} unidades", ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, f"Duración estimada de la obra: {duracion_meses} meses", ln=True)

    pdf_bytes = pdf.output(dest='S').encode('latin1')
    st.download_button("Descargar presupuesto en PDF", data=pdf_bytes, file_name="presupuesto_smartbuild.pdf", mime="application/pdf")
