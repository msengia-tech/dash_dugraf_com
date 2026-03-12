# data/loaders.py
import streamlit as st
import pandas as pd
from sqlalchemy import text
from pathlib import Path

from .db import get_engine_mexico

# Caminho relativo ao arquivo atual
BASE_DIR = Path(__file__).resolve().parent.parent
QUERY_FILE = BASE_DIR / "queries" / "vendas_mexico.sql"


def _read_query_file(path: Path) -> str:
    return path.read_text(encoding="utf-8")


@st.cache_data(ttl=3600)
def carregar_dados_mexico() -> pd.DataFrame:
    """
    Carrega o dataset do México usando a query em queries/vendas_mexico.sql.
    Retorna um DataFrame com a coluna 'emissao' convertida para datetime.
    """
    query = _read_query_file(QUERY_FILE)
    engine = get_engine_mexico()
    with engine.connect() as conn:
        df = pd.read_sql_query(text(query), conn, parse_dates=["emissao"])
    # Pequenas normalizações (exemplo)
    if "emissao" in df.columns:
        df["emissao"] = pd.to_datetime(df["emissao"])
    return df
