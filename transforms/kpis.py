# transforms/kpis.py
import pandas as pd


def filtrar_por_periodo(df: pd.DataFrame, col_data: str, start, end) -> pd.DataFrame:
    """Filtra df entre start e end (inclusive no final). Aceita date/datetime/str."""
    start_dt = pd.to_datetime(start)
    end_dt = pd.to_datetime(end) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
    return df[(df[col_data] >= start_dt) & (df[col_data] <= end_dt)].copy()


def calcular_faturado(df: pd.DataFrame, coluna: str = "total_us") -> float:
    """Soma segura da coluna de faturamento retornando 0 se coluna ausente."""
    if coluna not in df.columns:
        return 0.0
    return float(df[coluna].sum())


def calcular_variacao_perc(atual: float, anterior: float) -> float:
    """Variação percentual com tratamento de divisão por zero."""
    if anterior > 0:
        return (atual - anterior) / anterior
    return 0.0
