import datetime


def get_time():
    return datetime.datetime.now()


def build_entry(fieldnames, data):
    data.update({'submission_time': get_time()})
    entry = {key: 0 for key in fieldnames}
    entry.update(data)
    return entry

