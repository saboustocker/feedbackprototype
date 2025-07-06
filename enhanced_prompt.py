import psycopg2
from openai import OpenAI
import openai
import os
from dotenv import load_dotenv
import re

load_dotenv()

API_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_key)

conn = psycopg2.connect(
    dbname="prototype_feedback",
    user="postgres",
    password="Poeneyser.01",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

## define function to retreive relevant chunks 
def get_information(query, k = 5): 
    query_embedding = client.embeddings.create(
        input = query,
        model = "text-embedding-3-large"
    ).data[0].embedding

    sql = """
    SELECT information FROM information_table ORDER BY embedding <=> %s::vector
    LIMIT %s;
    """

    cur.execute(sql,(query_embedding,k))

    results = cur.fetchall()

    return results

query = "What is the scope fo BPMN?"
print(query)

docs = get_information(query)

context = "\n\n".join(row[0] for row in docs)

prompt = f"""
Use the following context to answer the question: 

{context}

Question: {query}

Answer:
"""

print(prompt)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": prompt}]
)

print(response.choices[0].message.content)