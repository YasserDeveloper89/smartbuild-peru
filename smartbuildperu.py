import streamlit as st
from fpdf import FPDF
import datetime

st.set_page_config(page_title="SmartBuild Perú", layout="centered")

st.title("SmartBuild Perú - Estimación de Presupuesto")

# Parámetros base
zonas = {
    "Lima - Miraflores": 1200,
    "Lima - Comas": 850,
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

tipos_construccion = {
    "Vivienda unifamiliar": 1.0,
    "Edificio multifamiliar": 1.15,
    "Local comercial": 1.2,
    "Oficina": 1.1,
    "Almacén": 0.9
}

# Inputs de usuario
zona = st.selectbox("Zona del terreno", list(zonas.keys()))
area = st.number_input("Área construida (m²)", min_value=10.0, max_value=2000.0, value=100.0, step=10.0)
pisos = st.number_input("Número de pisos", min_value=1, max_value=10, value=1)
acabado = st.selectbox("Tipo de acabado", list(acabados.keys()))
tipo_construccion = st.selectbox("Tipo de construcción", list(tipos_construccion.keys()))

if st.button("Calcular presupuesto"):
    # Cálculo
    base = zonas[zona]
    multi_acabado = acabados[acabado]
    multi_tipo = tipos_construccion[tipo_construccion]

    costo_m2 = base * multi_acabado * multi_tipo
    total = costo_m2 * area * pisos

    # Duración estimada (simplificada)
    duracion_meses = max(1, round((area * pisos) / 350, 1))

    # Materiales estimados
    cemento = round(area * pisos * 0.22, 1)  # bolsas
    arena = round(area * pisos * 0.15, 1)    # m3
    fierro = round(area * pisos * 12, 1)     # kg
    ladrillo = round(area * pisos * 130, 1)  # unidades

    # Resultados
    st.subheader("Resumen del presupuesto")
    st.success(f"Presupuesto estimado: S/ {total:,.2f}")
    st.write(f"Duración estimada de obra: {duracion_meses} meses")

    st.subheader("Materiales estimados")
    st.write(f"- Cemento: {cemento} bolsas")
    st.write(f"- Arena: {arena} m³")
    st.write(f"- Fierro: {fierro} kg")
    st.write(f"- Ladrillo: {ladrillo} unidades")

    # PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "SmartBuild Perú - Presupuesto", ln=True, align="C")
    pdf.ln(8)
    pdf.cell(200, 10, f"Fecha: {datetime.date.today().strftime('%d/%m/%Y')}", ln=True)
    pdf.cell(200, 10, f"Zona: {zona}", ln=True)
    pdf.cell(200, 10, f"Área: {area} m²", ln=True)
    pdf.cell(200, 10, f"Pisos: {pisos}", ln=True)
    pdf.cell(200, 10, f"Acabado: {acabado}", ln=True)
    pdf.cell(200, 10, f"Tipo: {tipo_construccion}", ln=True)
    pdf.cell(200, 10, f"Presupuesto estimado: S/ {total:,.2f}", ln=True)
    pdf.cell(200, 10, f"Duración: {duracion_meses} meses", ln=True)
    pdf.ln(8)
    pdf.cell(200, 10, "Materiales:", ln=True)
    pdf.cell(200, 10, f"Cemento: {cemento} bolsas", ln=True)
    pdf.cell(200, 10, f"Arena: {arena} m³", ln=True)
    pdf.cell(200, 10, f"Fierro: {fierro} kg", ln=True)
    pdf.cell(200, 10, f"Ladrillo: {ladrillo} unidades", ln=True)

    # Descargar PDF
    pdf_output = pdf.output(dest='S').encode('latin1')
    st.download_button(
        label="Descargar PDF",
        data=pdf_output,
        file_name="presupuesto_smartbuild.pdf",
        mime="application/pdf"
    )
