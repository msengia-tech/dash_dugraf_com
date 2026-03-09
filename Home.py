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
st.subheader("Período anterior vs Atual")
col1_p1, col2_p1, col1_p2, col2_p2 = st.columns(4)
with col1_p1:
    data_inicio_p1 = st.date_input(
        "Data Inicial",
        value=data_inicio_p1_padrao,
        key="p1_start",
        format="DD/MM/YYYY",
    )
with col2_p1:
    data_fim_p1 = st.date_input(
        "Data Final", value=data_fim_p1_padrao, key="p1_end", format="DD/MM/YYYY"
    )

with col1_p2:
    data_inicio_p2 = st.date_input(
        "Data Inicial",
        value=data_inicio_p2_padrao,
        key="p2_start",
        format="DD/MM/YYYY",
    )
with col2_p2:
    data_fim_p2 = st.date_input(
        "Data Final", value=data_fim_p2_padrao, key="p2_end", format="DD/MM/YYYY"
    )

st.markdown("---")
