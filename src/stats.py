"""
Módulo de Métricas e Rigor Estatístico Descritivo.
Alinhado à BNCC (EM13MAT316, EM13MAT104, EM13MAT202) e à rubrica de avaliação (Critério 2 - 0,90 pt).
"""
from typing import Dict, Any, List, Tuple
import numpy as np
import pandas as pd


def calcular_estatisticas_descritivas(series: pd.Series) -> Dict[str, Any]:
    """
    Calcula todas as métricas obrigatórias de tendência central, separatrizes,
    dispersão e identificação formal de outliers.
    
    Parâmetros:
        series: pd.Series com valores numéricos contínuos (ex: taxas de crescimento).
    
    Retorno:
        Dicionário estruturado com todas as métricas formatadas e explicadas.
    """
    clean_series = series.dropna().astype(float)
    if clean_series.empty:
        return {}
    
    n = len(clean_series)
    valores_ordenados = np.sort(clean_series.to_numpy())
    
    # 1. Medidas de Tendência Central
    media = float(np.mean(valores_ordenados))
    mediana = float(np.median(valores_ordenados))
    
    # Moda (arredondada a 1 casa para agrupar contínuos ou valor exato)
    series_arredondada = clean_series.round(1)
    modas = series_arredondada.mode()
    moda = float(modas.iloc[0]) if not modas.empty else media
    
    # 2. Separatrizes (Quartis)
    q1 = float(np.percentile(valores_ordenados, 25))
    q2 = float(np.percentile(valores_ordenados, 50))  # Mediana
    q3 = float(np.percentile(valores_ordenados, 75))
    iqr = float(q3 - q1)
    
    # 3. Medidas de Dispersão
    val_min = float(np.min(valores_ordenados))
    val_max = float(np.max(valores_ordenados))
    amplitude = float(val_max - val_min)
    
    # Desvio padrão amostral (ddof=1) e variância
    desvio_padrao = float(np.std(valores_ordenados, ddof=1)) if n > 1 else 0.0
    variancia = float(np.var(valores_ordenados, ddof=1)) if n > 1 else 0.0
    coeficiente_variacao = float((desvio_padrao / abs(media) * 100)) if media != 0 else 0.0
    
    # 4. Detecção Rigorosa de Outliers (Regra 1,5 * IQR de Tukey)
    limite_inferior = float(q1 - 1.5 * iqr)
    limite_superior = float(q3 + 1.5 * iqr)
    
    # Outliers moderados e extremos
    outliers_inferiores = clean_series[clean_series < limite_inferior].tolist()
    outliers_superiores = clean_series[clean_series > limite_superior].tolist()
    todos_outliers = sorted(outliers_inferiores + outliers_superiores)
    
    # Análise de Assimetria (Skewness)
    # Se média > mediana: assimetria positiva (puxada por cidades com altíssimo crescimento)
    # Se média < mediana: assimetria negativa (puxada por cidades que encolheram)
    diferenca_media_mediana = media - mediana
    if abs(diferenca_media_mediana) < 0.15:
        tipo_distribuicao = "Aproximadamente Simétrica"
        justificativa_assimetria = (
            "A média e a mediana estão praticamente coincidentes. Não há distorções severas unilaterais."
        )
    elif diferenca_media_mediana > 0:
        tipo_distribuicao = "Assimétrica à Direita (Positiva)"
        justificativa_assimetria = (
            f"A média ({media:.2f}%) é sensivelmente MAIOR que a mediana ({mediana:.2f}%). "
            f"Isso ocorre porque cidades com crescimento astronômico puxam a média para cima. "
            f"Neste cenário, a MEDIANA é a medida mais representativa e robusta do comportamento típico."
        )
    else:
        tipo_distribuicao = "Assimétrica à Esquerda (Negativa)"
        justificativa_assimetria = (
            f"A média ({media:.2f}%) é MENOR que a mediana ({mediana:.2f}%). "
            f"Cidades com forte retração populacional puxam a média para baixo, distorcendo a percepção de estabilidade."
        )
    
    return {
        "n": n,
        "media": round(media, 2),
        "mediana": round(mediana, 2),
        "moda": round(moda, 2),
        "q1": round(q1, 2),
        "q2": round(q2, 2),
        "q3": round(q3, 2),
        "iqr": round(iqr, 2),
        "min": round(val_min, 2),
        "max": round(val_max, 2),
        "amplitude": round(amplitude, 2),
        "desvio_padrao": round(desvio_padrao, 2),
        "variancia": round(variancia, 2),
        "coeficiente_variacao": round(coeficiente_variacao, 2),
        "limite_inferior_outlier": round(limite_inferior, 2),
        "limite_superior_outlier": round(limite_superior, 2),
        "qtd_outliers": len(todos_outliers),
        "outliers": todos_outliers,
        "tipo_distribuicao": tipo_distribuicao,
        "justificativa_assimetria": justificativa_assimetria
    }


def identificar_cidades_outliers(df: pd.DataFrame, coluna_taxa: str = "taxa_crescimento_pct") -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Identifica as linhas do DataFrame correspondentes aos outliers superiores e inferiores.
    
    Retorno:
        (df_outliers_superiores, df_outliers_inferiores)
    """
    stats = calcular_estatisticas_descritivas(df[coluna_taxa])
    if not stats:
        return pd.DataFrame(), pd.DataFrame()
    
    lim_inf = stats["limite_inferior_outlier"]
    lim_sup = stats["limite_superior_outlier"]
    
    outliers_sup = df[df[coluna_taxa] > lim_sup].sort_values(by=coluna_taxa, ascending=False)
    outliers_inf = df[df[coluna_taxa] < lim_inf].sort_values(by=coluna_taxa, ascending=True)
    
    return outliers_sup, outliers_inf


def calcular_metricas_demograficas(df_piramide: pd.DataFrame) -> Dict[str, float]:
    """
    Calcula índices demográficos formais com base na pirâmide etária:
    - Jovens (0 a 14 anos)
    - População em Idade Ativa (15 a 59 anos)
    - Idosos (60 anos ou mais)
    - Índice de Envelhecimento = (Idosos / Jovens) * 100
    - Razão de Dependência = ((Jovens + Idosos) / PIA) * 100
    - Razão de Sexo = (Total Homens / Total Mulheres) * 100
    """
    faixas_jovens = ["0 a 4 anos", "5 a 9 anos", "10 a 14 anos"]
    faixas_idosos = [
        "60 a 64 anos", "65 a 69 anos", "70 a 74 anos", "75 a 79 anos", "80 anos ou mais"
    ]
    
    jovens = df_piramide[df_piramide["faixa_etaria"].isin(faixas_jovens)]["total"].sum()
    idosos = df_piramide[df_piramide["faixa_etaria"].isin(faixas_idosos)]["total"].sum()
    pop_total = df_piramide["total"].sum()
    pia = pop_total - jovens - idosos
    
    total_homens = df_piramide["homens"].sum()
    total_mulheres = df_piramide["mulheres"].sum()
    
    indice_envelhecimento = (idosos / jovens * 100) if jovens > 0 else 0.0
    razao_dependencia = ((jovens + idosos) / pia * 100) if pia > 0 else 0.0
    razao_sexo = (total_homens / total_mulheres * 100) if total_mulheres > 0 else 100.0
    
    return {
        "populacao_total": int(pop_total),
        "total_jovens": int(jovens),
        "total_pia": int(pia),
        "total_idosos": int(idosos),
        "pct_jovens": round(jovens / pop_total * 100, 2) if pop_total > 0 else 0.0,
        "pct_idosos": round(idosos / pop_total * 100, 2) if pop_total > 0 else 0.0,
        "indice_envelhecimento": round(indice_envelhecimento, 2),
        "razao_dependencia": round(razao_dependencia, 2),
        "razao_sexo": round(razao_sexo, 2),
    }
