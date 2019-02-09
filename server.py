from flask import Flask, render_template, request, redirect, url_for
import data_logic as dl

app = Flask(__name__)


@app.route('/')
def route_main():
    latest = dl.get_data('question', dl.question_fieldnames, 'submission_time', 'ASC', limit='5')
    return render_template('list.html', questions=latest)


@app.route('/list')
def route_list():
    questions = dl.get_data('question', dl.question_fieldnames, 'submission_time', 'asc')
    return render_template('list.html', questions=questions)


@app.route('/questions/<question_id>')
def display_question(question_id):
    dl.add_view(question_id)
    question = dl.get_data('question', dl.question_fieldnames, 'id', 'asc', 'id', question_id)
    answers = dl.get_data('answer', dl.answer_fieldnames, 'submission_time', 'asc', 'question_id', question_id)
    comments = dl.get_data('comment', dl.comment_fieldnames, 'submission_time', 'asc')
    return render_template("questions.html",
                           q_id=int(question_id),
                           answers=answers,
                           question=question,
                           comments=comments
                           )


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def add_answer(question_id):
    if request.method == 'POST':
        new_answer = request.form.get('new_answer')
        dl.add_new_answer(new_answer, question_id)
        return redirect(url_for('display_question', question_id=question_id))
    return render_template("post-answer.html", q_id=question_id)


@app.route('/add_question', methods=['GET','POST'])
def route_add_question():
    if request.method == 'POST':
        question_id = dl.add_question(request.form.get('title'), request.form.get('details'))
        return redirect(url_for('display_question', question_id=question_id))
    else:
        return render_template('add-question.html')


@app.route('/vote_up/<question_id>')
def vote_up(question_id):
    dl.vote_counter(question_id, 'up')
    return redirect('/questions/' + question_id)


@app.route('/vote_down/<question_id>')
def vote_down(question_id):
    dl.vote_counter(question_id, 'down')
    return redirect('/questions/' + question_id)


@app.route('/question/<question_id>/delete', methods=['GET', 'POST'])
def delete_question(question_id, ):
    dl.delete_all_comments(question_id=question_id)
    dl.delete_question(question_id)
    dl.delete_question_answers(question_id)
    return redirect('/')


@app.route('/answer/<question_id>/<answer_id>/delete', methods=['GET', 'POST'])
def delete_answer(answer_id, question_id):
    dl.delete_all_comments(answer_id=answer_id)
    dl.delete_answer(answer_id)
    return redirect("/questions/"+str(question_id))


@app.route('/answer/<question_id>/<answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(answer_id, question_id):
    question = dl.get_data('question', dl.question_fieldnames, 'id', 'asc', 'id', question_id)
    answer = dl.get_data('answer', dl.answer_fieldnames, 'id', 'asc', 'id', answer_id)
    if request.method == "GET":
        return render_template("edit-answer.html", answer=answer, question=question)
    else:
        dl.edit_answer(answer_id, request.form.get("edit_a"))
        return redirect("/questions/"+str(question_id))


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def edit(question_id):
    question = dl.get_data('question', dl.question_fieldnames, 'id', 'asc', 'id', question_id)
    if request.method == "GET":
        return render_template("edit.html", question=question)
    else:
        dl.edit_question(question_id, request.form.get("edit_q"))
        return redirect("/questions/"+str(question_id))


@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def add_comment_question(question_id):
    if request.method == 'POST':
        message = request.form.get('message')
        dl.add_comment(message, question_id=question_id)
        return redirect(url_for('display_question', question_id=question_id))
    else:
        specific_url = url_for('add_comment_question', question_id=question_id)
        return render_template('new-comment.html', question_id=question_id, specific_url=specific_url)


@app.route('/answer/<answer_id>/new-comment', methods=['GET', 'POST'])
def add_comment_answer(answer_id):
    if request.method == 'POST':
        message = request.form.get('message')
        question_id = dl.get_question_id(answer_id)
        dl.add_comment(message, question_id=question_id, answer_id=answer_id)
        return redirect(url_for('display_question', question_id=question_id))
    else:
        specific_url = url_for('add_comment_answer', answer_id=answer_id)
        return render_template('new-comment.html', answer_id=answer_id, specific_url=specific_url)


@app.route('/comments/<comment_id>/delete', methods=['POST', 'GET'])
def delete_comment(comment_id):
    question_id = dl.get_question_id(comment_id=comment_id)
    if request.method == 'GET':
        return render_template('confirm.html', comment_id=comment_id, question_id=question_id)
    else:
        dl.delete_one_comment(comment_id)
        return redirect(url_for('display_question', question_id=question_id))


@app.route('/comments/<comment_id>/edit', methods=['GET', 'POST'])
def edit_comment(comment_id):
    if request.method == 'GET':
        comment = dl.get_data('comment', dl.comment_fieldnames, 'id', 'asc', 'id', comment_id)
        return render_template('edit-comment.html', comment=comment)
    else:
        message = request.form.get('message')
        dl.edit_comment(comment_id=comment_id, message=message)
        question_id = dl.get_question_id(comment_id=comment_id)
        return redirect(url_for('display_question', question_id=question_id))


@app.route('/search')
def search_question():
    quote = request.args.get('q')
    question_ids = dl.convert_search_result(dl.search_questions(quote))
    answer_ids = dl.convert_search_result(dl.search_answers(quote))
    ids = question_ids | answer_ids
    questions = dl.question_search_result(list(ids))
    return render_template('list.html', questions=questions)


if __name__ == "__main__":
    app.run()
