import streamlit as st

def check_auth():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    return st.session_state["authenticated"]

def render_login():
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    _, col_centro, _ = st.columns([1.5, 1, 1.5])
    
    with col_centro:
        with st.form(key='login_form', border=True):
            st.markdown("<h3 style='text-align: center; letter-spacing: 1.5px; font-weight: 800; color: #ffffff; margin-bottom: 2px;'>DCM SAFE</h3>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 12px; margin-bottom: 20px; letter-spacing: 0.5px;'>Cofre Local</p>", unsafe_allow_html=True)
            
            senha = st.text_input("Senha", type="password", key="login_senha_input", placeholder="Digite a senha")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            submit_button = st.form_submit_button("ACESSAR", type="primary", use_container_width=True)

            if submit_button:
                # Pega a senha configurada no secrets.toml de forma segura
                senha_correta = st.secrets.get("APP_PASSWORD", "admin")
                
                if senha == senha_correta:
                    st.session_state["authenticated"] = True
                    st.rerun()
                else:
                    st.error("Senha incorreta.")

def logout():
    st.session_state["authenticated"] = False