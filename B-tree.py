
"""
Zaimplementuj w języku Python uproszczoną wersję b-drzewa. Należy zaimplementować jedynie funkcję insert dodającą element do drzewa.
Ponadto dla uproszczenia założymy, że:
maksymalna liczba elementów w węźle jest nieparzysta (a więc pełny węzeł ma parzystą liczbę potomków). 
dodawanymi elementami będą same klucze (pomijamy dane, które zazwyczaj towarzyszą kluczom)
w wypadku, gdy węzeł, do którego ma być dodany element, jest pełny następuje jego podział (nie ma próby przesunięcia elementów do sąsiednich węzłów) 
nie sprawdzamy czy próbujemy wstawić już istniejący klucz 

Możliwa implementacja - dwie klasy: 
pierwsza klasa zawiera pole  wskazujące na korzeń drzewa, pole zawierające maksymalną liczbę potomków (lub maksymalną liczbę elementów w węźle)
    ustawiane przy tworzeniu obiektu tej klasy oraz metodę insert dodającą klucz i metodę wypisującą drzewo
druga klasa zawiera dwa pola: keys (lista kluczy), children (lista potomków).

W omawianej tu implementacji metoda insert zwraca informację czy wstawianie klucza spowodowało podział potomka (parę - element środkowy z podziału i utworzony
w jego trakcie węzeł)
Metoda insert zaczyna od przeszukania aktualnego węzła w poszukiwaniu klucza większego od wstawianego. Po znalezieniu sprawdza czy aktualny węzeł jest liściem:
 - jeżeli tak dodaje klucz (warto tu zrobić osobną funkcję dodającą do węzła - jest ona opisana poniżej), 
 - jeżeli nie - woła się rekurencyjnie dla 'lewego potomka' znalezionego klucza (w wypadku gdy wstawiany klucz jest większy od wszystkich w węźle 
to będzie to ostatni potomek)

Po powrocie z rekurencji może się okazać, że potomek do którego przeszliśmy został podzielony -  tak więc należy dodać do aktualnego węzła 
środkowy klucz z podziału i wskazanie na nowo-utworzony węzeł (ta sama funkcja dodająca do węzła co w poprzednim przypadku)
Funkcja dodająca do węzła otrzymuje jako parametry dodawany klucz oraz ewentualne wskazanie na nowo-utworzony węzeł ze swego poprzedniego wywołania.
Musi ona sprawdzić, czy węzeł nie jest pełny (jeżeli tak to podzielić go przepisując zarówno keys jak i children) i wpisać w odpowiednie miejsce klucz
(do listy keys) oraz ewentualne wskazanie na potomka (do listy children). Jeżeli nastąpił podział funkcja zwraca środkowy klucz z podziału i wskazanie
na utworzony w nowy węzeł. Jeżeli podziału nie było - można zwrócić None.

Na koniec metody insert należy sprawdzić, czy nie nastąpiło podzielenie root-a - wtedy trzeba utworzyć nowego roota z jednym elementem (środkiem podziału)
i wskazaniami na węzeł utworzony w podziale i na 'starego' root-a.
   

Poniższe funkcje mogą się przydać w tworzeniu metody wypisującej drzewo. Założono tu, że struktura danych opisująca węzeł to klasa zawierająca pola:
keys - tablica (lista) kluczy
children -  tablica (lista) potomków
size - liczba elementów w tablicy keys
oraz, że liście też posiadają listę dzieci (wszystkie==None)

    def print_tree(self):
        print("==============")
        self._print_tree(self.root, 0)
        print("==============")

    def _print_tree(self, node, lvl):
        if node!=None:
            for i in range(node.size+1): 	                	
                self._print_tree(node.children[i], lvl+1)
                if i<node.size:
                    print(lvl*'  ', node.keys[i])	

Oczywiście powyższe metody trzeba dostosować do własnej implementacji.
"""

class Node:
    def __init__(self, k):
        if (k - 1) % 2:
            self.children = [None] * k
            self.keys = [None] * (k - 1)
            self.size = 0
        else:
            raise ValueError('K nie jest parzyste')

    def actual_size(self):
        size = 0
        for i in self.keys:
            if i is not None:
                size += 1
        self.size = size
        return size

    def is_full(self):
        return len(self.keys) == self.actual_size()

    def insert_to_node(self, key):
        if not self.is_full():
            i = self.size
            set_i = False
            for idx, elem in enumerate(self.keys):
                if elem and key < elem and not set_i:
                    i = idx
                    set_i = True

            # Przesuń klucze
            copy_keys = self.keys[:i]
            copy_keys.append(key)
            for elem in self.keys[i:-1]:
                copy_keys.append(elem)
            self.keys = copy_keys

            # Przesuń potomków
            copy_children = self.children[i + 1:]
            self.children[i + 2:] = copy_children[:-1]
            self.actual_size()
            return
        else:
            raise ValueError('Full node')

    def remove_half_keys(self):
        copy = []
        for i in range((len(self.keys) + 1) // 2, len(self.keys)):
            copy.append(self.keys[i])
            self.keys[i] = None
        self.actual_size()
        return copy

    def remove_half_children(self):
        copy = []
        for i in range(len(self.children) // 2, len(self.children)):
            copy.append(self.children[i])
            self.children[i] = None
        return copy

    def divide(self):
        mid, self.keys[self.size // 2] = self.keys[self.size // 2], None
        new_node = Node(len(self.children))
        keys = self.remove_half_keys()
        new_node.keys[:len(keys)] = keys
        children = self.remove_half_children()
        new_node.children[:len(children)] = children
        new_node.actual_size()
        return mid, new_node


class B_Tree:
    def __init__(self, k):
        self.head = Node(k)

    def insert(self, key, node=None):
        if not node:
            node = self.head
        i = node.actual_size()
        set_i = False
        for idx, elem in enumerate(node.keys):
            if elem and key < elem and not set_i:
                i = idx
                set_i = True
        if node.children[i]:
            # Nie jest liściem
            child = node.children[i]
            mid, new_node = self.insert(key, child)
            if new_node:
                # Był podział
                if node.is_full():
                    # Jest pełny
                    mid2, new_node2 = node.divide()
                    if mid2 > mid:
                        # Dodaj do lewego
                        node.insert_to_node(mid)
                        node.children[node.size] = new_node
                    else:
                        # Dodaj do prawego
                        new_node2.insert_to_node(mid)
                        x = new_node.keys[0]
                        set_i = False
                        i = new_node2.size
                        for idx, elem in enumerate(new_node2.keys):
                            if elem and x < elem and not set_i:
                                set_i = True
                                i = idx
                        new_node2.children[i] = new_node
                    if node == self.head:
                        # Jest głową
                        self.head = Node(len(node.children))
                        self.head.keys[0] = mid2
                        self.head.children[0], self.head.children[1] = node, new_node2
                    else:
                        return mid2, new_node2
                else:
                    node.insert_to_node(mid)
                    for idx, elem in enumerate(node.keys):
                        if elem == mid:
                            node.children[idx + 1] = new_node
                    return None, None
            else:
                return None, None
        else:
            # Jest liściem
            if node.is_full():
                # Jest pełny
                if node == self.head:
                    # Jest głową
                    mid, new_node = node.divide()
                    self.head = Node(len(node.children))
                    self.head.keys[0] = mid
                    if mid > key:
                        # Dodaj do lewego
                        node.insert_to_node(key)
                    else:
                        # Dodaj do prawego
                        new_node.insert_to_node(key)
                    self.head.actual_size()
                    self.head.children[0], self.head.children[1] = node, new_node
                    return
                else:
                    mid, new_node = node.divide()
                    if mid > key:
                        # Dodaj do lewego
                        node.insert_to_node(key)
                    else:
                        # Dodaj do prawego
                        new_node.insert_to_node(key)
                    return mid, new_node
            else:
                # Nie jest pełny
                node.insert_to_node(key)
                return None, None

    def print_tree(self):
        print("==============")
        self._print_tree(self.head, 0)
        print("==============")

    def _print_tree(self, node, lvl):
        if node is not None:
            for i in range(node.size + 1):
                self._print_tree(node.children[i], lvl + 1)
                if i < node.size:
                    print(lvl * '  ', node.keys[i])

def main():
    b_tree1 = B_Tree(4)
    elements = [5, 17, 2, 14, 7, 4, 12, 1, 16, 8, 11, 9, 6, 13, 0, 3, 18, 15, 10, 19]
    for elem in elements:
        b_tree1.insert(elem)
    b_tree1.print_tree()

    b_tree2 = B_Tree(4)
    for i in range(20):
        b_tree2.insert(i)
    b_tree2.print_tree()
    for i in range(20, 200):
        b_tree2.insert(i)
    b_tree2.print_tree()

    b_tree3 = B_Tree(6)
    for i in range(200):
        b_tree3.insert(i)
    b_tree3.print_tree()


main()
