
"""
1. Możliwym sposobem wykorzystania kopca do posortowania tablicy  jest  wstawienie danych z nieposortowanej tablicy do kopca, 
a następnie zdejmowanie ich z wierzchołka i wstawianie z powrotem  do tablicy, która w ten sposób zostanie posortowana.

To podejście wymaga jednak dodatkowej pamięci na kopiec. W tym ćwiczeniu spróbujemy dokonać sortowania kopcowego w miejscu. Do tego wykorzystamy kod
napisany w ćwiczeniu dotyczącym kolejki priorytetowej. Napisane do tej pory metody będą wymagały jedynie niewielkich zmian.
Po pierwsze - utworzenie kopca z nieposortowanej tablicy:  
Już powinniśmy dysponować metodą naprawiającą kopiec przesuwającą korzeń w dół drzewa (używaną w dequeue). Wystarczy ją wywołać dla wszystkich węzłów 
nie będących liśćmi, co spowoduje ich przesunięcie we właściwe miejsce kopca. Należy jednak zachować kolejność: od ostatniego elementu, który nie jest
liściem (czyli rodzica ostatniego elementu tablicy), aż do korzenia.
Po drugie - utworzenie tablicy z kopca:
W zasadzie już mamy kod, który to realizuje - usuwając korzeń przemieszczamy go na ostatnią pozycję w kopcu (o ostatni przemieszczany w jego miejsce). 
Jednakże zapewne większość z Państwa ten element fizycznie usuwała z tablicy (np. metodą pop). Gdyby tego nie robić, to po 'usunięciu' wszystkich elementów 
z kopca dostaniemy posortowaną tablicę (jeżeli w kopcu wyższy priorytet był wyżej, to uzyskamy tablicę posortowaną rosnąco - na końcu wyląduje element 
największy, potem coraz mniejsze). Tak więc należy (jeżeli jest taka potrzeba) tak zmodyfikować metodę dequeue, żeby nie usuwała ostatniego elementu. 
Ponadto size w kopcu nie może zależeć od rozmiaru tablicy ale musi być 'ręcznie' zwiększany  w enqueue i zmniejszany w dequeue.
Na koniec proszę o uzupełnienie konstruktora klasy reprezentującej kopiec o parametr zawierający listę elementów do posortowania (jako parametr z 
wartością domyślną None). Jeżeli konstruktor zostanie zawołany z argumentem powinien on z przekazanej listy utworzyć kopiec przez zawołanie niżej opisanej 
metody heapify.

Napisz metodę heapify, która z otrzymanej tablicy wejściowej zbuduje kopiec w sposób opisany powyżej.
Niech dana będzie lista z danymi:
Dla tablicy: [(5,'A'), (5,'B'), (7,'C'), (2,'D'), (5,'E'), (1,'F'), (7,'G'), (5,'H'), (1,'I'), (2,'J')]
Stwórz na jej podstawie listę (tablicę), której elementy są obiektami klasy, zawierającą wartość (klucz/priorytet) i daną oraz metody magiczne < i > 
(tak jak w kolejce priorytetowej). Przekaż tę tablicę jako parametr przy tworzeniu kopca.
Wypisz utworzony kopiec jako tablicę i jako drzewo 2D, a następnie, po rozłożeniu kopca, wypisz posortowaną tablicę. Zaobserwuj, czy sortowanie jest stabilne,
tzn. czy kolejność elementów o tym samym priorytecie zostanie zachowana (w porównaniu z ich kolejnością w  tablicy wejściowej).


Drugi test: Wygeneruj losowo 10000 liczb w przedziale od 0 do 99 i wpisz je do tablicy. Wypisz czas sortowania takiej tablicy. W celu realizacji tego zadania  
należy zaimportować moduły random i time.  Do generowania liczb można wykorzystać zapis int(random.random() * 100) powodujący wylosowanie 
liczby całkowitej z zakresu 0-99, natomiast do pomiaru czasu można zaadaptować kod:

t_start = time.perf_counter()
# testowana metoda
t_stop = time.perf_counter()
print("Czas obliczeń:", "{:.7f}".format(t_stop - t_start))

==============================

2. Drugim algorytmem do zrealizowania jest sortowanie przez wybieranie.

Napisz dwie metody sortujące pythonową listę algorytmem przez wybieranie: jedną, wykorzystującą zamianę miejscami elementów (swap), i drugą, 
wykorzystującą przesunięcie elementów (shift). W tym drugim wypadku shift można osiągnąć przez pop i insert.
Dla listy: [(5,'A'), (5,'B'), (7,'C'), (2,'D'), (5,'E'), (1,'F'), (7,'G'), (5,'H'), (1,'I'), (2,'J')] sprawdź działanie obu metod sortowania przez 
wybieranie i porównaj wyniki (stwórz z listy tablicę elementów jak w poprzednim zadaniu). Zaobserwuj stabilność obu wersji algorytmu sortującego.

Drugi test: Wygeneruj losowo 10000 liczb w przedziale od 0 do 1000, którymi wypełnisz tablicę. Wypisz czasy sortowania takiej tablicy I porównaj z 
czasem sortowania kopcowego.
"""

import random
import time

class Node:
    def __init__(self, priority, data):
        self.priority_ = priority
        self.data_ = data

    def __gt__(self, other):
        return self.priority_ > other

    def __lt__(self, other):
        return self.priority_ < other

    def __repr__(self):
        return "{}:{}".format(self.priority_, self.data_)


class Heap:
    def __init__(self, tab=None, size=0):
        if tab is None:
            tab = []
        self.tab_ = tab
        self.size_ = len(self.tab_) if len(self.tab_) > size else size
        self.sorted_tab_ = []
        if tab:
            self.heapify()

    def left(self, idx):
        return 2*idx + 1

    def right(self, idx):
        return 2*idx + 2

    def parent(self, idx):
        return (idx - 1)//2

    def is_empty(self):
        return self.size_ == 0

    def peek(self):
        return self.tab_[0].data_

    def check_children(self, idx):
        swapped = ''
        idx_right = self.right(idx)
        idx_left = self.left(idx)
        if idx_right < self.size_ and self.tab_[idx_right] > self.tab_[idx]:
            self.tab_[idx_right], self.tab_[idx] = self.tab_[idx], self.tab_[idx_right]
            swapped = 'right'
        if idx_left < self.size_ and self.tab_[idx_left] > self.tab_[idx]:
            self.tab_[idx_left], self.tab_[idx] = self.tab_[idx], self.tab_[idx_left]
            swapped = 'left'
        if swapped == 'right':
            self.check_children(idx_right)
            return True
        elif swapped == 'left':
            self.check_children(idx_left)
            return True
        else:
            return False

    def heapify(self):
        if not self.is_empty():
            idx = self.parent(self.size_ - 1)
            while idx >= 0: #Dopóki jest w liście
                swapped = self.check_children(idx)
                if not swapped:
                    idx -= 1
            self.sorted_tab_ = self.tab_.copy()
            while self.size_:
                self.dequeue()
            self.size_ = len(self.tab_)
            return
        else:
            return None

    def dequeue(self):
        if not self.is_empty():
            result = self.sorted_tab_[0].data_
            self.sorted_tab_[0], self.sorted_tab_[self.size_ - 1] = self.sorted_tab_[self.size_ - 1], self.sorted_tab_[0]
            # self.tab_ = self.tab_[:-1]
            self.size_ -= 1
            idx = 0
            stop = False
            while self.right(idx) < self.size_ and not stop: #Dopóki ma dwójkę dzieci
                if self.sorted_tab_[self.right(idx)] > self.sorted_tab_[self.left(idx)]:
                    #Po prawej większy
                    if self.sorted_tab_[idx] < self.sorted_tab_[self.right(idx)]:
                        self.sorted_tab_[idx], self.sorted_tab_[self.right(idx)] = self.sorted_tab_[self.right(idx)], self.sorted_tab_[idx]
                        idx = self.right(idx)
                    elif self.sorted_tab_[idx] < self.sorted_tab_[self.left(idx)]:
                        self.sorted_tab_[idx], self.sorted_tab_[self.left(idx)] = self.sorted_tab_[self.left(idx)], self.sorted_tab_[idx]
                        idx = self.left(idx)
                    else:
                        stop = True
                else:
                    if self.sorted_tab_[idx] < self.sorted_tab_[self.left(idx)]:
                        self.sorted_tab_[idx], self.sorted_tab_[self.left(idx)] = self.sorted_tab_[self.left(idx)], self.sorted_tab_[idx]
                        idx = self.left(idx)
                    elif self.sorted_tab_[idx] < self.sorted_tab_[self.right(idx)]:
                        self.sorted_tab_[idx], self.sorted_tab_[self.right(idx)] = self.sorted_tab_[self.right(idx)], self.sorted_tab_[idx]
                        idx = self.right(idx)
                    else:
                        stop = True
            if self.left(idx) < self.size_ and self.sorted_tab_[self.left(idx)] > self.sorted_tab_[idx]: #Jeśli ma jedno dziecko
                self.sorted_tab_[idx], self.sorted_tab_[self.left(idx)] = self.sorted_tab_[self.left(idx)], self.sorted_tab_[idx]
            return result
        else:
            return None

    def enqueue(self, data, priority):
        new_node = Node(priority, data)
        self.tab_.append(new_node)
        self.size_ += 1
        idx = self.size_ - 1
        while self.parent(idx) >= 0:
            parent = self.parent(idx)
            if self.tab_[parent] < self.tab_[idx]:
                self.tab_[parent], self.tab_[idx] = self.tab_[idx], self.tab_[parent]
            idx = parent
        return

    def print_tab(self):
        print ('{', end=' ')
        for i in range(self.size_ - 1):
            print(self.tab_[i], end = ', ')
        if self.size_ - 1 >= 0 and self.tab_[self.size_ - 1]: print(self.tab_[self.size_ - 1] , end = ' ')
        print( '}')

    def print_sorted_tab(self):
        print ('{', end=' ')
        for i in range(self.size_ - 1):
            print(self.sorted_tab_[i], end = ', ')
        if self.size_ - 1 >= 0 and self.sorted_tab_[self.size_ - 1]: print(self.sorted_tab_[self.size_ - 1] , end = ' ')
        print( '}')

    def print_tree(self, idx, lvl):
        if idx < self.size_:
            self.print_tree(self.right(idx), lvl + 1)
            print(2 * lvl * '  ', self.tab_[idx] if self.tab_[idx] else None)
            self.print_tree(self.left(idx), lvl + 1)

def test1():
    tab = [(5, 'A'), (5, 'B'), (7, 'C'), (2, 'D'), (5, 'E'), (1, 'F'), (7, 'G'), (5, 'H'), (1, 'I'), (2, 'J')]
    copy_tab = []
    for tuple in tab:
        copy_tab.append(Node(tuple[0], tuple[1]))
    heapsort = Heap(copy_tab)
    heapsort.print_tab()
    heapsort.print_tree(0, 0)
    heapsort.print_sorted_tab()

def test2():
    tab = []
    for i in range(10000):
        tab.append(Node(random.randint(0, 99), 'X'))
    t_start = time.perf_counter()
    heapsort = Heap(tab)
    t_stop = time.perf_counter()
    print("Czas obliczeń:", "{:.7f}".format(t_stop - t_start))

def swap(tab):
    n = len(tab)
    for i in range(n):
        min_idx = i
        for j in range(i, n):
            if tab[j] < tab[min_idx]:
                min_idx = j
        tab[i], tab[min_idx] = tab[min_idx], tab[i]
    return tab

def shift(tab):
    n = len(tab)
    for i in range(n):
        min_idx = i
        for j in range(i, n):
            if tab[j] < tab[min_idx]:
                min_idx = j
        elem = tab.pop(min_idx)
        tab.insert(i, elem)
    return tab

def print_tab(tab):
    print('{', end=' ')
    for i in range(len(tab) - 1):
        print(tab[i], end=', ')
    if len(tab) - 1 >= 0 and tab[len(tab) - 1]: print(tab[len(tab) - 1], end=' ')
    print('}')

def test1_():
    tab = [(5, 'A'), (5, 'B'), (7, 'C'), (2, 'D'), (5, 'E'), (1, 'F'), (7, 'G'), (5, 'H'), (1, 'I'), (2, 'J')]
    copy_tab = []
    for tuple in tab:
        copy_tab.append(Node(tuple[0], tuple[1]))
    copy_tab2 = copy_tab.copy()
    print("Metoda swap: ")
    print_tab(swap(copy_tab))
    print("Metoda shift: ")
    print_tab(shift(copy_tab2))

def test2_():
    tab = [random.randint(0, 99) for _ in range(10000)]
    t_start1 = time.perf_counter()
    selection_sort1 = swap(tab)
    t_stop1 = time.perf_counter()
    print("Czas obliczeń dla metody swap:", "{:.7f}".format(t_stop1 - t_start1))
    t_start2 = time.perf_counter()
    selection_sort2 = shift(tab)
    t_stop2 = time.perf_counter()
    print("Czas obliczeń dla metody shift:", "{:.7f}".format(t_stop2 - t_start2))

def main():
    # Heapsort
    test1()
    test2()
    # Selection sort
    test1_()
    test2_()
main()
