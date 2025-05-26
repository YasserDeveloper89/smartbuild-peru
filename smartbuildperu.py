
import streamlit as st
from fpdf import FPDF

st.set_page_config(page_title="SmartBuild Perú", layout="centered")

st.title("SmartBuild Perú - Calculadora de Presupuesto de Vivienda")

# Entradas del usuario
ubicacion = st.selectbox("Ubicación", ["Lima", "Arequipa", "Cusco", "Trujillo", "Piura"])
area = st.number_input("Área en metros cuadrados (m²)", min_value=10.0, max_value=1000.0, step=1.0)
acabado = st.selectbox("Tipo de acabado", ["Básico", "Estándar", "Premium"])
pisos = st.number_input("Número de pisos", min_value=1, max_value=5, step=1)

# Costos estimados por m² por tipo y ciudad (simulados)
precios_base = {
    "Lima": 600,
    "Arequipa": 550,
    "Cusco": 580,
    "Trujillo": 530,
    "Piura": 500
}
mult_acabado = {"Básico": 1.0, "Estándar": 1.2, "Premium": 1.5}

# Materiales estimados (muy básicos)
def calcular_materiales(area_total):
    return {
        "Cemento (bolsas)": round(area_total * 0.2, 2),
        "Arena (m³)": round(area_total * 0.15, 2),
        "Ladrillos (unidades)": int(area_total * 120),
        "Acero (kg)": int(area_total * 10),
    }

# Calcular presupuesto
if st.button("Calcular presupuesto"):
    precio_m2 = precios_base[ubicacion] * mult_acabado[acabado]
    costo_total = precio_m2 * area * pisos
    materiales = calcular_materiales(area * pisos)

    st.success(f"Costo estimado total: S/ {costo_total:,.2f}")
    st.subheader("Materiales estimados:")
    for mat, cant in materiales.items():
        st.markdown(f"- **{mat}**: {cant}")

    # Guardar en historial
    if "historial" not in st.session_state:
        st.session_state.historial = []
    st.session_state.historial.append((ubicacion, area, acabado, pisos, costo_total))

    # Crear PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "SmartBuild Perú - Presupuesto", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, f"Ubicación: {ubicacion}", ln=True)
    pdf.cell(200, 10, f"Área: {area} m²", ln=True)
    pdf.cell(200, 10, f"Acabado: {acabado}", ln=True)
    pdf.cell(200, 10, f"Pisos: {pisos}", ln=True)
    pdf.cell(200, 10, f"Costo Total: S/ {costo_total:,.2f}", ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, "Materiales estimados:", ln=True)
    for mat, cant in materiales.items():
        pdf.cell(200, 10, f"- {mat}: {cant}", ln=True)

    # Descargar PDF en memoria
    pdf_data = pdf.output(dest='S').encode('latin1')

    st.download_button(
        label="Descargar PDF",
        data=pdf_data,
        file_name="presupuesto_smartbuild.pdf",
        mime="application/pdf"
    )

# Mostrar historial
if st.checkbox("Ver historial de presupuestos"):
    if "historial" in st.session_state and st.session_state.historial:
        for idx, entry in enumerate(st.session_state.historial[::-1], 1):
            st.markdown(f"**{idx}.** Ubicación: {entry[0]}, Área: {entry[1]} m², "
                        f"Acabado: {entry[2]}, Pisos: {entry[3]}, Total: S/ {entry[4]:,.2f}")
    else:
        st.info("Aún no hay cálculos guardados.")
