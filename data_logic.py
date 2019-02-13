import connection
import utility
from psycopg2 import sql

question_fieldnames = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
answer_fieldnames = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
comment_fieldnames = ['id', 'question_id', 'answer_id', 'message', 'submission_time', 'edited_count']


@connection.connection_handler
def get_all_rows(cursor, table_name, order_key, order_type, limit):
    cursor.execute(sql.SQL('''
                    SELECT * FROM {table}
                    ORDER BY {key} {type}
                    LIMIT {amount};
''').format(table=sql.Identifier(table_name),
            key=sql.Identifier(order_key),
            type=sql.SQL(order_type),
            amount=sql.Literal(limit)
            )   )
    return cursor.fetchall()


@connection.connection_handler
def add_row(cursor, table_name, fieldnames, row_to_add):
    pass

@connection.connection_handler
def get_data(cursor, table_name, column_names, order_key,
             order_type='asc', condition_key='id', condition_value=None, condition_op='=', limit=None):
    cond_op = sql.SQL(condition_op)
    if condition_value is None:
        cond_value = sql.SQL('NULL')
    else:
        cond_value = sql.Literal(condition_value)
    condition = sql.SQL('WHERE {key} {operator} {value}').format(key=sql.Identifier(condition_key),
                                                                 value=cond_value,
                                                                 operator=cond_op)
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
    ))
    data = cursor.fetchall()
    return data


@connection.connection_handler
def add_new_entry(cursor, fieldnames, data, table):
    fieldnames = fieldnames[1:]
    entry = utility.build_entry(fieldnames, data)
    sql_string = sql.SQL('''INSERT INTO {table} ({columns})
                            VALUES ({values});''').format(table=sql.Identifier(table),
                                                          columns=sql.SQL(', ').join(map(sql.Identifier, fieldnames)),
                                                          values=sql.SQL(', ').join(map(sql.Placeholder, fieldnames)))
    cursor.execute(sql_string, entry)


@connection.connection_handler
def update_entry(cursor, table, column_update, new_value, value_type, condition_key, condition_value,
                 condition_operator):
    if value_type == 'variable':
        value = sql.Placeholder('new_value')
    elif value_type == 'expression':
        value = sql.SQL(new_value)
    expression = sql.SQL('{column} = {value}').format(column=sql.Identifier(column_update),
                                                      value=value)
    condition = sql.SQL('{column} {operator} {value}').format(column=sql.Identifier(condition_key),
                                                              operator=sql.SQL(condition_operator),
                                                              value=sql.Placeholder('condition_value'))
    sql_string = sql.SQL('''UPDATE {table}
                            SET {expression}
                            WHERE {condition};''').format(table=sql.Identifier(table),
                                                          expression=expression,
                                                          condition=condition)
    cursor.execute(sql_string, {'condition_value': condition_value, 'new_value': new_value})


@connection.connection_handler
def delete_entries(cursor, table, condition_key, condition_value, operator):
    sql_string = sql.SQL('''
                            DELETE FROM {table}
                            WHERE {cond_key} {operator} {value}    ''').format(
        table=sql.SQL(table),
        cond_key=sql.SQL(condition_key),
        operator=sql.SQL(operator),
        value=sql.Placeholder('cond_value')
    )
    cursor.execute(sql_string, {'cond_value': condition_value})


@connection.connection_handler
def search_quote(cursor, quote):
    cursor.execute('''
                    SELECT id FROM question
                    WHERE message ILIKE %(quote)s OR title ILIKE %(quote)s
                    UNION
                    SELECT question_id FROM answer
                    WHERE message ILIKE %(quote)s;''', {'quote': '%' + quote + '%'})
    result = cursor.fetchall()
    result = tuple([items['id'] for items in result])
    return result
