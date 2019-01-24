from flask import Flask, render_template, request, redirect
import data_logic


app = Flask(__name__)


@app.route('/')
@app.route('/list')
def route_list():
    return render_template('list.html', dict=data_logic.get_all_questions())


@app.route('/questions/<question_id>')
def display(question_id):
    data_logic.add_view(question_id)
    answer, question = data_logic.display_question()
    return render_template("questions.html", q_id=question_id, answer=answer, question=question)


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def new_answer(question_id):
    if request.method == 'POST':
        new_answer = request.form.get('new_answer')
        data_logic.add_new_answer(new_answer, question_id)
        return redirect('/questions/' + question_id)
    return render_template("post_answer.html", q_id=question_id)


@app.route('/add_question', methods=['GET','POST'])
def route_add_question():
    if request.method == 'POST':
        question_to_add = data_logic.add_question(request.form.get('new_question'),request.form.get('details'))
        data_logic.new_question(question_to_add)
        return redirect('/questions/'+str(question_to_add['id']))
    else:
        return render_template('add_question.html')


@app.route('/vote_up/<question_id>')
def vote_up(question_id):
    data_logic.vote_counter(question_id, 'up')
    return redirect('/questions/'+question_id)


@app.route('/vote_down/<question_id>')
def vote_down(question_id):
    data_logic.vote_counter(question_id, 'down')
    return redirect('/questions/' + question_id)


@app.route('/question/<question_id>/delete', methods=['GET', 'POST'])
def delete_question(question_id):
    data_logic.delete_q(question_id)
    data_logic.delete_a(question_id)
    return redirect('/')



@app.route('/question/<question_id>/edit', methods=['GET','POST'])
def edit(question_id):
    questions = data_logic.get_all_questions()
    if request.method == "GET":
        return render_template("edit.html", q_id= question_id, questions=questions)
    else:
        data_logic.edit_question(question_id, request.form.get("edit_q"))
        return redirect("/questions/"+str(question_id))



if __name__ == "__main__":
    app.run()
