import streamlit as st
from fpdf import FPDF
import io

st.set_page_config(page_title="SmartBuild Perú", layout="centered")

st.title("SmartBuild Perú - Calculadora de Presupuesto de Construcción")

# Entradas del usuario
ubicacion = st.selectbox("Ubicación", ["Lima", "Cusco", "Arequipa", "Trujillo"])
area = st.number_input("Área en metros cuadrados", min_value=10, step=10)
acabado = st.selectbox("Tipo de acabado", ["Económico", "Estándar", "Premium"])
pisos = st.slider("Cantidad de pisos", 1, 5, 1)

# Costos por m² según acabado
costos_por_m2 = {
    "Económico": 350,
    "Estándar": 500,
    "Premium": 800
}

# Materiales estimados (puedes ajustar según ingeniería)
def calcular_materiales(area):
    arena = round(area * 0.05, 2)  # m³
    cemento = round(area * 0.2, 1)  # bolsas
    fierro = round(area * 3, 1)     # kg
    ladrillos = int(area * 60)      # unidades
    return arena, cemento, fierro, ladrillos

if st.button("Calcular Presupuesto"):
    costo_total = area * costos_por_m2[acabado]
    arena, cemento, fierro, ladrillos = calcular_materiales(area)

    st.subheader("Presupuesto estimado:")
    st.write(f"Total: S/ {costo_total:,.2f}")
    
    st.subheader("Detalles de materiales estimados:")
    st.write(f"Arena (m³): {arena}")
    st.write(f"Cemento (bolsas): {cemento}")
    st.write(f"Fierro (kg): {fierro}")
    st.write(f"Ladrillos: {ladrillos}")

    # Generar PDF en memoria
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Presupuesto - SmartBuild Perú", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Ubicación: {ubicacion}", ln=True)
    pdf.cell(200, 10, txt=f"Área: {area} m²", ln=True)
    pdf.cell(200, 10, txt=f"Acabado: {acabado}", ln=True)
    pdf.cell(200, 10, txt=f"Pisos: {pisos}", ln=True)
    pdf.cell(200, 10, txt=f"Presupuesto Total: S/ {costo_total:,.2f}", ln=True)
    pdf.ln(10)
    pdf.cell(200, 10, txt="Materiales estimados:", ln=True)
    pdf.cell(200, 10, txt=f"Arena: {arena} m³", ln=True)
    pdf.cell(200, 10, txt=f"Cemento: {cemento} bolsas", ln=True)
    pdf.cell(200, 10, txt=f"Fierro: {fierro} kg", ln=True)
    pdf.cell(200, 10, txt=f"Ladrillos: {ladrillos} unidades", ln=True)

    pdf_buffer = io.BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)

    st.download_button(
        label="Descargar presupuesto en PDF",
        data=pdf_buffer,
        file_name="presupuesto_smartbuild.pdf",
        mime='application/pdf'
    )
