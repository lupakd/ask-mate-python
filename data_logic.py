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
def vote_counter(cursor, question_id, direction, ):
    if direction =='up':
        cursor.execute("""
                        UPDATE question
                        SET vote_number = vote_number + 1, view_number = view_number - 1 
                        WHERE id = %(question_id)s;
                        """, {'question_id': question_id})
    else:
        cursor.execute("""
                       UPDATE question
                       SET vote_number = vote_number - 1, view_number = view_number - 1 
                       WHERE id = %(question_id)s;
                        """, {'question_id': question_id})


@connection.connection_handler
def edit_question(cursor, question_id, newdata):
    cursor.execute("""
                    UPDATE question
                    SET message = %(message)s
                    WHERE id = %(id)s;
                    """,{'message': newdata, 'id': question_id})


@connection.connection_handler
def edit_answer(cursor, answer_id, newdata):
    cursor.execute("""
                    UPDATE answer
                    SET message = %(message)s
                    WHERE id = %(answer_id)s;
                    """, {'message': newdata, 'answer_id': answer_id})


@connection.connection_handler
def delete_question(cursor, question_id):
    cursor.execute("""
                    DELETE FROM question
                    WHERE id = %(id)s
                    """, {'id': question_id})

@connection.connection_handler
def delete_question_answers(cursor, question_id):
    cursor.execute("""
                    DELETE FROM answer
                    WHERE question_id = %(question_id)s;
                    """, {'question_id': question_id})

@connection.connection_handler
def delete_answer(cursor, answer_id):
    cursor.execute('''
                    DELETE FROM answer
                    WHERE id = %(answer_id)s;
                    ''', {'answer_id': answer_id})


@connection.connection_handler
def delete_one_comment(cursor, comment_id):
    cursor.execute('''
                    DELETE FROM comment
                    WHERE  id = %(id)s;
                    ''', {'id': comment_id})


@connection.connection_handler
def delete_all_comments(cursor, answer_id=None, question_id=None):
    if answer_id is not None:
        cursor.execute('''
                        DELETE FROM comment
                        WHERE answer_id = %(answer_id)s;
                        ''', {'answer_id': answer_id})
    else:
        cursor.execute('''
                        DELETE FROM comment
                        WHERE question_id = %(question_id)s;
                        ''', {'question_id': question_id})


@connection.connection_handler
def get_all_comments(cursor):
    cursor.execute('''
                    SELECT * FROM comment;
                    ''')
    comments = cursor.fetchall()
    return comments


@connection.connection_handler
def get_one_comment(cursor, comment_id):
    cursor.execute('''
                    SELECT * FROM comment
                    WHERE id = %(comment_id)s;    
                ''', {'comment_id': comment_id}
                   )
    comment = cursor.fetchall()
    return comment


@connection.connection_handler
def add_comment(cursor,  message, question_id, answer_id=None):
    new_comment = {
                    'question_id': question_id,
                    'answer_id': answer_id,
                    'message': message,
                    'submission_time': get_date_time()
    }
    cursor.execute('''
                    INSERT INTO comment (question_id, answer_id, message, submission_time)
                    VALUES (%(question_id)s, %(answer_id)s, %(message)s, %(submission_time)s)        
                    ''', new_comment)


@connection.connection_handler
def get_question_id(cursor, answer_id=None, comment_id=None):
    if answer_id is not None:
        cursor.execute('''
                        SELECT question_id FROM answer
                        WHERE id = %(answer_id)s;
                    ''', {'answer_id': answer_id})
    else:
        cursor.execute('''
                                SELECT question_id FROM comment
                                WHERE id = %(comment_id)s;
                    ''', {'comment_id': comment_id})
    raw_id = cursor.fetchone()
    return raw_id['question_id']


@connection.connection_handler
def edit_comment(cursor, comment_id, message):
    cursor.execute('''
                    UPDATE comment
                    SET edited_count = edited_count + 1, message = %(message)s
                    WHERE id = %(comment_id)s;
    ''', {'comment_id': comment_id,
          'message': message}
                   )
