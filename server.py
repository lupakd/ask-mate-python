from flask import Flask, render_template, request, redirect, url_for
import data_logic as dl
import utility as util

app = Flask(__name__)


@app.route('/')
def route_main():
    latest = dl.get_data('question', dl.question_fieldnames, 'submission_time', 'ASC', condition_op='IS NOT', limit='5')
    return render_template('list.html', questions=latest)


@app.route('/list')
def route_list():
    questions = dl.get_data('question', dl.question_fieldnames, 'submission_time', 'asc', condition_op='IS NOT')
    return render_template('list.html', questions=questions)


@app.route('/questions/<question_id>')
def display_question(question_id):
    dl.update_entry('question', 'view_number', 'view_number + 1', 'expression', 'id', question_id, '=')
    question = dl.get_data('question', dl.question_fieldnames, 'id', 'asc', 'id', question_id)
    answers = dl.get_data('answer', dl.answer_fieldnames, 'submission_time', 'asc', 'question_id', question_id)
    comments = dl.get_data('comment', dl.comment_fieldnames, 'submission_time', 'asc', 'question_id', question_id)
    return render_template("questions.html",
                           question_id=question_id,
                           answers=answers,
                           question=question,
                           comments=comments,
                           question_header=util.format_fieldnames(dl.question_fieldnames),
                           answer_header=util.format_fieldnames(dl.answer_fieldnames),
                           comment_header=util.format_fieldnames(dl.comment_fieldnames)
                           )


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def route_add_answer(question_id):
    if request.method == 'POST':
        data = {'message': request.form.get('message'),
                'question_id': question_id}
        dl.add_new_entry(dl.answer_fieldnames, data, 'answer')
        return redirect(url_for('display_question', question_id=question_id))
    return render_template("post-answer.html", question_id=question_id)


@app.route('/add_question', methods=['GET','POST'])
def route_add_question():
    if request.method == 'POST':
        data = {'title': request.form.get('title'),
                'message': request.form.get('message')}
        dl.add_new_entry(dl.question_fieldnames, data, 'question')
        question_id = dl.get_data('question', ['id'], 'id', 'desc', limit=1)
        return redirect(url_for('display_question', question_id=question_id[0]['id']))
    else:
        return render_template('add-question.html')


@app.route('/vote_up/<question_id>')
def question_vote_up(question_id):
    dl.update_entry('question', 'vote_number', 'vote_number + 1', 'expression', 'id', question_id, '=')
    dl.update_entry('question', 'view_number', 'view_number - 1', 'expression', 'id', question_id, '=')
    return redirect(url_for('display_question', question_id=question_id))


@app.route('/vote_down/<question_id>')
def question_vote_down(question_id):
    dl.update_entry('question', 'vote_number', 'vote_number - 1', 'expression', 'id', question_id, '=')
    dl.update_entry('question', 'view_number', 'view_number - 1', 'expression', 'id', question_id, '=')
    return redirect(url_for('display_question', question_id=question_id))


@app.route('/question/<question_id>/delete', methods=['GET', 'POST'])
def route_delete_question(question_id):
    dl.delete_entries('comment', 'question_id', question_id, '=')
    dl.delete_entries('answer', 'question_id', question_id, '=')
    dl.delete_entries('question', 'id', question_id, '=')
    return redirect(url_for('route_list'))


@app.route('/answer/<question_id>/<answer_id>/delete', methods=['GET', 'POST'])
def delete_answer(answer_id, question_id):
    dl.delete_entries('comment', 'answer_id', answer_id, '=')
    dl.delete_entries('answer', 'id', answer_id, '=')
    return redirect(url_for('display_question', question_id=question_id))


@app.route('/answer/<question_id>/<answer_id>/edit', methods=['GET', 'POST'])
def route_edit_answer(answer_id, question_id):
    question = dl.get_data('question', dl.question_fieldnames, 'id', 'asc', 'id', question_id)
    answer = dl.get_data('answer', dl.answer_fieldnames, 'id', 'asc', 'id', answer_id)
    if request.method == "GET":
        return render_template("edit-answer.html", answer=answer, question=question)
    else:
        dl.update_entry('answer', 'message', request.form.get('message'), 'variable', 'id', answer_id, '=')
        return redirect(url_for('display_question', question_id=question_id))


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def route_edit_question(question_id):
    question = dl.get_data('question', dl.question_fieldnames, 'id', 'asc', 'id', question_id)
    if request.method == "GET":
        return render_template("edit-question.html", question=question)
    else:
        message = request.form.get('message')
        print(message)
        dl.update_entry('question', 'message', message, 'variable', 'id', question_id, '=')
        return redirect(url_for('display_question', question_id=question_id))


@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def add_comment_question(question_id):
    if request.method == 'POST':
        data = {'message': request.form.get('message'),
                'question_id': question_id,
                'answer_id': None}
        dl.add_new_entry(dl.comment_fieldnames, data, 'comment')
        return redirect(url_for('display_question', question_id=question_id))
    else:
        specific_url = url_for('add_comment_question', question_id=question_id)
        return render_template('new-comment.html', question_id=question_id, specific_url=specific_url)


@app.route('/answer/<answer_id>/new-comment', methods=['GET', 'POST'])
def add_comment_answer(answer_id):
    if request.method == 'POST':
        question_id = dl.get_data('answer', ['question_id'], 'id', 'asc', 'id', answer_id)
        data = {'message': request.form.get('message'),
                'answer_id': answer_id,
                'question_id':question_id[0]['question_id']}
        dl.add_new_entry(dl.comment_fieldnames, data, 'comment')
        return redirect(url_for('display_question', question_id=question_id[0]['question_id']))
    else:
        specific_url = url_for('add_comment_answer', answer_id=answer_id)
        return render_template('new-comment.html', answer_id=answer_id, specific_url=specific_url)


@app.route('/comments/<comment_id>/delete', methods=['POST', 'GET'])
def delete_comment(comment_id):
    question_id = dl.get_data('comment', ['question_id'], 'id', 'asc', 'id', comment_id)
    if request.method == 'GET':
        return render_template('confirm.html', comment_id=comment_id, question_id=question_id[0]['question_id'])
    else:
        dl.delete_entries('comment', 'id', comment_id, '=')
        return redirect(url_for('display_question', question_id=question_id[0]['question_id']))


@app.route('/comments/<comment_id>/edit', methods=['GET', 'POST'])
def edit_comment(comment_id):
    if request.method == 'GET':
        comment = dl.get_data('comment', dl.comment_fieldnames, 'id', 'asc', 'id', comment_id)
        return render_template('edit-comment.html', comment=comment)
    else:
        dl.update_entry('comment', 'message', request.form.get('message'), 'variable', 'id', comment_id, '=')
        dl.update_entry('comment', 'edited_count', 'edited_count + 1', 'expression', 'id', comment_id, '=')
        question_id = dl.get_data('comment', ['question_id'], 'id', 'asc', 'id', comment_id)
        return redirect(url_for('display_question', question_id=question_id[0]['question_id']))


@app.route('/search')
def search_question():
    quote = request.args.get('q')
    ids = dl.search_quote(quote)
    questions = dl.get_data('question', dl.question_fieldnames, 'submission_time', 'asc', 'id', ids, 'IN')
    return render_template('list.html', questions=questions)


if __name__ == "__main__":
    app.run()
