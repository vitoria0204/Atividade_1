import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# Configuração da página para o modo Wide (Dashboard tela cheia)
st.set_page_config(layout="wide")

st.title("📊 Dashboard de Municípios Brasileiros")
st.markdown("Dados extraídos em tempo real via API do IBGE")

# --- CONSUMO DE DADOS (API IBGE) ---
@st.cache_data
def carregar_dados():
    # 1. Lê o arquivo que você subiu no GitHub. 
    # (Ajuste o nome do arquivo se o seu não for 'municipios.csv')
    df_local = pd.read_csv("atividade_1/municipios.csv")
    
    # 2. Padroniza as colunas para o resto do dashboard funcionar.
    # ATENÇÃO: Substitua os nomes da direita pelos nomes exatos das colunas do SEU arquivo!
    df_formatado = pd.DataFrame({
        "municipio": df_local["nome_da_coluna_de_municipios"], # ex: df_local["Nome_Municipio"]
        "uf": df_local["nome_da_coluna_de_estados"],          # ex: df_local["Sigla_UF"]
        "regiao": df_local["nome_da_coluna_de_regioes"]       # ex: df_local["Regiao"]
    })
    
    return df_formatado
    
df = carregar_dados()

# --- COMPONENTE 1: CARDS (3 KPIs) ---
st.subheader("📌 Indicadores Chave (KPIs)")
col1, col2, col3 = st.columns(3)

total_municipios = len(df)
total_estados = df["uf"].nunique()
regiao_mais_municipios = df["regiao"].value_counts().idxmax()

col1.metric("Total de Municípios", f"{total_municipios:,}".replace(",", "."))
col2.metric("Total de Estados (UFs)", total_estados)
col3.metric("Região c/ Mais Municípios", regiao_mais_municipios)

st.markdown("---")

# --- PREPARAÇÃO DOS DADOS PARA OS GRÁFICOS ---
df_regiao = df["regiao"].value_counts().reset_index()
df_regiao.columns = ["Região", "Quantidade"]

# Organizando os gráficos lado a lado em duas colunas
col_grafico1, col_grafico2 = st.columns(2)

# --- COMPONENTE 2: GRÁFICO DE BARRAS ---
with col_grafico1:
    fig_bar = px.bar(
        df_regiao, 
        x="Região", 
        y="Quantidade", 
        title="Municípios por Região",
        color="Região",
        text_auto=True
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# --- COMPONENTE 3: GRÁFICO DE PIZZA ---
with col_grafico2:
    fig_pie = px.pie(
        df_regiao, 
        names="Região", 
        values="Quantidade", 
        title="Distribuição por Região"
    )
    # Ajuste para exibir a porcentagem nas fatias
    fig_pie.update_traces(textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")

# --- COMPONENTE 4: TABELA TOP 10 ---
st.subheader("🏆 Estados com Mais Municípios (Top 10)")

df_estados = df["uf"].value_counts().reset_index()
df_estados.columns = ["UF", "Quantidade"]

# Filtrando apenas os 10 primeiros (Ordenação decrescente já é nativa do value_counts)
top_10_estados = df_estados.head(10)

# Exibindo a tabela formatada no Streamlit
st.dataframe(top_10_estados, hide_index=True, use_container_width=True)
