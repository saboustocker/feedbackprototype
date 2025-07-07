from flask import Flask, request, render_template
import one_big_prompt
import prompt_chained

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def index():
    feedback = None
    if request.method == "POST":
        reflection = request.form["reflection"]
        feedback = prompt_chained.get_llm_feedback(reflection)
    return render_template("index.html", feedback=feedback)