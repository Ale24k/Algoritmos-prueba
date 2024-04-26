import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network

USERS = {
    '72721479': {'password': 'ola123', 'ciclo_actual': '2', 'cursos_aprobados': ['C0090', 'C0613', 'C0659','C0737','C0201','C8189']}
}

def verify_login(username, password):
    user_info = USERS.get(username)
    if user_info and user_info['password'] == password:
        return user_info
    return None

def draw_graph(df, user_info):
    """Dibuja el grafo con los cursos aprobados y los cursos que el usuario puede tomar."""
    # Convertir ciclos a enteros para comparaciones
    df['Ciclo'] = pd.to_numeric(df['Ciclo'], errors='coerce')

    # Filtrar cursos que están dentro de 3 ciclos adelante
    ciclo_actual = int(user_info['ciclo_actual'])
    df_filtrado = df[df['Ciclo'] <= ciclo_actual + 3]

    # Crear el grafo
    G = nx.from_pandas_edgelist(df_filtrado, 'Código', 'Codigo_del_Requisito', create_using=nx.DiGraph())
    net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")

    # Determinar cursos accesibles basados en requisitos cumplidos
    cursos_accesibles = set(user_info['cursos_aprobados'])  # Comenzar con cursos aprobados
    for _, row in df_filtrado.iterrows():
        if row['Codigo_del_Requisito'] in cursos_accesibles or pd.isna(row['Codigo_del_Requisito']):
            cursos_accesibles.add(row['Código'])

    # Añadir nodos con colores correspondientes
    for node in G.nodes:
        if node in user_info['cursos_aprobados']:
            net.add_node(node, title=node, color='green')  # Verde para aprobados
        elif node in cursos_accesibles:
            net.add_node(node, title=node, color='blue')  # Azul para accesibles
        else:
            net.add_node(node, title=node, color='gray')  # Gris para no accesibles

    # Añadir aristas
    for edge in G.edges:
        net.add_edge(edge[0], edge[1])

    # Mostrar el grafo
    net.show("graph.html")
    st.components.v1.html(net.html, height=800)

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
