from flask import Flask, render_template, request, redirect, flash
from surveys import satisfaction_survey

app = Flask(__name__)
app.secret_key = "do-not-do-this"

responses = []

@app.route('/')
def survey_init():
    return render_template("index.html", survey=satisfaction_survey)

@app.route('/questions/<int:qid>')
def show_question(qid):
    questions = satisfaction_survey.questions
    if qid >= len(questions):
        flash("Invalid question access. Redirected to the start page.")
        return redirect("/")
    if qid != len(responses):
        flash(f"Invalid question access. Redirected to question {len(responses)}")
        return redirect(f"/questions/{len(responses)}")
    question = satisfaction_survey.questions[qid]
    return render_template('questions.html', question=question, qid=qid)

@app.route('/answer', methods=['POST'])
def handle_response():
    answer = request.form['answer']
    responses.append(answer)

    if len(responses) < len(satisfaction_survey.questions):
        return redirect(f"/questions/{len(responses)}")
    else:
        return redirect('/complete')

@app.route('/complete')
def complete():
    return render_template('complete.html')