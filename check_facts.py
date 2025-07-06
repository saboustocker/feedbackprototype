import psycopg2
from openai import OpenAI
import openai
import os
from dotenv import load_dotenv
import re

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def get_facts_feedback(student_reflection: str) -> str:

    check_facts = f"""
    You will receive a self-reflection written by a student on a method they learned in a lecture and how they can apply this method in their practical work. Their task is to critically reflect on the method learned and how they can apply it in their practical work. 

    Check the text and extract all the factual knowledge on the method they state in their reflection. Make sure that you do not omit any facts stated.

    An example for factual knowledge is: "Business Process Model and Notation (BPMN) is a graphical representation for specifying business processes in a business process model."
    An example that is not factual knowledge is: "I was excited to learn about BPMN because it is a good tool for me." 

    This is the student reflection: 
    {student_reflection}

    Before your final answer, check for each fact that: 
    1. It really is a fact about the method and not about the student or the context.
    2. The student actually wrote that in their reflection.
    3. The wording is as close to the student's wording as possible.

    Your output has the following format: 

    [Fact 1] ... [End Fact 1]
    [Fact 2] ... [End Fact 2]
    ...

    Total Facts: number of facts
    
    """
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant for evaluating academic self-reflections. Your role is to very critically investigate the reflections to help the students make the most out of the exercise. You are strict but still well-meaning."},
        {"role": "user", "content": check_facts}
    ]

    response_baseline = openai.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.01
    )

    return response_baseline.choices[0].message.content.strip()

if __name__ == "__main__":
    print("Paste the student reflection below. Press ENTER twice to submit:\n")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    student_reflection = "\n".join(lines)

    feedback = get_facts_feedback(student_reflection)
    print("\nExtracted Facts:\n")
    print(feedback)