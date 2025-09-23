#Logica y datos de usuarios
import streamlit as st

usuarios = {
    'empleado1': 'empleado',
    'empleado2': 'empleado',
    'empleado3': 'empleado',
    'admin1': 'administrador'
}

def login():
    # Inicializar session_state si no existe
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['usuario'] = None
        st.session_state['rol'] = None
    
    # Si el usuario ya está autenticado, devolver los datos de sesión
    if st.session_state['logged_in']:
        return st.session_state['usuario'], st.session_state['rol']
    
    # Si no está autenticado, mostrar el formulario de inicio de sesión
    # Usar columnas para centrar el formulario
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.title("Inicio de sesión")
        usuario = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        login_button = st.button("Ingresar")
        
        if login_button:
            if usuario in usuarios:
                rol = usuarios[usuario]
                st.success(f"Hola {usuario}, rol: {rol}")
                
                # Guardar datos en session_state
                st.session_state['logged_in'] = True
                st.session_state['usuario'] = usuario
                st.session_state['rol'] = rol
                
                # Recargar la página para actualizar la interfaz
                st.rerun()
            else:
                st.error("Usuario no reconocido")
    
    # Si llegamos aquí, el usuario no se ha autenticado
    return None, None

def logout():
    # Limpiar session_state
    st.session_state['logged_in'] = False
    st.session_state['usuario'] = None
    st.session_state['rol'] = None
    st.rerun()
                st.success(f"Hola {usuario}, rol: {rol}")
            else:
                st.error("Usuario no reconocido")
        
    return usuario, rol
