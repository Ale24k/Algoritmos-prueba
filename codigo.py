import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Asumiendo que los usuarios están almacenados en este formato
USERS = {
    'user1': {'password': 'pass1', 'ciclo_actual': '2', 'cursos_aprobados': ['C001', 'C002', 'C003']}
}

def verify_login(username, password):
    """Verifica las credenciales del usuario."""
    user_info = USERS.get(username)
    if user_info and user_info['password'] == password:
        return user_info
    return None

def draw_graph(df, user_info):
    """Dibuja el grafo con los cursos aprobados marcados en verde."""
    G = nx.from_pandas_edgelist(df, 'Código', 'Codigo_del_Requisito', create_using=nx.DiGraph())
    ciclo_actual = int(user_info['ciclo_actual'])
    cursos_aprobados = user_info['cursos_aprobados']

    # Dibujar el grafo
    pos = nx.spring_layout(G)
    color_map = []
    for node in G:
        if node in cursos_aprobados:
            color_map.append('green')  # Curso aprobado
        else:
            color_map.append('red')  # Curso no aprobado

    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, node_color=color_map, with_labels=True, arrowstyle='->', arrowsize=10)
    st.pyplot(plt)

def main():
    st.title("Sistema de Visualización de Cursos")

    # Sección de carga de archivo
    uploaded_file = st.sidebar.file_uploader("Subir archivo CSV o Excel", type=['csv', 'xlsx'])
    df = None
    if uploaded_file:
        # Leer el archivo como un objeto buffer
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, engine='python')  # Usar el motor Python si hay problemas con el motor C
        else:
            df = pd.read_excel(uploaded_file)

    # Sección de login
    with st.sidebar:
        st.subheader("Login")
        username = st.text_input("Nombre de Usuario")
        password = st.text_input("Contraseña", type="password")
        login_button = st.button("Iniciar Sesión")

    if login_button:
        user_info = verify_login(username, password)
        if user_info and df is not None:
            st.success("Inicio de sesión exitoso")
            draw_graph(df, user_info)
        elif not user_info:
            st.error("Credenciales incorrectas")
        elif df is None:
            st.error("Por favor, carga un archivo antes de iniciar sesión")

if __name__ == "__main__":
    main()
