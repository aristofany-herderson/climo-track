import sqlite3


try:
    connection = sqlite3.connect("db.sqlite3")
    cursor = connection.cursor()

    cursor.execute("DELETE FROM app_hydrologicaldata;")

    connection.commit()

    print("Todos os registros da tabela `app_hydrologicaldata` foram deletados com sucesso!")

except Exception as e:
    print(f"Erro ao deletar dados da tabela `app_hydrologicaldata`: {e}")

finally:
    # Fecha a conexão com o banco de dados
    connection.close()
