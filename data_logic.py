import connection
from datetime import datetime

question_fieldnames = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
answer_fieldnames = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def get_all_questions():
    return connection.read_data('sample_data/question.csv')


def get_all_answers():
    return connection.read_data('sample_data/answer.csv')


def add_new_answer(answer, question_id):
    new_dict = {
        'id': new_id(),
        'submission_time': get_date_time(),
        'vote_number': 0,
        'question_id': question_id,
        'message': answer,
        'image': 0
    }
    connection.append_to_data('sample_data/answer.csv', new_dict)


def display_question():
    answer = get_all_answers()
    question = get_all_questions()
    return answer, question


def new_question(new_data):
    connection.append_to_data('sample_data/question.csv', new_data, question_fieldnames)


def get_date_time():
    return str(time.time())


def add_question(title, details):
    all_questions = get_all_questions()
    question_to_add = {
        question_fieldnames[0]: new_id(),
        question_fieldnames[1]: get_date_time(),
        question_fieldnames[2]: 0,
        question_fieldnames[3]: 0,
        question_fieldnames[4]: title,
        question_fieldnames[5]: details,
        question_fieldnames[6]: 'image'
    }
    return question_to_add


def add_view(question_id):
    questions = get_all_questions()
    for question in questions:
        if question['id'] == question_id:
            question['view_number'] = int(question['view_number']) + 1
    connection.update_data('sample_data/question.csv', questions, question_fieldnames)


def vote_counter(question_id, direction):
    questions = get_all_questions()
    for question in questions:
        if question['id'] == question_id:
            question['view_number'] = int(question['view_number']) - 1
            if direction == 'up':
                question['vote_number'] = int(question['vote_number']) + 1
            else:
                question['vote_number'] = int(question['vote_number']) - 1
    connection.update_data('sample_data/question.csv', questions, question_fieldnames)


def edit_question(question_id, newdata):
    questions = get_all_questions()
    for question in questions:
        if question["id"] == question_id:
            question["message"] = newdata + str("\n"+"{{Edited}}")
    connection.update_data("sample_data/question.csv",questions,question_fieldnames)


def delete_q(question_id):
    questions = get_all_questions()
    for question in questions:
        if question['id'] == question_id:
            questions.remove(question)
    connection.update_data('sample_data/question.csv', questions, question_fieldnames)


def delete_a(question_id):
    answers = get_all_answers()
    new_answers = []
    for answer in answers:
        if answer['question_id'] != question_id:
            new_answers.append(answer)
    connection.update_data('sample_data/answer.csv', new_answers, answer_fieldnames)