import connection


def get_all_questions():
    return connection.read_data('/sample_data/questions.csv')
