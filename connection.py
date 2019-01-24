import csv

def read_data(filename):
    list_of_data = []
    with open(filename, 'r') as File:
        for row in csv.DictReader(File):
            list_of_data.append(dict(row))
        return list_of_data


def append_to_data(filename, data, fieldnames):
    with open(filename, 'a') as File:
        writer = csv.DictWriter(File, fieldnames=fieldnames)
        writer.writerow(data)


def update_data(filename, data, fieldnames):
    with open(filename, 'wt') as File:
        writer = csv.DictWriter(File, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
