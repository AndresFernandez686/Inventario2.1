# UI y lógica de empleados (Inventario, delivery)
import streamlit as st
from datetime import date
from utils import df_to_csv_bytes

def empleado_inventario_ui(inventario, usuario, opciones_valde, guardar_inventario, guardar_historial):
    st.header("Inventario")
    fecha_carga = st.date_input("Selecciona la fecha de carga", value=date.today(), key="fecha_inv")

    tabs = st.tabs(list(inventario.keys()))
    
    # Inicializar registro de productos cargados si no existe
    if "productos_cargados" not in st.session_state:
        st.session_state.productos_cargados = {}
        
    for i, categoria in enumerate(inventario.keys()):
        with tabs[i]:
            productos = inventario[categoria]
            producto_seleccionado = st.selectbox(
                f"Producto de {categoria}",
                list(productos.keys()),
                key=f"sel_{categoria}"
            )

            # Eliminamos la opción de modo de actualización (Añadir/Reemplazar)
            # Ahora solo se permite modificación directa

            if categoria == "Por Kilos":
                st.markdown("### Selecciona la cantidad de baldes a registrar:")
                num_baldes = st.number_input(
                    "Cantidad de baldes",
                    min_value=1,
                    max_value=6,
                    value=6,
                    step=1,
                    key=f"num_baldes_{producto_seleccionado}_{fecha_carga}_{usuario}"
                )
                st.markdown(f"### Estado de hasta {num_baldes} baldes:")

                estados_baldes = []
                for n in range(1, num_baldes + 1):
                    key_balde = f"{producto_seleccionado}_balde_{n}_{fecha_carga}_{usuario}"
                    # Inicializa el valor solo si no existe
                    if key_balde not in st.session_state:
                        valor_guardado = None
                        if isinstance(productos[producto_seleccionado], list) and len(productos[producto_seleccionado]) >= n:
                            valor_guardado = productos[producto_seleccionado][n-1]
                        st.session_state[key_balde] = valor_guardado if valor_guardado is not None else "Vacío"
                    opcion = st.selectbox(
                        f"Balde {n}",
                        list(opciones_valde.keys()),
                        index=list(opciones_valde.keys()).index(st.session_state[key_balde]) if st.session_state[key_balde] in opciones_valde else 0,
                        key=key_balde
                    )
                    estados_baldes.append(opcion)

                if st.button(
                    f"Actualizar {producto_seleccionado} ({categoria})",
                    key=f"btn_{categoria}_{producto_seleccionado}"
                ):
                    # Solo guarda los baldes seleccionados
                    productos[producto_seleccionado] = estados_baldes.copy()
                    guardar_inventario(inventario)
                    
                    # Registrar que este producto fue actualizado por el usuario
                    if categoria not in st.session_state.productos_cargados:
                        st.session_state.productos_cargados[categoria] = {}
                    st.session_state.productos_cargados[categoria][producto_seleccionado] = estados_baldes
                    
                    guardar_historial(
                        fecha_carga, usuario, categoria, producto_seleccionado, estados_baldes, "Modificar"
                    )
                    st.success(f"Actualizado. Estado actual: {', '.join(estados_baldes)}")

                # Mostrar solo productos cargados por este empleado en esta sesión
                if st.session_state.productos_cargados.get(categoria):
                    st.subheader("Productos que has cargado:")
                    for p, c in st.session_state.productos_cargados[categoria].items():
                        if isinstance(c, list):
                            estados_no_vacios = [x for x in c if x != "Vacío"]
                            estados_vacios = [x for x in c if x == "Vacío"]
                            if estados_no_vacios:
                                st.write(f"- {p}: {', '.join(estados_no_vacios)}")
                            else:
                                st.write(f"- {p}: Todos vacíos")
                        else:
                            st.write(f"- {p}: {c}")

            else:
                cantidad = st.number_input("Cantidad (unidades)", min_value=0, step=1, key=f"cant_{categoria}_{producto_seleccionado}")
                if st.button(
                    f"Actualizar {producto_seleccionado} ({categoria})",
                    key=f"btn_{categoria}_{producto_seleccionado}"
                ):
                    cantidad = max(0, int(cantidad))
                    # Siempre reemplaza el valor (ya no hay opción de añadir)
                    productos[producto_seleccionado] = cantidad
                    guardar_inventario(inventario)
                    
                    # Registrar que este producto fue actualizado por el usuario
                    if categoria not in st.session_state.productos_cargados:
                        st.session_state.productos_cargados[categoria] = {}
                    st.session_state.productos_cargados[categoria][producto_seleccionado] = cantidad
                    
                    guardar_historial(
                        fecha_carga, usuario, categoria, producto_seleccionado, cantidad, "Modificar"
                    )
                    st.success(f"Actualizado. Nuevo stock: {productos[producto_seleccionado]}")

                # Mostrar solo productos cargados por este empleado en esta sesión
                if st.session_state.productos_cargados.get(categoria):
                    st.subheader("Productos que has cargado:")
                    for p, c in st.session_state.productos_cargados[categoria].items():
                        st.write(f"- {p}: {c if c > 0 else 'Vacío'}")

def empleado_delivery_ui(usuario, cargar_catalogo_delivery, guardar_venta_delivery, cargar_ventas_delivery):
    st.header("Delivery")
    catalogo = cargar_catalogo_delivery()
    activos = [item for item in catalogo if item.get("activo", True)]

    if not activos:
        st.info("No hay productos de delivery activos. Pide al administrador que agregue opciones.")
        return

    fecha_venta = st.date_input("Fecha de la venta", value=date.today(), key="fecha_deliv")
    opciones = [f"{it['nombre']} {'(PROMO)' if it.get('es_promocion', False) else ''}" for it in activos]
    seleccion = st.selectbox("Producto de delivery", opciones)
    idx = opciones.index(seleccion)
    item_sel = activos[idx]
    cantidad = st.number_input("Cantidad vendida", min_value=1, step=1)

    if st.button("Registrar venta de delivery"):
        guardar_venta_delivery(
            fecha_venta,
            usuario,
            item_sel["nombre"],
            cantidad,
            item_sel.get("es_promocion", False)
        )
        st.success("Venta registrada con éxito ✅")

    ventas = cargar_ventas_delivery()
    if not ventas.empty:
        ventas_hoy = ventas[(ventas["Usuario"] == usuario) & (ventas["Fecha"].dt.date == date.today())]
        if not ventas_hoy.empty:
            st.subheader("Tus ventas de delivery hoy")
            st.dataframe(ventas_hoy)
