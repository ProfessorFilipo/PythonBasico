###################################################################
###  L O A D E R   C S V   P A R A   M O N G O D B   A T L A S  ###
###################################################################
### Prof. Filipo Mor - junho de 2025                            ###
###################################################################
### Dataset do kaggle - 2015 Flight Delays and Cancellations    ###
### https://www.kaggle.com/datasets/usdot/flight-delays         ###
###################################################################

import pandas as pd
from pymongo import MongoClient

# Configurações
CAMINHO_ARQUIVO_CSV = 'airlines.csv'  # Nome do arquivo CSV
MONGO_URI = 'sua_string_de_conexao_mongodb_atlas'  # Sua string de conexão do MongoDB Atlas
NOME_BANCO_DE_DADOS = 'nome_do_seu_banco'  # Nome do seu banco de dados
NOME_COLECAO = 'airlines'  # Nome da coleção onde os dados serão inseridos

def conectar_mongodb(uri, db_nome):
    client = MongoClient(uri)
    db = client[db_nome]
    return db

def carregar_csv_no_mongodb(caminho_csv, db, nome_colecao):
    # Ler o CSV usando Pandas
    df = pd.read_csv(caminho_csv)
    # Converter DataFrame para uma lista de dicionários
    dados = df.to_dict(orient='records')
    # Obter ou criar a coleção
    colecao = db[nome_colecao]
    # Inserir os dados na coleção
    colecao.insert_many(dados)
    print(f"Dados carregados com sucesso na coleção '{nome_colecao}'.")

def main():
    # Conectar ao MongoDB
    db = conectar_mongodb(MONGO_URI, NOME_BANCO_DE_DADOS)
    # Carregar os dados do CSV para o MongoDB
    carregar_csv_no_mongodb(CAMINHO_ARQUIVO_CSV, db, NOME_COLECAO)

if __name__ == "__main__":
    main()