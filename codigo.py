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
    """Dibuja el grafo con los cursos aprobados y los cursos que el usuario puede tomar."""
    
    ciclo_actual = int(user_info['ciclo_actual'])
    cursos_aprobados = set(user_info['cursos_aprobados'])

    # Asegurarse de que los datos son del tipo correcto
    df['Ciclo'] = pd.to_numeric(df['Ciclo'], errors='coerce')
    df['Código'] = df['Código'].astype(str).str.strip()
    df['Cursos'] = df['Cursos'].astype(str).str.strip()
    df['Requisito'] = df['Requisito'].astype(str).str.strip()

    # Filtrar cursos que están dentro de 3 ciclos adelante
    df_filtrado = df[df['Ciclo'] <= ciclo_actual + 3]

    # Crear el grafo
    G = nx.from_pandas_edgelist(df_filtrado, 'Código', 'Requisito', create_using=nx.DiGraph())
    net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")

    # Determinar cursos accesibles basados en requisitos cumplidos
    cursos_accesibles = cursos_aprobados.copy()
    for _, row in df_filtrado.iterrows():
        if row['Requisito'] in cursos_accesibles or row['Requisito'] == 'nan':
            cursos_accesibles.add(row['Código'])

    # Añadir nodos con colores correspondientes
    for node in G.nodes:
        # No añadimos el nombre del curso al título para que no aparezca en el hover
        color = 'green' if node in cursos_aprobados else 'blue' if node in cursos_accesibles else 'gray'
        net.add_node(node, label=node, color=color)

    # ...[codigo existente para añadir aristas]...

    # Guardar y mostrar el grafo
    net.show_buttons(filter_=['physics'])
    net.save_graph("graph.html")

    # Inyectar el script para manejar el evento de clic directamente en el componente de HTML
    HtmlFile = open("graph.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read()

    # Añadir un script que se ejecutará cuando se haga clic en un nodo
    source_code += """
    <script type="text/javascript">
        document.addEventListener('DOMContentLoaded', function() {
            var container = document.getElementById('mynetwork');
            var data = {
                nodes: new vis.DataSet([
                    // ... Definición de los nodos ...
                ]),
                edges: new vis.DataSet([
                    // ... Definición de las aristas ...
                ])
            };
            var network = new vis.Network(container, data, {});
            network.on("click", function (params) {
                if (params.nodes.length > 0) {
                    var nodeId = params.nodes[0];
                    var node = data.nodes.get(nodeId);
                    alert('Curso: ' + node.title); // Aquí mostraríamos el nombre del curso
                }
            });
        });
    </script>
    """
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
