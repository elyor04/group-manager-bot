import pandas as pd
import sqlite3

# Read the CSV file into a DataFrame
csv_file = "data/sqlite.csv"
df = pd.read_csv(csv_file)

# Create a connection to the SQLite database (or create it if it doesn't exist)
db_file = "data/sqlite.db"
conn = sqlite3.connect(db_file)

# Convert the DataFrame to a SQL table
df.to_sql("user_info", conn, if_exists="replace", index=False)

# Commit the changes and close the connection
conn.commit()
conn.close()

print(f"Data from {csv_file} has been successfully written to {db_file}")
