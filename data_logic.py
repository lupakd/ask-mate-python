import connection
import datetime

question_fieldnames = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
answer_fieldnames = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def get_date_time(): #nagozn kell
    return datetime.datetime.now()


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
                    VALUES (%(submission_time)s, %(view_number)s, %(vote_number)s, %(title)s, %(message)s, %(image)s);
                    SELECT id FROM question
                    WHERE title = %(title)s;
    ''', question_to_add)
    question_id = cursor.fetchone()
    return question_id



@connection.connection_handler
def add_view(cursor, question_id):
    cursor.execute('''
                    UPDATE question
                    SET view_number = view_number + 1
                    WHERE id = %(question_id)s;
    ''', {'question_id': question_id})


@connection.connection_handler
def vote_counter(cursor, question_id, direction):
    if direction == 'up':
        cursor.execute('''
                        UPDATE question
                        SET vote_number = vote_number + 1, view_number = view_number - 1
                        WHERE id = %(question_id)s;
        ''', {'question_id': question_id})
    else:
        cursor.execute('''
                                UPDATE question
                                SET vote_number = vote_number - 1, view_number = view_number - 1
                                WHERE id = %(question_id)s;
                ''', {'question_id': question_id})


@connection.connection_handler
def edit_question(cursor, question_id, newdata):
    cursor.execute('''
                    UPDATE question
                    SET message = %(message)s     
                    WHERE id = %(question_id)s
    ''', {'question_id': question_id, 'message': newdata})


@connection.connection_handler
def delete_question(cursor, question_id):
    cursor.execute('''
                    DELETE FROM question
                    WHERE id = %(question_id)s;
    ''', {'question_id': question_id})


@connection.connection_handler
def delete_question_answers(cursor, question_id):
    cursor.execute('''
                    DELETE FROM answer
                    WHERE question_id = %(question_id)s;
    ''', {'question_id': question_id})


@connection.connection_handler
def delete_answer(cursor, answer_id):
    cursor.execute('''
                    DELETE FROM answer
                    WHERE id = %(answer_id)s;
    ''', {'answer_id': answer_id})
