import connection
import utility
from psycopg2 import sql


@connection.connection_handler
def question(cursor, title, message, user_id):
    data = {
        'submission_time': utility.get_date_time(),
        'view_number': 0,
        'vote_number': 0,
        'title': title,
        'message': message,
        'image': None
        'user_id': user_id
    }
    cursor.execute(
        sql.SQL("""
                INSERT INTO question (submission_time, view_number, vote_number, title, message, image, user_id)
                VALUES (%(submission_time)s, %(view_number)s, %(vote_number)s, %(title)s, %(message)s, %(image)s,
                %(user_id)s); 
                
                SELECT MAX(id) FROM question;
        """), data
    )
    question_id = cursor.fetchone()
    return question_id['max']

@connection.connection_handler
def answer(cursor, question_id, message):
    data = {
        'submission_time': utility.get_date_time(),
        'vote_number': 0,
        'question_id': question_id,
        'message': message,
        'image': None
    }
    cursor.execute(
        sql.SQL("""
               INSERT INTO answer (submission_time, vote_number, question_id, message, image)
               VALUES (%(submission_time)s, %(vote_number)s, %(question_id)s, %(message)s, %(image)s); 
        """), data
    )

@connection.connection_handler
def comment(cursor, message, question_id, answer_id='0'):
    data = {
        'question_id': question_id,
        'answer_id': answer_id,
        'message': message,
        'submission_time': utility.get_date_time(),
        'edited_count': 0
    }
    cursor.execute(
        sql.SQL("""
                INSERT INTO comment (question_id, answer_id, message, submission_time, edited_count)
                VALUES (%(question_id)s, %(answer_id)s, %(message)s, %(submission_time)s, %(edited_count)s) 
        """), data
    )