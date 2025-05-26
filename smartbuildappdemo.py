
import streamlit as st
import pandas as pd
from fpdf import FPDF
import base64

st.set_page_config(page_title="SmartBuild Perú PRO", layout="centered")

st.title("SmartBuild Perú PRO - Estimador de Costos de Construcción")

# FORMULARIO DE ENTRADA
st.subheader("Ingrese los datos del proyecto")

ubicacion = st.selectbox("Ubicación del proyecto", ["Lima", "Arequipa", "Cusco", "Trujillo"])
area = st.number_input("Área de construcción (m²)", min_value=10, max_value=1000, step=10)
pisos = st.number_input("Cantidad de pisos", min_value=1, max_value=10, step=1)
acabado = st.selectbox("Tipo de acabado", ["Básico", "Estándar", "Premium"])

# DATOS DE COSTOS
costos_base = {
    "Básico": 800,
    "Estándar": 1000,
    "Premium": 1300
}

factores_ubicacion = {
    "Lima": 1.0,
    "Arequipa": 0.95,
    "Cusco": 1.1,
    "Trujillo": 1.05
}

# FUNCIÓN PARA CALCULAR PRESUPUESTO Y MATERIALES
def calcular_presupuesto(area, pisos, acabado, ubicacion):
    costo_unitario = costos_base[acabado] * factores_ubicacion[ubicacion]
    costo_total = costo_unitario * area * pisos

    materiales = {
        "Cemento (bolsas)": round((area * pisos) / 50, 2),
        "Arena (m3)": round((area * pisos) / 66, 2),
        "Ladrillos (unidades)": round(area * pisos * 150, 2),
        "Fierro (kg)": round(area * pisos * 20, 2),
    }

    return costo_total, materiales

# FUNCIÓN PARA GENERAR PDF
def generar_pdf(costo_total, materiales, ubicacion, area, pisos, acabado):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "SmartBuild Perú PRO", ln=True, align="C")

    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(0, 10, f"Ubicación: {ubicacion}", ln=True)
    pdf.cell(0, 10, f"Área: {area} m²", ln=True)
    pdf.cell(0, 10, f"Pisos: {pisos}", ln=True)
    pdf.cell(0, 10, f"Acabado: {acabado}", ln=True)
    pdf.cell(0, 10, f"Costo estimado total: S/ {costo_total:,.2f}", ln=True)

    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Detalle de materiales:", ln=True)

    pdf.set_font("Arial", size=12)
    for mat, qty in materiales.items():
        pdf.cell(0, 10, f"{mat}: {qty}", ln=True)

    return pdf.output(dest="S").encode("latin1")

# BOTÓN DE CÁLCULO
if st.button("Calcular presupuesto"):
    costo_total, materiales = calcular_presupuesto(area, pisos, acabado, ubicacion)

    st.subheader("Resultado del Presupuesto")
    st.success(f"Costo estimado total: S/ {costo_total:,.2f}")
    st.write("Detalle de materiales estimados:")

    df = pd.DataFrame(materiales.items(), columns=["Material", "Cantidad"])
    st.table(df)

    # GENERAR PDF Y DESCARGA
    pdf_bytes = generar_pdf(costo_total, materiales, ubicacion, area, pisos, acabado)
    b64 = base64.b64encode(pdf_bytes).decode("utf-8")
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="presupuesto_smartbuild.pdf">Descargar PDF</a>'
    st.markdown(href, unsafe_allow_html=True)
