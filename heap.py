
"""
Celem ćwiczenia jest implementacja kolejki priorytetowej jako kopca (maksymalnego) zrealizowanego w postaci tablicy.
Jako tablicę można wykorzystać listę pythonową (albo z natywną obsługą, albo realokowaną  'ręcznie' jak w zadaniu z tablicą cykliczną). 

Element kolejki niech będzie obiektem klasy, której atrybutami będą dane i priorytet. Ta klasa powinna mieć zdefiniowane 'magiczne' metody pozwalające
na użycie na jej obiektach operatorów < i >  oraz wypisanie ich print-em w postaci priorytet : dane.
Klasa reprezentująca kolejkę powinna zawierać pola przechowujące:  tablicę i  jej aktualny rozmiar (w implementacji używającej standardowej listy pythonowej
to pole nie musi wystąpić) oraz następujące metody:
konstruktor tworzący pustą kolejkę
is_empty - zwracająca True jeżeli kolejka jest pusta
peek - zwracająca daną o najwyższym priorytecie (czyli największej wartości atrybutu priorytet)
dequeue - zwracająca None jeżeli kolejka jest pusta lub daną o najwyższym priorytecie (zdejmując ją z wierzchołka kopca)
enqueue - otrzymująca dane do wstawienia do kolejki (kopca) wraz z ich priorytetem.
Dodatkowo, aby usprawnić poruszanie się po kopcu, proszę napisać metody left i right, które otrzymawszy indeks węzła zwracają indeks odpowiednio
lewego i prawego potomka, oraz metodę parent, która na podstawie indeksu węzła zwraca indeks jego rodzica.

Należy także utworzyć funkcje/metody:  wypisująca kolejkę jak słownik (elementy tablicy jako pary priorytet : dane rozdzielone przecinkami, 
całość w nawiasach { }) i wypisująca kolejkę jak drzewo.
Do wypisania jak słownik  proszę wykorzystać poniższy kod (który można przerobić celem dostosowania do własnej implementacji):
    def print_tab(self):
        print ('{', end=' ')
        for i in range(self.size-1):
            print(self.tab[i], end = ', ')
        if self.tab[self.size-1]: print(self.tab[self.size-1] , end = ' ')
        print( '}')

Do wypisania drzewa proszę wykorzystać poniższy kod (który można przerobić celem dostosowania do własnej implementacji):
    def print_tree(self, idx, lvl):
        if idx<self.size:           
            self.print_tree(self.right(idx), lvl+1)
            print(2*lvl*'  ', self.tab[idx] if self.tab[idx] else None)           
            self.print_tree(self.left(idx), lvl+1)

Celem wypisania drzewa należałoby tak wywołać powyższą metodę:
    kol_prior.print_tree(0, 0);
"""

class Node:
    def __init__(self, data, priority):
        self.data_ = data
        self.priority_ = priority

    def __gt__(self, other):
        return self.priority_ > other

    def __lt__(self, other):
        return self.priority_ < other

    def __str__(self):
        return "{}:{}".format(self.priority_, self.data_)


class Heap:
    def __init__(self, size=0):
        self.tab_ = []
        self.size_ = size

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

    def dequeue(self):
        if not self.is_empty():
            result = self.tab_[0].data_
            self.tab_[0], self.tab_[-1] = self.tab_[-1], self.tab_[0]
            self.tab_ = self.tab_[:-1]
            self.size_ -= 1
            idx = 0
            while self.right(idx) < self.size_: #Dopóki ma dwójkę dzieci
                if self.tab_[self.right(idx)] > self.tab_[self.left(idx)]:
                    #Po prawej większy
                    if self.tab_[idx] < self.tab_[self.right(idx)]:
                        self.tab_[idx], self.tab_[self.right(idx)] = self.tab_[self.right(idx)], self.tab_[idx]
                        idx = self.right(idx)
                    elif self.tab_[idx] < self.tab_[self.left(idx)]:
                        self.tab_[idx], self.tab_[self.left(idx)] = self.tab_[self.left(idx)], self.tab_[idx]
                        idx = self.left(idx)
                else:
                    if self.tab_[idx] < self.tab_[self.left(idx)]:
                        self.tab_[idx], self.tab_[self.left(idx)] = self.tab_[self.left(idx)], self.tab_[idx]
                        idx = self.left(idx)
                    elif self.tab_[idx] < self.tab_[self.right(idx)]:
                        self.tab_[idx], self.tab_[self.right(idx)] = self.tab_[self.right(idx)], self.tab_[idx]
                        idx = self.right(idx)
            if self.left(idx) < self.size_ and self.tab_[self.left(idx)] > self.tab_[idx]: #Jeśli ma jedno dziecko
                self.tab_[idx], self.tab_[self.left(idx)] = self.tab_[self.left(idx)], self.tab_[idx]
            return result
        else:
            return None

    def enqueue(self, data, priority):
        new_node = Node(data, priority)
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

    def print_tree(self, idx, lvl):
        if idx < self.size_:
            self.print_tree(self.right(idx), lvl + 1)
            print(2 * lvl * '  ', self.tab_[idx] if self.tab_[idx] else None)
            self.print_tree(self.left(idx), lvl + 1)

def main():
    heap = Heap()
    keys = [4, 7, 6, 7, 5, 2, 2, 1]
    data = "ALGORYTM"
    for i in range(len(keys)):
        heap.enqueue(data[i], keys[i])
    heap.print_tree(0, 0)
    heap.print_tab()
    print(heap.dequeue())
    print(heap.peek())
    heap.print_tab()
    while not heap.is_empty():
        print(heap.dequeue())
    heap.print_tab()

main()