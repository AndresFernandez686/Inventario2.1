import streamlit as st
from datetime import date
from utils import df_to_csv_bytes
import pandas as pd

def admin_inventario_ui(inventario):
    # Muestra tablas para cada categoría y botones de descarga
    for categoria, productos in inventario.items():
        st.subheader(f"Categoría: {categoria}")
        
        # Crear DataFrame según la categoría
        if categoria == "Por Kilos":
            productos_csv = []
            for producto, baldes in productos.items():
                if isinstance(baldes, list):
                    estado_baldes = ", ".join(baldes)
                    llenos = sum(1 for b in baldes if b != "Vacío")
                    productos_csv.append({"Producto": producto, "Balde": estado_baldes, "Llenos": llenos})
                else:
                    productos_csv.append({"Producto": producto, "Balde": str(baldes), "Llenos": baldes if isinstance(baldes, (int, float)) else 0})
            df = pd.DataFrame(productos_csv)
        else:
            df = pd.DataFrame({
                "Producto": list(productos.keys()),
                "Cantidad": list(productos.values())
            })
        
        # Mostrar tabla
        st.dataframe(df)
        
        # Botón de descarga
        csv_bytes = df_to_csv_bytes(df)
        st.download_button(
            label=f"Descargar CSV de {categoria}",
            data=csv_bytes,
            file_name=f"inventario_{categoria.lower().replace(' ', '_')}.csv",
            mime="text/csv"
        )

def admin_historial_ui(historial_json):
    st.header("📅 Historial de cargas (por empleado / mes)")
    import pandas as pd

    # Validación robusta para evitar error DataFrame constructor not properly called!
    if not historial_json or not isinstance(historial_json, list) or not all(isinstance(e, dict) for e in historial_json):
        st.info("Aún no hay registros en el historial.")
        return

    historial = pd.DataFrame(historial_json)
    # Normaliza nombres columna
    if "fecha" in historial.columns:
        historial["Fecha"] = pd.to_datetime(historial["fecha"])
    if "usuario" in historial.columns:
        historial["Usuario"] = historial["usuario"]

    empleados = ["Todos"] + sorted(historial["Usuario"].dropna().unique().tolist())
    empleado_sel = st.selectbox("Empleado", empleados)
    año = st.number_input("Año", min_value=2000, max_value=2100, value=date.today().year)
    mes = st.number_input("Mes", min_value=1, max_value=12, value=date.today().month)

    filtro = historial[(historial["Fecha"].dt.year == año) & (historial["Fecha"].dt.month == mes)]
    if empleado_sel != "Todos":
        filtro = filtro[filtro["Usuario"] == empleado_sel]

    if not filtro.empty:
        st.dataframe(filtro.sort_values("Fecha"))
        csv_bytes = df_to_csv_bytes(filtro)
        st.download_button(
            label="Descargar historial filtrado (CSV)",
            data=csv_bytes,
            file_name=f"historial_{empleado_sel}_{mes:02d}_{año}.csv".replace(" ", "_"),
            mime="text/csv"
        )
    else:
        st.warning("No hay registros con ese filtro.")

def admin_delivery_ui(cargar_catalogo_delivery, guardar_catalogo_delivery, cargar_ventas_delivery):
    st.header("Gestión de Delivery (catálogo y ventas)")
    st.subheader("Catálogo de productos de delivery")
    catalogo = cargar_catalogo_delivery()

    with st.expander("Agregar nuevo producto de delivery"):
        nombre = st.text_input("Nombre del producto (ej: Promo 2x1 Chocolate)")
        es_promocion = st.checkbox("¿Es promoción?", value=False)
        activo = st.checkbox("Activo", value=True)
        if st.button("Guardar producto"):
            if not nombre.strip():
                st.error("El nombre no puede estar vacío.")
            else:
                if any(p["nombre"].lower() == nombre.strip().lower() for p in catalogo):
                    st.warning("Ya existe un producto con ese nombre.")
                else:
                    catalogo.append({
                        "nombre": nombre.strip(),
                        "es_promocion": bool(es_promocion),
                        "activo": bool(activo)
                    })
                    guardar_catalogo_delivery(catalogo)
                    st.success("Producto agregado al catálogo.")

    if catalogo:
        st.write("Productos actuales:")
        df_cat = pd.DataFrame(catalogo)
        st.dataframe(df_cat)

        st.subheader("Editar / Eliminar")
        nombres = [c["nombre"] for c in catalogo]
        sel = st.selectbox("Selecciona un producto", nombres)
        idx = nombres.index(sel)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            nuevo_activo = st.checkbox("Activo", value=catalogo[idx].get("activo", True), key=f"edit_activo_{idx}")
        with col2:
            nuevo_promo = st.checkbox("Promoción", value=catalogo[idx].get("es_promocion", False), key=f"edit_promo_{idx}")
        with col3:
            if st.button("Guardar cambios", key=f"save_{idx}"):
                catalogo[idx]["activo"] = nuevo_activo
                catalogo[idx]["es_promocion"] = nuevo_promo
                guardar_catalogo_delivery(catalogo)
                st.success("Cambios guardados.")
        with col4:
            if st.button("Eliminar producto", key=f"delete_{idx}"):
                catalogo.pop(idx)
                guardar_catalogo_delivery(catalogo)
                st.success("Producto eliminado del catálogo.")
    else:
        st.info("No hay productos en el catálogo.")

    st.divider()
    st.subheader("Ventas registradas de delivery")
    ventas_json = cargar_ventas_delivery()
    # Validación robusta para evitar error DataFrame constructor not properly called!
    if not ventas_json or not isinstance(ventas_json, list) or not all(isinstance(e, dict) for e in ventas_json):
        st.info("Aún no hay ventas registradas.")
        return

    ventas = pd.DataFrame(ventas_json)
    # Normaliza columnas
    if "fecha" in ventas.columns:
        ventas["Fecha"] = pd.to_datetime(ventas["fecha"])
    if "usuario" in ventas.columns:
        ventas["Usuario"] = ventas["usuario"]

    empleados = ["Todos"] + sorted(ventas["Usuario"].dropna().unique().tolist())
    año = st.number_input("Año (ventas)", min_value=2000, max_value=2100, value=date.today().year, key="anio_deliv")
    mes = st.number_input("Mes (ventas)", min_value=1, max_value=12, value=date.today().month, key="mes_deliv")

    filtro = ventas[(ventas["Fecha"].dt.year == año) & (ventas["Fecha"].dt.month == mes)]
    empleado_sel = st.selectbox("Empleado (ventas)", empleados)
    if empleado_sel != "Todos":
        filtro = filtro[filtro["Usuario"] == empleado_sel]

    if not filtro.empty:
        st.dataframe(filtro.sort_values("Fecha"))
