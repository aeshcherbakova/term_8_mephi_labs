import math
import matplotlib.pyplot as plt


def bandwidth(n):
    hy = 0
    for i in range(1, n + 1):
        hy += ((1 / n) * math.log2(1 / n))
    t = 0.5 * (n + 1)
    return -hy / t


def bandwidth_with_errors(n):
    t = (n + 1) / 2
    h = 0
    for j in range(1, n + 1):
        h_y_x = 0
        h_ex = 0
        for i in range(1, n + 1):
            h_ex = 0
            if j == i:
                h_ex += 0.6 * math.log2(0.6) * (-1)
            elif j == (i - 1) or j == (i + 1):
                h_ex += 0.2 * math.log2(0.2) * (-1)
            else:
                h_ex += (1/j) * math.log2(1/j) * (-1)
            h_y_x = (-1) * (1/i) * h_ex
        h += ((1 / n) * math.log2(1 / n)) * (-1) - h_y_x
    banw = h / t
    return banw


def bandwidth_with_probability(n):
    t = (n + 1) / 2
    h = 0
    for n_tmp in range(1, n + 1):
        h += ((1 / 2 ** n_tmp) * math.log2(1 / 2 ** n_tmp)) * (-1)
    banw = h / t
    return banw


if __name__ == "__main__":
    bw = 0
    n_final = 0
    bw_array = []
    n_array = []

    for n in range(1, 30):
        bw_tmp = bandwidth_with_errors(n)
        if bw_tmp > bw:
            bw = bw_tmp
            n_final = n
        bw_array.append(bw_tmp)
        n_array.append(n)

    print("Максимальная пропускная способность = ", bw)
    print("Число пакетов = ", n_final)

    plt.suptitle('График зависимости пропускной способности скрытого канала от числа пакетов')
    plt.xlabel('N - Число пакетов')
    plt.ylabel('Пропускная способность')
    plt.xticks(n_array)
    plt.plot(n_array, bw_array)
    plt.scatter(n_final, bw, color='red', marker='o')
    plt.show()



