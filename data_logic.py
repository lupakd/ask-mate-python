import connection


def new_id():
    return 24


def get_time_now():
    return 23423432


def get_all_questions():
    return connection.read_data('sample_data/question.csv')


def get_all_answers():
    return connection.read_data('sample_data/answer.csv')


def add_new_answer(answer, question_id):
    new_dict = {
        'id': new_id(),
        'submission_time': get_time_now(),
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
