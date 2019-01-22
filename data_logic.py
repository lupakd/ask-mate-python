import connection


def get_all_questions():
    return connection.read_data('sample_data/question.csv')


def get_all_answers():
    return connection.read_data('sample_data/answer.csv')

def display_question():
    answer = get_all_answers()
    question = get_all_questions()
    return answer, question
