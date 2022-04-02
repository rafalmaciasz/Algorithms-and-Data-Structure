
"""
Zaimplementuj listę z przeskokami (skip-list) poprzez stworzenie klasy zawierającej atrybut reprezentujący głowę listy (np. head) oraz metody:
konstruktor z parametrem określającym maksymalną 'wysokość' elementu listy - powinien tworzyć pusty element listy, którego tablica wskazań na następne elementy
będzie reprezentowała tablicę głów list na poszczególnych poziomach, ten element ma zostać przypisany do atrybutu head
search - wyszukująca i zwracająca wartość odpowiadającą podanemu kluczowi (lub None)
insert - wstawiająca daną wg podanego klucza - podczas szukania miejsca do wstawienia klucza powinna tu być tworzona lista  (tablica) zawierająca poprzedniki
znalezionego elementu  na każdym poziomie (znaleziony element to ten, którego klucz jest większy od klucza wstawianego elementu); dla poziomów,
których znaleziony element nie posiada  w tablicy poprzedników powinna być wpisana głowa listy (np. head).
remove - usuwająca daną o podanym kluczu
__str__ -  wypisującą listę w postaci par (klucz:wartość) (należy wypisać 'poziom 0' listy) 
Elementy listy również powinny być zaimplementowane jako klasa z atrybutami przechowującymi: klucz,  wartość (jakąś daną), liczbę poziomów oraz listę (tablicę)
ze wskazaniami na następny element o rozmiarze równym liczbie poziomów.
Do tworzenia elementów listy będzie przydatna funkcja/metoda losująca liczbę poziomów (jako metoda nie musi mieć parametru maxLevel, p zaś będziemy ustawiali na 0.5):
def randomLevel(p, maxLevel):
  lvl = 1   
  while random() < p and lvl <maxLevel:
        lvl = lvl + 1
  return lvl

W celach testowych przydatna  też będzie funkcja/metoda:  wypisująca całą listę (wszystkie poziomy) przez wypisanie kluczy na każdym z poziomów . Można w tym celu zaadoptować poniższą funkcję:
    def displayList_(self):
        node = self.head.next[0]  # pierwszy element na poziomie 0
        keys = []                           # lista kluczy na tym poziomie
        while(node != None):
            keys.append(node.key)
            node = node.next[0]

        for lvl in range(maxLevel-1, -1, -1):
            print("{}: ".format(lvl), end=" ")
            node = self.head.next[lvl]
            idx = 0
            while(node != None):                
                while node.key>keys[idx]:
                    print("  ", end=" ")
                    idx+=1
                idx+=1
                print("{:2d}".format(node.key), end=" ")     
                node = node.next[lvl]    
            print("")
 
"""

from typing import Union, List
from random import random

class Element:
    def __init__(self, lvl, key=None, value=None):
        self.key_ = key
        self.value_ = value
        self.lvl_ = lvl
        self.next_: List[Union[Element, None]] = [None] * lvl

class SkipList:
    def __init__(self, lvl=5):
        self.head_ = Element(lvl)
        self.maxLevel = lvl

    def search(self, key, elem: Union[Element, None, str] = 'unset'):
        if isinstance(elem, str):
            elem = self.head_
        for i in range(elem.lvl_ - 1, -1, -1):
            if elem.next_[i]:
                next = elem.next_[i]
                if key > next.key_:
                    return self.search(key, next)
                elif key == next.key_:
                    return next.value_

    def insert(self, key, value):
        elem = self.head_
        broken = []
        for i in range(elem.lvl_ - 1, -1, -1):
            elem = self.head_
            while elem.next_[i] and elem.next_[i].key_ <= key:
                if elem.next_[i].key_ == key:
                    #Overwrite value
                    elem.next_[i].value_ = value
                    return
                elif elem.next_[i].key_ < key:
                    elem = elem.next_[i]
            broken.append(elem)
        new = Element(lvl=self.randomLevel(0.5), key=key, value=value)
        for i in range(new.lvl_):
            new.next_[i] = broken[len(broken) - i - 1].next_[i]
            broken[len(broken) - i - 1].next_[i] = new
        return

    def remove(self, key):
        elem = self.head_
        for i in range(elem.lvl_ - 1, -1, -1):
            elem = self.head_
            while elem and elem.next_[i]:
                if elem.next_[i].key_ == key:
                    #Remove one
                    elem.next_[i] = elem.next_[i].next_[i]
                elif elem.next_[i].key_ < key:
                    elem = elem.next_[i]
                else:
                    elem = None

    def __str__(self):
        node = self.head_.next_[0]
        str_ = '{'
        while node.next_[0]:
            str_ += '{}:{}, '.format(node.key_, node.value_)
            node = node.next_[0]
        str_ += '{}:{}'.format(node.key_, node.value_)
        str_ += '}'
        return str_

    def displayList_(self):
        node = self.head_.next_[0]  # pierwszy element na poziomie 0
        keys = []  # lista kluczy na tym poziomie
        while node:
            keys.append(node.key_)
            node = node.next_[0]

        for lvl in range(self.maxLevel - 1, -1, -1):
            print("{}: ".format(lvl), end=" ")
            node = self.head_.next_[lvl]
            idx = 0
            while node:
                while node.key_ > keys[idx]:
                    print("  ", end=" ")
                    idx += 1
                idx += 1
                print("{:2d}".format(node.key_), end=" ")
                node = node.next_[lvl]
            print("")

    def randomLevel(self, p):
        lvl = 1
        while random() < p and lvl < self.maxLevel:
            lvl = lvl + 1
        return lvl
