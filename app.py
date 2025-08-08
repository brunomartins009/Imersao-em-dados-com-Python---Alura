# Aula 4 - Construa um dashboard interativo

# Aprender a usar a biblioteca Streamlit para a criação de um dashboard
# interativo simples, que permite visualizar dados filtrados e gerar
# gráficos de forma prática.

### ---------- Importações ----------

import streamlit as st
import pandas as pd
import plotly.express as px

### ---------- Configurações da página ----------

# Define o título da página, o ícone e o layout para ocupar a largura total da tela
st.set_page_config(
                    page_title="Dashboard de Salários na Área de Dados",
                    page_icon=":bar_chart:",
                    layout="wide",
)

### Carregamento de dados

df = pd.read_csv("dados-finais-imersao-alura.csv")

### Barra lateral (filtros)
st.sidebar.header("Filtros")

# Filtro de anos
anos_disponiveis = sorted(df['ano'].unique())
anos_selecionados = st.sidebar.multiselect("Ano", anos_disponiveis, default=anos_disponiveis)

# Filtro de níveis de experiência
niveis_disponiveis = sorted(df['nivel_experiencia'].unique())
niveis_selecionados = st.sidebar.multiselect("Nível de Experiência", niveis_disponiveis, default=niveis_disponiveis)

# Filtro tipo de contrato de emprego
contratos_disponiveis = sorted(df['contrato_emprego'].unique())
contratos_selecionados = st.sidebar.multiselect("Contrato de Emprego", contratos_disponiveis, default=contratos_disponiveis)

# Filtro de tamanho da empresa
tamanhos_disponiveis = sorted(df['tamanho_empresa'].unique())
tamanhos_selecionados = st.sidebar.multiselect("Tamanho da Empresa", tamanhos_disponiveis, default=tamanhos_disponiveis)

# ---------- Filtragem do datframe ------------
# O dataframe principal é filtrado com base nos filtros selecionados na barra lateral
df_filtrado = df[(df['ano'].isin(anos_selecionados)) &
                 (df['nivel_experiencia'].isin(niveis_selecionados)) &
                 (df['contrato_emprego'].isin(contratos_selecionados)) &
                 (df['tamanho_empresa'].isin(tamanhos_selecionados))
]

# ---------- Conteúdo principal ------------
st.title("Dashboard de Análise de Salários na Área de Dados")
st.markdown("Explore os dados salariais na área de dados nos últimos anos. Utilize os filtros à esquerda para refinar sua análise")

# ---------- Métricas principais (KPIs) ------------

st.subheader("Métricas gerais (Salário anual em USD)")

if not df_filtrado.empty:
    sallario_medio = df_filtrado['salario_em_usd'].mean()
    salario_maximo = df_filtrado['salario_em_usd'].max()
    total_registros = df_filtrado.shape[0]
    cargo_mais_frequente = df_filtrado['cargo'].mode()[0]
else:
    sallario_medio, salario_mediano, salario_maximo, total_registros, cargo_mais_frequente = 0, 0, 0, 0, "N/A"

col1, col2, col3, col4 = st.columns(4)
col1.metric("Salário Médio", f"${sallario_medio:,.0f}")
col2.metric("Salário Máximo", f"${salario_maximo:,.0f}")
col3.metric("Total de Registros", f"{total_registros:,}")
col4.metric("Cargo Mais Frequente", cargo_mais_frequente)

st.markdown("---")

# ---------- Análises visuais com Plotly ------------
st.subheader("Gráficos")

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    if not df_filtrado.empty:
        top_cargos = df_filtrado.groupby('cargo')['salario_em_usd'].mean().nlargest(10).sort_values(ascending=True).reset_index()
        grafico_cargos = px.bar(
            top_cargos,
            x='salario_em_usd',
            y='cargo',
            orientation='h',
            title='Top 10 Cargos por Salário Médio',
            labels={'salario_em_usd': 'Salário Médio Anual (USD)', 'cargo': ''}
        )
        grafico_cargos.update_layout(title_x=0.1, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(grafico_cargos, use_container_width=True)
    else:
        st.warning("Nenhum dado disponível para exibir o gráfico de cargos.")
    
with col_graf2:
    if not df_filtrado.empty:
        grafico_hist = px.histogram(
            df_filtrado,
            x='salario_em_usd',
            nbins=30,
            title='Distribuição dos Salários Anuais',
            labels={'salario_em_usd': 'Salário Anual (USD)', 'count': ''}
        )
        grafico_hist.update_layout(title_x=0.1)
        st.plotly_chart(grafico_hist, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de distribuição.")

col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    if not df_filtrado.empty:
        remoto_contagem = df_filtrado['tipo_trabalho'].value_counts().reset_index()
        remoto_contagem.columns = ['tipo_trabalho', 'quantidade']
        grafico_remoto = px.pie(
            remoto_contagem,
            names='tipo_trabalho',
            values='quantidade',
            title='Proporção dos tipos de trabalho',
            hole=0.5  
        )
        grafico_remoto.update_traces(textinfo='percent+label')
        grafico_remoto.update_layout(title_x=0.1)
        st.plotly_chart(grafico_remoto, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico dos tipos de trabalho.")

with col_graf4:
    if not df_filtrado.empty:
        df_ds = df_filtrado[df_filtrado['cargo'] == 'Data Scientist']
        media_ds_pais = df_ds.groupby('residencia_iso3')['salario_em_usd'].mean().reset_index()
        grafico_paises = px.choropleth(media_ds_pais,
            locations='residencia_iso3',
            color='salario_em_usd',
            color_continuous_scale='rdylgn',
            title='Salário médio de Cientista de Dados por país',
            labels={'salario_em_usd': 'Salário médio (USD)', 'residencia_iso3': 'País'})
        grafico_paises.update_layout(title_x=0.1)
        st.plotly_chart(grafico_paises, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de países.")

# --- Tabela de Dados Detalhados ---
st.subheader("Dados Detalhados")
st.dataframe(df_filtrado)