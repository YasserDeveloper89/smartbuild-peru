
import streamlit as st
from fpdf import FPDF

# --- DATOS BASE ---
costos_por_region = {
    "Lima": {"básico": 800, "intermedio": 1000, "premium": 1300},
    "Cusco": {"básico": 700, "intermedio": 950, "premium": 1200},
    "Arequipa": {"básico": 750, "intermedio": 980, "premium": 1250},
    "Otro": {"básico": 650, "intermedio": 900, "premium": 1150},
}

costos_terreno = {
    "Lima": 1200,
    "Cusco": 600,
    "Arequipa": 800,
    "Otro": 400
}

# --- APP STREAMLIT ---
st.set_page_config(page_title="SmartBuild Perú Pro", layout="centered")
st.title("SmartBuild Perú – Versión Pro")
st.subheader("Estimador profesional de costos de construcción para el mercado peruano.")

st.markdown("### Paso 1: Datos del proyecto")
area = st.number_input("Área del proyecto (m²):", min_value=20, max_value=1000, value=100)
ubicacion = st.selectbox("Ubicación:", list(costos_por_region.keys()))
acabado = st.selectbox("Nivel de acabados:", ["básico", "intermedio", "premium"])
pisos = st.slider("Cantidad de pisos:", 1, 5, 1)
terreno = st.selectbox("Tipo de terreno:", ["plano", "accidentado"])

st.markdown("### Paso 2: Cálculo de presupuesto")
if st.button("Calcular costos"):
    costo_m2 = costos_por_region[ubicacion][acabado]
    costo_construccion = costo_m2 * area * pisos

    incremento_terreno = 1.15 if terreno == "accidentado" else 1.0
    costo_terreno = costos_terreno[ubicacion] * area * incremento_terreno

    costo_total = costo_construccion + costo_terreno

    st.success("**Resultado del cálculo:**")
    st.markdown(f"- Costo de construcción: S/ {costo_construccion:,.2f}")
    st.markdown(f"- Costo del terreno estimado: S/ {costo_terreno:,.2f}")
    st.markdown(f"### Total estimado: S/ {costo_total:,.2f}")

    with st.expander("Exportar a PDF"):
        if st.button("Generar PDF"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(200, 10, "Reporte de Proyecto - SmartBuild Perú", ln=True, align="C")
            pdf.set_font("Arial", size=12)
            pdf.ln(10)
            pdf.multi_cell(0, 10, f"""
Ubicación: {ubicacion}
Área: {area} m²
Acabado: {acabado.title()}
Pisos: {pisos}
Tipo de terreno: {terreno}

Costo de construcción: S/ {costo_construccion:,.2f}
Costo del terreno: S/ {costo_terreno:,.2f}
Total estimado: S/ {costo_total:,.2f}
            """)
            output_path = "/mnt/data/reporte_smartbuild.pdf"
            pdf.output(output_path)
            st.success("PDF generado con éxito.")
            st.download_button("Descargar PDF", data=open(output_path, "rb"), file_name="SmartBuild_Reporte.pdf")

# --- Historial (simple cache local) ---
if "historial" not in st.session_state:
    st.session_state.historial = []

if st.button("Guardar este cálculo"):
    st.session_state.historial.append((ubicacion, area, acabado, pisos, costo_total))

if st.session_state.historial:
    st.markdown("### Historial de proyectos:")
    for idx, (ubi, a, ac, pi, total) in enumerate(st.session_state.historial, 1):
        st.markdown(f"{idx}. {ubi} | {a} m² | {ac} | {pi} pisos | Total: S/ {total:,.2f}")
