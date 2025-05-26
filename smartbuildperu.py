import streamlit as st
from fpdf import FPDF

# Interfaz
st.title("SmartBuild Perú - Estimación de Presupuesto")

ubicacion = st.selectbox("Ubicación del terreno", ["Lima", "Arequipa", "Cusco", "Trujillo", "Otro"])
area = st.number_input("Área (m²)", min_value=10.0, max_value=1000.0, value=100.0, step=10.0)
acabado = st.selectbox("Tipo de acabado", ["Económico", "Estándar", "Premium"])
pisos = st.number_input("Cantidad de pisos", min_value=1, max_value=5, value=1)

costos_base = {"Lima": 500, "Arequipa": 450, "Cusco": 400, "Trujillo": 420, "Otro": 380}
multiplicador = {"Económico": 1.0, "Estándar": 1.3, "Premium": 1.7}

if st.button("Calcular presupuesto"):
    costo_m2 = costos_base[ubicacion] * multiplicador[acabado]
    total = costo_m2 * area * pisos

    cemento = round(area * pisos * 0.2, 2)
    arena = round(area * pisos * 0.15, 2)
    fierro = round(area * pisos * 10, 2)
    ladrillo = round(area * pisos * 120, 2)

    st.success(f"Presupuesto estimado: S/ {total:,.2f}")
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
    pdf.cell(200, 10, f"Área: {area} m²", ln=True)
    pdf.cell(200, 10, f"Pisos: {pisos}", ln=True)
    pdf.cell(200, 10, f"Acabado: {acabado}", ln=True)
    pdf.cell(200, 10, f"Presupuesto: S/ {total:,.2f}", ln=True)
    pdf.ln(10)
    pdf.cell(200, 10, "Materiales:", ln=True)
    pdf.cell(200, 10, f"Cemento: {cemento} bolsas", ln=True)
    pdf.cell(200, 10, f"Arena: {arena} m³", ln=True)
    pdf.cell(200, 10, f"Fierro: {fierro} kg", ln=True)
    pdf.cell(200, 10, f"Ladrillo: {ladrillo} unidades", ln=True)

    # Convertir PDF a bytes y descargar
    pdf_data = pdf.output(dest='S').encode('latin1')
    st.download_button(
        label="Descargar presupuesto PDF",
        data=pdf_data,
        file_name="presupuesto_smartbuild.pdf",
        mime="application/pdf"
    )
