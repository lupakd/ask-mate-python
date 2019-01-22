from typing import Dict, List, Any

from flask import Flask, render_template, request, redirect
import data_logic


app = Flask(__name__)


@app.route('/')
@app.route('/list')
def route_list():
    return render_template('list.html', dict=data_logic.get_all_questions())


@app.route('/questions/<question_id>')
def display(question_id):
    answer, question = data_logic.display_question()
    return render_template("questions.html", q_id=question_id, answer=answer, question=question)


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def new_answer(question_id):
    if request.method == 'POST':
        new_answer = request.form.get('new_answer')
        print(new_answer)
        return redirect('/question/' + question_id)

    return render_template("post_answer.html", q_id=question_id)


if __name__ == "__main__":
    app.run()
