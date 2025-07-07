import psycopg2
from openai import OpenAI
import openai
import os
from dotenv import load_dotenv
import re

load_dotenv()

API_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_key)

postgres_PW = os.getenv("POSTGRES_PW")

conn = psycopg2.connect(
    dbname="prototype_feedback",
    user="postgres",
    password=postgres_PW,
    host="localhost",
    port="5432"
)

cur = conn.cursor()

## If not exists create database
try: 
    cur.execute("""
        CREATE TABLE IF NOT EXISTS information_table (
                id SERIAL PRIMARY KEY, 
                information TEXT,
                embedding vector(3072));
                """)

    conn.commit()

except psycopg2.Error as e:
    print("An error occurred:", e)


## Embedd Wikipedia Article
with open("wikipedia_article.html", "r", encoding="utf-8") as file:
    html_article = file.read()

print(html_article)

splitting_by = r"(?=<h1|<h2|<h3|</p><p|<ul|<table)"

chunks = re.split(splitting_by, html_article)

document_parts = []

for i, chunk in enumerate(chunks):
    print(i)
    print(chunk)
    document_parts.append(chunk)

for doc in document_parts: 
    response = client.embeddings.create(
        input=doc,
        model="text-embedding-3-large"
    )
    embedding = response.data[0].embedding

    cur.execute(
        "INSERT INTO information_table (information, embedding) VALUES (%s, %s)",
        (doc, embedding)
    )

conn.commit()
cur.close()
conn.close()


