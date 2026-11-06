# Números que Falam — Descobrindo o Brasil
## Dashboard de Indicadores do IBGE com Estatística Descritiva em Python
### Projeto Integrador • Python & Matemática • Etapa 3

> **Tema Escolhido:** Indicador 3 — População e Crescimento Demográfico  
> **Personas / Demandantes:** Prefeitos de Capitais — Carlos (Curitiba), Eduardo (Porto Alegre), Elisa (Belo Horizonte), Jorge (Salvador) e Roberto (Florianópolis).  
> **Corpo Docente:** Profª Conceição (Matemática) · Profª Janaína Duarte (Python) · Prof. Rubens Lemos (Python)

---

## 📌 1. Visão Geral e Contexto de Negócio

No âmbito da consultoria pública prestada por nossa startup de análise de dados, desenvolvemos um dashboard analítico em **Streamlit** integrado a dados oficiais do **Censo Demográfico do IBGE (2010 e 2022)**. 

Os prefeitos das capitais demandaram respostas estratégicas para a revisão de seus **Planos Diretores** e alocação orçamentária:
1. **Qual é a taxa média de crescimento populacional acumulada por cidade?**
2. **Onde estão situados os outliers de crescimento (cidades com expansão vertiginosa vs. retração populacional)?**
3. **Qual é o ritmo do envelhecimento populacional e como ele afeta as políticas de saúde e infraestrutura urbana?**

---

## 🧮 2. Rigor Matemático e Estatística Descritiva (Rubrica: 0,90 pt)

Em cumprimento às diretrizes da **Profª Conceição (Matemática)** e às habilidades da **BNCC (EM13MAT316, EM13MAT104, EM13MAT202)**, o sistema calcula de forma determinística:

| Métrica Estatística | Conceito Matemático | Aplicação no Cenário Demográfico |
| :--- | :--- | :--- |
| **Média Aritmética** | $\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i$ | Taxa média de crescimento, sensível a valores extremos. |
| **Mediana ($Q_2$)** | Ponto central com 50% dos dados abaixo e 50% acima | Medida robusta de tendência central que não se deixa distorcer por outliers. |
| **Moda** | Valor mais frequente na distribuição | Faixa percentual de crescimento mais comum entre as capitais. |
| **Quartis ($Q_1, Q_2, Q_3$)** | Divisão da série ordenada em 4 partes iguais (25%, 50%, 75%) | Estruturação da dispersão e delimitação do miolo da distribuição. |
| **Intervalo Interquartil ($IQR$)** | $IQR = Q_3 - Q_1$ | Dispersão dos 50% centrais dos dados; base para identificação de outliers. |
| **Amplitude** | $A = x_{\max} - x_{\min}$ | Distância total entre a cidade que mais cresceu e a que mais encolheu. |
| **Desvio Padrão Amostral ($s$)** | $s = \sqrt{\frac{1}{n-1}\sum_{i=1}^{n}(x_i - \bar{x})^2}$ | Grau de dispersão e homogeneidade das taxas de crescimento em torno da média. |
| **Detecção de Outliers (Tukey)** | $[Q_1 - 1{,}5 \cdot IQR, \; Q_3 + 1{,}5 \cdot IQR]$ | Identificação matemática objetiva de anomalias de crescimento e retração. |

### Justificativa do Impacto dos Outliers (Média vs. Mediana)
* **Assimetria Positiva:** Municípios como Boa Vista (+45,43%), Palmas (+32,57%) e Florianópolis (+27,53%) cresceram a taxas extraordinárias, puxando a **Média** para cima.
* **Impacto:** Nesses casos, a **Mediana** é o indicador de maior rigor metodológico para representar o comportamento típico das cidades brasileiras, pois permanece imune a essas distorções extremas.

---

## 🚀 3. Funcionalidades do Dashboard (Rubrica: 0,75 pt ETL + 0,60 pt Visualização)

* **Ingestão Híbrida e Upload:** Suporte nativo ao `st.file_uploader` para carregar bases customizadas em CSV e XLSX sem falhas, com base oficial do IBGE como *fallback*.
* **Filtros Dinâmicos na Barra Lateral:** Filtros combinados por Região Geográfica, Unidade da Federação (UF) e busca textual por município.
* **Modo Persona / Consultoria de Startup:** Seletor de prefeitos que gera briefing executivo personalizado na hora para a apresentação em "Roda de Conversa" (Critério 4 - 0,75 pt).
* **Quatro Abas Especializadas:**
  1. `Rigor Estatístico & Dispersão`: Boxplot anotado, cards de métricas e tabela de quartis e outliers.
  2. `Pirâmide Etária & Envelhecimento`: Pirâmide espelhada interativa (Censo 2022) e cálculo do Índice de Envelhecimento ($\frac{\text{Idosos 60+}}{\text{Jovens 0-14}} \times 100$).
  3. `Crescimento & Outliers (2010–2022)`: Gráficos de barras ordenadas com cores semânticas e trajetórias intercensitárias.
  4. `Sala de Notícias & Planejamento`: Curadoria de notícias oficiais do IBGE e recomendações para o Plano Diretor.

---

## 🛠️ 4. Instalação e Execução Local

### Pré-requisitos
* Python 3.10 ou superior.

### 1. Clonar o repositório
```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd projeto-py
```

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

### 3. Executar a suíte de testes unitários
```bash
pytest tests/
```

### 4. Iniciar o dashboard interativo
```bash
streamlit run app.py
```

---

## 📂 5. Estrutura do Projeto

```text
projeto-py/
├── data/                               # Bases de dados tratadas do IBGE (Censo 2010 e 2022)
│   ├── capitais_populacao_2010_2022.csv
│   └── piramide_etaria_capitais_2022.csv
├── src/
│   ├── download_data.py                # Consolidação das bases oficiais
│   ├── etl.py                          # Ingestão, validação e filtros (Critério 1)
│   ├── stats.py                        # Métricas matemáticas e Tukey (Critério 2)
│   └── views.py                        # Gráficos Plotly e componentes (Critério 3)
├── tests/
│   └── test_stats.py                   # Testes unitários automatizados
├── app.py                              # Aplicação Streamlit principal
├── requirements.txt                    # Dependências do projeto
├── README.md                           # Documentação da entrega individual
├── GEMINI.md                           # Diretrizes e regras do projeto
└── AGENTS.md                           # Regras de orquestração do agente
```

---

## 👥 6. Roteiro para a "Roda de Conversa" (Apresentação - 0,75 pt)

Na apresentação da startup para a banca de professores:
1. **Abertura (30s):** Apresentar a startup e a missão de transformar dados brutos do Censo 2022 em inteligência territorial para as capitais.
2. **O Problema das Personas (1 min):** Demonstrar como capitais como Porto Alegre (-5,43%) e Salvador (-9,64%) sofreram retração populacional, enquanto Florianópolis (+27,53%) explodiu demograficamente.
3. **Rigor Matemático (1 min):** Explicar no boxplot por que a Média é puxada pelos outliers superiores e por que a Mediana deve guiar o planejamento orçamentário.
4. **Impacto Prático (1 min):** Mostrar a pirâmide etária e o avanço do Índice de Envelhecimento, indicando que creches precisam dividir espaço orçamentário com centros de convivência e atenção primária à saúde do idoso.
