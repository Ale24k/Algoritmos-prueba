import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Asumiendo que los usuarios están almacenados en este formato
USERS = {
    '72721479': {'password': 'ola123', 'ciclo_actual': '2', 'cursos_aprobados': ['C0090', 'C0659', 'C0613','C0737','C0201','C8189']}
}

def verify_login(username, password):
    """Verifica las credenciales del usuario."""
    user_info = USERS.get(username)
    if user_info and user_info['password'] == password:
        return user_info
    return None

def main():
    st.title("Sistema de Visualización de Cursos")

    # Login Section
    with st.sidebar:
        st.subheader("Login")
        username = st.text_input("Nombre de Usuario")
        password = st.text_input("Contraseña", type="password")
        if st.button("Iniciar Sesión"):
            user_info = verify_login(username, password)
            if user_info:
                st.session_state['user_info'] = user_info
                st.success("Inicio de sesión exitoso")
            else:
                st.error("Credenciales incorrectas")

    # File Upload and Graph
    if 'user_info' in st.session_state:
        uploaded_file = st.file_uploader("Subir archivo CSV o Excel", type=['csv', 'xlsx'])
        if uploaded_file:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            G = nx.from_pandas_edgelist(df, 'Código', 'Codigo_del_Requisito', create_using=nx.DiGraph())

            ciclo_actual = int(st.session_state['user_info']['ciclo_actual'])
            cursos_aprobados = st.session_state['user_info']['cursos_aprobados']

            # Dibujar el grafo
            pos = nx.spring_layout(G)
            color_map = []
            for node in G:
                if node in cursos_aprobados:
                    color_map.append('green')
                else:
                    color_map.append('red')
            
            plt.figure(figsize=(10, 8))
            nx.draw(G, pos, node_color=color_map, with_labels=True, arrowstyle='->', arrowsize=10)
            st.pyplot(plt)

if __name__ == "__main__":
    main()


    st.button("Iniciar proceso de matrícula")

if __name__ == "__main__":
    main()
