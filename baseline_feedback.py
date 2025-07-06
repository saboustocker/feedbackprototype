import psycopg2
from openai import OpenAI
import openai
import os
from dotenv import load_dotenv
import re

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_baseline_feedback(student_reflection):

    check_baseline = f"""
    You will receive a self-reflection written by a student on a method they learned in a lecture and how they can apply this method in their practical work. Their task is to critically reflect on the method learned and how they can apply it in their practical work. 

    Check the text and extract the method they learned, as well as the way they plan to apply this method in their practical work. If one of the components is missing, state "missing". 

    Rate each of the components on a scale from 1 to 10 in terms of how specific it is. Indicators for specificity include naming examples, giving definitions, or specific applications. A rating of 1 is very generic, and a rating of 10 is highly specific.
    
    Respond in the following format: 

    Method: [shortly describe the method as it is described in the reflection.] OR missing
    Application: [shortly describe the application in their practical work as it is described in the reflection.] OR missing

    Specificity Method: 1 to 10 OR missing, if method is missing
    Specificity Application: 1 to 10 OR missing, if application is missing

    This is the student reflection: 
    {student_reflection}
    """
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant for evaluating academic self-reflections. Your role is to very critically investigate the reflections to help the students make the most out of the exercise. You are strict but still well-meaning."},
        {"role": "user", "content": check_baseline}
    ]

    response_baseline = openai.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.01
    )

    return response_baseline.choices[0].message.content.strip()


