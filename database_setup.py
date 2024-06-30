import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

# Create the pages table with a timestamp column
c.execute('''
          CREATE TABLE IF NOT EXISTS pages
          (id INTEGER PRIMARY KEY,
          title TEXT,
          content TEXT,
          keywords TEXT,
          votes INTEGER,
          timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)
          ''')

conn.commit()
conn.close()
