
"""
Algorytm Jarvisa

Idea algorytmu jest bardzo prosta - zaczynamy od skrajnego lewego punktu i “zagarniamy” punkty, przechodząc po zbiorze w kierunku lewoskrętnym. 
Zatem metoda ta sprowadza się do wyszukiwania “odpowiednich” punktów w kolejnych krokach. Jak to zrobić? Mając dany punkt p, należy znaleźć taki punkt q, 
że dla wszystkich pozostałych punktów r (p,q,r) jest lewoskrętne.


Implementacja:

Algorytm realizujemy dla przestrzeni 2D, więc należy zdefiniować punkt, posiadający dwie współrzędne - x i y.

Wyszukaj skrajny lewy punkt. Jeśli więcej niż jeden punkt ma tę samą minimalną współrzędną x, wybierz skrajny dolny punkt. Będzie to punkt 
poczatkowy i zarazem pierwszy punkt p.

W pętli wykonuj następujące kroki, dopóki nie wrócimy do punktu początkowego:

następny punkt q wybierany jest tak, aby dla dowolnego punktu r (p,q,r) było lewoskrętne. Do tego celu wybierz początkowe q jako kolejny punkt po p. 
Dalej, przechodząc przez kolejne punkty r, sprawdzamy, czy (p,q,r) jest prawoskrętne. Jeżeli tak, to q jest złym kandydatem (istnieje r - oznaczmy je 
r - dla którego (p,q,r) nie jest lewoskrętne). Z drugiej strony - jeżeli (p,q,r) jest prawoskrętne, to (p,r,q) jest lewoskrętne i odcinek (p,r) leży 
bliżej szukanej otoczki niż (p,q) - zatem r jest dobrym nowym kandydatem zastępującym q, gdyż wszystkie dotychczasowe punkty r dla których  (p,q,r) było 
lewoskrętne  będą także lewoskrętne dla (p, r, r) .  Czyli podstawiamy q=r i kontynuujemy sprawdzanie następnych punktów. Ostatecznie wartość q będzie 
określała punkt dla którego odcinek (p, q) należy do otoczki.

dodaj punkt q jako następujący po p (np. do listy), aby uzyskać zbiór kolejnych punktów wyznaczających wielokąt na koniec działania algorytmu

wartość q wstaw w miejsce p do kolejnej iteracji


Wyznacz punkty należące do wielokąta dla wejściowego zbioru (UWAGA - pierwsza współrzędna to x, druga y): (0, 3), (0, 0), (0, 1), (3, 0), (3, 3), a następnie 
dla (0, 3), (0, 1), (0, 0), (3, 0), (3, 3). W tej implementacji wyniki powinny być różne, jeśli podamy współliniowe punkty w różnej kolejności.

Potencjalnym rozwiązaniem tego problemu jest wyznaczenie najdalszego współliniowego punktu. Do punktu 3.1 dodaj warunek: jeśli (p,r,q) jest 
współliniowe i q leży pomiędzy p i r, to w miejsce q wstaw r (czyli wybierz dalszy współliniowy punkt). Sprawdź ponownie wyniki dla obu zbiorów - tym 
razem powinny być identyczne.
"""

from typing import Tuple, List

def Jarvis(points: List[Tuple], v2=False):
    min_x = 1000
    p, index_p = [], 0
    for i in range(len(points)):
        if points[i][0] <= min_x:
            min_x = points[i][0]
            p.append(points[i])
    if len(p) > 1:
        min_y = 1000
        p = p[0]
        for i in range(len(points)):
            if points[i][1] <= min_y:
                min_y = points[i][1]
                p, index_p = points[i], i
    q = points[0]
    otoczka = [p]
    while q != otoczka[0]:
        p = otoczka[-1]
        for point in points:
            if point not in otoczka:
                q = point
                break
        else:
            return otoczka
        for r in points:
            if r != p and r != q:
                if (q[1] - p[1]) * (r[0] - q[0]) - (r[1] - q[1]) * (q[0] - p[0]) > 0:
                    # Prawoskrętny
                    q = r
                elif (q[1] - p[1]) * (r[0] - q[0]) - (r[1] - q[1]) * (q[0] - p[0]) == 0 and \
                        (min(p[0], r[0]) < q[0] < max(p[0], r[0]) or
                         min(p[1], r[1]) < q[1] < max(p[1], r[1])) and v2:
                    # Współliniowe
                    q = r

        if q != otoczka[0]:
            otoczka.append(q)
    return otoczka

def main():
    points = [(2, 2), (4, 3), (5, 4), (0, 3), (0, 2), (0, 0), (2, 1), (2, 0), (4, 0)]
    print(Jarvis(points))
    print(Jarvis(points, v2=True))


main()
