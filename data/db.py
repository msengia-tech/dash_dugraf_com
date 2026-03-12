# data/db.py
import streamlit as st
from sqlalchemy import create_engine
from urllib.parse import quote_plus


@st.cache_resource
def get_engine_mexico():
    """
    Cria e retorna o SQLAlchemy engine para o banco do México.
    Lê as credenciais de st.secrets['mexico'].
    """
    mex = st.secrets["mexico"]
    HOST = mex["host"]
    PORT = int(mex.get("port", 3306))
    USER = mex["user"]
    PASSWORD = mex["password"]
    DB = mex["database"]

    password_encoded = quote_plus(PASSWORD)
    # Exemplo com pymysql (MySQL/MariaDB). Troque se usar outro SGDB.
    conn_str = (
        f"mysql+pymysql://{USER}:{password_encoded}@{HOST}:{PORT}/{DB}?charset=utf8mb4"
    )

    engine = create_engine(conn_str, pool_pre_ping=True)
    return engine
