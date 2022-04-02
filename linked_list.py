"""
Zaimplementuj w języku Python listę wiązaną jednokierunkową. Niech będzie ona zaimplementowana jako klasa zawierająca pole head.
Pole head należy rozumieć jako wskazanie na pierwszy element listy (należy stworzyć drugą , osobną, klasę reprezentującą elementy listy).
Pole to powinno być ustawiane w 'konstruktorze' na None (czyli konstruktor będzie odpowiednikiem funkcji tworzącej pustą listę).

Zaimplementuj poniższe funkcjonalności:
Transformatory:
• create - tę rolę będzie pełnił 'konstruktor' tworzący obiekt reprezentujący listę z polem head ustawionym na None
• destroy - usunięcie/zniszczenie całej listy - tu też jest łatwo - wystarczy ustawić head na None, a Python sam zwolni pamięć :)
• add - metoda dodająca na początek listy
• remove - metoda usuwająca element z początku listy
Obserwatory:
• is_empty - metoda zwracająca True dla pustej listy
• length - metoda zliczająca liczbę elementów
• get - metoda zwracająca pierwszy element (tylko dane, bez 'wskaźnika' - wewnętrzna reprezentacja ma być ukryta)

 a także metody pozwalające:
wypisać listę (nie musi to być __str__ tylko wypisanie listy na ekran, zakładając, że dane z elementu listy da się wypisać print-em)
dodać element na koniec listy
usunąć element z końca


Dodatkowo uzupełnij klasę o metody:
take(n) - metoda tworząca nową listę wiązaną z n pierwszych elementów listy (dla n większego od rozmiaru brane są wszystkie elementy)
drop(n) - metoda tworząca nową listę wiązaną z elementów podanej listy z pominięciem jej pierwszych n elementów (dla n większego od 
rozmiaru zwracana jest pusta lista). Uwaga - kolejność elementów w nowych listach nie powinna zostać odwrócona
"""

class Element:
    def __init__(self, data_, next_ = None):
        self.data_ = data_
        self.next_ = next_

class LinkedList:
    def __init__(self):
        self.head_ = None

    def destroy(self):
        self.head_ = None
        return

    def add(self, new_data):
        new = Element(new_data, self.head_)
        self.head_ = new
        return

    def remove(self):
        if self.head_:
            self.head_ = self.head_.next_
        return

    def is_empty(self):
        if not self.head_:
            return True
        else:
            return False

    def length(self):
        len = 0
        elem = self.head_
        while elem:
            len += 1
            elem = elem.next_
        return len

    def get(self):
        if not self.is_empty():
            return self.head_.data_
        else:
            raise ValueError("List is empty!")

    def print_list(self):
        if not self.is_empty():
            print("[{},".format(self.head_.data_))
            elem = self.head_.next_
            while elem:
                if elem.next_ is None:
                    print("{}]\n".format(elem.data_))
                else:
                    print("{},".format(elem.data_))
                elem = elem.next_
            return
        return

    def add_to_end(self, new_data):
        new = Element(new_data)
        if not self.is_empty():
            elem = self.head_
            while elem.next_:
                elem = elem.next_
            elem.next_ = new
            return
        else:
            self.head_ = new
            return

    def remove_from_end(self):
        elem = self.head_
        last_elem = None
        while elem.next_:
            last_elem = elem.next_
            elem = elem.next_
        elem = self.head_
        while elem.next_:
            if elem.next_ is last_elem:
                elem.next_ = None
            else:
                elem = elem.next_
        return

    def take(self, n):
        if not self.is_empty() and self.length() >= n:
            new_list = LinkedList()
            elem = self.head_
            for i in range(n):
                new_list.add_to_end(elem.data_)
                elem = elem.next_
            return new_list
        else:
            raise ValueError("Param n out of range!")

    def drop(self, n):
        if not self.is_empty() and self.length() > n:
            new_list = LinkedList()
            elem = self.head_
            for i in range(self.length()):
                if i < n:
                    elem = elem.next_
                else:
                    new_list.add_to_end(elem.data_)
                    if elem.next_:
                        elem = elem.next_
            return new_list
        elif self.length() == n:
            return LinkedList()
        else:
            raise ValueError("Param n out of range!")
            
