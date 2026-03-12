# app.py
import streamlit as st
import datetime

from components.header import show_header
from data.loaders import carregar_dados_mexico
from transforms.kpis import (
    filtrar_por_periodo,
    calcular_faturado,
    calcular_variacao_perc,
)
from utils.formats import fmt_currency, fmt_percent

show_header()

st.write("Conteúdo do dashboard abaixo...")

# Carrega dados (cacheado)
df_mx = carregar_dados_mexico()

# Datas padrão (YTD)
hoje = datetime.date.today()
ano_atual = hoje.year
ano_anterior = ano_atual - 1

data_inicio_p2_padrao = datetime.date(ano_atual, 1, 1)
data_fim_p2_padrao = hoje

data_inicio_p1_padrao = datetime.date(ano_anterior, 1, 1)
try:
    data_fim_p1_padrao = hoje.replace(year=ano_anterior)
except ValueError:
    data_fim_p1_padrao = hoje.replace(year=ano_anterior, day=28)

# Widgets de filtro
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

# Filtragem usando funções
df_p1 = filtrar_por_periodo(df_mx, "emissao", data_inicio_p1, data_fim_p1)
df_p2 = filtrar_por_periodo(df_mx, "emissao", data_inicio_p2, data_fim_p2)

# Métricas
faturado_us_p2 = calcular_faturado(df_p2, "total_us")
faturado_us_p1 = calcular_faturado(df_p1, "total_us")
delta_faturado_us_perc = calcular_variacao_perc(faturado_us_p2, faturado_us_p1)

# Exibição
col1, col2, col3, col4 = st.columns(4)
col1.metric(
    "US$ Faturado (Período Atual)",
    fmt_currency(faturado_us_p2, "USD"),
    fmt_percent(delta_faturado_us_perc),
)

st.markdown("---")
