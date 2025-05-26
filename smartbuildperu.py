import streamlit as st
from fpdf import FPDF

# Título
st.title("SmartBuild Perú - Estimación de Presupuesto")

# Entradas del usuario
ubicacion = st.selectbox("Ubicación del terreno", ["Lima", "Arequipa", "Cusco", "Trujillo", "Otro"])
distrito = st.text_input("Distrito (opcional)")
tipo_construccion = st.selectbox("Tipo de construcción", [
    "Vivienda unifamiliar",
    "Edificio multifamiliar",
    "Local comercial",
    "Oficina",
    "Almacén"
])
area = st.number_input("Área (m²)", min_value=10.0, max_value=1000.0, value=100.0, step=10.0)
acabado = st.selectbox("Tipo de acabado", ["Económico", "Estándar", "Premium"])
pisos = st.number_input("Cantidad de pisos", min_value=1, max_value=5, value=1)

# Costos base por ubicación (aproximados)
costos_base = {"Lima": 550, "Arequipa": 500, "Cusco": 470, "Trujillo": 490, "Otro": 450}
# Multiplicador por tipo de acabado
multiplicador = {"Económico": 1.0, "Estándar": 1.3, "Premium": 1.7}
# Costo base por tipo de construcción
costo_construccion = {
    "Vivienda unifamiliar": 1.0,
    "Edificio multifamiliar": 1.4,
    "Local comercial": 1.3,
    "Oficina": 1.5,
    "Almacén": 0.9
}

# Botón de cálculo
if st.button("Calcular presupuesto"):
    base = costos_base[ubicacion]
    mult_acabado = multiplicador[acabado]
    mult_tipo = costo_construccion[tipo_construccion]

    costo_m2 = base * mult_acabado * mult_tipo
    total = costo_m2 * area * pisos

    # Estimación de materiales
    cemento = round(area * pisos * 0.2, 2)
    arena = round(area * pisos * 0.15, 2)
    fierro = round(area * pisos * 10, 2)
    ladrillo = round(area * pisos * 120, 2)

    # Mostrar resultados
    st.success(f"Presupuesto estimado: S/ {total:,.2f}")
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
    pdf.cell(200, 10, f"Ubicación: {ubicacion} - {distrito}", ln=True)
    pdf.cell(200, 10, f"Tipo de construcción: {tipo_construccion}", ln=True)
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

    # Descargar PDF
    pdf_data = pdf.output(dest='S').encode('latin1')
    st.download_button(
        label="Descargar presupuesto PDF",
        data=pdf_data,
        file_name="presupuesto_smartbuild.pdf",
        mime="application/pdf"
    )
