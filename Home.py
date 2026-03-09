import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
from sqlalchemy import create_engine, text
import matplotlib.pyplot as plt
from babel.numbers import format_currency, format_decimal, format_percent
from babel.dates import format_date, format_datetime
from urllib.parse import quote_plus  # para codificar a senha de forma segura

from header import show_header

show_header()  # Exibe o cabeçalho padrão

# A partir daqui segue o resto do app...
st.write("Conteúdo do dashboard abaixo...")


# --- Conexão Segura com o banco do México ---
@st.cache_resource
def get_engine_mexico():
    # Recupera os dados das credenciais a partir do arquivo .streamlit/secrets.toml
    HOST = st.secrets["mexico"]["host"]
    PORT = int(st.secrets["mexico"]["port"])
    USER = st.secrets["mexico"]["user"]
    PASSWORD = st.secrets["mexico"]["password"]
    DB = st.secrets["mexico"]["database"]

    # Faz o encoding da senha para suportar caracteres especiais (ex: @, #, %, $)
    PASSWORD_ENCODED = quote_plus(PASSWORD)

    # Cria o engine com a string de conexão segura e charset utf8mb4 (suporte total a acentos e emoji)
    engine_mx = create_engine(
        f"mysql+pymysql://{USER}:{PASSWORD_ENCODED}@{HOST}:{PORT}/{DB}?charset=utf8mb4",
        pool_pre_ping=True,  # Garante conexão estável
    )
    return engine_mx


engine_mx = get_engine_mexico()

# --- Query México (já validada no ETL) ---
query_vendas_mx = """
SELECT 
  codpro, codigo_cliente, nota_fiscal, empresa, filial, razao_social, cidade, uf,
  nome_representante, apelido_representante, emissao, ano, mes, produto, fabricante,
  familia, tipo, qtde, unimed, m2, total_r, ptax_data, ptax_negociado, ptax_valor,
  total_us, us_m2, novo_comum, novo_trelleborg, ramo_categoria
FROM vw_dashboard_comercial_mexico
WHERE emissao > '2017-01-01'
ORDER BY emissao;
"""


@st.cache_data
def carregar_dados_mexico(query):
    with engine_mx.connect() as conn:
        df_mx = pd.read_sql_query(text(query), conn)
    return df_mx


df_mx = carregar_dados_mexico(query_vendas_mx)


# --- Cálculo das Datas Padrão (YTD) ---
hoje = datetime.date.today()
ano_atual = hoje.year
ano_anterior = ano_atual - 1

# Período 2 (Ano Atual YTD)
data_inicio_p2_padrao = datetime.date(ano_atual, 1, 1)
data_fim_p2_padrao = hoje

# Período 1 (Ano Anterior YTD)
data_inicio_p1_padrao = datetime.date(ano_anterior, 1, 1)
# Tenta criar a data correspondente no ano anterior, tratando o caso de ano bissexto
try:
    data_fim_p1_padrao = hoje.replace(year=ano_anterior)
except ValueError:
    # Se hoje for 29/Fev e o ano anterior não for bissexto, usa 28/Fev
    data_fim_p1_padrao = hoje.replace(year=ano_anterior, day=28)

# --- Filtros de Período ---

st.subheader("Filtros")
st.write("Período Anterior vs Atual")


col1_p1, col2_p1, col1_p2, col2_p2 = st.columns(4)
with col1_p1:
    data_inicio_p1 = st.date_input(
        "Data Inicial (período anterior)",
        value=data_inicio_p1_padrao,
        key="p1_start",
        format="DD/MM/YYYY",
    )
with col2_p1:
    data_fim_p1 = st.date_input(
        "Data Final (período anterior)",
        value=data_fim_p1_padrao,
        key="p1_end",
        format="DD/MM/YYYY",
    )

with col1_p2:
    data_inicio_p2 = st.date_input(
        "Data Inicial (período atual)",
        value=data_inicio_p2_padrao,
        key="p2_start",
        format="DD/MM/YYYY",
    )
with col2_p2:
    data_fim_p2 = st.date_input(
        "Data Final (período atual)",
        value=data_fim_p2_padrao,
        key="p2_end",
        format="DD/MM/YYYY",
    )

st.markdown("---")

# --- Filtragem do DataFrame ---

# Converte as datas do input para datetime para a comparação
data_inicio_p1_dt = pd.to_datetime(data_inicio_p1)
data_fim_p1_dt = (
    pd.to_datetime(data_fim_p1) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
)
data_inicio_p2_dt = pd.to_datetime(data_inicio_p2)
data_fim_p2_dt = (
    pd.to_datetime(data_fim_p2) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
)

# Cria dataframes separados para cada período usando os filtros de data
df_p1 = df_mx[
    (df_mx["emissao"] >= data_inicio_p1_dt) & (df_mx["emissao"] <= data_fim_p1_dt)
]

df_p2 = df_mx[
    (df_mx["emissao"] >= data_inicio_p2_dt) & (df_mx["emissao"] <= data_fim_p2_dt)
]

# --- Conteúdo Principal ---

st.subheader(" KPI's - Análise conforme filtros ")

# --- Cálculos para o Período 2 (Atual) ---
faturado_us_p2 = df_p2["total_us"].sum()

# --- Cálculos para o Período 1 (Anterior) ---
faturado_us_p1 = df_p1["total_us"].sum()


# --- Cálculos de Variação (Delta) em Percentual ---
def calcular_variacao_perc(atual, anterior):
    """Calcula a variação percentual de forma segura, evitando divisão por zero."""
    if anterior > 0:
        return (atual - anterior) / anterior
    # Se o anterior for 0, não há base para comparação percentual.
    # Pode retornar 0 ou um valor grande se o atual for > 0.
    # Retornar 0 é mais seguro para a visualização.
    return 0


delta_faturado_us_perc = calcular_variacao_perc(faturado_us_p2, faturado_us_p1)

# --- Inclusão dos CARDs com as métricas no Dashboard ---
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "US$ Faturado (Período Atual)",
    format_currency(faturado_us_p2, "USD", locale="pt_BR"),
    format_percent(delta_faturado_us_perc, locale="pt_BR", format="#,##0.00%"),
)

st.markdown("---")
