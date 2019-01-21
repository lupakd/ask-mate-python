def read_data(data):
    with open(data, 'r') as File:
        return File


def write_data(data):
    with open(data, "w") as File:
        return File


def append_to_data():
    with open(data, 'a+') as File:
        return File
