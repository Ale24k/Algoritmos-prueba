import streamlit as st
import pandas as pd

# Simulando una base de datos de usuarios
usuarios = pd.DataFrame({
    'DNI': ['12345678', '87654321'],
    'Nombre': ['Juan Perez', 'Ana Lopez'],
    'Ciclo': [2, 3],
    'CursosAprobados': [['C001,C002,C003,C004,C005'], ['C001', 'C002', 'C008']]
})

# Configuración de la página de Streamlit
st.title('Login para Sistema de Gestión de Cursos')

# Campo para ingresar el DNI
dni_input = st.text_input("Ingresa tu DNI:")

# Botón para iniciar sesión
if st.button('Iniciar Sesión'):
    usuario = usuarios[usuarios['DNI'] == dni_input]
    if not usuario.empty:
        # Usuario autenticado
        st.success(f"Bienvenido {usuario.iloc[0]['Nombre']}")
        # Aquí podrías añadir más funcionalidad, como mostrar los cursos aprobados
        st.write("Cursos Aprobados:", usuario.iloc[0]['CursosAprobados'])
    else:
        # Fallo en la autenticación
        st.error("DNI no encontrado. Por favor verifica e intenta de nuevo.")
