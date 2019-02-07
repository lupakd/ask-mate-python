import connection
import datetime

question_fieldnames = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
answer_fieldnames = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def get_date_time(): #nagozn kell
    return datetime.datetime.now()


@connection.connection_handler
def get_all_questions(cursor):
    cursor.execute('''
                    SELECT * FROM question
                    ORDER BY id asc;
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
def add_new_answer(cursor,answer, question_id):
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
                    'submission_time': get_date_time(),
                    'edited_count': 0
    }
    cursor.execute('''
                    INSERT INTO comment (question_id, answer_id, message, submission_time, edited_count)
                    VALUES (%(question_id)s, %(answer_id)s, %(message)s, %(submission_time)s, %(edited_count)s)        
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


@connection.connection_handler
def search_questions(cursor, quote):
    cursor.execute('''
                    SELECT id FROM question
                    WHERE message LIKE %(quote)s OR title LIKE %(quote)s;
    ''', {'quote': '%' + quote + '%'})
    question_ids = cursor.fetchall()
    return question_ids


@connection.connection_handler
def search_answers(cursor, quote):
    cursor.execute('''
                    SELECT question_id FROM answer
                    WHERE message LIKE %(quote)s;
    ''', {'quote': '%' + quote + '%'})
    answer_ids = cursor.fetchall()
    for line in answer_ids:
        line['id'] = line.pop('question_id')
    return answer_ids


def convert_search_result(ids):
    processed_ids = []
    for line in ids:
        processed_ids.append(line['id'])
    return set(processed_ids)


@connection.connection_handler
def question_search_result(cursor, ids):
    ids = tuple(ids)
    cursor.execute('''
                    SELECT * FROM question
                    WHERE id IN %(id_list)s; 
    ''', {'id_list': tuple(ids)})
    questions = cursor.fetchall()
    return questions


@connection.connection_handler
def get_single_question(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM question
                    WHERE id = %(question_id)s;
    """, {'question_id': question_id})
    question = cursor.fetchone()
    return question


@connection.connection_handler
def get_single_answer(cursor, answer_id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE id = %(a_id)s;
    """, {'a_id': answer_id})
    question = cursor.fetchone()
    return question


@connection.connection_handler
def get_latest_questions(cursor):
    cursor.execute("""
                    SELECT * FROM question
                    ORDER BY id desc LIMIT 5;
    """)
    questions = cursor.fetchall()
    return questions