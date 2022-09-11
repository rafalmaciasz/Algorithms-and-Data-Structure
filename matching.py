
"""
Implementacje różnych metod wyszukiwania wzorca.

"""

import time

def hash(word, N):
    d = 256
    q = 101
    hw = 0
    for i in range(N):
        hw = (hw * d + ord(word[i])) % q
    return hw

def basic_match(S, W):
    result = []
    m = 0
    l_s = len(S)
    counter = 0
    while m < l_s:
        counter += 1
        if S[m] == W[0]:
            i = 1
            l_w, x = len(W), 1
            while i < l_w:
                counter += 1
                if S[m + i] == W[i]:
                    x += 1
                    i += 1
                else:
                    break
            if x == l_w:
                result.append(m)
        m += 1
    return result, counter

def Rabin_Karp(S, W):
    M, N = len(S), len(W)
    counter = 0
    result = []
    hW = hash(W, N)
    for m in range(M - N + 1):
        hS = hash(S[m: m + N], N)
        counter += 1
        if hS == hW:
            if S[m: m + N] == W:
                result.append(m)
    return result, counter

def Rabin_Karp_rolling_hash(S, W):
    M, N = len(S), len(W)

    d = 256
    q = 101
    h = 1
    for i in range(N - 1):
        h = (h * d) % q

    counter = 0
    collision = 0
    result = []
    hW = hash(W, N)
    hS = hash(S[: N], N)
    for m in range(M - N + 1):
        counter += 1
        if hS == hW:
            if S[m: m + N] == W:
                result.append(m)
            else:
                collision += 1
        if m + N < M:
            hS = (d * (hS - ord(S[m]) * h) + ord(S[m + N])) % q
    return result, counter, collision

def kmp_table(W):
    T = []
    pos, cnd = 1, 0
    T.append(-1)
    while pos < len(W):
        if W[pos] == W[cnd]:
            # x = T[cnd]
            T.append(T[cnd])
        else:
            T.append(cnd)
            while cnd >= 0 and W[pos] != W[cnd]:
                cnd = T[cnd]
        pos += 1
        cnd += 1
    T.append(cnd)
    return T

def Knuth_Morris_Pratt(S, W):
    result = []
    num_of_pos = 0
    m, i = 0, 0
    T = kmp_table(W)
    counter = 0
    while m < len(S):
        counter += 1
        if W[i] == S[m]:
            m += 1
            i += 1
            if i == len(W):
                result.append(m - i)
                num_of_pos += 1
                i = T[i]
        else:
            i = T[i]
            if i < 0:
                m += 1
                i += 1
    return result, counter

def main():
    with open("lotr.txt", encoding='utf-8') as f:
        text = f.readlines()

    S = ' '.join(text).lower()
    W = 'time.'
    t_start = time.perf_counter()
    m, counter = basic_match(S, W)
    t_stop = time.perf_counter()
    print("Czas obliczeń:", "{:.7f}".format(t_stop - t_start))
    print(len(m), counter)

    t_start = time.perf_counter()
    m2, counter2 = Rabin_Karp(S, W)
    t_stop = time.perf_counter()
    print("Czas obliczeń dla Rabin-Karp:", "{:.7f}".format(t_stop - t_start))
    print(len(m2), counter2)

    t_start = time.perf_counter()
    m3, counter3, collision3 = Rabin_Karp_rolling_hash(S, W)
    t_stop = time.perf_counter()
    print("Czas obliczeń dla Rabin-Karp z rolling hash:", "{:.7f}".format(t_stop - t_start))
    print(len(m3), counter3, collision3)

    t_start = time.perf_counter()
    m4, counter4 = Knuth_Morris_Pratt(S, W)
    t_stop = time.perf_counter()
    print("Czas obliczeń dla Knuth-Morris-Pratt:", "{:.7f}".format(t_stop - t_start))
    print(len(m4), counter4)


main()
