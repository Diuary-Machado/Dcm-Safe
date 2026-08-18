import streamlit as st
import importlib

import auth
import styles
import database
from views import lancamentos, dashboard, fechamento, gerenciar

importlib.reload(auth)
importlib.reload(styles)
importlib.reload(database)
importlib.reload(lancamentos)
importlib.reload(dashboard)
importlib.reload(fechamento)
importlib.reload(gerenciar)

st.set_page_config(page_title="DCM SAFE", layout="wide")

# Carrega o CSS global centralizado
styles.load_css()

# Controle de Autenticação
if not auth.check_auth():
    auth.render_login()
else:
    st.sidebar.title("DCM SAFE")
    st.sidebar.markdown("Cofre Financeiro Local")
    st.sidebar.markdown("---")
    
    st.sidebar.subheader("Escolha a tela:")
    menu = st.sidebar.radio(
        "", 
        ["Novo Lancamento", "Dashboard e Graficos", "Fechamento de Mes", "Gerenciar Lancamentos"],
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    if st.sidebar.button("Trancar Sistema"):
        auth.logout()
        st.rerun()

    # Roteamento das telas
    if menu == "Novo Lancamento":
        lancamentos.render()
    elif menu == "Dashboard e Graficos":
        dashboard.render()
    elif menu == "Fechamento de Mes":
        fechamento.render()
    elif menu == "Gerenciar Lancamentos":
        gerenciar.render()