from flask import Flask, render_template, request, redirect, flash, session
from surveys import satisfaction_survey

app = Flask(__name__)
app.secret_key = "do-not-do-this"

@app.route('/')
def survey_init():
    return render_template("index.html", survey=satisfaction_survey)

@app.route("/start", methods=["POST"])
def start_survey():
    session["responses"] = []
    return redirect("/questions/0")


@app.route('/questions/<int:qid>')
def show_question(qid):
    responses = session.get("responses", [])
    if qid >= len(satisfaction_survey.questions):
        flash("Invalid question access. Redirected to the start page.")
        return redirect("/complete")
    if qid != len(responses):
        flash(f"Invalid question access. Redirected to question {len(responses)}")
        return redirect(f"/questions/{len(responses)}")
    question = satisfaction_survey.questions[qid]
    return render_template('questions.html', question=question, qid=qid)

@app.route('/answer', methods=['POST'])
def handle_response():
    answer = request.form['answer']
    responses = session.get("responses", [])
    responses.append(answer)
    session["responses"] = responses

    if len(responses) < len(satisfaction_survey.questions):
        return redirect(f"/questions/{len(responses)}")
    else:
        return redirect('/complete')

@app.route('/complete')
def complete():
    return render_template('complete.html')