import streamlit as st
from fpdf import FPDF

# Interfaz principal
st.title("SmartBuild Perú - Estimación de Presupuesto")

# Selección de ubicación, tipo de construcción y parámetros
ubicacion = st.selectbox("Ubicación del terreno", ["Lima", "Arequipa", "Cusco", "Trujillo", "Otro"])
tipo_construccion = st.selectbox("Tipo de construcción", [
    "Vivienda unifamiliar",
    "Edificio multifamiliar",
    "Local comercial",
    "Oficina",
    "Almacén"
])
area = st.number_input("Área total (m²)", min_value=10.0, max_value=1000.0, value=100.0, step=10.0)
pisos = st.number_input("Cantidad de pisos", min_value=1, max_value=5, value=1)
acabado = st.selectbox("Tipo de acabado", ["Económico", "Estándar", "Premium"])

# Costos base y multiplicadores
costos_base = {"Lima": 900, "Arequipa": 850, "Cusco": 800, "Trujillo": 820, "Otro": 780}
multiplicador = {"Económico": 1.0, "Estándar": 1.25, "Premium": 1.5}

if st.button("Calcular presupuesto"):
    costo_m2 = costos_base[ubicacion] * multiplicador[acabado]
    total = costo_m2 * area * pisos

    # Materiales estimados
    cemento = round(area * pisos * 0.2, 2)
    arena = round(area * pisos * 0.15, 2)
    fierro = round(area * pisos * 10, 2)
    ladrillo = round(area * pisos * 120, 2)

    # Duración estimada
    duracion_meses = (area * pisos) / 100
    if duracion_meses < 1:
        duracion_dias = round(duracion_meses * 30)
        duracion_texto = f"Aprox. {duracion_dias} días"
    else:
        meses = int(duracion_meses)
        semanas = int((duracion_meses - meses) * 4)
        duracion_texto = f"Aprox. {meses} meses" + (f" y {semanas} semanas" if semanas else "")

    # Mostrar resultados
    st.success(f"Presupuesto estimado: S/ {total:,.2f}")
    st.write(f"**Duración estimada de la obra:** {duracion_texto}")
    st.subheader("Materiales estimados")
    st.write(f"- Cemento: {cemento} bolsas")
    st.write(f"- Arena: {arena} m³")
    st.write(f"- Fierro: {fierro} kg")
    st.write(f"- Ladrillo: {ladrillo} unidades")

    # Crear PDF
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
    pdf.cell(200, 10, f"Presupuesto: S/ {total:,.2f}", ln=True)
    pdf.cell(200, 10, f"Duración estimada: {duracion_texto}", ln=True)
    pdf.ln(10)
    pdf.cell(200, 10, "Materiales:", ln=True)
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
