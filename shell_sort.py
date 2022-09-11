
"""
1. Sortowanie metodą Shella to w pewnym sensie uogólniona metoda sortowania przez wstawianie (ang. insertion sort). 
W wersji "zwykłej" elementy przesuwane są o 1 pozycję aż trafią na odpowiednie miejsce.

W metodzie Shella możliwe jest przesuwanie elementów położonych dalej od siebie, co zmniejsza liczbę operacji i zwiększa efektywność działania. 
Zamiast przesuwania elementów lepiej może się sprawdzić swapowanie. Zamiast sprawdzania i przesuwania o 1 element poruszamy się co h elementów. 
Taka operacja powinna być powtórzona h razy (czyli startujemy po kolei z pierwszych h elementów, rozpatrując za każdym razem co h-ty element). 
Po wykonaniu wszystkich h przebiegów wartość h jest zmniejszana i cały proces powtarzany, aż do momentu, gdy h osiągnie wartość 1 
(to będzie ostatnie powtórzenie).

Istotnym czynnikiem, świadczącym o efektywności metody Shella, jest dobór odpowiednich odstępów h. Niestety, znalezienie optymalnych wartości jest 
bardzo trudnym zadaniem. W pierwotnej propozycji shella h zaczynało od wartości N//2 i było zmniejszane również dwukrotnie - zacznij od tej implementacji.

Lepszym wyborem początkowej wartości h może być największa wartość (3k-1)/2, mniejsza od N/3, gdzie N to liczba elementów w zbiorze. 
Mniejsze odstępy h otrzymujemy poprzez całkowitoliczbowe dzielenie poprzedniej wartości h przez 3.

Wygeneruj 10000 losowych elementów (o wartościach od 0 do 99), którymi wypełnisz wejściową tablicę. Wykonaj sortowanie metodą Shella. 
Porównaj i wyświetl czas wykonania względem "zwykłego" insertion sort. Porównaj także ten czas  z czasem wykonania sortowania kopcowego.

==============================

2. W algorytmie sortowania szybkiego wybierany jest element, względem którego dokonuje się podziału tablicy na dwie – wierającą elementy mniejsze 
oraz większe od wybranego. Tę procedurę powtarza się na obu częściach tablicy w sposób rekurencyjny, aż do otrzymania pojedynczych elementów w powstałych 
w ten sposób tablicach (które rzecz jasna są posortowane). Taki algorytm ma średnią złożoność obliczeniową rzędu O(n log n). Może się jednak zdarzyć 
przypadek bardzo niekorzystny, w którym wybierany będzie element największy/najmniejszy. W takiej sytuacji jedna z nowo tworzonych tablic będzie miała 
rozmiar o 1 mniejszy od tablicy dzielonej. W ogólnym przypadku może być zatem konieczne n-1 wywołań funkcji, gdzie n to liczba elementów do posortowania. 
Złożoność obliczeniowa w pesymistycznym przypadku pogarsza się do O(n2).

Rozwiązaniem tego problemu, zapobiegającym pogorszeniu klasy złożoności problemu, jest wybór „właściwego” elementu, względem którego realizowany jest 
podział tablicy. Można do tego celu zastosować algorytm magicznych piątek, znany także jako mediana median.

Zanim przejdziemy do jego opisu skupmy się na chwilę na klasycznym algorytmie szybkim. Jest on dość prosty do wyrażenia 'słownego' przysparza jednak 
trochę problemów w momencie, kiedy trzeba wyznaczyć granicę obu części, dla któych metoda ma być powtórzona. Pewnym ułatwieniem jest wybór zawsze 
pierwszego lub ostatniego elementu dzielącego - ale nasza poprawka ma właśnie wybierać element dzielący, co komplikuje wyznaczanie granicy. 
Dlatego proponuję stworzyć wersję quicksort, która nie działa w miejscu, ale za to jest bardzo prosta w implementacji. Sortowaną listę dzielimy 
na trzy listy zawierające: elementy większe od elementu dzielącego,  elementy mniejsze od niego oraz elementy równe dzielącemu. Wystarczy, że funkcja 
sortująca zwróci listę będącą konkatenacją  wyniku rekurencyjnego wywołania quicksort-a dla pierwszej z list, trzeciej listy oraz wyniku rekurencyjnego 
wywołania quicksort-a dla drugiej listy. Elementem dzielącym może być pierwszy element sortowanej listy.

Po zaimplementowaniu quicksorta i sprawdzeniu poprawności jego działania przejdźmy do algorytmu wyznaczania lepszego elementu dzielącego. 
W tym celu listę należy podzielić na listy 5-elementowe (ostatnia może być niepełna), z których dla każdej wyznaczana jest mediana (dotyczy to także ostatniej, 
ewentualnie krótszej listy). Wyznaczone mediany umieszczane są w liście, dla której powyższa procedura jest powtarzana. Ostatecznie otrzyma się listę 
jednoelementową zawierającą wartość stanowiącą dobry element do dokonania podziału.

W powyższym algorytmie trudność może sprawić szybkie wyznaczenie mediany z 5-ciu (i mniej) elementów. Można tego dokonać stosując kilka porównań. 
Poniższy kod realizuje medianę z 5-ciu i 3-ch. Pozostałe przypadki proszę zaimplementować samodzielnie.

def median_3(a, b, c):
    return max(min(a,b),min(c,max(a,b)))

def median_5(a, b, c, d, e):
      f=max(min(a,b),min(c,d)) # usuwa najmniejsza z 4
      g=min(max(a,b),max(c,d)) # usuwa największą z 4
      return median_3(e,f,g)

Po implementacji sprawdź, czy uzyskiwane są identyczne rezultaty dla obu wersji quicksorta (klasycznej i magicznych piątek).

Podobnie jak w poprzednim ćwiczeniu wygeneruj 10000 losowych elementów (o wartościach od 0 do 99), którymi wypełnisz wejściową tablicę. 
Wykonaj sortowanie oboma metodami i porównaj  czas ich  wykonania.
"""

import random
import time

def swap(tab, i, h):
    tab[i], tab[i - h] = tab[i - h], tab[i]
    if i - 2*h >= 0 and tab[i - h] < tab[i - 2*h]:
        swap(tab, i - h, h)
    return tab

def shell_sort(tab):
    n = len(tab)
    # h = n // 2
    h = 1
    while h + 1.5 < n / 3:
        h += 1.5
    h = int(h)
    while h > 0:
        for i in range(h, n):
            if tab[i] < tab[i - h]:
                swap(tab, i, h)
        # h = h // 2
        if h > 2:
            h = h // 3
        else:
            h = h // 2
    return tab

def median_sort(tab):
    # Wybór mediany
    medians = tab.copy()
    while len(medians) > 1:
        medians_copy = []
        n = len(medians)
        for i in range(0, n, 5):
            if i < (n // 5) * 5:
                medians_copy.append(median_5(medians[i: i + 5]))
            else:
                n_i = len(medians[i:])
                if n_i == 4:
                    medians_copy.append(median_4(medians[i:]))
                elif n_i == 3:
                    medians_copy.append(median_3(medians[i:]))
                elif n_i == 2:
                    medians_copy.append(median_2(medians[i:]))
                else:
                    medians_copy.append(medians[-1])
        medians = medians_copy

    gr, eq, ls = [], [], []
    for elem in tab:
        if elem > medians[0]:
            gr.append(elem)
        elif elem < medians[0]:
            ls.append(elem)
        else:
            eq.append(elem)
    if len(tab) > 2:
        return median_sort(ls) + eq + median_sort(gr)
    else:
        return ls + eq + gr

def median_2(tab):
    return (tab[0] + tab[1]) / 2

def median_3(tab):
    return max(min(tab[0], tab[1]), min(tab[2], max(tab[0], tab[1])))

def median_4(tab):
    f = max(min(tab[0], tab[1]), min(tab[2], tab[3]))  # usuwa najmniejsza z 4
    g = min(max(tab[0], tab[1]), max(tab[2], tab[3]))  # usuwa największą z 4
    tab_2 = [f, g]
    return median_2(tab_2)

def median_5(tab):
    f = max(min(tab[0], tab[1]), min(tab[2], tab[3]))  # usuwa najmniejsza z 4
    g = min(max(tab[0], tab[1]), max(tab[2], tab[3]))  # usuwa największą z 4
    tab_2 = [tab[4], f, g]
    return median_3(tab_2)


def main():
    tab = [random.randint(0, 99) for _ in range(10000)]

    t_start_shell = time.perf_counter()
    _ = shell_sort(tab)
    t_stop_shell = time.perf_counter()
    print("Czas sortowania metodą shell_sort:", "{:.7f}".format(t_stop_shell - t_start_shell))

    t_start_median = time.perf_counter()
    _ = median_sort(tab)
    t_stop_median = time.perf_counter()
    print("Czas sortowania metodą median_sort:", "{:.7f}".format(t_stop_median - t_start_median))


main()
