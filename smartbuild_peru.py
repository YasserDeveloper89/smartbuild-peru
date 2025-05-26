
import streamlit as st
from fpdf import FPDF

st.set_page_config(page_title="SmartBuild Perú PRO", layout="wide")

st.title("SmartBuild Perú PRO - Estimador de Costos de Construcción")

# Parámetros
ubicaciones = {
    "Lima": 1600,
    "Arequipa": 1400,
    "Cusco": 1300,
    "Piura": 1250,
    "Trujillo": 1350
}

precios_terreno = {
    "Urbano consolidado": 500,
    "Semiurbano": 300,
    "Rural": 150
}

acabados = {
    "Básico": 1.0,
    "Estándar": 1.2,
    "Premium": 1.5
}

materiales = {
    "Cemento (bolsas)": 0.2,
    "Arena (m3)": 0.15,
    "Ladrillos (unidades)": 30,
    "Fierro (kg)": 20
}

# Estado de historial
if 'historial' not in st.session_state:
    st.session_state.historial = []

st.sidebar.header("Parámetros del proyecto")
ubicacion = st.sidebar.selectbox("Ubicación", list(ubicaciones.keys()))
area = st.sidebar.slider("Área a construir (m²)", 30, 500, 100)
pisos = st.sidebar.selectbox("Cantidad de pisos", [1, 2, 3])
acabado = st.sidebar.radio("Tipo de acabado", list(acabados.keys()))
terreno = st.sidebar.radio("Tipo de terreno", list(precios_terreno.keys()))

def calcular_costo_total(area, acabado, pisos, terreno, ubicacion):
    base = ubicaciones[ubicacion]
    modificador = acabados[acabado]
    terreno_costo = precios_terreno[terreno] * area
    construccion = base * area * modificador * pisos
    return construccion + terreno_costo

def estimar_materiales(area, pisos):
    return {
        "Cemento (bolsas)": int(area * pisos * materiales["Cemento (bolsas)"]),
        "Arena (m3)": round(area * pisos * materiales["Arena (m3)"], 1),
        "Ladrillos (unidades)": int(area * pisos * materiales["Ladrillos (unidades)"]),
        "Fierro (kg)": int(area * pisos * materiales["Fierro (kg)"])
    }

st.header("Resultado del Presupuesto")

if st.button("Calcular presupuesto"):
    costo_total = calcular_costo_total(area, acabado, pisos, terreno, ubicacion)
    st.session_state.costo_actual = costo_total
    materiales_estimados = estimar_materiales(area, pisos)

    st.subheader(f"Costo estimado total: S/ {costo_total:,.2f}")
    st.write("**Detalle de materiales estimados:**")
    st.table(materiales_estimados)

    st.session_state.materiales_actuales = materiales_estimados

if st.button("Guardar este cálculo"):
    if 'costo_actual' in st.session_state:
        st.session_state.historial.append({
            "ubicacion": ubicacion,
            "area": area,
            "acabado": acabado,
            "pisos": pisos,
            "terreno": terreno,
            "costo": st.session_state.costo_actual,
            "materiales": st.session_state.materiales_actuales
        })
        st.success("Cálculo guardado en historial.")
    else:
        st.warning("Primero realiza un cálculo.")

st.subheader("Historial")
for i, item in enumerate(st.session_state.historial):
    st.markdown(f"**Proyecto {i+1}** - {item['ubicacion']}, {item['area']} m², {item['pisos']} pisos")
    st.write(f"Costo: S/ {item['costo']:,.2f}")
    with st.expander("Ver materiales"):
        st.table(item["materiales"])

# Exportar PDF
def exportar_pdf(info):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Resumen del Presupuesto - SmartBuild Perú", ln=1, align='C')
    for k, v in info.items():
        if k != "materiales":
            pdf.cell(200, 10, txt=f"{k.capitalize()}: {v}", ln=1)
    pdf.ln(5)
    pdf.cell(200, 10, txt="Materiales estimados:", ln=1)
    for mat, val in info["materiales"].items():
        pdf.cell(200, 10, txt=f"{mat}: {val}", ln=1)
    path = "/mnt/data/reporte_smartbuild.pdf"
    pdf.output(path)
    return path

if st.button("Exportar último presupuesto en PDF"):
    if st.session_state.historial:
        ruta = exportar_pdf(st.session_state.historial[-1])
        st.success("PDF generado.")
        with open(ruta, "rb") as file:
            st.download_button("Descargar PDF", file, file_name="presupuesto_smartbuild.pdf")
    else:
        st.warning("No hay cálculos guardados aún.")
