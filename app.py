from flask import Flask, request, render_template
import reflection_feedback

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def index():
    feedback = None
    if request.method == "POST":
        reflection = request.form["reflection"]
        feedback = reflection_feedback.get_llm_feedback(reflection)
    return render_template("index.html", feedback=feedback)