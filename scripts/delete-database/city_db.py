import sqlite3


try:
    connection = sqlite3.connect("db.sqlite3")
    cursor = connection.cursor()

    cursor.execute("DELETE FROM app_city;")

    connection.commit()

    print("Todos os registros da tabela `app_city` foram deletados com sucesso!")

except Exception as e:
    print(f"Erro ao deletar dados da tabela `app_city`: {e}")

finally:
    # Fecha a conexão com o banco de dados
    connection.close()
