"""
Aplicação Principal — Números que Falam: Descobrindo o Brasil
Dashboard de População e Crescimento Demográfico (Indicador 3)
Projeto Integrador de Python e Matemática
Professores: Profª Conceição (Matemática) · Profª Janaína Duarte (Python) · Prof. Rubens Lemos (Python)
"""
import streamlit as st
import pandas as pd
from src.etl import carregar_dados_capitais, carregar_dados_piramide, aplicar_filtros_laterais
from src.stats import (
    calcular_estatisticas_descritivas,
    identificar_cidades_outliers,
    calcular_metricas_demograficas
)
from src.views import (
    plot_boxplot_dispersao,
    plot_crescimento_barras,
    plot_piramide_etaria,
    plot_evolucao_comparativa,
    get_noticias_demograficas
)

# Configuração da Página
st.set_page_config(
    page_title="Números que Falam • Demografia e Crescimento",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização Refinada e Sóbria (House Style Policy & Civic Analytics)
st.markdown("""
<style>
    /* Tipografia e espaçamentos limpos */
    .main-title {
        font-size: 1.85rem;
        font-weight: 700;
        color: inherit !important;
        margin-bottom: 0.2rem;
        letter-spacing: -0.02em;
    }
    .subtitle {
        font-size: 0.95rem;
        color: inherit !important;
        opacity: 0.85;
        margin-bottom: 1.2rem;
    }
    .stat-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .stat-label {
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748B;
        font-weight: 600;
    }
    .stat-value {
        font-size: 1.75rem;
        font-weight: 700;
        color: #0F172A;
        margin: 4px 0;
    }
    .stat-detail {
        font-size: 0.8rem;
        color: #64748B;
    }
    .persona-box {
        background-color: #F8FAFC;
        border-left: 4px solid #2563EB;
        padding: 14px 18px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 18px;
    }
    .news-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 18px;
        margin-bottom: 14px;
    }
    .news-tag {
        display: inline-block;
        padding: 2px 8px;
        font-size: 0.72rem;
        font-weight: 600;
        border-radius: 4px;
        background-color: #EFF6FF;
        color: #1D4ED8;
        margin-bottom: 8px;
    }
    @media (prefers-color-scheme: dark) {
        .main-title, h1, h2, h3, h4 { color: #FFFFFF !important; }
        .subtitle, p, span { color: #E2E8F0; }
    }
</style>
""", unsafe_allow_html=True)


def main():
    # ==========================================
    # BARRA LATERAL (Critério 1 - Ingestão e Filtros)
    # ==========================================
    with st.sidebar:
        st.markdown("### 🏛️ Números que Falam")
        st.caption("Dashboard de Apoio à Gestão Pública Municipal")
        st.divider()

        # Recurso Mandatório: Upload de Arquivos
        st.markdown("#### 📂 Ingestão de Dados (Upload)")
        uploaded_file = st.file_uploader(
            "Carregar base alternativa (CSV ou XLSX):",
            type=["csv", "xlsx", "xls"],
            help="Carregue uma planilha com colunas 'municipio', 'pop_2010' e 'pop_2022' ou 'taxa_crescimento_pct'."
        )

        st.divider()
        st.markdown("#### 🎯 Atuação de Consultoria (Personas)")
        
        # Mapeamento dos prefeitos
        opcoes_persona = [
            "Visão Geral (Todas as Capitais)",
            "Carlos — Prefeito de Curitiba (PR)",
            "Eduardo — Prefeito de Porto Alegre (RS)",
            "Elisa — Prefeita de Belo Horizonte (MG)",
            "Jorge — Prefeito de Salvador (BA)",
            "Roberto — Prefeito de Florianópolis (SC)"
        ]
        persona_selecionada = st.selectbox("Selecione a Persona demandante:", opcoes_persona)

        st.divider()
        st.markdown("#### 🔍 Filtros Territoriais")
        
        # Carrega dados preliminares para preencher opções dos filtros
        df_base, status_fonte = carregar_dados_capitais(uploaded_file)
        
        if df_base.empty:
            st.error(status_fonte)
            return

        regioes_disponiveis = sorted(df_base["regiao"].dropna().unique().tolist()) if "regiao" in df_base.columns else []
        regioes_selecionadas = st.multiselect("Região Geográfica:", regioes_disponiveis, default=[])

        ufs_disponiveis = sorted(df_base["uf"].dropna().unique().tolist()) if "uf" in df_base.columns else []
        ufs_selecionadas = st.multiselect("Unidade da Federação (UF):", ufs_disponiveis, default=[])

        termo_busca = st.text_input("Filtrar por nome da cidade:", "")

        st.caption(f"Fonte ativa: *{status_fonte}*")
        st.caption("Censo Demográfico IBGE (2010 / 2022)")

    # Aplicação dos filtros territoriais
    df_filtrado = aplicar_filtros_laterais(df_base, regioes_selecionadas, ufs_selecionadas, termo_busca)

    # ==========================================
    # CABEÇALHO PRINCIPAL
    # ==========================================
    st.markdown('<div class="main-title">Indicador 3: População e Crescimento Demográfico</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">Análise estatística descritiva, velocidade de crescimento intercensitário (2010–2022) '
        'e transição demográfica para fundamentação dos Planos Diretores.</div>',
        unsafe_allow_html=True
    )

    # Briefing Executivo da Persona Selecionada
    if persona_selecionada != "Visão Geral (Todas as Capitais)":
        cidade_alvo = persona_selecionada.split("—")[1].split("(")[0].strip().replace("Prefeito de ", "").replace("Prefeita de ", "")
        dados_cidade = df_base[df_base["municipio"].str.lower() == cidade_alvo.lower()]
        
        taxa_cid = dados_cidade["taxa_crescimento_pct"].values[0] if not dados_cidade.empty else 0.0
        pop22_cid = dados_cidade["pop_2022"].values[0] if not dados_cidade.empty else 0
        
        st.markdown(f"""
        <div class="persona-box">
            <h4 style="margin: 0 0 6px 0; color: inherit;">📋 Briefing Executivo: {persona_selecionada}</h4>
            <p style="margin: 0; font-size: 0.92rem; color: inherit; opacity: 0.9;">
                <b>Diagnóstico de {cidade_alvo}:</b> População apurada em 2022 de <b>{pop22_cid:,}</b> habitantes, com 
                taxa acumulada de crescimento de <b style="color: {'#0D9488' if taxa_cid >= 0 else '#BE123C'}">{taxa_cid:+.2f}%</b> entre 2010 e 2022.<br>
                <b>Diretriz para o Plano Diretor:</b> {'Priorizar infraestrutura urbana e contenção de adensamento acelerado.' if taxa_cid > 10 else 'Reorganizar redes de atenção básica e transporte público frente à estabilização/retração demográfica.'}
            </p>
        </div>
        """, unsafe_allow_html=True)

    # ==========================================
    # CÁLCULOS ESTATÍSTICOS (Critério 2 - Rigor)
    # ==========================================
    coluna_analise = "taxa_crescimento_pct"
    stats = calcular_estatisticas_descritivas(df_filtrado[coluna_analise])
    outliers_sup, outliers_inf = identificar_cidades_outliers(df_filtrado, coluna_analise)

    # ==========================================
    # NAVEGAÇÃO EM 4 ABAS
    # ==========================================
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Rigor Estatístico & Dispersão",
        "👥 Pirâmide Etária & Envelhecimento",
        "📈 Crescimento & Outliers (2010–2022)",
        "📰 Sala de Notícias & Planejamento"
    ])

    # ----------------------------------------------------
    # ABA 1: RIGOR ESTATÍSTICO & DISPERSÃO (Rubrica Matemática)
    # ----------------------------------------------------
    with tab1:
        st.markdown("#### Medidas de Tendência Central e Dispersão")
        st.caption(f"Cálculos baseados em amostra filtrada de {stats.get('n', 0)} municípios/capitais brasileiras.")

        # Cards das métricas principais
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        with c1:
            st.metric("Média Aritmética", f"{stats.get('media', 0):.2f}%")
        with c2:
            st.metric("Mediana (Q2)", f"{stats.get('mediana', 0):.2f}%")
        with c3:
            st.metric("Moda", f"{stats.get('moda', 0):.2f}%")
        with c4:
            st.metric("Desvio Padrão", f"{stats.get('desvio_padrao', 0):.2f}%")
        with c5:
            st.metric("IQR (Q3 - Q1)", f"{stats.get('iqr', 0):.2f}%")
        with c6:
            st.metric("Amplitude Total", f"{stats.get('amplitude', 0):.2f}%")

        st.divider()

        # Detalhamento de Quartis e Assimetria
        col_esq, col_dir = st.columns([1, 1])

        with col_esq:
            st.markdown("##### 📐 Separatrizes e Regra de Outliers (Tukey)")
            df_quartis = pd.DataFrame([
                {"Medida": "Mínimo", "Valor": f"{stats.get('min', 0):.2f}%", "Significado": "Menor crescimento registrado"},
                {"Medida": "1º Quartil (Q1 - 25%)", "Valor": f"{stats.get('q1', 0):.2f}%", "Significado": "25% das cidades cresceram abaixo deste valor"},
                {"Medida": "Mediana (Q2 - 50%)", "Valor": f"{stats.get('q2', 0):.2f}%", "Significado": "Divisor central da amostra (robusto)"},
                {"Medida": "3º Quartil (Q3 - 75%)", "Valor": f"{stats.get('q3', 0):.2f}%", "Significado": "75% das cidades cresceram até este valor"},
                {"Medida": "Máximo", "Valor": f"{stats.get('max', 0):.2f}%", "Significado": "Maior crescimento registrado"},
                {"Medida": "Limite Inferior de Outlier", "Valor": f"{stats.get('limite_inferior_outlier', 0):.2f}%", "Significado": "Q1 - 1,5 × IQR"},
                {"Medida": "Limite Superior de Outlier", "Valor": f"{stats.get('limite_superior_outlier', 0):.2f}%", "Significado": "Q3 + 1,5 × IQR"},
            ])
            st.dataframe(df_quartis, use_container_width=True, hide_index=True)

            st.markdown(f"""
            **Diagnóstico da Distribuição:** `{stats.get('tipo_distribuicao', '')}`  
            > *{stats.get('justificativa_assimetria', '')}*
            """)

        with col_dir:
            # Boxplot Interativo
            fig_box = plot_boxplot_dispersao(df_filtrado, stats, coluna_analise)
            st.plotly_chart(fig_box, use_container_width=True)

        # Cidades Outliers Identificadas
        st.markdown("##### ⚠️ Identificação Formal de Outliers de Crescimento")
        total_outliers = stats.get("qtd_outliers", 0)
        if total_outliers > 0:
            st.warning(f"Foram identificados **{total_outliers} municípios anômalos (outliers)** além dos limites de 1,5 × IQR.")
            col_out1, col_out2 = st.columns(2)
            with col_out1:
                st.markdown("**Cidades com Crescimento Exorbitante (Outliers Superiores):**")
                if not outliers_sup.empty:
                    st.dataframe(outliers_sup[["municipio", "uf", "pop_2010", "pop_2022", "taxa_crescimento_pct"]], hide_index=True)
                else:
                    st.info("Nenhuma cidade ultrapassou o limite superior.")
            with col_out2:
                st.markdown("**Cidades com Retração Severa (Outliers Inferiores):**")
                if not outliers_inf.empty:
                    st.dataframe(outliers_inf[["municipio", "uf", "pop_2010", "pop_2022", "taxa_crescimento_pct"]], hide_index=True)
                else:
                    st.info("Nenhuma cidade ficou abaixo do limite inferior.")
        else:
            st.success("Não foram detectados outliers estatísticos na seleção atual sob o critério de 1,5 × IQR.")

    # ----------------------------------------------------
    # ABA 2: PIRÂMIDE ETÁRIA & ENVELHECIMENTO
    # ----------------------------------------------------
    with tab2:
        st.markdown("#### Estrutura Etária e Transição Demográfica (Censo 2022)")
        df_piramide_all = carregar_dados_piramide()

        if not df_piramide_all.empty:
            locais_disponiveis = df_piramide_all["localidade"].unique().tolist()
            
            # Se uma persona estiver selecionada, foca na cidade dela
            default_index = 0
            if persona_selecionada != "Visão Geral (Todas as Capitais)":
                for idx, loc in enumerate(locais_disponiveis):
                    if loc.lower() in persona_selecionada.lower():
                        default_index = idx
                        break

            local_escolhido = st.selectbox("Selecione a Localidade para visualizar a pirâmide:", locais_disponiveis, index=default_index)
            df_piramide_local = df_piramide_all[df_piramide_all["localidade"] == local_escolhido]

            metricas_demo = calcular_metricas_demograficas(df_piramide_local)

            # KPIs Demográficos
            k1, k2, k3, k4, k5 = st.columns(5)
            with k1:
                st.metric("População Total", f"{metricas_demo['populacao_total']:,}")
            with k2:
                st.metric("% Jovens (0 a 14)", f"{metricas_demo['pct_jovens']:.1f}%")
            with k3:
                st.metric("% Idosos (60+)", f"{metricas_demo['pct_idosos']:.1f}%")
            with k4:
                st.metric("Índice de Envelhecimento", f"{metricas_demo['indice_envelhecimento']:.1f}")
            with k5:
                st.metric("Razão de Sexo (H/M)", f"{metricas_demo['razao_sexo']:.1f}")

            st.caption("ℹ️ *Índice de Envelhecimento:* Número de idosos (60+) para cada 100 jovens (0 a 14 anos).")

            fig_piramide = plot_piramide_etaria(df_piramide_all, local_escolhido)
            st.plotly_chart(fig_piramide, use_container_width=True)

            st.markdown(f"""
            > **Leitura Demográfica para o Gestor de {local_escolhido}:**  
            > Com um Índice de Envelhecimento de **{metricas_demo['indice_envelhecimento']}**, a estrutura populacional reflete 
            > o estreitamento da base (queda da taxa de natalidade) e o alargamento das faixas adultas e seniores. 
            > O município deve readequar a atenção primária de saúde e o mobiliário urbano para acessibilidade da terceira idade.
            """)
        else:
            st.warning("Base de dados da pirâmide etária não disponível.")

    # ----------------------------------------------------
    # ABA 3: CRESCIMENTO & RANKING (2010 x 2022)
    # ----------------------------------------------------
    with tab3:
        st.markdown("#### Velocidade do Crescimento Populacional (2010 a 2022)")
        
        col_graf1, col_graf2 = st.columns([3, 2])
        with col_graf1:
            fig_barras = plot_crescimento_barras(df_filtrado, coluna_analise)
            st.plotly_chart(fig_barras, use_container_width=True)
            
        with col_graf2:
            st.markdown("##### 📈 Trajetória Intercensitária")
            cidades_destaque = ["Curitiba", "Porto Alegre", "Belo Horizonte", "Salvador", "Florianópolis"]
            fig_linhas = plot_evolucao_comparativa(df_base, cidades_destaque)
            st.plotly_chart(fig_linhas, use_container_width=True)

        st.markdown("##### 📋 Tabela Completa de Dados")
        st.dataframe(
            df_filtrado[["municipio", "uf", "regiao", "pop_2010", "pop_2022", "variacao_absoluta", "taxa_crescimento_pct", "taxa_anual_pct"]],
            use_container_width=True,
            hide_index=True
        )

    # ----------------------------------------------------
    # ABA 4: SALA DE NOTÍCIAS & PLANEJAMENTO URBANO
    # ----------------------------------------------------
    with tab4:
        st.markdown("#### 📰 Sala de Imprensa & Contexto do Planejamento Urbano")
        st.caption("Reportagens e dados oficiais contextualizados para fundamentação do Plano Diretor.")

        noticias = get_noticias_demograficas()
        for notic in noticias:
            st.markdown(f"""
            <div class="news-card">
                <span class="news-tag">{notic['categoria']}</span>
                <h4 style="margin: 4px 0 8px 0; color: inherit;">{notic['titulo']}</h4>
                <p style="margin: 0 0 10px 0; font-size: 0.9rem; color: inherit; opacity: 0.85;">{notic['resumo']}</p>
                <div style="font-size: 0.78rem; color: inherit; opacity: 0.75;">
                    <b>Fonte:</b> {notic['fonte']} · <b>Data:</b> {notic['data']} · 
                    <a href="{notic['url']}" target="_blank" style="color: #2563EB; text-decoration: none;">Acessar matéria original ↗</a>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.divider()
        st.markdown("##### 🌆 Impacto no Plano Diretor das Cidades-Alvo")
        st.write("""
        * **Curitiba e Belo Horizonte:** Consolidação urbana com crescimento vegetativo mínimo demandam foco em requalificação de centros urbanos e mobilidade ativa.
        * **Porto Alegre e Salvador:** A retração populacional relativa impõe reavaliação de receitas tributárias (IPTU/FPM) e readequação de serviços públicos subutilizados.
        * **Florianópolis:** Aceleração do crescimento impõe rigor no zoneamento ecológico e investimentos pesados em saneamento básico e malha viária.
        """)

    # ==========================================
    # RODAPÉ INSTITUCIONAL
    # ==========================================
    st.divider()
    st.caption(
        "**Projeto Integrador de Python & Matemática** • Tema 3: População e Crescimento Demográfico • "
        "Orientação: Profª Conceição, Profª Janaína Duarte e Prof. Rubens Lemos • "
        "Dados: IBGE Censo Demográfico 2010 e 2022 • Metodologia de Startup & Consultoria Pública"
    )


if __name__ == "__main__":
    main()
