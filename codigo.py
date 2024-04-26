import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Simulando una base de datos de usuarios
usuarios = {
    '12345678': {'nombre': 'Juan Perez', 'ciclo': 2, 'cursos_aprobados': ['C0090', 'C0613']},
    '12345679': {'nombre': 'Juan Perez', 'ciclo': 2, 'cursos_aprobados': ['C0659', 'C0613']},
    
}

def crear_grafo(df_malla):
    G = nx.DiGraph()
    for _, row in df_malla.iterrows():
        G.add_node(row['Código'], nombre=row['Nombre'])
        if row['Requisito'] != 'Ninguno':
            G.add_edge(row['Requisito'], row['Código'])
    return G

def visualizar_grafo(G, cursos_aprobados):
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=500, node_color='lightblue', font_size=8)
    plt.show()

# Streamlit UI
st.title('Sistema de Gestión de Cursos')
dni_input = st.text_input("Ingresa tu DNI:")
archivo_curricular = st.file_uploader("Carga el plan de estudios de tu carrera en formato CSV", type=['csv'])

if st.button('Iniciar Sesión y Cargar Plan de Estudios'):
    if dni_input in usuarios and archivo_curricular is not None:
        usuario = usuarios[dni_input]
        st.success(f"Bienvenido {usuario['nombre']}")

        # Leer el archivo CSV y crear el DataFrame
        df_malla = pd.read_csv(archivo_curricular)
        G = crear_grafo(df_malla)

        # Visualizar el grafo en base a los cursos aprobados
        visualizar_grafo(G, usuario['cursos_aprobados'])
    else:
        st.error("Por favor verifica el DNI o asegúrate de haber cargado el archivo CSV.")
