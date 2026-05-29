import os
from pathlib import Path
import pandas as pd
import duckdb
import pandera.pandas as pa
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Importamos os schemas funcionais diretamente
from app.schema import ProductSchemaKPI, ProdutoSchema


def load_settings():
    """Carrega as configurações a partir de variáveis de ambiente."""
    dotenv_path = Path.cwd() / ".env"
    load_dotenv(dotenv_path=dotenv_path)

    settings = {
        "db_host": os.getenv("POSTGRES_HOST"),
        "db_user": os.getenv("POSTGRES_USER"),
        "db_pass": os.getenv("POSTGRES_PASSWORD"),
        "db_name": os.getenv("POSTGRES_DB"),
        "db_port": os.getenv("POSTGRES_PORT"),
    }
    return settings


def extrair_do_sql(query: str) -> pd.DataFrame:
    """Extrai dados do banco de dados SQL usando a consulta fornecida."""
    settings = load_settings()
    connection_string = f"postgresql://{settings['db_user']}:{settings['db_pass']}@{settings['db_host']}:{settings['db_port']}/{settings['db_name']}"
    engine = create_engine(connection_string)

    with engine.connect() as conn, conn.begin():
        df_crm = pd.read_sql(query, conn)

    # Validação manual no retorno usando o schema clássico
    return ProdutoSchema.validate(df_crm)


def transformar(df: pd.DataFrame) -> pd.DataFrame:
    """Transforma os dados do DataFrame aplicando cálculos e normalizações."""
    # Garante que o dado que entra está correto
    df_validado_entrada = ProdutoSchema.validate(df)
    
    # Executa as transformações
    df_validado_entrada["valor_total_estoque"] = df_validado_entrada["quantidade"] * df_validado_entrada["preco"]
    df_validado_entrada["categoria_normalizada"] = df_validado_entrada["categoria"].str.lower()
    df_validado_entrada["disponibilidade"] = df_validado_entrada["quantidade"] > 0

    # Garante que o dado transformado segue o contrato de saída antes de entregar
    return ProductSchemaKPI.validate(df_validado_entrada)


def load_to_duckdb(df: pd.DataFrame, table_name: str, db_file: str = "my_duckdb.db"):
    """Carrega o DataFrame no DuckDB, criando ou substituindo a tabela especificada."""
    df_validado = ProductSchemaKPI.validate(df)
    
    con = duckdb.connect(database=db_file, read_only=False)
    con.register("df_temp", df_validado)
    con.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM df_temp")
    con.close()


if __name__ == "__main__":
    query = "SELECT * FROM produtos_bronze_email"
    
    print("Iniciando extração do Postgres...")
    df_crm = extrair_do_sql(query=query)
    
    print("Aplicando transformações e validações do Pandera...")
    df_crm_kpi = transformar(df_crm)

    print("Salvando o espelho dos dados transformados em JSON...")
    with open("dados_transformados.json", "w", encoding="utf-8") as file:
        file.write(df_crm_kpi.to_json(orient="records", indent=4))

    print("Carregando os dados validados no DuckDB...")
    load_to_duckdb(df=df_crm_kpi, table_name="tabela_kpi")
    
    print("Pipeline finalizado com sucesso!")