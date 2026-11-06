# Regras do Projeto Integrador

## Indicador Escolhido
- **Indicador 3: População e Crescimento Demográfico**
  - **Persona / Cenário:** Prefeitos de Capitais (Carlos/Curitiba, Eduardo/Porto Alegre, Elisa/Belo Horizonte, Jorge/Salvador, Roberto/Florianópolis).
  - **Objetivo:** Velocidade do crescimento demográfico, envelhecimento populacional, taxa média acumulada, outliers de crescimento (cidades que cresceram exageradamente vs encolheram).
  - **Entregáveis técnicos:**
    - Barra lateral com upload de dados (`st.file_uploader`) e filtros (Região, UF, Faixa Etária, Ano do Censo/Pesquisa).
    - Métricas e KPIs estatísticos: Média, Mediana, Moda, Quartis (Q1, Q2, Q3), IQR, Amplitude, Desvio Padrão e Outliers (regra 1,5 * IQR).
    - Gráficos interativos (Pirâmide etária, mapa de calor/crescimento, projeção/linhas).
    - Seção de notícias sobre transição demográfica/envelhecimento e imagens.

## Diretrizes de Operação (Regras de Interação)
1. **Aguardar alinhamento apenas no planejamento:** A etapa de apresentação prévia e espera por ordem expressa aplica-se **apenas quando estivermos planejando como fazer** (decisões conceituais, novas funcionalidades ou desenho da solução). Durante a execução, desenvolvimento de código, ajustes visuais/CSS e correção de bugs, atue diretamente com agilidade.
2. **Passo a passo transparente:** Todo código e cálculo deve ser validado e explicado antes da consolidação final.
3. **Formato das entregas:** Preparar o projeto com estrutura modular para permitir tanto a entrega individual quanto a unificação final com o grupo no GitHub.
