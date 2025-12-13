import sys
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime, timedelta

file_name = sys.argv[1]
cdc_column = sys.argv[2]
primary_key = sys.argv[3]

csv_path = f'/opt/airflow/csv/{file_name}'

engine = create_engine('postgresql+psycopg2://admin:admin123@localhost:5432/postgres')

df = pd.read_csv(csv_path)

# Filter only yesterdays data and deduplicated data
yesterday = datetime.now() - timedelta(days=1)
df[cdc_column] = pd.to_datetime(df[cdc_column])
df = df[df[cdc_column].dt.date == yesterday.date()]
df = df.drop_duplicates(subset=[primary_key], keep='first')

if not df.empty:
    df.to_sql(file_name.split(".")[0], engine, if_exists='append', index=False)
    print(f"{file_name} incremental load complete.")
else:
    print(f"No new records to load for {file_name}.")
