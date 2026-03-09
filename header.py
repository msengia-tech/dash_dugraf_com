import streamlit as st
from pathlib import Path
import base64


def show_header():
    st.set_page_config(page_title="Dashboard Dugraf", layout="wide")

    # Caminho do logo local
    logo_path = "assets/logo_dugraf_branco.png"

    def img_to_base64(path):
        p = Path(path)
        if not p.exists():
            return ""
        return base64.b64encode(p.read_bytes()).decode()

    logo_b64 = img_to_base64(logo_path)

    st.markdown(
        f"""
        <style>
        /* Container que ocupa largura inteira e mantém o header */
        .single-row-header {{
            position: relative;
            width: 100%;
            height: 100px; /* ajuste a altura total do header aqui */
            display: flex;
            align-items: center; /* alinha verticalmente o conteúdo ao centro da "linha" */
            justify-content: center; /* centraliza o título horizontalmente */
            background: transparent;
            margin-bottom: 12px;
            padding-top: 4px; /* mantém pequeno espaçamento interno se necessário */
        }}

        /* Título centralizado */
        .single-row-header h1 {{
            margin: 0;
            font-size: 34px;
            font-weight: 700;
            text-align: center;
            z-index: 2; /* fica acima do logo se houver sobreposição */
            color: white; /* ajuste conforme seu background */
        }}

        /* Logo posicionado mais à esquerda e um pouco acima da linha central */
        .single-row-logo {{
            position: absolute;
            left: 12px;  /* distância da borda esquerda — aumente/decrease conforme desejar */
            top: -12px;   /* ajuste para "subir" ou "descer" o logo */
            width: 150px; /* controla o tamanho do logo */
            height: auto;
            z-index: 3;
        }}

        /* Responsividade: reduz tamanho / posicionamento em telas pequenas */
        @media (max-width: 800px) {{
            .single-row-header {{ height: 86px; }}
            .single-row-header h1 {{ font-size: 22px; }}
            .single-row-logo {{ left: 10px; width: 110px; top: -8px; }}
        }}
        @media (max-width: 420px) {{
            .single-row-header {{ height: 90px; }}
            .single-row-header h1 {{ font-size: 18px; }}
            .single-row-logo {{ left: 6px; width: 90px; top: 4px; }}
        }}
        </style>

        <div class="single-row-header">
            <!-- Logo embutido em base64 para carregar localmente -->
            <img class="single-row-logo" src="data:image/png;base64,{logo_b64}" alt="Logo" />
            <h1>DASHBOARD DUGRAF - DIRETORIA</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )
