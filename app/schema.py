import pandas as pd
import pandera.pandas as pa  # Atualizado para remover o aviso (Warning) do terminal

# 1. Schema para os dados brutos que vêm do Postgres
ProdutoSchema = pa.DataFrameSchema({
    "id_produto": pa.Column(int, required=True),  # Adicionado!
    "email": pa.Column(str, required=True),       # Adicionado!
    "nome": pa.Column(str),
    "quantidade": pa.Column(int, pa.Check.ge(0)),
    "preco": pa.Column(float, pa.Check.gt(0)),
    "categoria": pa.Column(str)
}, strict=True, coerce=True)

# 2. Schema para a camada de KPIs (dados transformados)
ProductSchemaKPI = pa.DataFrameSchema({
    "id_produto": pa.Column(int, required=True),  # Adicionado!
    "email": pa.Column(str, required=True),       # Adicionado!
    "nome": pa.Column(str),
    "quantidade": pa.Column(int, pa.Check.ge(0)),
    "preco": pa.Column(float, pa.Check.gt(0)),
    "categoria": pa.Column(str),
    # Campos calculados pelo seu ETL
    "valor_total_estoque": pa.Column(float, pa.Check.ge(0)),
    "categoria_normalizada": pa.Column(str),
    "disponibilidade": pa.Column(bool)
}, strict=True, coerce=True)