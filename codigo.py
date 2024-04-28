from pyvis.network import Network
import pandas as pd
import streamlit as st
import networkx as nx

# Asumiendo que este es el diccionario de usuarios con sus credenciales y cursos aprobados
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
    """Dibuja el grafo organizado por ciclos, con los cursos aprobados y los cursos que el usuario puede tomar."""
    ciclo_actual = int(user_info['ciclo_actual'])
    cursos_aprobados = set(user_info['cursos_aprobados'])

    # Convertir ciclos a enteros y limpiar códigos de curso para consistencia
    df['Ciclo'] = pd.to_numeric(df['Ciclo'], errors='coerce').fillna(0).astype(int)
    df['Código'] = df['Código'].astype(str).str.strip()
    df['Codigo_del_Requisito'] = df['Codigo_del_Requisito'].astype(str).str.strip()

    # Crear el grafo dirigido
    G = nx.DiGraph()

    # Preparar nodos con información completa para evitar errores
    for index, row in df.iterrows():
        G.add_node(row['Código'], label=row['Código'], level=int(row['Ciclo']),
                   color='blue' if row['Código'] in cursos_aprobados and pd.notna(row['Codigo_del_Requisito']) else 'gray')
        if pd.notna(row['Codigo_del_Requisito']):
            G.add_edge(row['Codigo_del_Requisito'], row['Código'])
            if row['Codigo_del_Requisito'] in cursos_aprobados:
                G.nodes[row['Código']]['color'] = 'green'

    # Inicializar la visualización del grafo
    net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white", directed=True)
    net.barnes_hut()  # Usar el algoritmo de optimización Barnes-Hut para una mejor distribución espacial

    # Añadir nodos y aristas a PyVis net
    for node, attrs in G.nodes(data=True):
        net.add_node(node, label=attrs.get('label', node), color=attrs.get('color', 'gray'), level=attrs.get('level', 0))
    for edge in G.edges:
        net.add_edge(edge[0], edge[1])

    # Configurar la disposición del grafo por niveles
    net.set_options("""
    {
      "layout": {
        "hierarchical": {
          "enabled": true,
          "direction": "UD",  // De arriba hacia abajo
          "sortMethod": "directed"  // Asegurar que la dirección de las aristas influye en la disposición
        }
      }
    }
    """)

    # Guardar y mostrar el grafo
    net.show("graph.html")
    st.components.v1.iframe("graph.html", width=800, height=600)
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
