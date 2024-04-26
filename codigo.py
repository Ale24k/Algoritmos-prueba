import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from pyvis.network import Network

USERS = {
    '72721479': {'password': 'ola123', 'ciclo_actual': '2', 'cursos_aprobados': ['C0090', 'C0613', 'C0659','C0737','C0201','C8189']}
}

def verify_login(username, password):
    user_info = USERS.get(username)
    if user_info and user_info['password'] == password:
        return user_info
    return None

def draw_graph_nx(df, user_info):
    G = nx.from_pandas_edgelist(df, 'Código', 'Codigo_del_Requisito', create_using=nx.DiGraph())
    pos = nx.spring_layout(G, k=0.75)  # Aumenta el parámetro k para más espacio entre nodos
    color_map = ['green' if node in user_info['cursos_aprobados'] else 'red' for node in G]
    
    plt.figure(figsize=(12, 12))  # Aumenta el tamaño para una mejor visualización
    nx.draw(G, pos, node_color=color_map, with_labels=True, node_size=700, font_size=10)
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
