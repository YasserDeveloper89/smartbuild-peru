import streamlit as st
from fpdf import FPDF
import pydeck as pdk

# Título
st.title("SmartBuild Perú - Estimación de Presupuesto")

# Entrada de datos
ubicacion = st.selectbox("Ubicación del terreno", ["Lima", "Arequipa", "Cusco", "Trujillo", "Otro"])
area = st.number_input("Área (m²)", min_value=10.0, max_value=1000.0, value=100.0, step=10.0)
acabado = st.selectbox("Tipo de acabado", ["Económico", "Estándar", "Premium"])
pisos = st.number_input("Cantidad de pisos", min_value=1, max_value=5, value=1)

# Costos por m2 base y multiplicadores por acabado
costos_base = {"Lima": 1000, "Arequipa": 950, "Cusco": 900, "Trujillo": 920, "Otro": 850}
multiplicador = {"Económico": 1.0, "Estándar": 1.3, "Premium": 1.7}
riesgo_sismico = {"Lima": "Alto", "Arequipa": "Muy Alto", "Cusco": "Medio", "Trujillo": "Alto", "Otro": "Desconocido"}
clima = {"Lima": "Templado, poca lluvia", "Arequipa": "Seco, templado", "Cusco": "Frío, lluvia frecuente", "Trujillo": "Templado, algo húmedo", "Otro": "Variable"}

if st.button("Calcular presupuesto"):
    costo_m2 = costos_base[ubicacion] * multiplicador[acabado]
    total = costo_m2 * area * pisos

    # Estimaciones de materiales
    cemento = round(area * pisos * 0.2, 2)
    arena = round(area * pisos * 0.15, 2)
    fierro = round(area * pisos * 10, 2)
    ladrillo = round(area * pisos * 120, 2)

    # Duración estimada (simplificada)
    duracion_meses = round((area * pisos) / 1000 * 3, 1)

    st.success(f"Presupuesto estimado: S/ {total:,.2f}")
    st.subheader("Materiales estimados")
    st.write(f"- Cemento: {cemento} bolsas")
    st.write(f"- Arena: {arena} m³")
    st.write(f"- Fierro: {fierro} kg")
    st.write(f"- Ladrillo: {ladrillo} unidades")

    st.subheader("Duración estimada de la obra")
    st.write(f"**{duracion_meses} meses**")

    st.subheader("Condiciones locales")
    st.write(f"- **Clima típico**: {clima[ubicacion]}")
    st.write(f"- **Riesgo sísmico**: {riesgo_sismico[ubicacion]}")

    # Mapa simple con coordenadas fijas por ciudad
    coordenadas = {
        "Lima": (-12.0464, -77.0428),
        "Arequipa": (-16.4090, -71.5375),
        "Cusco": (-13.5319, -71.9675),
        "Trujillo": (-8.1120, -79.0288),
        "Otro": (-12.0, -76.9)
    }

    lat, lon = coordenadas[ubicacion]
    st.subheader("Ubicación en el mapa")
    st.pydeck_chart(pdk.Deck(
        map_style="mapbox://styles/mapbox/streets-v11",
        initial_view_state=pdk.ViewState(latitude=lat, longitude=lon, zoom=11, pitch=50),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=[{"position": [lon, lat], "size": 100}],
                get_position="position",
                get_color="[200, 30, 0, 160]",
                get_radius="size",
            ),
        ],
    ))

    # PDF
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
    pdf.cell(200, 10, f"Duración estimada: {duracion_meses} meses", ln=True)
    pdf.ln(10)
    pdf.cell(200, 10, "Materiales:", ln=True)
    pdf.cell(200, 10, f"Cemento: {cemento} bolsas", ln=True)
    pdf.cell(200, 10, f"Arena: {arena} m³", ln=True)
    pdf.cell(200, 10, f"Fierro: {fierro} kg", ln=True)
    pdf.cell(200, 10, f"Ladrillo: {ladrillo} unidades", ln=True)
    pdf.cell(200, 10, f"Clima típico: {clima[ubicacion]}", ln=True)
    pdf.cell(200, 10, f"Riesgo sísmico: {riesgo_sismico[ubicacion]}", ln=True)

    pdf_data = pdf.output(dest='S').encode('latin1')
    st.download_button(
        label="Descargar presupuesto PDF",
        data=pdf_data,
        file_name="presupuesto_smartbuild.pdf",
        mime="application/pdf"
    )
