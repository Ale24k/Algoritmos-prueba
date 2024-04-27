import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network

# Datos de ejemplo para usuarios
USERS = {
    '72721479': {'password': 'ola123', 'ciclo_actual': '2', 'cursos_aprobados': ['C0090', 'C0613', 'C0659','C0737','C0201','C8189']},
    '71715585': {'password': 'ola123', 'ciclo_actual': '3', 'cursos_aprobados': ['C0090', 'C0613', 'C0659','C0737','C0201','C8189','C0614','C0657','C0622','C8190','C8191','C0667']}

}

def verify_login(username, password):
    """ Verifica las credenciales del usuario. """
    user_info = USERS.get(username)
    if user_info and user_info['password'] == password:
        return user_info
    return None

def draw_graph(df, user_info):
    """Dibuja el grafo con los cursos aprobados y los cursos que el usuario puede tomar, mostrando nombres en los nodos."""
    ciclo_actual = int(user_info['ciclo_actual'])
    cursos_aprobados = set(user_info['cursos_aprobados'])

    # Verificar si las columnas necesarias existen en el DataFrame
    required_columns = ['Ciclo', 'Código', 'Codigo_del_Requisito', 'Nombre']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        st.error(f"Faltan las siguientes columnas en el archivo cargado: {', '.join(missing_columns)}")
        return  # Detener la ejecución si faltan columnas

    # Convertir ciclos a enteros y limpiar códigos de curso para consistencia
    df['Ciclo'] = pd.to_numeric(df['Ciclo'], errors='coerce')
    df['Código'] = df['Código'].astype(str).str.strip()
    df['Nombre'] = df['Nombre'].astype(str).str.strip()
    df['Codigo_del_Requisito'] = df['Codigo_del_Requisito'].astype(str).str.strip()

    # Filtrar cursos que están dentro de 3 ciclos adelante
    df_filtrado = df[df['Ciclo'] <= ciclo_actual + 3]

    # Crear el grafo
    G = nx.from_pandas_edgelist(df_filtrado, 'Código', 'Codigo_del_Requisito', create_using=nx.DiGraph())
    net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")

    # Determinar cursos accesibles basados en requisitos cumplidos
    cursos_accesibles = cursos_aprobados.copy()
    for _, row in df_filtrado.iterrows():
        if row['Codigo_del_Requisito'] in cursos_accesibles or row['Codigo_del_Requisito'] == 'nan':
            cursos_accesibles.add(row['Código'])

    # Añadir nodos con colores correspondientes y título con el nombre del curso
    for node in G.nodes:
        nombre_curso = df_filtrado.loc[df_filtrado['Código'] == node, 'Nombre'].values[0] if 'Nombre' in df_filtrado.columns else "Nombre desconocido"
        color = 'green' if node in cursos_aprobados else 'blue' if node in cursos_accesibles else 'gray'
        titulo = f"{node}: {nombre_curso}"
        net.add_node(node, title=titulo, color=color)

    # Añadir aristas
    for edge in G.edges:
        net.add_edge(edge[0], edge[1])

    # Guardar y mostrar el grafo
    net.save_graph("graph.html")
    HtmlFile = open("graph.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    st.components.v1.html(source_code, height=800)


def main():
    st.title("Sistema de Visualización de Cursos")

    username = st.sidebar.text_input("Nombre de Usuario")
    password = st.sidebar.text_input("Contraseña", type="password")
    uploaded_file = st.sidebar.file_uploader("Subir archivo CSV o Excel", type=['csv', 'xlsx'])

    if st.sidebar.button("Iniciar Sesión"):
        user_info = verify_login(username, password)
        if user_info:
            if uploaded_file:
                df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
                draw_graph(df, user_info)
            else:
                st.error("Por favor, carga un archivo antes de iniciar sesión")
        else:
            st.error("Credenciales incorrectas")

if __name__ == "__main__":
    main()
