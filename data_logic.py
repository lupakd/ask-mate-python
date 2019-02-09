import connection
import utility
from psycopg2 import sql

question_fieldnames = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
answer_fieldnames = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
comment_fieldnames = ['id', 'question_id', 'answer_id', 'message', 'submission_time', 'edited_count']


@connection.connection_handler
def get_data(cursor, table_name, column_names, order_key,
             order_type='asc', condition_key=None, condition_value=None, limit=None):
    if condition_key is None:
        condition_key = 'id'
        condition_value = sql.SQL('NULL')
        operator = sql.SQL('IS NOT')
    else:
        condition_value = sql.Literal(condition_value)
        operator = sql.SQL('=')
    condition = sql.SQL('WHERE {key} {operator} {value}').format(
                                                    key=sql.Identifier(condition_key),
                                                    value=condition_value,
                                                    operator=operator)
    limit_count = sql.SQL('LIMIT {}').format(sql.Literal(limit))
    cursor.execute(sql.SQL("""SELECT {column} FROM {table}
                              {cond}
                              ORDER BY {order} {type} {limit};
                    """).format(
        column=sql.SQL(', ').join(map(sql.Identifier, column_names)),
        table=sql.Identifier(table_name),
        order=sql.Identifier(order_key),
        type=sql.SQL(order_type),
        cond=condition,
        limit=limit_count
    ), column_names)
    data = cursor.fetchall()
    return data


@connection.connection_handler
def add_new_entry(cursor, fieldnames, data, table):
    fieldnames = fieldnames[1:]
    entry = utility.build_entry(fieldnames, data)
    columns = sql.SQL(', ').join(map(sql.Identifier, fieldnames))
    values = sql.SQL(', ').join(map(sql.Placeholder, fieldnames))
    print(fieldnames)
    print(columns)
    print(values)
    sql_string = sql.SQL('''INSERT INTO {table} ({columns})
                            VALUES ({values});''').format(table=sql.Identifier(table),
                                                          columns=columns,
                                                          values=values)
    cursor.execute(sql_string, entry)


@connection.connection_handler
def update_entry(cursor, table, expression, condition):
    pass


@connection.connection_handler
def add_view(cursor, question_id):
    cursor.execute('''
                    UPDATE question
                    SET view_number = view_number + 1
                    WHERE id = %(question_id)s;
                    ''', {'question_id': question_id})


@connection.connection_handler
def vote_counter(cursor, question_id, direction, ):
    if direction == 'up':
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
                    """, {'message': newdata, 'id': question_id})


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


