import psycopg2
from openai import OpenAI
import openai
import os
from dotenv import load_dotenv
import re
import check_facts

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

## query is: method output
def get_facts_from_reflection(student_reflection):
    output_facts = check_facts.get_facts_feedback(student_reflection)
    facts = []
    facts = re.findall(r'\[Fact \d+\] (.*?) \[End Fact \d+\]', output_facts)
    return facts

## define function to retreive relevant chunks
def get_information(query, k = 3): 
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

## function that factchecks each claim
def give_factual_feedback(query):
    
    results_rag = get_information(query)

    context = "\n\n".join(row[0] for row in results_rag)

    prompt = f"""
    Evaluate the following statement for factual correctness:
    {query}

    Use the following context to answer the question: 

    {context}

    Cite the paragraphs you used where they are relevant.

    If the statement is correct, repeat the statement verbatim and state "this statement is correct". In this case, do NOT provide any context.
    If the statement is incorrect, repeat the statement verbatim and state "this statement is incorrect". In this case, also explain why based on the context.

    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.01
    )

    return (response.choices[0].message.content)


