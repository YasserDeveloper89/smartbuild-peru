import streamlit as st
from fpdf import FPDF
import io

st.set_page_config(page_title="SmartBuild Perú", layout="centered")

st.title("SmartBuild Perú")
st.subheader("Calculadora de Presupuesto de Construcción")

# Entradas del usuario
ubicacion = st.selectbox("Ubicación del terreno", ["Lima", "Arequipa", "Cusco", "Otra"])
area = st.number_input("Área a construir (en m²)", min_value=10, max_value=1000, step=10)
acabado = st.selectbox("Tipo de acabado", ["Económico", "Intermedio", "Lujo"])
pisos = st.slider("Número de pisos", 1, 5, 1)

# Costos base por m² según ubicación y acabado
costos_base = {
    "Lima": {"Económico": 1200, "Intermedio": 1600, "Lujo": 2200},
    "Arequipa": {"Económico": 1000, "Intermedio": 1400, "Lujo": 2000},
    "Cusco": {"Económico": 1100, "Intermedio": 1500, "Lujo": 2100},
    "Otra": {"Económico": 900, "Intermedio": 1300, "Lujo": 1800},
}

# Estimar materiales básicos (valores simples para ejemplo)
def estimar_materiales(area, pisos):
    return {
        "Cemento (bolsas)": area * pisos * 0.3,
        "Arena (m³)": area * pisos * 0.2,
        "Ladrillos (unidades)": area * pisos * 120,
        "Hierro (kg)": area * pisos * 15,
        "Mano de obra (jornales)": area * pisos * 0.2,
    }

# Calcular
if st.button("Calcular presupuesto"):
    costo_unitario = costos_base[ubicacion][acabado]
    costo_total = costo_unitario * area * pisos
    materiales_estimados = estimar_materiales(area, pisos)

    st.success(f"Presupuesto estimado: S/ {costo_total:,.2f}")
    st.subheader("Materiales estimados:")
    for mat, qty in materiales_estimados.items():
        st.write(f"- {mat}: {qty:.2f}")

    # Crear PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Presupuesto Detallado - SmartBuild Perú", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Ubicación: {ubicacion}", ln=True)
    pdf.cell(200, 10, txt=f"Área: {area} m²", ln=True)
    pdf.cell(200, 10, txt=f"Acabado: {acabado}", ln=True)
    pdf.cell(200, 10, txt=f"Pisos: {pisos}", ln=True)
    pdf.cell(200, 10, txt=f"Presupuesto estimado: S/ {costo_total:,.2f}", ln=True)
    pdf.ln(10)
    pdf.cell(200, 10, txt="Materiales estimados:", ln=True)
    for mat, qty in materiales_estimados.items():
        pdf.cell(200, 10, txt=f"- {mat}: {qty:.2f}", ln=True)

    # PDF en memoria
    pdf_buffer = io.BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)

    # Botón de descarga
    st.download_button(
        label="Descargar presupuesto en PDF",
        data=pdf_buffer,
        file_name="Presupuesto_SmartBuild.pdf",
        mime="application/pdf"
    )
