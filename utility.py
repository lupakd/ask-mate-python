import datetime


question_fieldnames = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
answer_fieldnames = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
comment_fieldnames = ['id', 'question_id', 'answer_id', 'message', 'submission_time', 'edited_count']


def format_fieldnames(fieldnames):
    formatted = [item.capitalize().replace('_', ' ') for item in fieldnames]
    return formatted


def get_time():
    return datetime.datetime.now()


def build_entry(fieldnames, data):
    data.update({'submission_time': get_time()})
    entry = {key: 0 for key in fieldnames}
    entry.update(data)
    return entry

