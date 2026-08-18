import streamlit as st
import database
import pandas as pd
import plotly.express as px

def render():
    st.subheader("Business Intelligence - Painel Executivo Consolidado")
    
    df = database.get_transactions()
    
    if df.empty:
        st.info("Nenhum lançamento cadastrado ainda. Vá em 'Novo Lançamento' para começar.")
        return

    # Conversão de datas
    df['dt'] = pd.to_datetime(df['date'], errors='coerce')
    df['Data_BR'] = df['dt'].dt.strftime('%d/%m/%Y')

    meses_pt = {
        1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
        5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
        9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
    }
    
    df['Mes_Nome'] = df['dt'].dt.month.map(meses_pt) + " de " + df['dt'].dt.year.astype(str)
    df['Mes_Ordenacao'] = df['dt'].dt.strftime('%Y-%m')

    # --- FILTRO EXECUTIVO DE MÊS (SLICER) ---
    meses_unicos = df.sort_values('dt', ascending=False)[['Mes_Ordenacao', 'Mes_Nome']].drop_duplicates().values
    opcoes_mes = ["Todos os Meses"] + [m[1] for m in meses_unicos]
    
    col_f1, col_f2 = st.columns([2, 2])
    with col_f1:
        mes_selecionado = st.selectbox("Filtro Executivo (Mês de Fechamento):", opcoes_mes, key="bi_mes_filter")
    
    df_filtrado = df.copy()
    if mes_selecionado != "Todos os Meses":
        df_filtrado = df_filtrado[df_filtrado['Mes_Nome'] == mes_selecionado]

    # --- KPI CARDS EXECUTIVOS (SEM EMOJIS) ---
    entradas = df_filtrado[df_filtrado['type'] == 'Entrada / Receita']['amount'].sum()
    gastos = df_filtrado[df_filtrado['type'] == 'Saida / Gasto']['amount'].sum()
    aportes = df_filtrado[df_filtrado['type'] == 'Aporte / Reserva']['amount'].sum()
    saldo = entradas - gastos - aportes

    st.markdown("---")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Total Entradas", f"R$ {entradas:,.2f}")
    kpi2.metric("Total Gastos", f"R$ {gastos:,.2f}")
    kpi3.metric("Total Aportes", f"R$ {aportes:,.2f}")
    kpi4.metric("Saldo Líquido", f"R$ {saldo:,.2f}")

    st.markdown("---")
    
    # ==========================================
    # GRADE DE 4 GRÁFICOS PROFISSIONAIS (2x2)
    # ==========================================
    
    col_g1, col_g2 = st.columns(2, gap="medium")
    
    # GRÁFICO 1: EVOLUÇÃO TEMPORAL (LINHAS COM MARCADORES)
    with col_g1:
        st.subheader("1. Evolução Temporal do Caixa (Diário)")
        if not df_filtrado.empty:
            df_timeline = df_filtrado.groupby(['dt', 'type'])['amount'].sum().reset_index().sort_values('dt')
            fig_line = px.line(
                df_timeline,
                x='dt',
                y='amount',
                color='type',
                markers=True,
                template='plotly_dark',
                labels={'dt': 'Data', 'amount': 'Valor (R$)', 'type': 'Tipo'}
            )
            fig_line.update_layout(
                margin=dict(t=10, b=10, l=10, r=10),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.info("Sem dados para a evolução temporal.")

    # GRÁFICO 2: COMPARATIVO POR TIPO (COLUNAS)
    with col_g2:
        st.subheader("2. Comparativo por Tipo de Movimento")
        df_tipo_sum = df_filtrado.groupby('type')['amount'].sum().reset_index()
        if not df_tipo_sum.empty:
            fig_bar = px.bar(
                df_tipo_sum, 
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
            st.info("Sem dados para o comparativo.")

    st.markdown("---")
    
    col_g3, col_g4 = st.columns(2, gap="medium")

    # GRÁFICO 3: COMPOSIÇÃO DE GASTOS (DONUT)
    with col_g3:
        st.subheader("3. Composição Percentual de Gastos")
        df_gastos = df_filtrado[df_filtrado['type'] == 'Saida / Gasto']
        if not df_gastos.empty:
            fig_donut = px.pie(
                df_gastos, 
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
            st.info("Nenhum gasto registrado para a composição.")

    # GRÁFICO 4: RANKING DE GASTOS (BARRAS HORIZONTAIS)
    with col_g4:
        st.subheader("4. Ranking Analítico de Gastos por Categoria")
        if not df_gastos.empty:
            df_cat_bar = df_gastos.groupby('category')['amount'].sum().reset_index().sort_values('amount', ascending=True)
            fig_h_bar = px.bar(
                df_cat_bar,
                x='amount',
                y='category',
                orientation='h',
                template='plotly_dark',
                text_auto='.2f',
                color='amount',
                color_continuous_scale='Blues'
            )
            fig_h_bar.update_layout(
                margin=dict(t=10, b=10, l=10, r=10),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis_title="Valor Total (R$)",
                yaxis_title="",
                coloraxis_showscale=False
            )
            st.plotly_chart(fig_h_bar, use_container_width=True)
        else:
            st.info("Nenhum dado para o ranking de categorias.")