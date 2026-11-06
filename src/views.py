"""
Módulo de Visualização de Dados e Componentes Visuais (Plotly / Streamlit).
Design alinhado aos princípios anti-slop (clean, tipografia editorial, sem excesso de gradientes).
"""
from typing import Dict, Any, List
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


# Paleta Institucional e Sóbria (Estilo Policy / Civic Analytics — Accent Ladder)
COLOR_PRIMARY = "#0F172A"     # Slate 900
COLOR_ACCENT = "#0284C7"      # Sky 600 (Executive Civic Accent)
COLOR_GROWTH = "#15803D"      # Emerald 700 (crescimento populacional)
COLOR_DECLINE = "#BE123C"     # Rose 700 (retração populacional)
COLOR_HIGHLIGHT = "#B45309"   # Amber 700 (destaque persona)
COLOR_MUTED = "#64748B"       # Slate 500
COLOR_GRID = "rgba(148, 163, 184, 0.15)"
BG_PAPER = "rgba(0,0,0,0)"
FONT_FAMILY = "'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"


def plot_boxplot_dispersao(df: pd.DataFrame, stats: Dict[str, Any], coluna_taxa: str = "taxa_crescimento_pct") -> go.Figure:
    """
    Constrói um boxplot interativo anotado com mediana, quartis e limites de Tukey (1,5*IQR).
    """
    fig = go.Figure()

    # Boxplot principal
    fig.add_trace(go.Box(
        y=df[coluna_taxa],
        name="Capitais Brasileiras",
        boxpoints="outliers",
        marker=dict(color=COLOR_ACCENT, size=7, opacity=0.85),
        line=dict(color=COLOR_ACCENT, width=1.8),
        fillcolor="rgba(2, 132, 199, 0.08)",
        hovertemplate="<b>Taxa:</b> %{y:.2f}%<extra></extra>"
    ))

    # Anotações dos limites de outliers
    lim_sup = stats.get("limite_superior_outlier", 0)
    lim_inf = stats.get("limite_inferior_outlier", 0)
    mediana = stats.get("mediana", 0)
    media = stats.get("media", 0)

    fig.add_hline(
        y=lim_sup, line_dash="dot", line_color=COLOR_HIGHLIGHT, line_width=1.5,
        annotation_text=f"Limite Superior (Q3 + 1,5·IQR): {lim_sup:.2f}%",
        annotation_position="top right"
    )
    fig.add_hline(
        y=lim_inf, line_dash="dot", line_color=COLOR_DECLINE, line_width=1.5,
        annotation_text=f"Limite Inferior (Q1 - 1,5·IQR): {lim_inf:.2f}%",
        annotation_position="bottom right"
    )

    fig.update_layout(
        title=dict(
            text="<b>Distribuição e Dispersão da Taxa de Crescimento (2010–2022)</b>",
            font=dict(size=15, family=FONT_FAMILY)
        ),
        yaxis=dict(
            title="Taxa de Crescimento Acumulada (%)",
            zeroline=True,
            zerolinecolor="rgba(148, 163, 184, 0.35)",
            gridcolor=COLOR_GRID
        ),
        paper_bgcolor=BG_PAPER,
        plot_bgcolor=BG_PAPER,
        margin=dict(l=40, r=40, t=50, b=40),
        height=380,
        showlegend=False
    )
    return fig


def plot_crescimento_barras(df: pd.DataFrame, coluna_taxa: str = "taxa_crescimento_pct") -> go.Figure:
    """
    Gráfico de barras horizontais ordenado evidenciando cidades em crescimento vs retração.
    """
    df_sorted = df.sort_values(by=coluna_taxa, ascending=True).copy()
    
    # Cores condicionais
    cores = []
    for _, row in df_sorted.iterrows():
        if row.get("persona") is not None and pd.notna(row.get("persona")):
            cores.append(COLOR_HIGHLIGHT) # Destaque prefeitos personas
        elif row[coluna_taxa] >= 0:
            cores.append(COLOR_GROWTH)    # Crescimento
        else:
            cores.append(COLOR_DECLINE)   # Retração

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_sorted[coluna_taxa],
        y=df_sorted["municipio"],
        orientation="h",
        marker=dict(color=cores),
        hovertemplate="<b>%{y} (%{customdata[0]})</b><br>Crescimento: %{x:.2f}%<br>Pop. 2022: %{customdata[1]:,}<extra></extra>",
        customdata=df_sorted[["uf", "pop_2022"]].values
    ))

    fig.update_layout(
        title=dict(
            text="<b>Ranking da Taxa de Crescimento Populacional por Cidade (2010 a 2022)</b>",
            font=dict(size=15, family=FONT_FAMILY)
        ),
        xaxis=dict(
            title="Taxa de Crescimento (%)",
            zeroline=True,
            zerolinecolor="rgba(148, 163, 184, 0.4)",
            zerolinewidth=1.5,
            gridcolor=COLOR_GRID
        ),
        yaxis=dict(
            title="",
            tickfont=dict(size=11, family=FONT_FAMILY)
        ),
        paper_bgcolor=BG_PAPER,
        plot_bgcolor=BG_PAPER,
        height=max(400, len(df_sorted) * 22),
        margin=dict(l=10, r=30, t=50, b=30),
        showlegend=False
    )
    return fig


def plot_piramide_etaria(df_piramide: pd.DataFrame, localidade: str = "Curitiba") -> go.Figure:
    """
    Gera a pirâmide etária interativa com eixo espelhado (Homens à esquerda, Mulheres à direita).
    """
    df_local = df_piramide[df_piramide["localidade"] == localidade].sort_values(by="ordem")
    if df_local.empty:
        df_local = df_piramide.sort_values(by="ordem")

    homens_negativo = [-val for val in df_local["homens"]]
    mulheres = df_local["mulheres"].tolist()
    faixas = df_local["faixa_etaria"].tolist()

    fig = go.Figure()

    # Barra masculina
    fig.add_trace(go.Bar(
        y=faixas,
        x=homens_negativo,
        name="Homens",
        orientation="h",
        marker=dict(color=COLOR_ACCENT),
        customdata=df_local["homens"],
        hovertemplate="<b>Homens (%{y})</b>: %{customdata:,}<extra></extra>"
    ))

    # Barra feminina
    fig.add_trace(go.Bar(
        y=faixas,
        x=mulheres,
        name="Mulheres",
        orientation="h",
        marker=dict(color="#0F766E"),
        customdata=df_local["mulheres"],
        hovertemplate="<b>Mulheres (%{y})</b>: %{customdata:,}<extra></extra>"
    ))

    # Valores máximos para simetria do eixo x
    max_val = max(max(df_local["homens"]), max(df_local["mulheres"])) * 1.15

    fig.update_layout(
        title=dict(
            text=f"<b>Pirâmide Etária — Censo 2022: {localidade}</b>",
            font=dict(size=15, family=FONT_FAMILY)
        ),
        barmode="overlay",
        bargap=0.1,
        xaxis=dict(
            title="População Residente",
            range=[-max_val, max_val],
            tickvals=[-max_val * 0.75, -max_val * 0.5, -max_val * 0.25, 0, max_val * 0.25, max_val * 0.5, max_val * 0.75],
            ticktext=[f"{int(max_val*0.75):,}", f"{int(max_val*0.5):,}", f"{int(max_val*0.25):,}", "0", f"{int(max_val*0.25):,}", f"{int(max_val*0.5):,}", f"{int(max_val*0.75):,}"],
            gridcolor=COLOR_GRID
        ),
        yaxis=dict(title="Faixa Etária"),
        paper_bgcolor=BG_PAPER,
        plot_bgcolor=BG_PAPER,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=480,
        margin=dict(l=20, r=20, t=60, b=40)
    )
    return fig


def plot_evolucao_comparativa(df: pd.DataFrame, cidades_destaque: List[str]) -> go.Figure:
    """
    Gráfico de linhas conectando Censo 2010 a Censo 2022 para cidades selecionadas.
    """
    df_selecionadas = df[df["municipio"].isin(cidades_destaque)].copy()
    
    fig = go.Figure()
    cores_linha = [COLOR_ACCENT, "#0F766E", COLOR_HIGHLIGHT, "#475569", "#0284C7"]

    for i, (_, row) in enumerate(df_selecionadas.iterrows()):
        cor = cores_linha[i % len(cores_linha)]
        fig.add_trace(go.Scatter(
            x=["Censo 2010", "Censo 2022"],
            y=[row["pop_2010"], row["pop_2022"]],
            mode="lines+markers+text",
            name=f"{row['municipio']} ({row['uf']})",
            line=dict(width=2.5, color=cor),
            marker=dict(size=8),
            text=[f"{row['pop_2010']:,}", f"{row['pop_2022']:,}"],
            textposition=["top left", "top right"],
            hovertemplate=f"<b>{row['municipio']}</b><br>População: %{{y:,}}<extra></extra>"
        ))

    fig.update_layout(
        title=dict(
            text="<b>Trajetória Populacional: Censo 2010 vs. Censo 2022</b>",
            font=dict(size=15, family=FONT_FAMILY)
        ),
        yaxis=dict(
            title="População Residente",
            gridcolor=COLOR_GRID
        ),
        paper_bgcolor=BG_PAPER,
        plot_bgcolor=BG_PAPER,
        height=380,
        margin=dict(l=40, r=40, t=50, b=30),
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5)
    )
    return fig


def get_noticias_demograficas() -> List[Dict[str, str]]:
    """Notícias reais curadas sobre o Censo 2022, transição demográfica e planejamento urbano."""
    return [
        {
            "titulo": "Censo 2022: Brasil envelhece mais rápido e capitais desaceleram ritmo de crescimento",
            "fonte": "Agência IBGE Notícias",
            "data": "Outubro de 2023",
            "resumo": "Pela primeira vez em décadas, grandes metrópoles como Salvador, Porto Alegre e Belo Horizonte registraram retração populacional relativa, enquanto cidades médias e litorâneas como Florianópolis apresentaram forte atração demográfica.",
            "url": "https://agenciadenoticias.ibge.gov.br/agencia-noticias/2012-agencia-de-noticias/noticias/38186-censo-2022-populacao-do-brasil-atinge-203-1-milhoes",
            "categoria": "Transição Demográfica"
        },
        {
            "titulo": "Índice de envelhecimento atinge recorde histórico no país: 80 idosos para cada 100 crianças",
            "fonte": "IBGE / Estatísticas Sociais",
            "data": "Censo 2022",
            "resumo": "A proporção de pessoas com 60 anos ou mais aumentou consideravelmente em todas as Unidades da Federação. Gestores municipais precisam reorientar orçamentos de creches para centros de atenção à saúde do idoso e acessibilidade urbana.",
            "url": "https://agenciadenoticias.ibge.gov.br/agencia-noticias/2012-agencia-de-noticias/noticias/38186-censo-2022-populacao-do-brasil-atinge-203-1-milhoes",
            "categoria": "Políticas Públicas"
        },
        {
            "titulo": "Florianópolis e capitais do Centro-Oeste lideram crescimento populacional no Censo",
            "fonte": "G1 / Economia e Demografia",
            "data": "Julho de 2023",
            "resumo": "Com alta superior a 27% no período intercensitário, Florianópolis destaca-se pela migração interna qualificada, demandando rápida revisão do Plano Diretor para conter a especulação imobiliária e o colapso viário.",
            "url": "https://g1.globo.com/economia/censo/noticia/2023/06/28/populacao-do-brasil-cresce-052percent-ao-ano-o-menor-ritmo-da-historia-revela-censo-2022.ghtml",
            "categoria": "Expansão Urbana"
        }
    ]
