"""
Testes unitários para validação do rigor estatístico (Profª Conceição / Matemática).
Executa verificação dos cálculos de Média, Mediana, Quartis, IQR, Desvio Padrão e Outliers.
"""
import pytest
import pandas as pd
import numpy as np
from src.stats import calcular_estatisticas_descritivas, identificar_cidades_outliers, calcular_metricas_demograficas


def test_estatisticas_distribuicao_conhecida():
    # Conjunto de teste controlado: [10, 20, 30, 40, 50, 60, 70]
    dados = pd.Series([10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0])
    stats = calcular_estatisticas_descritivas(dados)
    
    assert stats["n"] == 7
    assert stats["media"] == 40.0
    assert stats["mediana"] == 40.0
    assert stats["min"] == 10.0
    assert stats["max"] == 70.0
    assert stats["amplitude"] == 60.0
    assert stats["q1"] == 25.0
    assert stats["q3"] == 55.0
    assert stats["iqr"] == 30.0
    # Limites de Outlier: Q1 - 1.5*30 = 25 - 45 = -20; Q3 + 1.5*30 = 55 + 45 = 100
    assert stats["limite_inferior_outlier"] == -20.0
    assert stats["limite_superior_outlier"] == 100.0
    assert stats["qtd_outliers"] == 0


def test_deteccao_outliers_com_disparidade():
    # Conjunto com um outlier astronômico (cidade que disparou) e um de retração
    dados = pd.Series([1.0, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 50.0, -25.0])
    stats = calcular_estatisticas_descritivas(dados)
    
    # 50.0 deve ser outlier superior e -25.0 deve ser outlier inferior
    assert 50.0 in stats["outliers"]
    assert -25.0 in stats["outliers"]
    assert stats["qtd_outliers"] >= 2
    # Média deve ser expressivamente deslocada em relação à mediana
    assert stats["media"] > stats["mediana"]
    assert "Assimétrica à Direita" in stats["tipo_distribuicao"]


def test_identificacao_cidades_outliers_dataframe():
    df = pd.DataFrame([
        {"municipio": "Normalville", "taxa_crescimento_pct": 2.0},
        {"municipio": "MediaCity", "taxa_crescimento_pct": 3.0},
        {"municipio": "Equilibrada", "taxa_crescimento_pct": 2.5},
        {"municipio": "MegaBoom", "taxa_crescimento_pct": 45.0},  # Outlier sup
        {"municipio": "CriseLand", "taxa_crescimento_pct": -20.0}, # Outlier inf
    ])
    
    out_sup, out_inf = identificar_cidades_outliers(df, "taxa_crescimento_pct")
    assert not out_sup.empty
    assert "MegaBoom" in out_sup["municipio"].values
    assert not out_inf.empty
    assert "CriseLand" in out_inf["municipio"].values


def test_metricas_demograficas():
    df_piramide = pd.DataFrame([
        {"faixa_etaria": "0 a 4 anos", "homens": 100, "mulheres": 100, "total": 200},
        {"faixa_etaria": "5 a 9 anos", "homens": 100, "mulheres": 100, "total": 200},
        {"faixa_etaria": "10 a 14 anos", "homens": 100, "mulheres": 100, "total": 200},
        {"faixa_etaria": "20 a 24 anos", "homens": 500, "mulheres": 500, "total": 1000},
        {"faixa_etaria": "60 a 64 anos", "homens": 150, "mulheres": 150, "total": 300},
        {"faixa_etaria": "80 anos ou mais", "homens": 150, "mulheres": 150, "total": 300},
    ])
    
    res = calcular_metricas_demograficas(df_piramide)
    assert res["total_jovens"] == 600
    assert res["total_idosos"] == 600
    assert res["indice_envelhecimento"] == 100.0  # 600 / 600 * 100 = 100%
    assert res["razao_sexo"] == 100.0
