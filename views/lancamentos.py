import streamlit as st
import database
from datetime import datetime

def render():
    st.subheader("Novo Lancamento")
    st.markdown("<p style='color: #9ca3af; font-size: 14px; margin-bottom: 20px;'>Selecione os gastos fixos abaixo para lancamento rapido ou preencha o formulario manual.</p>", unsafe_allow_html=True)

    if "sucesso_msg" in st.session_state:
        st.success(st.session_state["sucesso_msg"])
        del st.session_state["sucesso_msg"]

    # --- SECAO DE GASTOS FIXOS (CHECKBOXES) ---
    df_fixed = database.get_fixed_expenses()
    
    if not df_fixed.empty:
        st.markdown("### Gastos Fixos Cadastrados")
        date_fixed = st.date_input("Data para aplicacao dos fixos", datetime.today(), format="DD/MM/YYYY", key="input_date_fixed")
        
        selected_items = []
        for idx, row in df_fixed.iterrows():
            f_id = row['id']
            f_desc = row['description']
            f_cat = row['category']
            f_val = row['amount']
            f_type = row['type']
            
            if st.checkbox(f"{f_desc} - R$ {f_val:,.2f} [{f_type}]", key=f"fix_chk_{f_id}"):
                selected_items.append(row)

        if selected_items:
            if st.button("Lancar Fixos Selecionados", type="primary", key="btn_lancar_fixos"):
                date_db = str(date_fixed)
                for item in selected_items:
                    database.add_transaction(date_db, item['description'], item['category'], item['amount'], item['type'])
                st.session_state["sucesso_msg"] = f"Foram lancados {len(selected_items)} gastos fixos com sucesso em {date_fixed.strftime('%d/%m/%Y')}!"
                st.rerun()
        
        st.markdown("<br>---<br>", unsafe_allow_html=True)

    # --- FORMULARIO DE LANCAMENTO MANUAL ---
    st.markdown("### Lancamento Manual Avulso")
    with st.form(key="form_lancamento", border=True):
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            date = st.date_input("Data do Lancamento", datetime.today(), format="DD/MM/YYYY", key="input_date")
            raw_valor = st.text_input("Valor (R$)", value="", placeholder="Ex: 1090,00 ou 1090.00", key="input_valor")
            t_type = st.radio("Tipo de Movimento", ["Entrada / Receita", "Saida / Gasto", "Aporte / Reserva"], key="input_type")
        
        with col2:
            description = st.text_input("Descricao", placeholder="Ex: Gasolina Jetta, Mercado, Salario", key="input_desc")
            category = st.selectbox("Categoria", [
                "Salario e Entradas", 
                "Fixos e Parcelas (Celular/Assinaturas)", 
                "Combustivel (Jetta)", 
                "Lazer e Compras", 
                "Mercado e Refeicoes (VA)", 
                "Investimentos", 
                "Fundo de Seguranca", 
                "Outros"
            ], key="input_cat")

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Salvar no Banco Local")

        if submitted:
            amount = 0.0
            if raw_valor.strip() != "":
                try:
                    v_str = raw_valor.strip().replace("R$", "").strip()
                    if "," in v_str and "." in v_str:
                        v_str = v_str.replace(".", "").replace(",", ".")
                    elif "," in v_str:
                        v_str = v_str.replace(",", ".")
                    amount = float(v_str)
                except ValueError:
                    amount = 0.0

            if description.strip() == "":
                st.error("A descricao nao pode ficar vazia!")
            elif amount <= 0:
                st.error("O valor precisa ser maior que zero!")
            else:
                date_db = str(date)
                date_br = date.strftime("%d/%m/%Y")
                
                database.add_transaction(date_db, description, category, amount, t_type)
                st.session_state["sucesso_msg"] = f"Lancamento registrado com sucesso: {description} (R$ {amount:,.2f}) em {date_br}"
                
                for key in ["input_valor", "input_desc"]:
                    if key in st.session_state:
                        del st.session_state[key]
                
                st.rerun()