import os
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_llm_feedback(reflection: str) -> str:

    full_prompt = f"""

    You will get several components based on which you must give feedback on a reflection written by a student on a method they learned in a lecture and how they can apply this method in their practical work. Their task is to critically reflect on the method learned and how they can apply it in their practical work. The feedback you will give consists of the following components: 

    1. Did the student factually understand the method?
    2. Did the student critically reflect on the method itself?
    3. Did the student critically reflect how they can apply this method in their practical work?

    You must give feedback on three levels: 
    1. Task-based level: How well was the task "critically reflect on the method learned and how you can apply it in their practical work." achieved?
    2. Process level: how well is the reflection and train of thought formulated? 
    3. Progress level: what does the student need to improve?

    The reflection is written in German. Please answer in German in 100-200 words. Answer as one coherent text and don't use bullet points. Answer in the first person, addressing the student directly. Use the German informal "du". 

    Use the following information to formulate your feedback:

    Critical reflection written by the student: 
    {reflection}
    
    Baseline task achievement: 
    Check the text and extract the method they learned, as well as the way they plan to apply this method in their practical work. If one of the components is missing, state "missing". 

    Rate each of the components on a scale from 1 to 10 in terms of how specific it is. Indicators for specificity include naming examples, giving definitions, or specific applications. A rating of 1 is very generic, and a rating of 10 is highly specific.
    
    Respond in the following format: 

    Method: [shortly describe the method as it is described in the reflection.] OR missing
    Application: [shortly describe the application in their practical work as it is described in the reflection.] OR missing

    Specificity Method: 1 to 10 OR missing, if method is missing
    Specificity Application: 1 to 10 OR missing, if application is missing.


    Factual knowledge:
    Check the text and extract all the factual knowledge on the method they state in their reflection. Make sure that you do not omit any facts stated.

    An example for factual knowledge is: "Business Process Model and Notation (BPMN) is a graphical representation for specifying business processes in a business process model."
    An example that is not factual knowledge is: "I was excited to learn about BPMN because it is a good tool for me." 

    Before your final answer, check for each fact that: 
    1. It really is a fact about the method and not about the student or the context.
    2. The student actually wrote that in their reflection.
    3. The wording is as close to the student's wording as possible.

    Your output has the following format: 

    [Fact 1] ... [End Fact 1]
    [Fact 2] ... [End Fact 2]
    
    If the statement is correct, repeat the statement verbatim and state "this statement is correct". In this case, do NOT provide any context.
    If the statement is incorrect, repeat the statement verbatim and state "this statement is incorrect". In this case, also explain why based on the context.


    Reflection:
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

    Ensure that you consider all aspects equally.

    """
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant for evaluating academic self-reflections. Your role is to very critically investigate the reflections to help the students make the most out of the exercise. You are strict but still well-meaning."},
        {"role": "user", "content": full_prompt}
    ]

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.01
    )

    return response.choices[0].message.content.strip()