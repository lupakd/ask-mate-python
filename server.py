from flask import Flask, render_template, request, redirect, url_for
import data_logic


app = Flask(__name__)


@app.route('/')
@app.route('/list')
def route_list():
    return render_template('list.html', dict=data_logic.get_all_questions())


@app.route('/questions/<question_id>')
def display(question_id):
    data_logic.add_view(question_id)
    answer = data_logic.get_all_answers()
    question = data_logic.get_all_questions()
    comments = data_logic.get_all_comments()
    return render_template("questions.html",
                           q_id=int(question_id),
                           answer=answer,
                           question=question,
                           comments=comments,
                           question_id=question_id)


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
        question_id = data_logic.add_question(request.form.get('new_question'), request.form.get('details'))
        return redirect('/questions/'+str(question_id['id']))
    else:
        return render_template('add_question.html')


@app.route('/vote_up/<question_id>')
def vote_up(question_id):
    data_logic.vote_counter(question_id, 'up')
    return redirect('/questions/' + question_id)


@app.route('/vote_down/<question_id>')
def vote_down(question_id):
    data_logic.vote_counter(question_id, 'down')
    return redirect('/questions/' + question_id)


@app.route('/question/<question_id>/delete', methods=['GET', 'POST'])
def delete_question(question_id, ):
    data_logic.delete_all_comments(question_id=question_id) #todo not tested
    data_logic.delete_question(question_id)
    data_logic.delete_question_answers(question_id)
    return redirect('/')


@app.route('/answer/<question_id>/<answer_id>/delete', methods=['GET', 'POST'])
def delete_answer(answer_id, question_id):
    data_logic.delete_all_comments(answer_id=answer_id)   #todo not tested
    data_logic.delete_answer(answer_id)
    return redirect("/questions/"+str(question_id))

@app.route('/answer/<question_id>/<answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(answer_id, question_id):
    answers = data_logic.get_all_answers()
    questions = data_logic.get_all_questions()
    if request.method == "GET":
        return render_template("edit_answer.html", a_id=int(answer_id), question_id=int(question_id), answers=answers,
                               questions=questions)
    else:
        data_logic.edit_answer(answer_id, request.form.get("edit_a"))
        return redirect("/questions/"+str(question_id))


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def edit(question_id):
    questions = data_logic.get_all_questions()
    if request.method == "GET":
        return render_template("edit.html", q_id=int(question_id), questions=questions)
    else:
        data_logic.edit_question(question_id, request.form.get("edit_q"))
        return redirect("/questions/"+str(question_id))


@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def add_comment_question(question_id):
    if request.method == 'POST':
        message = request.form.get('message')
        data_logic.add_comment(message, question_id=question_id)
        return redirect(url_for('display', question_id=question_id))
    elif request.method == 'GET':
        specific_url = url_for('add_comment_question', question_id=question_id)
        return render_template('new-comment.html', question_id=question_id, specific_url=specific_url)


@app.route('/answer/<answer_id>/new-comment', methods=['GET', 'POST'])
def add_comment_answer(answer_id):
    if request.method == 'POST':
        message = request.form.get('message')
        question_id = data_logic.get_question_id(answer_id)
        data_logic.add_comment(message, question_id=question_id, answer_id=answer_id)
        return redirect(url_for('display', question_id=question_id))
    elif request.method == 'GET':
        specific_url = url_for('add_comment_answer', answer_id=answer_id)
        return render_template('new-comment.html', answer_id=answer_id, specific_url=specific_url)


@app.route('/comments/<comment_id>/delete', methods=['POST', 'GET'])
def delete_comment(comment_id):
    question_id = data_logic.get_question_id(comment_id=comment_id)
    if request.method == 'GET':
        return render_template('confirm.html', comment_id=comment_id, question_id=question_id)
    else:
        data_logic.delete_one_comment(comment_id)
        return redirect(url_for('display', question_id=question_id))


if __name__ == "__main__":
    app.run()
