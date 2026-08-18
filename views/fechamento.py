import streamlit as st
import database
import pandas as pd
import plotly.express as px

def render():
    st.subheader("Fechamento de Mes e Balanco do Periodo")
    
    df = database.get_transactions()
    
    if df.empty:
        st.info("Nenhum lancamento cadastrado ainda. Va em 'Novo Lancamento' para comecar.")
        return

    df['dt'] = pd.to_datetime(df['date'], errors='coerce')
    df['Data_BR'] = df['dt'].dt.strftime('%d/%m/%Y')

    meses_pt = {
        1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
        5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
        9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
    }
    
    df['Mes_Nome'] = df['dt'].dt.month.map(meses_pt) + " de " + df['dt'].dt.year.astype(str)
    df['Mes_Ordenacao'] = df['dt'].dt.strftime('%Y-%m')

    meses_unicos = df.sort_values('dt', ascending=False)[['Mes_Ordenacao', 'Mes_Nome']].drop_duplicates().values
    lista_meses = [m[1] for m in meses_unicos]

    if not lista_meses:
        st.warning("Nenhum mes disponivel para fechamento.")
        return

    mes_selecionado = st.selectbox("Selecione o mes que deseja fechar e auditar:", lista_meses)
    
    if mes_selecionado:
        df_mes = df[df['Mes_Nome'] == mes_selecionado]
        
        t_ent = df_mes[df_mes['type'] == 'Entrada / Receita']['amount'].sum()
        t_gas = df_mes[df_mes['type'] == 'Saida / Gasto']['amount'].sum()
        t_apo = df_mes[df_mes['type'] == 'Aporte / Reserva']['amount'].sum()
        t_res = t_ent - t_gas - t_apo
        
        st.markdown(f"### Balanco Consolidado: {mes_selecionado}")
        
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        col_m1.metric("Entradas do Mes", f"R$ {t_ent:,.2f}")
        col_m2.metric("Gastos do Mes", f"R$ {t_gas:,.2f}")
        col_m3.metric("Aportes do Mes", f"R$ {t_apo:,.2f}")
        col_m4.metric("Resultado Liquido", f"R$ {t_res:,.2f}")

        st.markdown("---")
        
        # Verifica se o mês está fechado diretamente no banco de dados (Persistente ao atualizar)
        ja_fechado = database.is_month_closed(mes_selecionado)

        if not ja_fechado:
            if st.button(f"Consolidar Fechamento de {mes_selecionado}", type="primary"):
                @st.dialog("Confirmar Fechamento de Periodo")
                def abrir_modal_confirmacao():
                    st.write(f"Deseja realmente consolidar e fechar o periodo de **{mes_selecionado}**?")
                    st.write(f"Resultado Liquido Auditado: R$ {t_res:,.2f}")
                    
                    col_b1, col_b2 = st.columns(2)
                    with col_b1:
                        if st.button("Sim, Confirmar", type="primary"):
                            database.close_month_db(mes_selecionado)
                            st.toast(f"Fechamento de {mes_selecionado} consolidado com sucesso!")
                            st.rerun()
                    with col_b2:
                        if st.button("Cancelar"):
                            st.rerun()
                
                abrir_modal_confirmacao()
        else:
            st.button(f"Periodo de {mes_selecionado} Ja Consolidado", disabled=True)

        if ja_fechado:
            st.success(f"Periodo de {mes_selecionado} consolidado com sucesso. Fatura analitica e graficos gerados abaixo:")
            
            st.markdown("---")
            st.subheader(f"Fatura e Graficos Analiticos - {mes_selecionado}")
            
            col_g1, col_g2 = st.columns(2, gap="medium")
            
            with col_g1:
                st.subheader("Composicao de Gastos da Fatura")
                df_gastos_mes = df_mes[df_mes['type'] == 'Saida / Gasto']
                if not df_gastos_mes.empty:
                    fig_donut = px.pie(
                        df_gastos_mes, 
                        names='category', 
                        values='amount', 
                        hole=0.55,
                        template='plotly_dark'
                    )
                    fig_donut.update_layout(
                        margin=dict(t=10, b=10, l=10, r=10),
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
                    )
                    st.plotly_chart(fig_donut, use_container_width=True)
                else:
                    st.info("Nenhum gasto registrado neste mes para compor a fatura.")

            with col_g2:
                st.subheader("Resumo Consolidado do Periodo")
                df_tipo_mes = df_mes.groupby('type')['amount'].sum().reset_index()
                if not df_tipo_mes.empty:
                    fig_bar = px.bar(
                        df_tipo_mes, 
                        x='type', 
                        y='amount', 
                        color='type',
                        template='plotly_dark',
                        text_auto='.2f'
                    )
                    fig_bar.update_layout(
                        margin=dict(t=10, b=10, l=10, r=10),
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        showlegend=False,
                        xaxis_title="",
                        yaxis_title="Valor (R$)"
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)
                else:
                    st.info("Nenhum dado financeiro para este mes.")

        st.markdown("---")
        st.subheader(f"Lancamentos do mes de {mes_selecionado}")
        
        df_display = df_mes[['id', 'Data_BR', 'description', 'category', 'amount', 'type']].copy()
        df_display.columns = ['ID', 'Data', 'Descricao', 'Categoria', 'Valor (R$)', 'Tipo']
        st.dataframe(df_display, use_container_width=True)