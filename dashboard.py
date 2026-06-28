import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Configuração da página para o modo Wide (Dashboard tela cheia)
st.set_page_config(layout="wide")

st.title("📊 Dashboard de Municípios Brasileiros")
st.markdown("Dados extraídos localmente do arquivo CSV")

# --- CONSUMO E TRATAMENTO DE DADOS ---
@st.cache_data
def carregar_dados():
    # SOLUÇÃO DO FILENOTFOUND: Descobre dinamicamente a pasta onde o script está rodando
    caminho_atual = os.path.dirname(__file__)
    caminho_csv = os.path.join(caminho_atual, "municipio.csv")
    
    # Carrega o CSV do usuário
    df_local = pd.read_csv(caminho_csv)
    
    # DICIONÁRIO DE MAPEAMENTO: Converte o 'codigo_uf' do seu CSV em Estado e Região
    mapeamento_uf = {
        11: {"uf": "RO", "regiao": "Norte"}, 12: {"uf": "AC", "regiao": "Norte"},
        13: {"uf": "AM", "regiao": "Norte"}, 14: {"uf": "RR", "regiao": "Norte"},
        15: {"uf": "PA", "regiao": "Norte"}, 16: {"uf": "AP", "regiao": "Norte"},
        17: {"uf": "TO", "regiao": "Norte"},
        21: {"uf": "MA", "regiao": "Nordeste"}, 22: {"uf": "PI", "regiao": "Nordeste"},
        23: {"uf": "CE", "regiao": "Nordeste"}, 24: {"uf": "RN", "regiao": "Nordeste"},
        25: {"uf": "PB", "regiao": "Nordeste"}, 26: {"uf": "PE", "regiao": "Nordeste"},
        27: {"uf": "AL", "regiao": "Nordeste"}, 28: {"uf": "SE", "regiao": "Nordeste"},
        29: {"uf": "BA", "regiao": "Nordeste"},
        31: {"uf": "MG", "regiao": "Sudeste"}, 32: {"uf": "ES", "regiao": "Sudeste"},
        33: {"uf": "RJ", "regiao": "Sudeste"}, 35: {"uf": "SP", "regiao": "Sudeste"},
        41: {"uf": "PR", "regiao": "Sul"}, 42: {"uf": "SC", "regiao": "Sul"},
        43: {"uf": "RS", "regiao": "Sul"},
        50: {"uf": "MS", "regiao": "Centro-Oeste"}, 51: {"uf": "MT", "regiao": "Centro-Oeste"},
        52: {"uf": "GO", "regiao": "Centro-Oeste"}, 53: {"uf": "DF", "regiao": "Centro-Oeste"}
    }
    
    # Cria as colunas de texto baseadas no código numérico do CSV
    df_local["uf"] = df_local["codigo_uf"].map(lambda x: mapeamento_uf.get(x, {}).get("uf", "Desconhecido"))
    df_local["regiao"] = df_local["codigo_uf"].map(lambda x: mapeamento_uf.get(x, {}).get("regiao", "Desconhecido"))
    
    # Padroniza as colunas necessárias para os gráficos seguintes
    df_formatado = pd.DataFrame({
        "municipio": df_local["nome"],
        "uf": df_local["uf"],
        "regiao": df_local["regiao"]
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
    fig_pie.update_traces(textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")

# --- COMPONENTE 4: TABELA TOP 10 ---
st.subheader("🏆 Estados com Mais Municípios (Top 10)")

df_estados = df["uf"].value_counts().reset_index()
df_estados.columns = ["UF", "Quantidade"]

top_10_estados = df_estados.head(10)
st.dataframe(top_10_estados, hide_index=True, use_container_width=True)
