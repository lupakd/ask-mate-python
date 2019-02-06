import connection
import time

question_fieldnames = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
answer_fieldnames = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def new_id(response):
    return int(response[-1]['id']) + 1

@connection.connection_handler
def get_all_questions(cursor):
    cursor.execute('''
                    SELECT * FROM question;
    ''')
    questions = cursor.fetchall()
    return questions


@connection.connection_handler
def get_all_answers(cursor):
    cursor.execute('''
                        SELECT * FROM answer;
        ''')
    answers = cursor.fetchall()
    return answers


@connection.connection_handler
def add_new_answer(cursor, answer, question_id):
    new_dict = {
        'id': new_id(get_all_answers()),
        'submission_time': get_date_time(),
        'vote_number': 0,
        'question_id': question_id,
        'message': answer,
        'image': 0
    }
    cursor.execute('''
                    INSERT INTO answer (submission_time, vote_number, question_id, message, image)
                    VALUES (%(submission_time)s, %(vote_number)s, %(question_id)s, %(message)s, %(image)s)
    ''', new_dict)


def get_date_time():
    return str(int(time.time()))


@connection.connection_handler
def add_question(cursor, title, details):
    question_to_add = {
        question_fieldnames[1]: get_date_time(),
        question_fieldnames[2]: 0,
        question_fieldnames[3]: 0,
        question_fieldnames[4]: title,
        question_fieldnames[5]: details,
        question_fieldnames[6]: 'image'
    }
    cursor.execute('''
                    INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
                    VALUES (%(submission_time)s, %(view_number)s, %(vote_number)s, %(title)s, %(message)s, %(image)s)
    ''', question_to_add)
    question = cursor.fetchall()
    return question


@connection.connection_handler
def add_view(cursor, question_id):
    cursor.execute('''
                    UPDATE question
                    SET view_number = view_number + 1
                    WHERE id = %(question_id)s;
    ''', {'question_id': question_id})


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


def delete_question(question_id):
    questions = get_all_questions()
    for question in questions:
        if question['id'] == question_id:
            questions.remove(question)
    connection.update_data('sample_data/question.csv', questions, question_fieldnames)


def delete_question_answers(question_id):
    answers = get_all_answers()
    new_answers = answers.copy()
    for answer in answers:
        if answer['question_id'] == question_id:
            new_answers.remove(answer)
    connection.update_data('sample_data/answer.csv', new_answers, answer_fieldnames)


def delete_answer(answer_id):
    answers = get_all_answers()
    new_answers = answers.copy()
    for answer in answers:
        if answer['id'] == answer_id:
            new_answers.remove(answer)
    connection.update_data('sample_data/answer.csv', new_answers, answer_fieldnames)
