import psycopg2
from dotenv import dotenv_values

secrets = dotenv_values("src/.env")

conn = psycopg2.connect(
    database="postgres",
    user=secrets.get("POSTGRES_USER"),
    password=secrets.get("POSTGRES_PASSWORD"),
    host="127.0.0.1",
    port="5432",
)

conn.autocommit = True

cursor = conn.cursor()
# Creating Database pokemon_kafka
sql = """select 'CREATE database pokemon_kafka'
    WHERE NOT EXISTS 
    (SELECT FROM pg_database WHERE datname = 'pokemon_kafka');"""

cursor.execute(sql)
print("Database pokemon-kafka created successfully or already existing")
conn.close()

# Switching to new database pokemon_kafka
conn = psycopg2.connect(
    database="pokemon_kafka",
    user="postgres",
    password="S3cret",
    host="127.0.0.1",
    port="5432",
)

cursor = conn.cursor()

# Creating Table pokemon_battle
sql = """CREATE TABLE IF NOT EXISTS pokemon_battle(
    pokemon_name VARCHAR(50) NOT NULL,
    ability CHAR(20),
    timestamp TIMESTAMP)"""
cursor.execute(sql)
conn.commit()

print("Table pokemon_battle created successfully or already existing")

conn.close()
