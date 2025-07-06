import os
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

instructions = """
You will receive a self-reflection written by a student on a method they learned in a lecture and how they can apply this method in their practical work. Their task is to critically reflect on the method learned and how they can apply it in their practical work. 

You must classify the reflection in according to the following levels: 
1. **Remembering**: Recognizing or recalling knowled ge from memory. Remembering is when memory is used to produce or retrieve definitions, facts, or lists, or to recite previously learned information.

2. **Understanding**: Constructing meaning from different types of functions be they written or graphic messages or activities like interpreting, exemplifying, classifying, summarizing, inferring, comparing, or explaining.

3. **Applying**: Carrying out or using a procedure through executing, or implementing. Applying relates to or refers to situations where learned material is used through products like models, presentations, interviews or simulations.

4. **Analyzing**: Breaking materials or concepts into parts, determining how the parts relate to one another or how they interrelate, or how the parts relate to an overall structure or purpose. Mental actions included in this function are differentiating, organizing, and attributing, as well as being able to distinguish  between the components or parts. When one is analyzing, he/she can illustrate this mental function by creating spreadsheets, surveys, charts, or diagrams, or graphic representations.

5. **Evaluating**: Making judgments based on criteria and standards through checking and critiquing. Critiques, recommendations, and reports are some of the products that can be created to demonstrate the processes of evaluation. In the newer taxonomy, evaluating comes before creating as it is often a necessary part of the precursory behavior before one creates something.

6. **Creating**: Putting elements together to form a coherent or functional whole; reorganizing elements into a new pattern or structure through generating, planning, or producing. Creating requires users to put parts together in a new way, or synthesize parts into something new and different creating a new form or product.


The reflection is on one of the five levels. Students should aim to reach at least level 4 out of 5. 

Based on the five levels and how the student is situated, give feedback on the following questions: 
1. How well was the goal to write a critical reflection on a method and how it can be applied achieved?
2. How good is the process to get there? 
3. (if needed): What does the student need to get to the next level?

The reflection will be in German. Give your feedback in German. 

"""




def get_llm_feedback(reflection: str) -> str:

    full_prompt = f"""{instructions}

    Student Reflection (in German:)
    \"\"\"
    {reflection}
    \"\"\"

    """
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant for evaluating academic self-reflections."},
        {"role": "user", "content": full_prompt}
    ]

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.25
    )

    return response.choices[0].message.content.strip()