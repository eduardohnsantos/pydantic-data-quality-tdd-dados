import pandas as pd
from app.etl import transformar

def test_calculo_valor_total_estoque():
    # Preparação
    df = pd.DataFrame(
        {
            "nome": ["Produto A", "Produto B"],  # <-- Coluna adicionada
            "quantidade": [10, 5],
            "preco": [20.0, 100.0],
            "categoria": ["brinquedos", "eletrônicos"],
        }
    )
    # Ação
    result = transformar(df)
    
    # Asserção
    assert (result["valor_total_estoque"] == [200.0, 500.0]).all()


def test_normalizacao_categoria():
    # Preparação
    df = pd.DataFrame(
        {
            "nome": ["Produto A", "Produto B"],  # <-- Coluna adicionada
            "quantidade": [1, 2],
            "preco": [10.0, 20.0],
            "categoria": ["Brinquedos", "Eletrônicos"],
        }
    )
    # Ação
    result = transformar(df)
    
    # Asserção
    assert (result["categoria_normalizada"] == ["brinquedos", "eletrônicos"]).all()


def test_determinacao_disponibilidade():
    # Preparação
    df = pd.DataFrame(
        {
            "nome": ["Produto A", "Produto B"],  # <-- Coluna adicionada
            "quantidade": [0, 2],
            "preco": [10.0, 20.0],
            "categoria": ["brinquedos", "eletrônicos"],
        }
    )
    # Ação
    result = transformar(df)
    
    # Asserção
    assert (result["disponibilidade"] == [False, True]).all()