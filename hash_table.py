
"""
Zaimplementuj tablicę mieszającą w postaci klasy zawierającej 'tablicę statyczną', np.:
tab = [None for i in range(size)]
gdzie size jest parametrem 'konstruktora'.

Klasa powinna mieć zaimplementowaną metodę realizującą funkcję mieszającą, obliczającą modulo rozmiaru tablicy
oraz metodę rozwiązującą kolizję metodą adresowania otwartego (z próbkowaniem kwadratowym, gdzie c1 i c2 powinny być
parametrami konstruktora z domyślnym ustawieniem odpowiednio 1 i 0 - czyli domyślnie mamy próbkowanie liniowe).
Zakładamy, że funkcja mieszająca może otrzymać wprost liczbę, lub napis - wówczas należy go zamienić na liczbę poprzez zsumowanie
kodów ASCII wszystkich jego liter (funkcja ord).

Następnie należy zaimplementować metody:
konstruktor (z parametrami: rozmiar tablicy oraz c1, c2  jak powyżej) tworzący pustą tablicę (wypełnioną None-ami)
search - wyszukująca i zwracająca wartość odpowiadającą podanemu kluczowi (lub None w wypadku nieznalezienia)
insert - wstawiająca daną wg podanego klucza, jeżeli element o takim kluczu istnieje, jego wartość powinna zostać nadpisana
remove - usuwająca daną o podanym kluczu (początkowo zaimplementuj usuwanie przez wpisanie None w  miejsce wskazane przez wyliczony indeks).
__str__ -  wypisującą tablicę w postaci par {klucz:wartość, ...} - tak jak wypisywany jest pythonowy słownik; 'Puste' miejsce niech będzie wypisywane jako None
Metody insert i remove powinny w jakiś sposób informować o niepowodzeniu (insert - brak miejsca, remove - brak danej o podanym kluczu).
Może to być np. wyjątek lub zwracana wartość None. W takim wypadku w miejscu wywołania niech pojawia się komunikaty "Brak miejsca" i "Brak danej".
  
Elementy tablicy również powinny być zaimplementowane jako klasa z dwoma atrybutami przechowującymi: klucz oraz  wartość (jakąś daną).
"""

from typing import Union
class Element_:
    def __init__(self, data, key):
        self.data_ = data
        self.key_ = key

class HashTable:
    def __init__(self, size, c1 = 1, c2 = 0):
        self.tab_: list = [None] * size
        self.size_ = size
        self.c1_ = c1
        self.c2_ = c2

    def is_full(self):
        return all(self.tab_)

    def hash(self, key):
        if isinstance(key, str):
            #Compute ASCII values
            new_key = 0
            for i in key:
                new_key += ord(i)
            key = new_key
        return key % self.size_

    def solve_collision(self, key):
        i = 1
        ind = self.hash(key)
        while True:
            if i < self.size_:
                new_ind = (ind + self.c1_ * i + self.c2_ * i ** 2) % self.size_
                if not self.tab_[new_ind] or self.tab_[new_ind].key_ == key:
                    return new_ind
                else:
                    i += 1
            else:
                return None

    def search(self, key):
        if isinstance(key, str):
            new_key = 0
            for i in key:
                new_key += ord(i)
            key = new_key
        ind = self.hash(key)
        if self.tab_[ind] and self.tab_[ind].key_ == key:
            return self.tab_[ind].data_
        else:
            new_ind = self.solve_collision(key)
            if new_ind and self.tab_[new_ind] and self.tab_[new_ind].key_ == key:
                return self.tab_[new_ind].data_
            else:
                return None

    def insert(self, data, key):
        ind = self.hash(key)
        try:
            if self.tab_[ind] and self.tab_[ind].key_ != key:
                #Collision
                raise Exception
            else:
                self.tab_[ind] = Element_(data, key)
                return
        except Exception:
            if not self.is_full():
                new_ind = self.solve_collision(key)
                if new_ind is not None:
                    self.tab_[new_ind] = Element_(data, key)
                else:
                    raise ValueError("Lack of space")
            else:
                raise ValueError("Lack of space")

    def remove(self, key):
        if isinstance(key, str):
            new_key = 0
            for i in key:
                new_key += ord(i)
            key = new_key
        ind = self.hash(key)
        if ind < self.size_:
            self.tab_[ind] = None
        else:
            raise ValueError("There is no elem with that key")

    def __str__(self):
        str = "{"
        for i in self.tab_:
            if i:
                if i == self.tab_[-1]:
                    str += '{0}:{1}'.format(i.key_, i.data_)
                else:
                    str += '{0}:{1}, '.format(i.key_, i.data_)
            else:
                str += 'None, '
        str += '}'
        return str
