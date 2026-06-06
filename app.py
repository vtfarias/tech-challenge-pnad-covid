import csv
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="PNAD COVID-19 | Painel Hospitalar",
    page_icon="H",
    layout="wide",
    initial_sidebar_state="expanded",
)


BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "dados_dashboard"

ARQUIVOS = {
    "barreira": "analise_01_barreira_economica.csv",
    "informalidade": "analise_02_informalidade_risco.csv",
    "perfil_grave": "analise_03_perfil_grave.csv",
    "protecao_social": "analise_04_protecao_social.csv",
    "mapa_desigualdade": "analise_05_mapa_desigualdade.csv",
    "evolucao": "analise_06_evolucao_mensal.csv",
    "escolaridade_genero": "analise_07_escolaridade_genero.csv",
    "moradia": "analise_08_moradia_endividamento.csv",
    "sus_privado": "analise_09_sus_privado.csv",
    "correlacoes": "correlacoes_economico_clinico.csv",
}

UF_SIGLAS = {
    11: "RO", 12: "AC", 13: "AM", 14: "RR", 15: "PA", 16: "AP", 17: "TO",
    21: "MA", 22: "PI", 23: "CE", 24: "RN", 25: "PB", 26: "PE", 27: "AL",
    28: "SE", 29: "BA", 31: "MG", 32: "ES", 33: "RJ", 35: "SP", 41: "PR",
    42: "SC", 43: "RS", 50: "MS", 51: "MT", 52: "GO", 53: "DF",
}

MESES_ORDEM = {
    "Janeiro": 1,
    "Fevereiro": 2,
    "Marco": 3,
    "Março": 3,
    "Abril": 4,
    "Maio": 5,
    "Junho": 6,
    "Julho": 7,
    "Agosto": 8,
    "Setembro": 9,
    "Outubro": 10,
    "Novembro": 11,
    "Dezembro": 12,
}

LABELS = {
    "pct_buscou_atendimento": "% buscou atendimento",
    "pct_internado_entre_atendidos": "% internado entre atendidos",
    "pct_entubado_entre_internados": "% entubado entre internados",
    "pct_fez_teste": "% fez teste",
    "pct_positivo_entre_resultados_validos": "% positividade",
    "pct_dificuldade_respirar": "% dificuldade respiratória",
    "pct_perda_cheiro_sabor": "% perda de cheiro/sabor",
    "pct_diabetes": "% diabetes",
    "pct_hipertensao": "% hipertensão",
    "pct_asma": "% asma",
    "pct_doenca_coracao": "% doença do coração",
    "pct_depressao": "% depressão",
    "pct_cancer": "% câncer",
    "pct_alguma_comorbidade": "% alguma comorbidade",
    "pct_sem_plano": "% sem plano de saúde",
    "pct_ate_1_sm_entre_renda_informada": "% até 1 salário mínimo",
    "pct_informal_entre_ocupados_com_info": "% informalidade",
    "pct_baixa_protecao_domiciliar": "% baixa proteção domiciliar",
    "pct_recebeu_auxilio": "% recebeu auxílio",
    "pct_recebeu_bolsa_familia": "% recebeu Bolsa Família",
    "pct_recebeu_seguro_desemprego": "% recebeu seguro-desemprego",
    "pct_pegou_emprestimo": "% pegou empréstimo",
    "pct_trabalhou": "% trabalhou",
    "pct_home_office": "% home office",
    "pct_afastado_trabalho": "% afastado do trabalho",
    "media_itens_protecao": "média de itens de proteção",
}

PALETA = ["#0F766E", "#2563EB", "#B45309", "#475569", "#7F1D1D", "#6B7280"]


CSS = """
<style>
:root {
    --ink: #172033;
    --muted: #5F6B7A;
    --line: #D9E2EC;
    --panel: #F8FAFC;
    --teal: #0F766E;
    --blue: #2563EB;
    --amber: #B45309;
    --red: #991B1B;
}
html, body, .stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"] {
    background: #FFFFFF;
    color: var(--ink);
}
.block-container {
    padding-top: 4.25rem;
    padding-bottom: 2.25rem;
    padding-left: clamp(1rem, 2.4vw, 2.75rem);
    padding-right: clamp(1rem, 2.4vw, 2.75rem);
    max-width: 1280px;
}
[data-testid="stSidebar"] {
    background: #F7FAFC;
    border-right: 1px solid var(--line);
}
[data-testid="stSidebar"] * {
    color: var(--ink);
}
h1, h2, h3, p, label, span, div {
    color: var(--ink);
    letter-spacing: 0;
}
.hero-title {
    font-size: clamp(1.55rem, 2.4vw, 2.1rem);
    line-height: 1.15;
    font-weight: 750;
    margin-bottom: .2rem;
}
.hero-subtitle {
    color: var(--muted);
    font-size: .98rem;
    margin-bottom: 1.35rem;
}
.section-note {
    color: var(--muted);
    font-size: .95rem;
    margin: .15rem 0 1.1rem 0;
}
.callout {
    border: 1px solid var(--line);
    border-left: 5px solid var(--blue);
    background: #FFFFFF;
    padding: .85rem 1rem;
    border-radius: 8px;
    margin: .75rem 0;
}
.callout strong {
    color: var(--ink);
}
.callout-action {
    border-left-color: var(--teal);
    background: #F4FBF8;
}
.callout-warning {
    border-left-color: var(--amber);
    background: #FFF8ED;
}
.callout-risk {
    border-left-color: var(--red);
    background: #FFF7F7;
}
.small-note {
    color: var(--muted);
    font-size: .85rem;
}
[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #DDE6F0;
    padding: .85rem .9rem;
    border-radius: 8px;
}
[data-testid="stMetricLabel"] {
    color: #42526A;
}
[data-testid="stMetricValue"] {
    color: #172033;
    font-weight: 750;
}
.reference-card {
    background: #FFFFFF;
    border: 1px solid #DDE6F0;
    padding: .85rem .9rem;
    border-radius: 8px;
    min-height: 112px;
}
.reference-card-label {
    color: #42526A;
    font-size: .88rem;
    margin-bottom: .35rem;
}
.reference-card-value {
    color: #172033;
    font-size: 1.55rem;
    line-height: 1.2;
    font-weight: 750;
    white-space: normal;
}
.reference-card-note {
    color: var(--muted);
    font-size: .82rem;
    margin-top: .4rem;
}
div[data-testid="stDataFrame"] {
    border: 1px solid var(--line);
    border-radius: 8px;
}
@media (max-width: 1100px) {
    .block-container {
        padding-top: 4.75rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    [data-testid="stMetric"] {
        padding: .7rem .75rem;
    }
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


def detectar_separador(caminho: Path) -> str:
    try:
        amostra = caminho.read_text(encoding="utf-8-sig", errors="ignore")[:4096]
        return csv.Sniffer().sniff(amostra, delimiters=",;|\t").delimiter
    except Exception:
        return ","


@st.cache_data(show_spinner=False)
def carregar_csv(nome_arquivo: str) -> pd.DataFrame:
    caminho = DATA_DIR / nome_arquivo
    if not caminho.exists():
        return pd.DataFrame()

    sep = detectar_separador(caminho)
    for encoding in ("utf-8-sig", "utf-8", "latin1"):
        try:
            df = pd.read_csv(caminho, sep=sep, encoding=encoding)
            return preparar_dataframe(df)
        except Exception:
            continue
    return pd.DataFrame()


def preparar_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace({"": np.nan, "nan": np.nan, "None": np.nan})

    for col in df.columns:
        if col.startswith("pct_") or col in {"n_amostra", "populacao_estimada", "media_itens_protecao", "correlacao"}:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "uf" in df.columns:
        df["uf"] = pd.to_numeric(df["uf"], errors="coerce")
        df["uf_sigla"] = df["uf"].map(UF_SIGLAS).fillna(df["uf"].astype("Int64").astype(str))

    if "v1013" in df.columns:
        df["ordem_mes"] = pd.to_numeric(df["v1013"], errors="coerce")
    elif "mes_nome" in df.columns:
        df["ordem_mes"] = df["mes_nome"].map(MESES_ORDEM)

    return df


@st.cache_data(show_spinner=False)
def carregar_todos() -> dict[str, pd.DataFrame]:
    return {chave: carregar_csv(arquivo) for chave, arquivo in ARQUIVOS.items()}


def fmt_num(valor, casas: int = 0) -> str:
    if pd.isna(valor):
        return "n/d"
    numero = float(valor)
    if casas == 0:
        return f"{numero:,.0f}".replace(",", ".")
    return f"{numero:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def fmt_pct(valor, casas: int = 1) -> str:
    if pd.isna(valor):
        return "n/d"
    return f"{float(valor):.{casas}f}%".replace(".", ",")


def nome_indicador(coluna: str) -> str:
    return LABELS.get(coluna, coluna.replace("_", " "))


def eh_percentual(coluna: str) -> bool:
    return coluna.startswith("pct_")


def titulo_eixo(coluna: str, eixo_padrao: str | None = None) -> str:
    if eixo_padrao:
        return eixo_padrao
    if eh_percentual(coluna):
        return "Percentual"
    if coluna == "media_itens_protecao":
        return "Média de itens de proteção"
    if coluna == "populacao_estimada":
        return "População estimada"
    if coluna == "populacao_sem_plano_estimada":
        return "População estimada sem plano"
    if coluna == "correlacao_abs":
        return "Correlação absoluta"
    return nome_indicador(coluna)


def template_rotulo(coluna: str) -> str:
    return "%{text:.1f}%" if eh_percentual(coluna) else "%{text:.1f}"


def ordenar_mes(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty or "ordem_mes" not in df.columns:
        return df
    return df.sort_values("ordem_mes")


def filtrar_mes(df: pd.DataFrame, mes: str) -> pd.DataFrame:
    if df.empty or mes == "Todos" or "mes_nome" not in df.columns:
        return df.copy()
    return df[df["mes_nome"] == mes].copy()


AVISO_RECORTE_TRANSVERSAL = (
    "Para rankings e comparações transversais, utilizamos o último mês disponível quando o filtro está em Todos, "
    "evitando mistura de recortes mensais."
)


def ultimo_mes_disponivel(df: pd.DataFrame) -> str:
    if df.empty or "mes_nome" not in df.columns:
        return "n/d"
    ref = linha_referencia(df)
    if ref is None:
        return "n/d"
    return str(ref.get("mes_nome", "n/d"))


def periodo_disponivel(df: pd.DataFrame) -> str:
    if df.empty or "mes_nome" not in df.columns:
        return "n/d"
    meses_df = ordenar_mes(df)["mes_nome"].dropna().drop_duplicates().tolist()
    if not meses_df:
        return "n/d"
    if len(meses_df) == 1:
        return str(meses_df[0])
    return f"{meses_df[0]} a {meses_df[-1]}"


def filtrar_recorte_transversal(df: pd.DataFrame, mes: str) -> pd.DataFrame:
    if df.empty or "mes_nome" not in df.columns:
        return df.copy()
    if mes != "Todos":
        return filtrar_mes(df, mes)

    ordenado = ordenar_mes(df)
    if "ordem_mes" in ordenado.columns and ordenado["ordem_mes"].notna().any():
        ultimo = ordenado["ordem_mes"].max()
        return ordenado[ordenado["ordem_mes"] == ultimo].copy()

    ultimo_mes = ordenado["mes_nome"].dropna().iloc[-1]
    return ordenado[ordenado["mes_nome"] == ultimo_mes].copy()


def aviso_recorte_transversal():
    if mes_global == "Todos":
        st.info(AVISO_RECORTE_TRANSVERSAL)


def filtrar_amostra_grafico(df: pd.DataFrame, contexto: str) -> pd.DataFrame:
    if df.empty or "n_amostra" not in df.columns:
        return df

    amostra = pd.to_numeric(df["n_amostra"], errors="coerce")
    pequenos = amostra.notna() & (amostra < 30)
    if pequenos.any():
        st.warning(
            f"{contexto}: {int(pequenos.sum())} registro(s) com n_amostra < 30 foram removidos do gráfico principal."
        )
        return df.loc[~pequenos].copy()
    return df


def media_ponderada(df: pd.DataFrame, coluna: str, peso: str = "populacao_estimada") -> float:
    if df.empty or coluna not in df.columns:
        return np.nan
    dados = df[[coluna] + ([peso] if peso in df.columns else [])].dropna(subset=[coluna]).copy()
    if dados.empty:
        return np.nan
    valores = pd.to_numeric(dados[coluna], errors="coerce")
    if peso in dados.columns:
        pesos = pd.to_numeric(dados[peso], errors="coerce").fillna(0)
        validos = valores.notna() & (pesos > 0)
        if validos.any():
            return np.average(valores[validos], weights=pesos[validos])
    return valores.mean()


def agregar_ponderado(df: pd.DataFrame, grupo: list[str], colunas: list[str]) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()
    linhas = []
    for chaves, g in df.groupby(grupo, dropna=False):
        if not isinstance(chaves, tuple):
            chaves = (chaves,)
        linha = dict(zip(grupo, chaves))
        if "n_amostra" in g.columns:
            linha["n_amostra"] = g["n_amostra"].sum()
        if "populacao_estimada" in g.columns:
            linha["populacao_estimada"] = g["populacao_estimada"].sum()
        for col in colunas:
            if col in g.columns:
                linha[col] = media_ponderada(g, col)
        linhas.append(linha)
    return pd.DataFrame(linhas)


def coletar_meses(dados: dict[str, pd.DataFrame]) -> list[str]:
    meses = []
    for df in dados.values():
        if not df.empty and "mes_nome" in df.columns:
            meses.extend(df["mes_nome"].dropna().unique().tolist())
    return sorted(set(meses), key=lambda mes: MESES_ORDEM.get(mes, 99))


def filtro_lateral(df: pd.DataFrame, coluna: str, label: str, limite: int | None = None) -> pd.DataFrame:
    if df.empty or coluna not in df.columns:
        return df
    opcoes = sorted(df[coluna].dropna().unique().tolist(), key=str)
    if limite:
        opcoes = opcoes[:limite]
    if not opcoes:
        return df
    selecionados = st.sidebar.multiselect(label, opcoes, default=opcoes)
    if not selecionados:
        return df.iloc[0:0].copy()
    return df[df[coluna].isin(selecionados)].copy()


def aplicar_layout_fig(fig, yaxis_title: str = "Percentual"):
    fig.update_layout(
        template="plotly_white",
        colorway=PALETA,
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(color="#172033", size=12),
        title_x=0.01,
        title_font_size=18,
        legend_title_text="",
        margin=dict(l=16, r=16, t=62, b=34),
        xaxis_title="",
        yaxis_title=yaxis_title,
        hovermode="x unified",
        hoverlabel=dict(bgcolor="#FFFFFF", font_color="#172033", bordercolor="#D9E2EC"),
    )
    fig.update_xaxes(showgrid=False, automargin=True, tickfont=dict(color="#334155"))
    fig.update_yaxes(gridcolor="#E5E7EB", zerolinecolor="#D1D5DB", automargin=True, tickfont=dict(color="#334155"))
    return fig


def grafico_barras(
    df: pd.DataFrame,
    x: str,
    y: str,
    titulo: str,
    color: str | None = None,
    orientation: str = "v",
    top: int | None = None,
    xaxis_title: str | None = None,
    yaxis_title: str | None = None,
):
    if df.empty or x not in df.columns or y not in df.columns:
        st.info("Dados insuficientes para este gráfico.")
        return
    df = filtrar_amostra_grafico(df, titulo)
    dados = df.dropna(subset=[x, y]).copy()
    dados[y] = pd.to_numeric(dados[y], errors="coerce")
    dados = dados.dropna(subset=[y])
    eixo_categoria = x
    if orientation == "h" and dados[x].duplicated().any():
        if color and color in dados.columns:
            dados["_categoria_plot"] = dados[x].astype(str) + " | " + dados[color].astype(str)
            eixo_categoria = "_categoria_plot"
        else:
            st.warning(
                f"{titulo}: categorias duplicadas foram consolidadas pelo maior valor para evitar sobreposição visual."
            )
            dados = dados.sort_values(y, ascending=False).drop_duplicates(subset=[x], keep="first")
    if top:
        dados = dados.sort_values(y, ascending=False).head(top)
    if dados.empty:
        st.info("Não há registros válidos para este gráfico.")
        return

    fig = px.bar(
        dados,
        x=x if orientation == "v" else y,
        y=y if orientation == "v" else eixo_categoria,
        color=color if color in dados.columns else None,
        orientation=orientation,
        title=titulo,
        text=y,
        custom_data=[c for c in ["n_amostra", "populacao_estimada"] if c in dados.columns],
    )
    if color and color in dados.columns:
        fig.update_layout(barmode="group")
    fig.update_traces(texttemplate=template_rotulo(y), textposition="outside", cliponaxis=False)
    aplicar_layout_fig(fig, yaxis_title="" if orientation == "h" else titulo_eixo(y, yaxis_title))
    if orientation == "h":
        fig.update_layout(xaxis_title=titulo_eixo(y, xaxis_title))
        fig.update_yaxes(categoryorder="total ascending")
    else:
        fig.update_layout(xaxis_title=xaxis_title or "")
    st.plotly_chart(fig, width="stretch")


def grafico_linhas(df: pd.DataFrame, x: str, y_cols: list[str], titulo: str):
    colunas = [col for col in y_cols if col in df.columns]
    if df.empty or x not in df.columns or not colunas:
        st.info("Dados insuficientes para este gráfico.")
        return
    df = filtrar_amostra_grafico(df, titulo)
    if df.empty:
        st.info("Não há registros com amostra suficiente para este gráfico.")
        return
    dados = ordenar_mes(df)[[x] + colunas].dropna(how="all", subset=colunas)
    dados_long = dados.melt(id_vars=x, value_vars=colunas, var_name="indicador", value_name="percentual")
    dados_long["indicador"] = dados_long["indicador"].map(nome_indicador)
    fig = px.line(dados_long, x=x, y="percentual", color="indicador", markers=True, title=titulo)
    fig.update_traces(line_width=3, marker_size=8)
    aplicar_layout_fig(fig)
    st.plotly_chart(fig, width="stretch")


def grafico_dispersao(df: pd.DataFrame, x: str, y: str, titulo: str, color: str | None = None):
    if df.empty or x not in df.columns or y not in df.columns:
        st.info("Dados insuficientes para este gráfico.")
        return
    df = filtrar_amostra_grafico(df, titulo)
    dados = df.dropna(subset=[x, y]).copy()
    if dados.empty:
        st.info("Não há registros com amostra suficiente para este gráfico.")
        return
    fig = px.scatter(
        dados,
        x=x,
        y=y,
        size="populacao_estimada" if "populacao_estimada" in dados.columns else None,
        color=color if color in dados.columns else None,
        hover_name="uf_sigla" if "uf_sigla" in dados.columns else None,
        title=titulo,
    )
    fig.update_traces(marker=dict(opacity=0.78, line=dict(width=1, color="#FFFFFF")))
    aplicar_layout_fig(fig, yaxis_title=nome_indicador(y))
    fig.update_layout(xaxis_title=nome_indicador(x))
    st.plotly_chart(fig, width="stretch")


def chamada(tipo: str, texto: str):
    classes = {
        "leitura": "callout",
        "acao": "callout callout-action",
        "cuidado": "callout callout-warning",
        "risco": "callout callout-risk",
    }
    titulos = {
        "leitura": "Leitura executiva",
        "acao": "Ação recomendada",
        "cuidado": "Critério de interpretação",
        "risco": "Implicação hospitalar",
    }
    st.markdown(
        f"<div class='{classes[tipo]}'><strong>{titulos[tipo]}:</strong> {texto}</div>",
        unsafe_allow_html=True,
    )


def cabecalho(titulo: str, contexto: str):
    st.header(titulo)
    st.markdown(f"<div class='section-note'>{contexto}</div>", unsafe_allow_html=True)


def tabela_tecnica(titulo: str, df: pd.DataFrame):
    with st.expander(titulo, expanded=False):
        if df.empty:
            st.info("Arquivo sem registros após os filtros.")
        else:
            st.dataframe(df.drop(columns=["ordem_mes"], errors="ignore"), width="stretch", hide_index=True)


def metricas(cols: list[tuple[str, str, str | None]]):
    colunas = st.columns(len(cols))
    for col, (label, valor, ajuda) in zip(colunas, cols):
        with col:
            st.metric(label, valor, help=ajuda)


def card_periodo_referencia(valor: str, legenda: str):
    st.markdown(
        f"""
        <div class="reference-card" title="{legenda}">
            <div class="reference-card-label">Período de referência</div>
            <div class="reference-card-value">{valor}</div>
            <div class="reference-card-note">{legenda}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def linha_referencia(df: pd.DataFrame) -> pd.Series | None:
    if df.empty:
        return None
    return ordenar_mes(df).iloc[-1]


CATEGORIAS_AUDITORIA = {
    "barreira": ["faixa_renda", "plano_saude"],
    "informalidade": ["categoria_ocupacional", "formalidade_trabalho", "grau_isolamento"],
    "perfil_grave": ["faixa_etaria", "raca", "faixa_renda", "plano_saude"],
    "protecao_social": ["faixa_renda"],
    "mapa_desigualdade": ["uf_sigla", "regiao"],
    "escolaridade_genero": ["sexo", "escolaridade"],
    "moradia": ["moradia", "nivel_protecao_domiciliar"],
    "sus_privado": ["local_atendimento", "plano_saude"],
}


def meses_disponiveis_texto(df: pd.DataFrame) -> str:
    if df.empty or "mes_nome" not in df.columns:
        return "não se aplica"
    return ", ".join(ordenar_mes(df)["mes_nome"].dropna().drop_duplicates().astype(str).tolist())


def contar_categorias_duplicadas_todos(chave: str, df: pd.DataFrame) -> int | str:
    cols = CATEGORIAS_AUDITORIA.get(chave)
    if df.empty or not cols or not set(cols).issubset(df.columns):
        return "não se aplica"
    try:
        labels = df[cols].fillna("Sem informação").apply(
            lambda row: " | ".join([str(valor) for valor in row]),
            axis=1,
        )
        return int(labels.duplicated().sum())
    except Exception:
        return "não calculado"


dados = carregar_todos()
meses = coletar_meses(dados)

st.sidebar.title("PNAD COVID-19")
st.sidebar.caption("Painel hospitalar com CSVs locais materializados.")

pagina = st.sidebar.radio(
    "Navegação",
    [
        "1. Visão executiva",
        "2. Sinais de alerta",
        "3. Acesso ao cuidado",
        "4. Perfil clínico",
        "5. Territórios e rede",
        "6. Trabalho e proteção social",
        "7. Correlações e critérios",
        "8. Plano de ação",
    ],
)

mes_global = st.sidebar.selectbox("Mês de análise", ["Todos"] + meses, index=0)
st.sidebar.markdown(
    "<span class='small-note'>O filtro usa apenas a coluna mes_nome dos CSVs disponíveis.</span>",
    unsafe_allow_html=True,
)

st.markdown("<div class='hero-title'>Painel Hospitalar | PNAD COVID-19</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='hero-subtitle'>Leitura clínica, social e territorial para planejamento de resposta em novos surtos.</div>",
    unsafe_allow_html=True,
)


if pagina == "1. Visão executiva":
    cabecalho(
        "Síntese para decisão assistencial",
        "Resumo dos sinais de demanda, acesso e vulnerabilidade que orientam triagem, leitos e comunicação.",
    )

    df_ev_serie = ordenar_mes(dados["evolucao"])
    df_ev_ref = filtrar_recorte_transversal(dados["evolucao"], mes_global)
    df_territorio = filtrar_recorte_transversal(dados["mapa_desigualdade"], mes_global)
    df_perfil = filtrar_recorte_transversal(dados["perfil_grave"], mes_global)
    ref = linha_referencia(df_ev_ref)
    aviso_recorte_transversal()

    if ref is not None:
        if mes_global == "Todos":
            col_periodo, col_indicadores, col_positividade, col_internacao = st.columns(4)
            with col_periodo:
                card_periodo_referencia("Set-Nov/2020", "Setembro a Novembro de 2020")
            with col_indicadores:
                st.metric(
                    "Indicadores de referência",
                    str(ref.get("mes_nome", "n/d")),
                    help="Último mês disponível usado nos cards e rankings transversais.",
                )
            with col_positividade:
                st.metric(
                    "% positividade",
                    fmt_pct(ref.get("pct_positivo_entre_resultados_validos")),
                    help="Entre resultados válidos.",
                )
            with col_internacao:
                st.metric(
                    "% internação",
                    fmt_pct(ref.get("pct_internado_entre_atendidos")),
                    help="Entre pessoas que buscaram atendimento.",
                )
        else:
            metricas_ref = [
                ("Mês de referência", str(ref.get("mes_nome", "n/d")), "Mês selecionado no filtro global."),
                ("População estimada", fmt_num(ref.get("populacao_estimada")), "Peso populacional agregado no CSV."),
                ("% positividade", fmt_pct(ref.get("pct_positivo_entre_resultados_validos")), "Entre resultados válidos."),
                ("% internação", fmt_pct(ref.get("pct_internado_entre_atendidos")), "Entre pessoas que buscaram atendimento."),
            ]
            metricas(metricas_ref)

    col1, col2 = st.columns([1.15, 1])
    with col1:
        grafico_linhas(
            df_ev_serie,
            "mes_nome",
            ["pct_fez_teste", "pct_positivo_entre_resultados_validos", "pct_internado_entre_atendidos"],
            "Indicadores mensais de alerta operacional",
        )
    with col2:
        ranking = df_territorio.copy()
        if not ranking.empty and "uf_sigla" in ranking.columns:
            ranking["territorio"] = ranking["uf_sigla"] + " | " + ranking["regiao"].astype(str)
        grafico_barras(
            ranking,
            "territorio" if "territorio" in ranking.columns else "regiao",
            "pct_sem_plano",
            "UFs com maior percentual de população sem plano de saúde",
            orientation="h",
            top=8,
            xaxis_title="Percentual sem plano de saúde",
        )

    if not df_perfil.empty:
        grupo = agregar_ponderado(
            df_perfil,
            ["faixa_etaria"],
            ["pct_alguma_comorbidade", "pct_internado_entre_atendidos", "pct_entubado_entre_internados"],
        )
        grafico_barras(
            grupo,
            "faixa_etaria",
            "pct_alguma_comorbidade",
            "Comorbidades por faixa etária",
            orientation="v",
        )

    chamada(
        "leitura",
        "A combinação de positividade, sintomas respiratórios, internação entre atendidos e percentual de população sem plano funciona como painel de pressão assistencial.",
    )
    chamada(
        "risco",
        "Quando esses sinais crescem juntos, o hospital deve antecipar gargalos de triagem, oxigênio, leitos e encaminhamento para rede SUS.",
    )
    chamada(
        "acao",
        "Acompanhar semanalmente os grupos de maior vulnerabilidade clínica e territorial antes de abrir expansão de capacidade em regime emergencial.",
    )
    tabela_tecnica("Dados técnicos usados nesta visão", pd.concat([df_ev_ref, df_territorio], axis=0, ignore_index=True))


elif pagina == "2. Sinais de alerta":
    cabecalho(
        "Evolução mensal para alerta operacional",
        "Série agregada de testagem, positividade, sintomas e gravidade para apoiar gatilhos de contingência.",
    )
    df = ordenar_mes(dados["evolucao"])

    if df.empty:
        st.warning("Arquivo analise_06_evolucao_mensal.csv sem dados.")
    else:
        st.info("Esta página mostra a série temporal completa disponível no CSV, ordenada por v1013.")
        ref = linha_referencia(df)
        metricas(
            [
                ("Indicadores de referência", str(ref.get("mes_nome", "n/d")), "Último mês disponível na série temporal."),
                ("% fez teste", fmt_pct(ref.get("pct_fez_teste")), "Percentual de pessoas com teste registrado."),
                ("% positividade", fmt_pct(ref.get("pct_positivo_entre_resultados_validos")), "Entre resultados válidos."),
                ("% dificuldade respiratória", fmt_pct(ref.get("pct_dificuldade_respirar")), "Sintoma de maior prioridade clínica."),
            ]
        )

        col1, col2 = st.columns(2)
        with col1:
            grafico_linhas(df, "mes_nome", ["pct_fez_teste", "pct_positivo_entre_resultados_validos"], "Testagem e positividade")
        with col2:
            grafico_linhas(df, "mes_nome", ["pct_dificuldade_respirar", "pct_perda_cheiro_sabor"], "Sintomas monitorados")
        grafico_linhas(
            df,
            "mes_nome",
            ["pct_internado_entre_atendidos", "pct_entubado_entre_internados"],
            "Gravidade entre atendidos e internados",
        )

        chamada(
            "leitura",
            "A curva mensal deve ser lida como sinal de pressão, não como previsão automática. A internação é medida entre atendidos.",
        )
        chamada(
            "acao",
            "Definir gatilhos internos para reforço de equipe, estoque de oxigênio, EPIs e comunicação ao pronto atendimento.",
        )
        chamada("cuidado", "Internação entre atendidos não representa taxa de internação sobre toda a população pesquisada.")
        tabela_tecnica("Tabela técnica: evolução mensal", ordenar_mes(df))


elif pagina == "3. Acesso ao cuidado":
    cabecalho(
        "Renda, plano de saúde e porta de entrada",
        "Avalia barreiras de acesso e diferenças entre locais de atendimento para orientar fluxo assistencial.",
    )
    df_barreira = filtrar_recorte_transversal(dados["barreira"], mes_global)
    df_sus = filtrar_recorte_transversal(dados["sus_privado"], mes_global)
    aviso_recorte_transversal()

    df_barreira = filtro_lateral(df_barreira, "faixa_renda", "Faixa de renda")
    df_barreira = filtro_lateral(df_barreira, "plano_saude", "Plano de saúde")
    df_sus = filtro_lateral(df_sus, "local_atendimento", "Local de atendimento")
    df_sus = filtro_lateral(df_sus, "plano_saude", "Plano de saúde na rede")

    metricas(
        [
            ("% buscou atendimento", fmt_pct(media_ponderada(df_barreira, "pct_buscou_atendimento")), "Média ponderada por população estimada."),
            ("% internação", fmt_pct(media_ponderada(df_barreira, "pct_internado_entre_atendidos")), "Entre atendidos."),
            ("% entubação", fmt_pct(media_ponderada(df_sus, "pct_entubado_entre_internados")), "Entre internados."),
            ("% comorbidade", fmt_pct(media_ponderada(df_sus, "pct_alguma_comorbidade")), "Nos registros por local de atendimento."),
        ]
    )

    col1, col2 = st.columns(2)
    with col1:
        grafico_barras(
            df_barreira,
            "faixa_renda",
            "pct_buscou_atendimento",
            "Busca por atendimento por renda e plano",
            color="plano_saude",
        )
    with col2:
        grafico_barras(
            df_barreira,
            "faixa_renda",
            "pct_internado_entre_atendidos",
            "Internação entre atendidos por renda e plano",
            color="plano_saude",
        )

    grafico_barras(
        df_sus,
        "local_atendimento",
        "pct_internado_entre_atendidos",
        "Gravidade por local de atendimento e plano",
        color="plano_saude",
        orientation="h",
    )

    chamada(
        "leitura",
        "Renda e plano de saúde ajudam a qualificar barreiras de acesso e a provável concentração de demanda na rede pública.",
    )
    chamada(
        "acao",
        "Organizar fluxos de encaminhamento entre pronto atendimento, UPA/SUS, hospital SUS e rede privada conforme sinais de gravidade.",
    )
    chamada(
        "cuidado",
        "Locais de atendimento não devem ser somados como partes de um único total; podem representar respostas múltiplas.",
    )
    tabela_tecnica("Tabela técnica: barreira econômica", df_barreira)
    tabela_tecnica("Tabela técnica: SUS x privado", df_sus)


elif pagina == "4. Perfil clínico":
    cabecalho(
        "Grupos com maior vulnerabilidade clínica",
        "Cruza faixa etária, raça, renda e plano com comorbidades e desfechos de gravidade.",
    )
    df = filtrar_recorte_transversal(dados["perfil_grave"], mes_global)
    aviso_recorte_transversal()
    df = filtro_lateral(df, "faixa_etaria", "Faixa etária")
    df = filtro_lateral(df, "raca", "Raça/cor")
    df = filtro_lateral(df, "faixa_renda", "Faixa de renda clínica")
    df = filtro_lateral(df, "plano_saude", "Plano de saúde clínico")

    metricas(
        [
            ("% alguma comorbidade", fmt_pct(media_ponderada(df, "pct_alguma_comorbidade")), "Diabetes, hipertensão, asma, coração, depressão ou câncer."),
            ("% hipertensão", fmt_pct(media_ponderada(df, "pct_hipertensao")), "Média ponderada."),
            ("% internação", fmt_pct(media_ponderada(df, "pct_internado_entre_atendidos")), "Entre atendidos."),
            ("% entubação", fmt_pct(media_ponderada(df, "pct_entubado_entre_internados")), "Entre internados."),
        ]
    )

    grupo_idade = agregar_ponderado(
        df,
        ["faixa_etaria"],
        ["pct_alguma_comorbidade", "pct_hipertensao", "pct_diabetes", "pct_internado_entre_atendidos"],
    )
    grupo_renda = agregar_ponderado(
        df,
        ["faixa_renda", "plano_saude"],
        ["pct_alguma_comorbidade", "pct_internado_entre_atendidos"],
    )

    col1, col2 = st.columns(2)
    with col1:
        grafico_barras(grupo_idade, "faixa_etaria", "pct_alguma_comorbidade", "Comorbidades por faixa etária")
    with col2:
        grafico_barras(grupo_idade, "faixa_etaria", "pct_internado_entre_atendidos", "Internação entre atendidos por faixa etária")
    grafico_barras(
        grupo_renda,
        "faixa_renda",
        "pct_alguma_comorbidade",
        "Comorbidades por renda e plano de saúde",
        color="plano_saude",
    )

    chamada(
        "leitura",
        "Faixa etária e comorbidades sustentam a priorização clínica. Renda e plano qualificam risco de acesso tardio.",
    )
    chamada(
        "acao",
        "Priorizar triagem respiratória e monitoramento ativo para grupos com maior carga de comorbidade e sinais de agravamento.",
    )
    chamada("cuidado", "Recortes com amostra pequena devem ser interpretados em conjunto com outros indicadores e não devem orientar decisão isolada.")
    tabela_tecnica("Tabela técnica: perfil grave", df)


elif pagina == "5. Territórios e rede":
    cabecalho(
        "Territórios vulneráveis e dependência da rede",
        "Identifica UFs/regiões com maior proporção sem plano, baixa renda, informalidade e menor proteção domiciliar.",
    )
    df = filtrar_recorte_transversal(dados["mapa_desigualdade"], mes_global)
    aviso_recorte_transversal()
    df = filtro_lateral(df, "regiao", "Região")
    if not df.empty and "uf_sigla" in df.columns:
        df["territorio"] = df["uf_sigla"] + " | " + df["regiao"].astype(str)

    metricas(
        [
            ("% sem plano", fmt_pct(media_ponderada(df, "pct_sem_plano")), "Dependência potencial da rede pública."),
            ("% até 1 SM", fmt_pct(media_ponderada(df, "pct_ate_1_sm_entre_renda_informada")), "Entre renda informada."),
            ("% informalidade", fmt_pct(media_ponderada(df, "pct_informal_entre_ocupados_com_info")), "Entre ocupados com informação."),
            ("Proteção domiciliar", fmt_num(media_ponderada(df, "media_itens_protecao"), 2), "Média de itens de proteção."),
        ]
    )

    col1, col2 = st.columns(2)
    with col1:
        grafico_barras(
            df,
            "territorio",
            "pct_sem_plano",
            "UFs com maior percentual de população sem plano de saúde",
            orientation="h",
            top=10,
            xaxis_title="Percentual sem plano de saúde",
        )
    with col2:
        grafico_barras(
            df,
            "territorio",
            "pct_ate_1_sm_entre_renda_informada",
            "UFs com maior percentual de população até 1 salário mínimo",
            orientation="h",
            top=10,
            xaxis_title="Percentual até 1 salário mínimo",
        )
    grafico_dispersao(
        df,
        "pct_sem_plano",
        "pct_informal_entre_ocupados_com_info",
        "Percentual sem plano x informalidade por UF",
    )

    chamada(
        "leitura",
        "A leitura é por UF. A região no rótulo indica a localização da UF, não um total regional comparável.",
    )
    chamada(
        "acao",
        "Antecipar campanhas, testagem orientada e pactuação de leitos nos territórios com maior vulnerabilidade combinada.",
    )
    tabela_tecnica("Tabela técnica: mapa de desigualdade", df)


elif pagina == "6. Trabalho e proteção social":
    cabecalho(
        "Exposição econômica, proteção social e moradia",
        "Relaciona trabalho presencial, benefícios sociais, endividamento e proteção domiciliar com sinais de pressão clínica.",
    )
    df_inf = filtrar_recorte_transversal(dados["informalidade"], mes_global)
    df_social = filtrar_recorte_transversal(dados["protecao_social"], mes_global)
    df_moradia = filtrar_recorte_transversal(dados["moradia"], mes_global)
    df_esc = filtrar_recorte_transversal(dados["escolaridade_genero"], mes_global)
    aviso_recorte_transversal()

    aba1, aba2, aba3 = st.tabs(["Trabalho", "Proteção social", "Moradia"])

    with aba1:
        df_inf = filtro_lateral(df_inf, "categoria_ocupacional", "Categoria ocupacional")
        df_inf = filtro_lateral(df_inf, "formalidade_trabalho", "Formalidade")
        df_inf = filtro_lateral(df_inf, "grau_isolamento", "Grau de isolamento")

        metricas(
            [
                ("% trabalhou", fmt_pct(media_ponderada(df_inf, "pct_trabalhou")), "Média ponderada."),
                ("% home office", fmt_pct(media_ponderada(df_inf, "pct_home_office")), "Proxy de menor exposição presencial."),
                ("% internação", fmt_pct(media_ponderada(df_inf, "pct_internado_entre_atendidos")), "Entre atendidos."),
            ]
        )
        grafico_barras(
            df_inf,
            "categoria_ocupacional",
            "pct_home_office",
            "Home office por ocupação e formalidade",
            color="formalidade_trabalho",
            orientation="h",
            top=12,
        )
        grafico_barras(
            df_inf,
            "categoria_ocupacional",
            "pct_internado_entre_atendidos",
            "Internação entre atendidos por ocupação",
            color="grau_isolamento",
            orientation="h",
            top=12,
        )
        tabela_tecnica("Tabela técnica: informalidade e risco", df_inf)

    with aba2:
        df_social = filtro_lateral(df_social, "faixa_renda", "Renda em proteção social")
        metricas(
            [
                ("% auxílio", fmt_pct(media_ponderada(df_social, "pct_recebeu_auxilio")), "Recebimento de auxílio emergencial."),
                ("% Bolsa Família", fmt_pct(media_ponderada(df_social, "pct_recebeu_bolsa_familia")), "Benefício informado no CSV."),
                ("% buscou atendimento", fmt_pct(media_ponderada(df_social, "pct_buscou_atendimento")), "Busca por cuidado."),
            ]
        )
        df_social_grafico = filtrar_amostra_grafico(df_social, "Benefícios sociais por renda")
        df_long = df_social_grafico.melt(
            id_vars=["faixa_renda"],
            value_vars=[c for c in ["pct_recebeu_auxilio", "pct_recebeu_bolsa_familia", "pct_recebeu_seguro_desemprego"] if c in df_social_grafico],
            var_name="indicador",
            value_name="percentual",
        )
        df_long["indicador"] = df_long["indicador"].map(nome_indicador)
        fig = px.bar(df_long.dropna(), x="faixa_renda", y="percentual", color="indicador", barmode="group", title="Benefícios sociais por renda", text="percentual")
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside", cliponaxis=False)
        aplicar_layout_fig(fig)
        st.plotly_chart(fig, width="stretch")
        tabela_tecnica("Tabela técnica: proteção social", df_social)

    with aba3:
        df_moradia = filtro_lateral(df_moradia, "moradia", "Condição de moradia")
        df_moradia = filtro_lateral(df_moradia, "nivel_protecao_domiciliar", "Proteção domiciliar")
        grupo = agregar_ponderado(
            df_moradia,
            ["nivel_protecao_domiciliar"],
            ["pct_pegou_emprestimo", "pct_recebeu_seguro_desemprego", "pct_internado_entre_atendidos", "media_itens_protecao"],
        )
        metricas(
            [
                ("% empréstimo", fmt_pct(media_ponderada(df_moradia, "pct_pegou_emprestimo")), "Sinal de pressão financeira."),
                ("% seguro desemprego", fmt_pct(media_ponderada(df_moradia, "pct_recebeu_seguro_desemprego")), "Proteção social relacionada ao trabalho."),
                ("Itens de proteção", fmt_num(media_ponderada(df_moradia, "media_itens_protecao"), 2), "Média informada no CSV."),
            ]
        )
        col1, col2 = st.columns(2)
        with col1:
            grafico_barras(grupo, "nivel_protecao_domiciliar", "pct_pegou_emprestimo", "Endividamento por proteção domiciliar")
        with col2:
            grafico_barras(grupo, "nivel_protecao_domiciliar", "media_itens_protecao", "Itens de proteção por domicílio")
        tabela_tecnica("Tabela técnica: moradia e endividamento", df_moradia)

    chamada(
        "leitura",
        "Trabalho presencial, menor home office e fragilidade social reduzem a capacidade de isolamento e podem aumentar demanda tardia.",
    )
    chamada(
        "acao",
        "Direcionar comunicação preventiva a trabalhadores presenciais e acionar rede de atenção básica e assistência social para domicílios vulneráveis.",
    )
    chamada("cuidado", "As associações por trabalho, renda e moradia não devem ser interpretadas como causalidade.")


elif pagina == "7. Correlações e critérios":
    cabecalho(
        "Correlação econômico-clínica",
        "Leitura exploratória das relações sociais com internação e entubação, preservando critérios de interpretação estatística.",
    )
    df = dados["correlacoes"].copy()
    if df.empty:
        st.warning("Arquivo correlacoes_economico_clinico.csv sem dados.")
    else:
        df["correlacao_abs"] = df["correlacao"].abs()
        df["par"] = df["variavel_social"].astype(str) + " -> " + df["desfecho_clinico"].astype(str)
        df = df.sort_values("correlacao_abs")

        metricas(
            [
                ("Maior |correlação|", fmt_num(df["correlacao_abs"].max(), 4), "Força absoluta máxima observada."),
                ("Pares avaliados", fmt_num(df.shape[0]), "Linhas do CSV de correlações."),
                ("Interpretação predominante", df["interpretacao"].mode().iloc[0], "Classificação do próprio arquivo."),
            ]
        )
        fig = px.bar(
            df,
            x="correlacao_abs",
            y="par",
            color="direcao",
            orientation="h",
            title="Força absoluta das correlações sociais x desfechos clínicos",
            text="correlacao",
        )
        fig.update_traces(texttemplate="%{text:.3f}", textposition="outside", cliponaxis=False)
        aplicar_layout_fig(fig, yaxis_title="")
        fig.update_layout(xaxis_title="Correlação absoluta")
        st.plotly_chart(fig, width="stretch")

        chamada(
            "leitura",
            "As correlações são muito fracas. Elas ajudam a compor contexto social, mas não substituem avaliação clínica nem planejamento de capacidade.",
        )
        chamada("cuidado", "Correlação não significa causalidade. Alguns métodos são exploratórios e não ponderados, conforme observação do próprio CSV.")
        chamada(
            "acao",
            "Usar correlações apenas como apoio à discussão acadêmica e à priorização de monitoramento, não como regra automática de decisão.",
        )
        tabela_tecnica("Tabela técnica: correlações", df.drop(columns=["correlacao_abs"], errors="ignore"))


elif pagina == "8. Plano de ação":
    cabecalho(
        "Matriz executiva para novo surto",
        "Plano de resposta hospitalar organizado por sinal observado, risco, resposta recomendada e área responsável.",
    )

    matriz = pd.DataFrame(
        [
            {
                "sinal observado": "Aumento de positividade",
                "risco hospitalar": "Maior entrada de casos suspeitos e pressão sobre triagem",
                "resposta recomendada": "Reforçar testagem orientada, isolamento informado e comunicação ao pronto atendimento",
                "área responsável": "Vigilância hospitalar e Pronto Atendimento",
            },
            {
                "sinal observado": "Alta dificuldade respiratória",
                "risco hospitalar": "Crescimento de demanda por avaliação rápida e suporte ventilatório",
                "resposta recomendada": "Preparar fluxo respiratório, oxigênio, sala de estabilização e critérios de transferência",
                "área responsável": "Emergência, Enfermagem e Engenharia Clínica",
            },
            {
                "sinal observado": "Internação entre atendidos em alta",
                "risco hospitalar": "Ocupação acelerada de leitos e equipes",
                "resposta recomendada": "Acionar plano de leitos, escala de contingência e revisão diária de capacidade",
                "área responsável": "NIR, Direção Assistencial e Clínica Médica",
            },
            {
                "sinal observado": "Territórios com alto percentual sem plano",
                "risco hospitalar": "Maior dependência da rede SUS e risco de chegada tardia",
                "resposta recomendada": "Pactuar referência, orientar UPA/SUS e antecipar campanhas locais",
                "área responsável": "Regulação, Atenção Básica e Gestão da Rede",
            },
            {
                "sinal observado": "Alta comorbidade em grupos específicos",
                "risco hospitalar": "Maior probabilidade de agravamento clínico",
                "resposta recomendada": "Priorizar triagem, monitoramento ativo e protocolos para crônicos",
                "área responsável": "Triagem, Equipe Médica e Segurança do Paciente",
            },
            {
                "sinal observado": "Baixa proteção social, moradia vulnerável ou endividamento",
                "risco hospitalar": "Menor adesão a isolamento e busca tardia por cuidado",
                "resposta recomendada": "Integrar orientação hospitalar com assistência social e atenção primária",
                "área responsável": "Serviço Social, Atenção Básica e Comunicação",
            },
            {
                "sinal observado": "Baixo home office em ocupações presenciais",
                "risco hospitalar": "Exposição contínua e maior circulação comunitária",
                "resposta recomendada": "Comunicação preventiva direcionada e orientação de sinais de alarme",
                "área responsável": "Comunicação, Saúde Ocupacional e Educação em Saúde",
            },
        ]
    )

    st.dataframe(matriz, width="stretch", hide_index=True)
    chamada(
        "leitura",
        "O painel deve ser usado como instrumento de priorização: combina sinais clínicos, acesso, território e vulnerabilidade social.",
    )
    chamada(
        "acao",
        "Revisar a matriz em reunião executiva e definir gatilhos objetivos de ativação para triagem, leitos, oxigênio, EPIs e comunicação.",
    )

    with st.expander("Ver notas metodológicas", expanded=False):
        criterios = pd.DataFrame(
            [
                ["Tamanho amostral", "Resultados com baixa contagem devem ser interpretados como evidência exploratória e analisados em conjunto com outros indicadores."],
                ["Internação entre atendidos", "O indicador expressa a proporção de internações entre pessoas que buscaram atendimento, não uma taxa populacional geral."],
                ["Correlação", "Associações estatísticas descrevem coocorrência entre variáveis e não devem ser interpretadas, isoladamente, como relação causal."],
                ["Locais de atendimento", "Categorias de local de atendimento podem representar respostas múltiplas e não devem ser somadas como partes exclusivas de um único total."],
            ],
            columns=["critério de interpretação", "nota metodológica"],
        )
        st.dataframe(criterios, width="stretch", hide_index=True)


elif pagina == "Anexo técnico":
    cabecalho(
        "Validação dos CSVs usados no painel",
        "Conferência dos arquivos locais, número de linhas, colunas e campos percentuais carregados pelo Streamlit.",
    )

    resumo = []
    for chave, arquivo in ARQUIVOS.items():
        df = dados[chave]
        resumo.append(
            {
                "arquivo": arquivo,
                "linhas": df.shape[0],
                "colunas": df.shape[1],
                "meses disponíveis": meses_disponiveis_texto(df),
                "último mês disponível": ultimo_mes_disponivel(df),
                "categorias duplicadas em Todos": contar_categorias_duplicadas_todos(chave, df),
                "percentuais": len([c for c in df.columns if c.startswith("pct_")]),
                "status": "OK" if not df.empty else "vazio ou ausente",
            }
        )
    st.dataframe(pd.DataFrame(resumo), width="stretch", hide_index=True)
    chamada(
        "cuidado",
        "Alguns CSVs são recortes materializados por mês. Rankings e comparações transversais usam o último mês disponível quando o filtro está em Todos para não misturar recortes mensais.",
    )

    arquivo_sel = st.selectbox("Arquivo para auditoria", list(ARQUIVOS.values()))
    chave_sel = [chave for chave, arquivo in ARQUIVOS.items() if arquivo == arquivo_sel][0]
    df_sel = dados[chave_sel]

    metricas(
        [
            ("Linhas", fmt_num(df_sel.shape[0]), None),
            ("Colunas", fmt_num(df_sel.shape[1]), None),
            ("Campos vazios", fmt_num(df_sel.isna().sum().sum()), None),
        ]
    )
    with st.expander("Colunas do arquivo selecionado", expanded=False):
        st.code("\n".join(df_sel.columns.tolist()))
    tabela_tecnica("Tabela técnica: arquivo selecionado", df_sel)
    chamada(
        "cuidado",
        "O painel usa somente os CSVs da pasta dados_dashboard. Não há conexão com AWS, Athena, banco de dados, API ou internet.",
    )

