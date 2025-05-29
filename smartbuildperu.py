import streamlit as st
from fpdf import FPDF
import datetime
import math
import pandas as pd

st.set_page_config(page_title="SmartBuild Perú", layout="centered")
st.title("SmartBuild Perú - Estimación de presupuestos para proyectos de construcción")

# Zonas y coordenadas
zonas_info = {
    "Miraflores": {"lat": -12.1211, "lon": -77.0290, "clima": "Templado húmedo"},
    "San Isidro": {"lat": -12.0976, "lon": -77.0365, "clima": "Templado húmedo"},
    "San Borja": {"lat": -12.0931, "lon": -77.0012, "clima": "Templado seco"},
    "Comas": {"lat": -11.9364, "lon": -77.0622, "clima": "Cálido seco"},
    "Villa El Salvador": {"lat": -12.2225, "lon": -76.9724, "clima": "Cálido húmedo"},
    "Surco": {"lat": -12.1588, "lon": -76.9818, "clima": "Templado"},
    "La Molina": {"lat": -12.0892, "lon": -76.9468, "clima": "Seco y soleado"},
    "Ate": {"lat": -12.0443, "lon": -76.9052, "clima": "Seco templado"},
    "Centro de Lima": {"lat": -12.0464, "lon": -77.0428, "clima": "Húmedo urbano"}
}

zona = st.selectbox("Selecciona la zona o distrito", list(zonas_info.keys()))
tipo_construccion = st.selectbox("Tipo de construcción", [
    "Vivienda unifamiliar", "Edificio multifamiliar",
    "Local comercial", "Oficina", "Almacén"
])
area = st.number_input("Área del terreno (m²)", min_value=10.0, max_value=1000.0, value=100.0, step=10.0)
pisos = st.number_input("Cantidad de pisos", min_value=1, max_value=10, value=1)
acabado = st.selectbox("Tipo de acabado", ["Económico", "Estándar", "Premium"])

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
    duracion_meses = math.ceil((area * pisos) / 300)

    # Materiales estimados
    cemento = round(area * pisos * 0.2, 1)
    arena = round(area * pisos * 0.15, 1)
    fierro = round(area * pisos * 10, 1)
    ladrillo = round(area * pisos * 120, 1)

    # Mostrar resultados
    st.success(f"Presupuesto estimado: S/ {total:,.2f}")
    st.markdown(f"**Duración estimada:** {duracion_meses} meses")

    st.markdown("### Materiales estimados:")
    st.write(f"- Cemento: {cemento} bolsas")
    st.write(f"- Arena: {arena} m³")
    st.write(f"- Fierro: {fierro} kg")
    st.write(f"- Ladrillo: {ladrillo} unidades")

    # Mostrar clima
    clima = zonas_info[zona]["clima"]
    st.markdown(f"**Clima típico en {zona}:** {clima}")

    # Mostrar mapa
    st.markdown("### Ubicación en el mapa:")
    df = pd.DataFrame([{
        'lat': zonas_info[zona]["lat"],
        'lon': zonas_info[zona]["lon"]
    }])
    st.map(df)

    # PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Presupuesto de Construcción - SmartBuild Perú", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, f"Fecha: {datetime.datetime.now().strftime('%d/%m/%Y')}", ln=True)
    pdf.cell(200, 10, f"Zona: {zona}", ln=True)
    pdf.cell(200, 10, f"Clima: {clima}", ln=True)
    pdf.cell(200, 10, f"Tipo de construcción: {tipo_construccion}", ln=True)
    pdf.cell(200, 10, f"Área: {area} m²", ln=True)
    pdf.cell(200, 10, f"Pisos: {pisos}", ln=True)
    pdf.cell(200, 10, f"Acabado: {acabado}", ln=True)
    pdf.cell(200, 10, f"Duración estimada: {duracion_meses} meses", ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, f"Presupuesto estimado: S/ {total:,.2f}", ln=True)
    pdf.ln(10)
    pdf.cell(200, 10, "Materiales estimados:", ln=True)
    pdf.cell(200, 10, f"- Cemento: {cemento} bolsas", ln=True)
    pdf.cell(200, 10, f"- Arena: {arena} m³", ln=True)
    pdf.cell(200, 10, f"- Fierro: {fierro} kg", ln=True)
    pdf.cell(200, 10, f"- Ladrillo: {ladrillo} unidades", ln=True)

    pdf_bytes = pdf.output(dest='S').encode('latin1')

    st.download_button(
        label="Descargar presupuesto en PDF",
        data=pdf_bytes,
        file_name="presupuesto_smartbuild.pdf",
        mime="application/pdf"
)
