import streamlit as st
from fpdf import FPDF
import math

# Título principal
st.title("SmartBuild Perú - Estimación de Presupuesto")

# Selección de zona o ciudad
zonas_lima = {
    "Miraflores": 1200,
    "San Isidro": 1250,
    "San Borja": 1150,
    "Surco": 1100,
    "La Molina": 1050,
    "Jesús María": 1000,
    "Pueblo Libre": 950,
    "Comas": 800,
    "Villa El Salvador": 750
}
otras_ciudades = {
    "Arequipa": 900,
    "Cusco": 850,
    "Trujillo": 800,
    "Otro": 750
}

ubicacion = st.selectbox("Ubicación del terreno", list(zonas_lima.keys()) + list(otras_ciudades.keys()))

# Selección de tipo de construcción
tipo_construccion = st.selectbox("Tipo de construcción", [
    "Vivienda unifamiliar",
    "Edificio multifamiliar",
    "Local comercial",
    "Oficina",
    "Almacén"
])

# Parámetros generales
area = st.number_input("Área total (m²)", min_value=10.0, max_value=1000.0, value=100.0, step=10.0)
pisos = st.number_input("Cantidad de pisos", min_value=1, max_value=5, value=1)
acabado = st.selectbox("Tipo de acabado", ["Económico", "Estándar", "Premium"])
multiplicador_acabado = {"Económico": 1.0, "Estándar": 1.3, "Premium": 1.7}

# Cálculo al presionar el botón
if st.button("Calcular presupuesto"):
    if ubicacion in zonas_lima:
        costo_base = zonas_lima[ubicacion]
    else:
        costo_base = otras_ciudades[ubicacion]

    costo_m2 = costo_base * multiplicador_acabado[acabado]
    costo_total = costo_m2 * area * pisos

    # Materiales aproximados
    cemento = round(area * pisos * 0.25, 2)
    arena = round(area * pisos * 0.20, 2)
    fierro = round(area * pisos * 12, 2)
    ladrillo = round(area * pisos * 130, 2)

    # Duración estimada redondeada a meses completos
    duracion_meses = math.ceil((area * pisos) / 300)

    # Mostrar resultados
    st.success(f"Presupuesto estimado: S/ {costo_total:,.2f}")
    st.write(f"Duración estimada de la obra: {duracion_meses} meses")
    st.subheader("Materiales estimados")
    st.write(f"- Cemento: {cemento} bolsas")
    st.write(f"- Arena: {arena} m³")
    st.write(f"- Fierro: {fierro} kg")
    st.write(f"- Ladrillo: {ladrillo} unidades")

    # Generar PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Presupuesto SmartBuild Perú", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, f"Ubicación: {ubicacion}", ln=True)
    pdf.cell(200, 10, f"Tipo de construcción: {tipo_construccion}", ln=True)
    pdf.cell(200, 10, f"Área: {area} m²", ln=True)
    pdf.cell(200, 10, f"Pisos: {pisos}", ln=True)
    pdf.cell(200, 10, f"Acabado: {acabado}", ln=True)
    pdf.cell(200, 10, f"Presupuesto estimado: S/ {costo_total:,.2f}", ln=True)
    pdf.cell(200, 10, f"Duración estimada: {duracion_meses} meses", ln=True)
    pdf.ln(10)
    pdf.cell(200, 10, "Materiales estimados:", ln=True)
    pdf.cell(200, 10, f"Cemento: {cemento} bolsas", ln=True)
    pdf.cell(200, 10, f"Arena: {arena} m³", ln=True)
    pdf.cell(200, 10, f"Fierro: {fierro} kg", ln=True)
    pdf.cell(200, 10, f"Ladrillo: {ladrillo} unidades", ln=True)

    # Descargar PDF
    pdf_data = pdf.output(dest='S').encode('latin1')
    st.download_button(
        label="Descargar presupuesto en PDF",
        data=pdf_data,
        file_name="presupuesto_smartbuild.pdf",
        mime="application/pdf"
    )
