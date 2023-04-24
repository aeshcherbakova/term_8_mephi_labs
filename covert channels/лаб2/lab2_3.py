import csv
import matplotlib.pyplot as plt


def read_file(file_name):
    result = []
    with open(file_name, encoding='utf-8') as r_file:
        dump = csv.reader(r_file, delimiter=",")
        count = 0
        for row in dump:
            if count > 99:
                result.append(row[1])
            count += 1
    return result


if __name__ == "__main__":
    # достаем метки времени из дампа
    timestamps = read_file('dump_7.csv')

    # высчитываем интервалы
    intervals = [float(timestamps[i + 1]) - float(timestamps[i]) for i in range(len(timestamps) - 1)]

    covert_message = ''
    for i in range(len(intervals)):
        if intervals[i] < 1.1:
            covert_message += '0'
        else:
            covert_message += '1'

    string = ''
    for i in range(0, len(covert_message), 8):
        string += chr(int(covert_message[i:i + 8], 2))

    print(string)
