#Logica y datos de usuarios
import streamlit as st

usuarios = {
    'empleado1': 'empleado',
    'empleado2': 'empleado',
    'empleado3': 'empleado',
    'admin1': 'administrador'
}

def login():
    # Usar columnas para centrar el formulario
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.title("Inicio de sesión")
        usuario = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        login_button = st.button("Ingresar")
        
        rol = None
        if login_button:
            if usuario in usuarios:
                rol = usuarios[usuario]
                st.success(f"Hola {usuario}, rol: {rol}")
            else:
                st.error("Usuario no reconocido")
        
    return usuario, rol
