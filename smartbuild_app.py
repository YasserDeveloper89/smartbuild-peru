
import streamlit as st

st.set_page_config(page_title="SmartBuild Perú", layout="centered")

st.title("SmartBuild Perú")
st.subheader("Estimador inteligente de materiales de construcción")

# Inputs
area = st.number_input("Área construida (m²)", min_value=10, max_value=1000, step=10)

structure_type = st.selectbox("Tipo de estructura", ["Casa", "Oficina", "Local comercial"])

efficiency = st.radio(
    "Nivel de eficiencia energética",
    ["Económico", "Balanceado", "Sostenible"]
)

# Estimaciones base por m²
material_factors = {
    "Cemento (bolsas)": 0.25,
    "Ladrillos (unidades)": 12,
    "Acero (kg)": 2
}

costs_per_unit = {
    "Cemento (bolsas)": 30,
    "Ladrillos (unidades)": 1.2,
    "Acero (kg)": 10
}

if st.button("Calcular estimación"):
    st.markdown("### Resultados estimados")

    results = []
    total_cost = 0

    for material, factor in material_factors.items():
        cantidad = round(area * factor)
        costo = round(cantidad * costs_per_unit[material])
        results.append((material, cantidad, costo))
        total_cost += costo

    # Mano de obra estimada
    labor_cost = int(area * 20)
    total_cost += labor_cost
    results.append(("Mano de obra", "-", labor_cost))

    # Mostrar tabla
    st.table({
        "Material": [r[0] for r in results],
        "Cantidad estimada": [r[1] for r in results],
        "Costo estimado (S/.)": [r[2] for r in results]
    })

    st.markdown(f"### **Costo total aproximado: S/. {total_cost}**")
    st.info("Valores aproximados según precios promedio del mercado peruano.")
