import streamlit as st from fpdf import FPDF import datetime

st.set_page_config(page_title="SmartBuild Perú", layout="centered")

Datos de distritos con costos aproximados por m2 en soles

costos_distritos = { "Miraflores": 1200, "San Isidro": 1300, "San Borja": 1100, "Santiago de Surco": 1050, "Jesús María": 950, "Pueblo Libre": 900, "Los Olivos": 800, "Comas": 700, "Villa El Salvador": 650, "Otros": 600 }

Multiplicadores por tipo de acabado y construcción

multiplicador_acabado = {"Económico": 1.0, "Estándar": 1.3, "Premium": 1.7} multiplicador_tipo = { "Vivienda unifamiliar": 1.0, "Edificio multifamiliar": 1.2, "Local comercial": 1.5, "Oficina": 1.4, "Almacén": 1.1 }

Interfaz

st.title("SmartBuild Perú - Estimador de Presupuesto Profesional")

distrito = st.selectbox("Selecciona el distrito", list(costos_distritos.keys())) area = st.number_input("Área del proyecto (m²)", min_value=10.0, max_value=1000.0, value=100.0, step=10.0) pisos = st.number_input("Cantidad de pisos", min_value=1, max_value=5, value=1) tipo_construccion = st.selectbox("Tipo de construcción", list(multiplicador_tipo.keys())) acabado = st.selectbox("Tipo de acabado", list(multiplicador_acabado.keys()))

if st.button("Calcular presupuesto"): # Cálculo de presupuesto costo_m2 = costos_distritos[distrito] * multiplicador_acabado[acabado] * multiplicador_tipo[tipo_construccion] total = costo_m2 * area * pisos

# Estimación de materiales (valores aproximados)
cemento = round(area * pisos * 0.2, 1)
arena = round(area * pisos * 0.15, 1)
fierro = round(area * pisos * 10, 1)
ladrillo = round(area * pisos * 120, 1)

# Estimación de duración
duracion_meses = round((area * pisos) / 300.0, 1)

# Mostrar resultados
st.success(f"Presupuesto estimado: S/ {total:,.2f}")
st.markdown(f"**Duración estimada de la obra:** {duracion_meses} meses")

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
pdf.cell(200, 10, f"Fecha: {datetime.date.today()}", ln=True)
pdf.cell(200, 10, f"Distrito: {distrito}", ln=True)
pdf.cell(200, 10, f"Tipo de construcción: {tipo_construccion}", ln=True)
pdf.cell(200, 10, f"Acabado: {acabado}", ln=True)
pdf.cell(200, 10, f"Área: {area} m² | Pisos: {pisos}", ln=True)
pdf.cell(200, 10, f"Presupuesto estimado: S/ {total:,.2f}", ln=True)
pdf.cell(200, 10, f"Duración estimada: {duracion_meses} meses", ln=True)
pdf.ln(5)
pdf.cell(200, 10, "Materiales estimados:", ln=True)
pdf.cell(200, 10, f"- Cemento: {cemento} bolsas", ln=True)
pdf.cell(200, 10, f"- Arena: {arena} m³", ln=True)
pdf.cell(200, 10, f"- Fierro: {fierro} kg", ln=True)
pdf.cell(200, 10, f"- Ladrillo: {ladrillo} unidades", ln=True)

pdf_data = pdf.output(dest='S').encode('latin1')

st.download_button(
    label="Descargar presupuesto en PDF",
    data=pdf_data,
    file_name="presupuesto_smartbuild.pdf",
    mime="application/pdf"
)

