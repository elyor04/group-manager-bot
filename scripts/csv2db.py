import pandas as pd
import sqlite3

csv_file = "data/sqlite.csv"
db_file = "data/sqlite.db"
table_name = "user_info"

df = pd.read_csv(csv_file)
conn = sqlite3.connect(db_file)
df.to_sql(table_name, conn, if_exists="replace", index=False)

conn.commit()
conn.close()
print(f"Data from {csv_file} has been written to {table_name} in {db_file}")
