"""
python -m scripts.db2csv
"""
import sqlite3
import pandas as pd

db_file = "data/sqlite.db"
table_name = "UserInfos"
csv_file = "data/sqlite.csv"

conn = sqlite3.connect(db_file)
df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
df.to_csv(csv_file, index=False)

conn.close()
print(f"Data from {table_name} in {db_file} has been written to {csv_file}")
