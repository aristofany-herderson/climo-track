import pandas as pd
import sqlite3
import os
import requests
import datetime

CSV_FILE = "./database/municipios.csv"
CSV_URL = "https://raw.githubusercontent.com/kelvins/municipios-brasileiros/master/csv/municipios.csv"
DATA_URL = 'https://archive-api.open-meteo.com/v1/era5'
START_DATE = '2021-01-01'
END_DATE = '2021-12-31'

if not os.path.exists(CSV_FILE):
  print("Baixando arquivo de municípios...")
  response = requests.get(CSV_URL)
  with open(CSV_FILE, 'wb') as f:
    f.write(response.content)
  print("Download concluído.")
  
from datetime import datetime

def calculate_monthly_averages(hourly_data, temperature_data, rain_data):
  monthly_data = {
    "temperature": {month: [] for month in range(1, 13)},
    "rain": {month: [] for month in range(1, 13)}
  }
  
  for i, timestamp in enumerate(hourly_data):
    date_obj = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M") 
    month = date_obj.month  
    
    monthly_data["temperature"][month].append(temperature_data[i])
    monthly_data["rain"][month].append(rain_data[i])
  
  monthly_results = {
    "temperature": {month: (sum(values) / len(values)) if values else 0 for month, values in monthly_data["temperature"].items()},
    "rain": {month: sum(values) if values else 0 for month, values in monthly_data["rain"].items()}
  }
  
  return monthly_results

try:
  connection = sqlite3.connect("db.sqlite3");
  df = pd.read_csv(CSV_FILE)
  
  for row in df.itertuples():
    if (row.codigo_uf == 24):
      params = {
        'latitude': row.latitude,
        'longitude': row.longitude,
        "start_date": START_DATE,
        "end_date": END_DATE,
        "hourly": "temperature_2m,rain",
        "timezone": "America/Sao_Paulo"
      }
      
      response = requests.get(DATA_URL, params=params)
      data = response.json()
      monthly_averages = calculate_monthly_averages(data["hourly"]["time"], data["hourly"]["temperature_2m"], data["hourly"]["rain"])
      temperature = monthly_averages['temperature']
      rain = monthly_averages['rain']
      
      print(row.codigo_ibge, temperature[1], rain[2])

      query = f"""
      INSERT INTO app_hydrologicaldata (
          station_id, 
          temperature_average_january, temperature_average_february, temperature_average_march, temperature_average_april,
          temperature_average_may, temperature_average_june, temperature_average_july, temperature_average_august,
          temperature_average_september, temperature_average_october, temperature_average_november, temperature_average_december,
          precipitation_average_january, precipitation_average_february, precipitation_average_march, precipitation_average_april,
          precipitation_average_may, precipitation_average_june, precipitation_average_july, precipitation_average_august,
          precipitation_average_september, precipitation_average_october, precipitation_average_november, precipitation_average_december
      )
      VALUES (
          {row.codigo_ibge},
          {temperature[1]}, {temperature[2]}, {temperature[3]}, {temperature[4]},
          {temperature[5]}, {temperature[6]}, {temperature[7]}, {temperature[8]},
          {temperature[9]}, {temperature[10]}, {temperature[11]}, {temperature[12]},
          {rain[1]}, {rain[2]}, {rain[3]}, {rain[4]},
          {rain[5]}, {rain[6]}, {rain[7]}, {rain[8]},
          {rain[9]}, {rain[10]}, {rain[11]}, {rain[12]}
      )
      """
      connection.execute(query)
      connection.commit()
      
except Exception as e:
    print(f"Erro de execução: {e}")