import csv

columntitles = ['id','submission_time','view_number','vote_number','title','message','image']


def read_data(filename):
    list_of_data = []
    with open(filename, 'r') as File:
        for row in csv.DictReader(File):
            list_of_data.append(dict(row))
        return list_of_data

#
# def append_to_data(filename):
#     with open(filename, 'a+') as File:
#         writer = csv.DictWriter(File, columntitles=columntitles)
#         writer.writerow()
#         pass
