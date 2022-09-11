
"""
Zaimplementuj algorytm Rabina-Karpa do wyszukiwania wielu wzorców z wykorzystaniem filtru Blooma. Przyjmij P = 0.001, n = 20, b i k oblicz na podstawie 
zamieszczonych powyżej wzorów. Dla uproszczenia przyjmij, że wszystkie wzorce mają tę samą długość N (dla chętnych - wyszukiwanie wzorców o różnej długości). 
Jeśli wzorzec nie został odrzucony przez filtr - sprawdź, czy ciągi faktycznie się zgadzają. 
Algorytm Rabina-Karpa w tej wersji pozwala bardzo szybko odrzucić miejsca, gdzie na pewno nie ma szukanych ciągów. Wypisz, ile razy pojawiły się dane wzorce. 
Wypisz także detekcje fałszywie pozytywne oraz ich liczbę.

Jeśli wspomnianych przypadków jest bardzo dużo, możesz zwiększyć rozmiar tablicy b (np. o 50%). Innym rozwiązaniem jest zmiana funkcji haszujących 
(np. poprzez wybór większych liczb pierwszych).

Zastosuj tzw. rolling hash do liczenia kolejnych wartości skrótów. Możesz się posłużyć wzorem z pierwszego ćwiczenia lub zamiast korzystania ze zmiennej h, 
liczyć d**(N-1) % q (przypomnienie: N - długość wzorca, q - liczba pierwsza, d - podstawa systemu). Wpisując do tablicy filtru Blooma, pamiętaj o obliczeniu 
odpowiedniego indeksu.

Pseudokod (źródło: Wikipedia):
function RabinKarpSet(string S[1..M], set of string subs, N):
    set hsubs := emptySet #inicjalizacja filtru Blooma

    foreach sub in subs #dla każdego wzorca

        insert hash(sub[1..N]) into hsubs #wyznacz wartości hash i wstaw do tablicy

    hs := hash(S[1..N]) #hash początkowych N elementów z S

    for m from 1 to M-N+1 #okno przesuwne

        if hs ∈ hsubs and S[m..m+N-1] ∈ subs #jeśli hash się zgadza i ciąg jest ten sam

            return m #zwróć indeks

        hs := hash(S[m+1..m+N]) #hash elementów przesuniętych o 1

    return not found

Do weryfikacji algorytmu możesz wykorzystać najpierw własny, prosty tekst, a później plik lotr.txt jak w pierwszym ćwiczeniu. Możesz wyszukiwać elementy 
własne lub z przykładowego zbioru: 
['gandalf', 'looking', 'blocked', 'comment', 'pouring', 'finally', 'hundred', 'hobbits', 'however', 'popular', 'nothing', 'enjoyed', 'stuffed', 'relaxed', 
'himself', 'present', 'deliver', 'welcome', 'baggins', 'further'].

Sprawdź czas działania dla wyszukiwania jednego wzorca oraz dla n wzorców - czy czas przeszukiwania wzrósł n-krotnie, czy nie? W ramach eksperymentów możesz 
sprawdzić wpływ różnych parametrów na działanie metody.
"""

import numpy as np
import time

def hash_1(sub, N):
    d = 256
    q = 101
    hw = 0
    for i in range(N):
        hw = (hw * d + ord(sub[i])) % q
    return hw

def hash_2(sub, N):
    d = 256
    q = 107
    hw = 0
    for i in range(N):
        hw = (hw * d + ord(sub[i])) % q
    return hw

def hash_sub(sub, k, b, N):
    idxs = []
    for i in range(k):
        idxs.append((hash_1(sub, N) + i * hash_2(sub, N)) % b)
    return idxs

def Bloom(S, subs):
    M, n = len(S), len(subs)
    N = len(subs[0])
    P = 0.001
    b = int((-n * np.log(P)) / (np.log(2) ** 2))
    k = int(b / n * np.log(2))
    result = []

    hsubs = [0] * b

    for sub in subs:
        idxs = hash_sub(sub, k, b, N)
        for idx in idxs:
            hsubs[idx] = 1

    hS = hash_sub(S[: N], k, b, N)
    for m in range(M - N + 1):
        zero = False
        for idx in hS:
            if not hsubs[idx]:
                zero = True
        if not zero and S[m: m + N] in subs:
            result.append(m)
        if m + N < M:
            hS = hash_sub(S[m + 1: m + N + 1], k, b, N)
    return result

def num_of_occurences(S, idxs, subs):
    result = {}
    for sub in subs:
        result[sub] = 0
    N = len(subs[0])
    for idx in idxs:
        for sub in subs:
            if sub == S[idx: idx + N]:
                result[sub] += 1
    return result

def main():
    with open("lotr.txt", encoding='utf-8') as f:
        text = f.readlines()

    S = ' '.join(text).lower()
    subs = ['gandalf', 'looking', 'blocked', 'comment', 'pouring', 'finally', 'hundred', 'hobbits', 'however',
            'popular', 'nothing', 'enjoyed', 'stuffed', 'relaxed', 'himself', 'present', 'deliver', 'welcome',
            'baggins', 'further']

    t_start = time.perf_counter()
    idxs = Bloom(S, [subs[0]])
    t_stop = time.perf_counter()
    set_1_sub = num_of_occurences(S, idxs, [subs[0]])
    print("Czas obliczeń dla jednego wzorca: {}".format(t_stop - t_start))
    print(set_1_sub)

    t_start = time.perf_counter()
    idxs = Bloom(S, subs)
    t_stop = time.perf_counter()
    set_n_subs = num_of_occurences(S, idxs, subs)
    print("Czas obliczeń dla n wzorców: {}".format(t_stop - t_start))
    print(set_n_subs)


main()
