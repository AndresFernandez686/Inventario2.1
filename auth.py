#Logica y datos de usuarios
import streamlit as st

usuarios = {
    'empleado1': 'empleado',
    'empleado2': 'empleado',
    'empleado3': 'empleado',
    'admin1': 'administrador'
}

def login():
    st.sidebar.title("Inicio de sesión")
    usuario = st.sidebar.text_input("Usuario (ej: empleado1, admin1)")
    rol = None
    if usuario in usuarios:
        rol = usuarios[usuario]
        st.sidebar.success(f"Hola {usuario}, rol: {rol}")
    elif usuario:
        st.sidebar.error("Usuario no reconocido")
    return usuario, rol
