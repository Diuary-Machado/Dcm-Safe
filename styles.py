import streamlit as st

def load_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');

        html, body, .stApp, p, div, label, input, button, select, textarea {
            font-family: 'Outfit', sans-serif !important;
        }

        .stApp {
            background: linear-gradient(135deg, #0d0f14 0%, #13151b 100%);
            color: #f1f5f9 !important;
        }

        [data-testid="stSidebar"] {
            background-color: #111318 !important;
            border-right: 1px solid #1f2430 !important;
        }

        div[data-testid="stForm"], [data-testid="stMetric"], .stDataFrame {
            background-color: #161922 !important;
            border: 1px solid #232938 !important;
            border-radius: 18px !important;
            padding: 26px !important;
            box-shadow: 0 12px 35px rgba(0, 0, 0, 0.7) !important;
        }

        h1, h2, h3, h4 {
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 700 !important;
            letter-spacing: -0.5px;
            background: linear-gradient(135deg, #ffffff 30%, #a5b4fc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        label, .stCheckbox span, .stRadio label, p {
            color: #cbd5e1 !important;
            font-weight: 500 !important;
            letter-spacing: 0.2px;
        }

        .stTextInput input, .stSelectbox select, .stDateInput input {
            background-color: #0d0f14 !important;
            border: 1px solid #283044 !important;
            border-radius: 12px !important;
            color: #f1f5f9 !important;
            padding: 10px 14px !important;
            transition: all 0.3s ease-in-out;
        }

        input[type="password"] {
            padding-right: 60px !important;
        }

        .stTextInput input:focus, .stSelectbox select:focus, .stDateInput input:focus {
            border-color: #06b6d4 !important;
            box-shadow: 0 0 15px rgba(6, 182, 212, 0.3) !important;
        }

        /* Centraliza o container do botão de submissão do formulário */
        div[data-testid="stFormSubmitButton"] {
            display: flex !important;
            justify-content: center !important;
            width: 100% !important;
        }

        /* Botão ACESSAR com tamanho personalizado (menor) e centralizado */
        div[data-testid="stFormSubmitButton"] > button {
            background: linear-gradient(135deg, #7c3aed 0%, #db2777 100%) !important;
            color: #ffffff !important;
            font-weight: 700 !important;
            border-radius: 12px !important;
            border: none !important;
            width: 200px !important; /* Largura controlada e elegante */
            padding: 0.70rem 1rem !important;
            letter-spacing: 0.8px;
            text-transform: uppercase;
            box-shadow: 0 4px 20px rgba(219, 39, 119, 0.4);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        div[data-testid="stFormSubmitButton"] > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(219, 39, 119, 0.6);
            opacity: 0.95;
        }

        .stButton>button {
            background-color: #1c212e !important;
            color: #f1f5f9 !important;
            border: 1px solid #2d3548 !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            transition: all 0.25s ease;
        }

        .stButton>button:hover {
            background-color: #252c3d !important;
            border-color: #06b6d4 !important;
            color: #06b6d4 !important;
            transform: translateY(-1px);
        }

        [data-testid="stMetricValue"] {
            color: #06b6d4 !important;
            font-weight: 700 !important;
            font-size: 28px !important;
        }

        [data-testid="stMetricLabel"] {
            color: #94a3b8 !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            font-size: 11px !important;
            letter-spacing: 0.5px;
        }
        
        .stDataFrame {
            padding: 12px !important;
        }
        </style>
    """, unsafe_allow_html=True)