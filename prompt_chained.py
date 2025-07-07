import os
from dotenv import load_dotenv
import openai
import baseline_feedback
import check_facts
import factual_feedback
import reflection_feedback

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_llm_feedback(reflection: str) -> str:

    baseline_output = baseline_feedback.get_baseline_feedback(reflection)
    print(baseline_output)

    fact_extract = check_facts.get_facts_feedback(reflection)
    print(fact_extract)

    facts_array = factual_feedback.get_facts_from_reflection(fact_extract)
    print(facts_array)

    feedbacks_facts = []

    for fact in facts_array:
        feedback = factual_feedback.give_factual_feedback(fact)
        feedbacks_facts.append(feedback)

    reflection_output = reflection_feedback.get_reflection_feedback(reflection)

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

    Baseline task achievement: This is the assessment if the components of the task (critical reflection on the method and on how it can be applied) are given. Also consider how precise the reflection is: 
    {baseline_output}

    Factual knowledge: These are the facts about the method the student claims, and information about their correctness: 
    {facts_array}

    Reflection: This is an assessment on how advanced the answer by the student is in terms of critical reflection. It is based on Bloom's taxonomy. When referencing Bloom's taxonomy, explain on which level they are and why, and also tell them how they can get to the next level. Always mention that this assessment is based on the taxonomy by Bloom.
    {reflection_output}

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