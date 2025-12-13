import sys
import pandas as pd
from sqlalchemy import create_engine

file_name = sys.argv[1]
csv_path = f'../csv/{file_name}'

# Connect to Postgres
engine = create_engine('postgresql+psycopg2://admin:admin123@localhost:5432/postgres')

# Read CSV and load into Postgres
df = pd.read_csv(csv_path)
df.to_sql(file_name.split(".")[0], engine, if_exists='replace', index=False)
print(f"{file_name} initial load complete.")
