import os
import sqlite3

import pandas as pd

BASE_DIR = os.path.join(os.path.dirname(__file__))

data = pd.read_csv(os.path.join(BASE_DIR, 'data', 'sql_source.csv'))

conn = sqlite3.connect(os.path.join(BASE_DIR, 'databases', 'wine_data.db'))
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS wine_data (
                  Winery TEXT,
                  Year INTEGER,
                  Wine_ID INTEGER UNIQUE,
                  Wine TEXT,
                  Rating REAL,
                  Reviews INTEGER,
                  Price REAL,
                  Region TEXT,
                  Primary_Grape TEXT,
                  Natural BOOLEAN,
                  Country TEXT,
                  Style TEXT,
                  Country_Code TEXT
                )''')

data.to_sql('wine_data', conn, if_exists='replace', index=False)
conn.close()