import streamlit as st
import database
import pandas as pd
import sqlite3

def render():
    st.subheader("Gerenciamento Geral, Gastos Fixos e Limpeza")
    st.markdown("<p style='color: #9ca3af; font-size: 14px; margin-bottom: 20px;'>Gerencie seus gastos fixos, reabra periodos consolidados, realize exclusoes em massa por data/mes ou audite registros individuais.</p>", unsafe_allow_html=True)

    # --- SECAO 1: CADASTRO E GERENCIAMENTO DE GASTOS FIXOS ---
    st.markdown("### Cadastro de Gastos Fixos")
    with st.form("form_add_fixed", border=True):
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            f_desc = st.text_input("Descricao do Gasto Fixo", placeholder="Ex: Aluguel, Internet, Netflix")
            f_val = st.text_input("Valor Padrao (R$)", placeholder="Ex: 150.00")
        with f_col2:
            f_cat = st.selectbox("Categoria Fixa", [
                "Fixos e Parcelas (Celular/Assinaturas)", 
                "Salario e Entradas", 
                "Combustivel (Jetta)", 
                "Lazer e Compras", 
                "Mercado e Refeicoes (VA)", 
                "Investimentos", 
                "Fundo de Seguranca", 
                "Outros"
            ], key="f_cat_key")
            f_type = st.radio("Tipo", ["Saida / Gasto", "Aporte / Reserva", "Entrada / Receita"], key="f_type_key")
        
        submitted_fixed = st.form_submit_button("Salvar Novo Gasto Fixo")
        if submitted_fixed:
            try:
                val_float = float(f_val.replace(",", "."))
                if f_desc.strip() and val_float > 0:
                    database.add_fixed_expense(f_desc, f_cat, val_float, f_type)
                    st.toast("Gasto fixo cadastrado com sucesso!")
                    st.rerun()
                else:
                    st.error("Preencha a descricao e um valor valido.")
            except ValueError:
                st.error("Valor numerico invalido.")

    df_fixed = database.get_fixed_expenses()
    if not df_fixed.empty:
        st.markdown("#### Gastos Fixos Atuais")
        for idx, row in df_fixed.iterrows():
            col_fx1, col_fx2 = st.columns([4, 1])
            with col_fx1:
                st.write(f"- **{row['description']}**: R$ {row['amount']:,.2f} [{row['type']}] ({row['category']})")
            with col_fx2:
                if st.button("Excluir", key=f"del_fix_{row['id']}"):
                    database.delete_fixed_expense(row['id'])
                    st.toast("Gasto fixo removido.")
                    st.rerun()

    df = database.get_transactions()
    if df.empty:
        st.markdown("---")
        st.info("Nenhum lancamento de transacao cadastrado no banco de dados.")
        return

    df['dt'] = pd.to_datetime(df['date'], errors='coerce')
    df['Data_BR'] = df['dt'].dt.strftime('%d/%m/%Y')
    meses_pt = {1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril", 5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto", 9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"}
    df['Mes_Nome'] = df['dt'].dt.month.map(meses_pt) + " de " + df['dt'].dt.year.astype(str)

    # --- SECAO 2: CONTROLE DE MESES FECHADOS ---
    st.markdown("---")
    st.markdown("### Controle de Meses Fechados")
    meses_disponiveis = df['Mes_Nome'].dropna().unique().tolist()
    meses_fechados_db = database.get_closed_months()
    
    if meses_fechados_db:
        st.write("Meses atualmente consolidados:")
        for m_fechado in meses_fechados_db:
            col_r1, col_r2 = st.columns([3, 1])
            with col_r1:
                st.write(f"- {m_fechado}")
            with col_r2:
                if st.button(f"Reabrir {m_fechado}", key=f"btn_reabrir_{m_fechado}"):
                    database.reopen_month_db(m_fechado)
                    st.toast(f"O mes de {m_fechado} foi reaberto.")
                    st.rerun()
    else:
        st.info("Nenhum mes consolidado no momento.")

    # --- SECAO 3: LIMPEZA EM MASSA POR DATA OU MES (ERROS DE LANCAMENTO) ---
    st.markdown("---")
    st.markdown("### Limpeza em Massa por Periodo (Erros de Lancamento)")
    st.markdown("Se houver muitos lancamentos incorretos em uma data especifica ou mes, voce pode remove-los em lote.")

    tipo_limpeza = st.radio("Selecione o criterio de limpeza em massa:", ["Por Data Especifica", "Por Mes Completo"], key="tipo_limpeza_radio")
    
    if tipo_limpeza == "Por Data Especifica":
        datas_unicas = sorted(df['date'].dropna().unique().tolist(), reverse=True)
        data_escolhida = st.selectbox("Selecione a data para excluir todos os registros:", datas_unicas, key="sel_data_limpeza")
        
        if data_escolhida:
            qtd_registros = len(df[df['date'] == data_escolhida])
            st.warning(f"Atencao: Existem {qtd_registros} registro(s) na data {data_escolhida}.")
            
            if st.button("Excluir Todos os Registros desta Data", type="primary", key="btn_del_date"):
                @st.dialog("Confirmacao de Exclusao em Massa")
                def confirmar_limpeza_data():
                    st.write(f"Tem certeza que deseja apagar **todos os {qtd_registros} registros** da data {data_escolhida}?")
                    st.write("Esta acao e irreversivel e afetara diretamente o banco de dados.")
                    
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("Sim, Excluir Tudo", type="primary", key="confirm_del_date"):
                            conn = sqlite3.connect("finance.db")
                            cursor = conn.cursor()
                            cursor.execute("DELETE FROM transactions WHERE date = ?", (data_escolhida,))
                            conn.commit()
                            conn.close()
                            st.toast("Registros excluidos com sucesso!")
                            st.rerun()
                    with c2:
                        if st.button("Cancelar", key="cancel_del_date"):
                            st.rerun()
                confirmar_limpeza_data()

    else:
        mes_escolhido_limpeza = st.selectbox("Selecione o mes completo para excluir:", meses_disponiveis, key="sel_mes_limpeza")
        
        if mes_escolhido_limpeza:
            df_mes_alvo = df[df['Mes_Nome'] == mes_escolhido_limpeza]
            qtd_mes = len(df_mes_alvo)
            st.warning(f"Atencao: Existem {qtd_mes} registro(s) no mes de {mes_escolhido_limpeza}.")
            
            if st.button("Excluir Todos os Registros deste Mes", type="primary", key="btn_del_month"):
                @st.dialog("Confirmacao de Exclusao em Massa do Mes")
                def confirmar_limpeza_mes():
                    st.write(f"Tem certeza que deseja apagar **todos os {qtd_mes} registros** do mes de {mes_escolhido_limpeza}?")
                    st.write("Esta acao e irreversivel.")
                    
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("Sim, Excluir Mes Inteiro", type="primary", key="confirm_del_month"):
                            conn = sqlite3.connect("finance.db")
                            cursor = conn.cursor()
                            for d_val in df_mes_alvo['date'].unique():
                                cursor.execute("DELETE FROM transactions WHERE date = ?", (d_val,))
                            conn.commit()
                            conn.close()
                            st.toast(f"Todos os registros de {mes_escolhido_limpeza} foram apagados!")
                            st.rerun()
                    with c2:
                        if st.button("Cancelar", key="cancel_del_month"):
                            st.rerun()
                confirmar_limpeza_mes()

    # --- SECAO 4: AUDITORIA E EXCLUSAO INDIVIDUAL ---
    st.markdown("---")
    st.markdown("### Auditoria e Exclusao Individual de Registros")
    st.markdown("Selecione um registro especifico para visualizar detalhes ou exclui-lo com seguranca.")

    for index, row in df.iterrows():
        reg_id = row['id']
        reg_data = row['Data_BR']
        reg_desc = row['description']
        reg_cat = row['category']
        reg_val = row['amount']
        reg_tipo = row['type']
        
        with st.expander(f"[{reg_data}] {reg_desc} - R$ {reg_val:,.2f} ({reg_tipo})"):
            st.write(f"**ID do Registro:** {reg_id}")
            st.write(f"**Data:** {reg_data}")
            st.write(f"**Descricao:** {reg_desc}")
            st.write(f"**Categoria:** {reg_cat}")
            st.write(f"**Valor:** R$ {reg_val:,.2f}")
            st.write(f"**Tipo:** {reg_tipo}")
            
            if st.button(f"Excluir Registro ID {reg_id}", key=f"del_ind_{reg_id}", type="primary"):
                @st.dialog("Confirmar Exclusao Individual")
                def confirmar_exclusao_individual():
                    st.write(f"Deseja realmente excluir o registro **{reg_desc}** no valor de **R$ {reg_val:,.2f}**?")
                    
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("Sim, Excluir", key=f"yes_del_{reg_id}", type="primary"):
                            conn = sqlite3.connect("finance.db")
                            cursor = conn.cursor()
                            cursor.execute("DELETE FROM transactions WHERE id = ?", (reg_id,))
                            conn.commit()
                            conn.close()
                            st.toast("Registro excluido com sucesso!")
                            st.rerun()
                    with c2:
                        if st.button("Cancelar", key=f"no_del_{reg_id}"):
                            st.rerun()
                confirmar_exclusao_individual()