from flask import Flask, request, render_template
import baseline_prompt

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def index():
    feedback = None
    if request.method == "POST":
        reflection = request.form["reflection"]
        feedback = baseline_prompt.get_llm_feedback(reflection)
    return render_template("index.html", feedback=feedback)