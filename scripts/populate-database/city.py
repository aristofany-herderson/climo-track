import pandas as pd
import sqlite3
import os
import requests

CSV_FILE = "./database/municipios.csv"
CSV_URL = "https://raw.githubusercontent.com/kelvins/municipios-brasileiros/master/csv/municipios.csv"

if not os.path.exists(CSV_FILE):
    print("Baixando arquivo de municípios...")
    response = requests.get(CSV_URL)
    with open(CSV_FILE, 'wb') as f:
        f.write(response.content)
    print("Download concluído.")

try:
    fields = ['codigo_ibge', 'nome', 'codigo_uf']
    df = pd.read_csv(CSV_FILE, delimiter=",", on_bad_lines="skip", encoding='UTF-8', usecols=fields)
    df = df[df['codigo_uf'] == 24]
    
    df = df.rename(columns={
        'codigo_ibge': 'id',
        'nome': 'station'
    })
    df["state_id"] = 1

    df.columns = df.columns.str.strip()
    connection = sqlite3.connect("db.sqlite3")
    
    df.drop(columns=['codigo_uf'], inplace=True)  
    df.to_sql('app_city', connection, if_exists='replace', index=False)

    connection.close()

    print("Tabela `City` populada com sucesso com os dados do RN!")
    print(df)

except Exception as e:
    print(f"Erro ao popular a tabela `City`: {e}")
