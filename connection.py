import csv

columntitles = ['id', 'submission_time','view_number','vote_number','title','message','image']
columntitles_answer = ['id','submission_time','vote_number','question_id','message','image']

def read_data(filename):
    list_of_data = []
    with open(filename, 'r') as File:
        for row in csv.DictReader(File):
            list_of_data.append(dict(row))
    return list_of_data


def append_to_data(filename, data):
    with open(filename, 'a') as File:
        writer = csv.DictWriter(File, fieldnames=columntitles_answer)
        writer.writerow(data)
