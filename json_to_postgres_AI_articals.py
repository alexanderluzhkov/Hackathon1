import json
import psycopg2

# Load JSON data
with open("ai_articles_counts.json", "r") as f:
    data = json.load(f)

# Connect to PostgreSQL database
conn = psycopg2.connect(
    dbname='AI_scholarly_articles_number_per_year', 
    user='postgres', 
    password='Begemotik', 
    host='localhost'
)
cursor = conn.cursor()

# Create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS articles (
    topic TEXT,
    year INTEGER,
    count INTEGER
)
''')
conn.commit()

# Insert data into the database
for topic, yearly_counts in data.items():
    for year, count in yearly_counts.items():
        cursor.execute('''
        INSERT INTO articles (topic, year, count)
        VALUES (%s, %s, %s)
        ''', (topic, year, count))

conn.commit()

# Query the database to verify insertion
cursor.execute('SELECT * FROM articles')
rows = cursor.fetchall()

# Print the rows
for row in rows:
    print(row)

# Close the connection
conn.close()
