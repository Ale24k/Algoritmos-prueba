from pyvis.network import Network
import pandas as pd
import streamlit as st
import networkx as nx

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

from pyvis.network import Network
import pandas as pd
import streamlit as st
import networkx as nx

def draw_graph(df, user_info):
    """Dibuja el grafo con los cursos aprobados y los cursos que el usuario puede tomar, mostrando conexiones directas de requisitos."""
    ciclo_actual = int(user_info['ciclo_actual'])
    cursos_aprobados = set(user_info['cursos_aprobados'])

    df['Ciclo'] = pd.to_numeric(df['Ciclo'], errors='coerce')
    df['Código'] = df['Código'].astype(str).str.strip()
    df['Nombre Requisito'] = df['Nombre Requisito'].astype(str).str.strip()

    # Filtrar cursos que están dentro de 3 ciclos adelante del actual
    df_filtrado = df[df['Ciclo'] <= ciclo_actual + 3]

    # Crear el grafo dirigido
    G = nx.DiGraph()
    for index, row in df_filtrado.iterrows():
        if row['Código'] not in G.nodes():
            G.add_node(row['Código'], title=row['Código'], color='gray') 

        if pd.notna(row['Nombre Requisito']):
            if row['Nombre Requisito'] in cursos_aprobados:
                if row['Código'] not in cursos_aprobados:
                    G.add_edge(row['Nombre Requisito'], row['Código'])
                    G.nodes[row['Código']]['color'] = 'blue'  # Curso accesible
            G.add_node(row['Nombre Requisito'], title=row['Nombre Requisito'], color='green' if row['Nombre Requisito'] in cursos_aprobados else 'gray')

    nodos_mostrados = G.nodes()
    df_mostrados = df[df['Código'].isin(nodos_mostrados)].copy()
    df_mostrados = df_mostrados[['Ciclo', 'Código', 'Nombre']].drop_duplicates().sort_values(by='Ciclo')
    
    st.write("Cursos Mostrados en el Grafo")
    st.dataframe(df_mostrados)

    net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")

    for node, node_attrs in G.nodes(data=True):
        net.add_node(node, title=node, color=node_attrs['color'])
    for edge in G.edges:
        net.add_edge(edge[0], edge[1])

    net.save_graph("graph.html")
    HtmlFile = open("graph.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    st.components.v1.html(source_code, height=800)

def main():
    st.title("Sistema de Visualización de Cursos")

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if st.session_state['logged_in']:
        # Botón de cierre de sesión
        if st.sidebar.button("Cerrar Sesión"):
            st.session_state['logged_in'] = False
            st.session_state['user_info'] = None
            st.experimental_rerun()

        uploaded_file = st.sidebar.file_uploader("Subir archivo CSV o Excel", type=['csv', 'xlsx'])
        if uploaded_file:
            # Asegurarse de leer el archivo correcto en función de su extensión
            df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
            draw_graph(df, st.session_state['user_info'])

    else:
        # Ingreso de datos de usuario
        username = st.sidebar.text_input("Nombre de Usuario")
        password = st.sidebar.text_input("Contraseña", type="password")

        if st.sidebar.button("Iniciar Sesión"):
            user_info = verify_login(username, password)
            if user_info:
                st.session_state['logged_in'] = True
                st.session_state['user_info'] = user_info
                st.experimental_rerun()
            else:
                st.error("Credenciales incorrectas")

if __name__ == "__main__":
    main()
