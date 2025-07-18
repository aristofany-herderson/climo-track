import pandas as pd
import sqlite3

state_name = "Rio Grande do Norte" 

data = {'name': [state_name]}
df = pd.DataFrame(data)

connection = sqlite3.connect("db.sqlite3")

df.to_sql('app_state', connection, if_exists='append', index=False)
print(df)
