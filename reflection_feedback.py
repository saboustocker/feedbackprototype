import os
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_reflection_feedback(reflection):
    
    instructions = f"""
    You will receive a self-reflection written by a student on a method they learned in a lecture and how they can apply this method in their practical work. Their task is to critically reflect on the method learned and how they can apply it in their practical work. 

    Your task is to assess if a critical reflection has taken place. A critical reflection is when a person not only analyzes a method and its possible applications, but also evaluates it. A critical reflection should be specific and fact-related, and not generic.

    You must classify the reflection in according to the following levels. Ensure you conduct the classification in regards to the task: critically reflecting on the method and how to apply it, and not on the learning process. 

    1. **Remembering**: Recognizing or recalling knowled ge from memory. Remembering is when memory is used to produce or retrieve definitions, facts, or lists, or to recite previously learned information.

    2. **Understanding**: Constructing meaning from different types of functions be they written or graphic messages or activities like interpreting, exemplifying, classifying, summarizing, inferring, comparing, or explaining.

    3. **Applying**: Carrying out or using a procedure through executing, or implementing. Applying relates to or refers to situations where learned material is used through products like models, presentations, interviews or simulations.

    4. **Analyzing**: Breaking materials or concepts into parts, determining how the parts relate to one another or how they interrelate, or how the parts relate to an overall structure or purpose. Mental actions included in this function are differentiating, organizing, and attributing, as well as being able to distinguish  between the components or parts. When one is analyzing, he/she can illustrate this mental function by creating spreadsheets, surveys, charts, or diagrams, or graphic representations.

    5. **Evaluating**: Making judgments based on criteria and standards through checking and critiquing. Critiques, recommendations, and reports are some of the products that can be created to demonstrate the processes of evaluation. In the newer taxonomy, evaluating comes before creating as it is often a necessary part of the precursory behavior before one creates something. Evaluation in this sense is NOT the same as self-evaluation.

    6. **Creating**: Putting elements together to form a coherent or functional whole; reorganizing elements into a new pattern or structure through generating, planning, or producing. Creating requires users to put parts together in a new way, or synthesize parts into something new and different creating a new form or product.

    Assess which level the reflection achieved. 

    Also state two to three aspects the student can improve on to reach the next level.

    This is the student reflection:
    {reflection}
    """

    messages = [
        {"role": "system", "content": "You are a helpful assistant for evaluating academic self-reflections. Your role is to very critically investigate the reflections to help the students make the most out of the exercise. You are strict but still well-meaning."},
        {"role": "user", "content": instructions}
    ]

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.01
    )

    return response.choices[0].message.content.strip()