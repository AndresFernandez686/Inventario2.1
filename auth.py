# Logica y datos de usuarios
import streamlit as st

usuarios = {
    'empleado1': {'password': 'clave123', 'rol': 'empleado'},
    'empleado2': {'password': 'clave123', 'rol': 'empleado'},
    'empleado3': {'password': 'clave123', 'rol': 'empleado'},
    'admin1': {'password': 'admin123', 'rol': 'administrador'}
}

def login():
    # Agregar CSS personalizado para centrar el contenido
    st.markdown("""
        <style>
        .login-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            background-color: #f8f9fa;
        }
        .title-centered {
            text-align: center;
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Crear una estructura de columnas para centrar el contenido
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<h2 class="title-centered">Inicio de sesión</h2>', unsafe_allow_html=True)
        
        usuario = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        
        login_button = st.button("Ingresar")
        
        rol = None
        if login_button:
            if usuario in usuarios and usuarios[usuario]['password'] == password:
                rol = usuarios[usuario]['rol']
                st.success(f"Hola {usuario}, rol: {rol}")
            else:
                st.error("Usuario o contraseña incorrectos")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    return usuario, rol
