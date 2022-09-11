
"""
W ramach ćwiczenia w języku Python zaimplementowany zostanie algorytm aproksymowanego dopasowania ciągu.

Implementacja aproksymowanego dopasowania ciągu znakowego (approximate string matching) z wykorzystaniem PD

Idea: wyznaczanie dopasowań niedokładnych polega na określeniu funkcji kosztu, która określi jak bardzo dwa ciągi różnią się od siebie 
(w pewnym sensie miara odległości). Miara ta powinna uwzględniać liczbę zmian jakie trzeba wykonać, aby z ciągu A uzyskać ciąg B.
"""

import numpy as np
import time

def string_compare(P, T, i, j):
    if i == 0:
        return j - 1
    if j == 0:
        return i - 1
    change = string_compare(P, T, i - 1, j - 1) + int(P[i] != T[j])
    insert = string_compare(P, T, i, j - 1) + 1
    remove = string_compare(P, T, i - 1, j) + 1
    return min(change, insert, remove)

def PD(P, T):
    D = np.zeros([len(P), len(T)])
    D[0, :] = np.arange(0, len(T))
    D[:, 0] = np.arange(0, len(P))

    parent = [['X' for _ in range(len(T))] for _ in range(len(P))]
    parent[0][1:] = ['I' for _ in range(1, len(T))]
    for i in range(1, len(P)):
        parent[i][0] = 'D'

    for i in range(1, len(P)):
        for j in range(1, len(T)):
            change = D[i - 1, j - 1] + int(P[i] != T[j])
            insert = D[i, j - 1] + 1
            remove = D[i - 1, j] + 1
            D[i, j] = min(change, insert, remove)
            operation = np.argmin([change, insert, remove])
            if operation == 0:
                if P[i] == T[j]:
                    parent[i][j] = 'M'
                else:
                    parent[i][j] = 'S'
            elif operation == 1:
                parent[i][j] = 'I'
            else:
                parent[i][j] = 'D'
    return int(D[-1][-1]), parent

def recreate_path(parent):
    i = len(parent) - 1
    j = len(parent[0]) - 1
    result = []
    while parent[i][j] != 'X' and i >= 0 and j >= 0:
        oper = parent[i][j]
        if parent[i][j] == 'M' or parent[i][j] == 'S':
            i -= 1
            j -= 1
        elif parent[i][j] == 'D':
            i -= 1
        else:
            j -= 1
        result.append(oper)
    result.reverse()
    return ''.join(result)

def fitting(P, T):
    D = np.zeros([len(P), len(T)])
    D[:, 0] = np.arange(0, len(P))

    parent = [['X' for _ in range(len(T))] for _ in range(len(P))]
    for i in range(1, len(P)):
        parent[i][0] = 'D'

    for i in range(1, len(P)):
        for j in range(1, len(T)):
            change = D[i - 1, j - 1] + int(P[i] != T[j])
            insert = D[i, j - 1] + 1
            remove = D[i - 1, j] + 1
            D[i, j] = min(change, insert, remove)

    i = len(P) - 1
    j = np.argmin(D[i, :])
    return j

def longest_seq(P, T):
    D = np.zeros([len(P), len(T)])
    D[0, :] = np.arange(0, len(T))
    D[:, 0] = np.arange(0, len(P))

    parent = [['X' for _ in range(len(T))] for _ in range(len(P))]
    parent[0][1:] = ['I' for _ in range(1, len(T))]
    for i in range(1, len(P)):
        parent[i][0] = 'D'

    for i in range(1, len(P)):
        for j in range(1, len(T)):
            change = D[i - 1, j - 1] + int(P[i] != T[j]) * 1000000
            insert = D[i, j - 1] + 1
            remove = D[i - 1, j] + 1
            D[i, j] = min(change, insert, remove)
            operation = np.argmin([change, insert, remove])
            if operation == 0:
                if P[i] == T[j]:
                    parent[i][j] = 'M'
                else:
                    parent[i][j] = 'S'
            elif operation == 1:
                parent[i][j] = 'I'
            else:
                parent[i][j] = 'D'
    result = ''
    path = recreate_path(parent)
    j = 0
    for i in range(len(path)):
        if path[i] == 'M':
            result += T[i - j + 1]
        elif path[i] == 'D':
            j += 1
    return result

def longest_seq_mono(T):
    P = ' '
    p = []
    for dig in T[1:]:
        p.append(int(dig))
    p.sort()
    for dig in p:
        P += str(dig)
    return longest_seq(P, T)


def main():
    P = ' kot'
    T = ' pies'

    t_start = time.perf_counter()
    rek = string_compare(P, T, len(P) - 1, len(T) - 1)
    t_stop = time.perf_counter()
    # print("Czas obliczen metody rekurencyjnej: {}".format(t_stop - t_start))
    print(rek)

    P = ' biały autobus'
    T = ' czarny autokar'

    t_start = time.perf_counter()
    PD_, _ = PD(P, T)
    t_stop = time.perf_counter()
    # print("Czas obliczen metody dynamicznej: {}".format(t_stop - t_start))
    print(PD_)

    P = ' thou shalt not'
    T = ' you should not'

    _, parent = PD(P, T)
    t_start = time.perf_counter()
    path = recreate_path(parent)
    t_stop = time.perf_counter()
    # print("Czas obliczen metody odtwarzania ścieżki: {}".format(t_stop - t_start))
    print(path)

    P = ' ban'
    T = ' mokeyssbanana'

    t_start = time.perf_counter()
    idx = fitting(P, T)
    t_stop = time.perf_counter()
    # print("Czas obliczen metody dopasowywania podciągów: {}".format(t_stop - t_start))
    idx -= len(P) - 2
    print(idx)

    # P = ' bin'
    #
    # t_start = time.perf_counter()
    # idx2 = fitting(P, T)
    # t_stop = time.perf_counter()
    # print("Czas obliczen metody dopasowywania podciągów: {}".format(t_stop - t_start))
    # idx2 -= len(P) - 2
    # print(idx2)

    P = ' democrat'
    T = ' republican'

    t_start = time.perf_counter()
    seq = longest_seq(P, T)
    t_stop = time.perf_counter()
    # print("Czas obliczen metody najdłuższej sekwencji: {}".format(t_stop - t_start))
    print(seq)

    T = ' 243517698'

    t_start = time.perf_counter()
    seq2 = longest_seq_mono(T)
    t_stop = time.perf_counter()
    # print("Czas obliczen metody najdłuższej sekwencji monotonicznej: {}".format(t_stop - t_start))
    print(seq2)


main()
