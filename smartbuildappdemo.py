import streamlit as st

st.set_page_config(page_title="SmartBuild PRO", layout="centered")

st.title("SmartBuild PRO: Cálculo de Materiales de Construcción")

st.subheader("Ingrese los datos de su proyecto:")

area = st.number_input("Área construida (m²)", min_value=1, step=1)

if area:
    # Factores reales por m²
    factores = {
        "Cemento (bolsas)": 1,
        "Arena (m³)": 0.25,
        "Piedra (m³)": 0.12,
        "Acero (kg)": 12,
        "Ladrillos (unidades)": 120
    }

    st.subheader("Materiales Estimados:")

    for material, factor in factores.items():
        cantidad = round(area * factor, 2)
        st.write(f"{material}: {cantidad}")

    st.success("Cálculo completado con datos reales de referencia.")

    # Exportar como texto plano
    if st.button("Exportar como archivo .txt"):
        with open("reporte_materiales.txt", "w") as f:
            f.write(f"Presupuesto para {area} m²:\n\n")
            for material, factor in factores.items():
                cantidad = round(area * factor, 2)
                f.write(f"{material}: {cantidad}\n")
        st.download_button("Descargar reporte", data=open("reporte_materiales.txt", "rb"), file_name="reporte_materiales.txt")

else:
    st.info("Ingrese un área válida para comenzar.")
