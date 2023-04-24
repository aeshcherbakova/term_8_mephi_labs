import csv
import numpy as np
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

    # смотрим распределение длин межпакетных интервалов
    distributed_intervals = []
    counts = []
    intervals_amounts = 40
    step = max(intervals) / intervals_amounts
    # будем также смотреть среднюю длину межпакетного интервала
    average_interval = np.mean(intervals)
    index_of_average = 0

    print("Всего пакетов: " + str(len(intervals)))
    print("Максимальный временной интервал: " + str(max(intervals)))
    print("Средняя длина межпакетного интервала: " + str(average_interval))

    count = 0
    for i in range(intervals_amounts):
        # сами интервалы
        distributed_intervals.append(count)
        # инициализируем нулями массив распределений
        counts.append(0)
        # запоминаем индекс интервала, наиболее похожего на средний
        if count + step > average_interval and count <= average_interval:
            index_of_average = i
        count += step


    # заполняем массив распределения
    for i in range(len(intervals)):
        for j in range(len(distributed_intervals) - 1):
            # добавляем счетчик интервалу, который попал в текущий
            if distributed_intervals[j] < intervals[i] and intervals[i] < distributed_intervals[j + 1]:
                counts[j] += 1
                break

    print("Максимум пакетов со схожей длиной межпакетного интервала: " + str(max(counts)))
    print("Пакетов со средней длиной межпакетного интервала: " + str(counts[index_of_average]))
    print("Вероятность присутствия скрытого канала: " + str(int((1 - counts[index_of_average]/max(counts)) * 100)) + "%")

    fig, ax = plt.subplots()
    plt.xlabel("Длина межпакетного интервала", fontsize=16)
    plt.ylabel("Количество отправленных пакетов", fontsize=16)
    ax.bar(distributed_intervals, counts, width=0.05, edgecolor='black')
    plt.show()
