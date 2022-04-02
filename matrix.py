
"""
Zaimplementuj w języku Python tablicę dwuwymiarową (macierz), do której dostęp będzie można zrealizować jak np. w języku C, czyli:
nazwa_tablicy[nr_wiersza][nr_kolumny]
Zaimplementowany typ danych powinien pozwalać na operacje dodawania (operatorem +)  i mnożenia, w znaczeniu mnożenia macierzowego (operatorem *)
Wykorzystaj w tym celu klasę.  Dla przypomnienia - specjalne (tzw. magiczne) metody definiujące odpowiednie operatory to:
__add__ - definiuje +
__mul__ - definiuje *
__getitem__ - definiuje [ ]
Dodatkowo proszę zapewnić możliwość wypisania macierzy (wierszami) przez funkcję print poprzez zdefiniowanie metody __str__
Klasa powinna też mieć metodę size zwracającą liczbę wierszy i liczbę kolumn (ALTRNTYWNIE: powinna zostać zaimplementowana metoda __len__)
W operacjach dodawania i mnożenia proszę sprawdzać czy macierze mają odpowiednie rozmiary. Wynikiem tych operacji powinien być nowy obiekt.

Sama macierz może być reprezentowana w postaci listy list, przy czym pole wewnętrznie reprezentujące macierz  (czyli np. ta lista list) ma być prywatne dla klasy. 
Należy zaimplementować 'konstruktor', który stworzy macierz (obiekt tworzonej klasy) na dwa sposoby:
albo otrzyma on jako argument krotkę  zawierającą oba rozmiary macierzy 
albo otrzyma wprost listę list wypełnioną wartościami.
Można wykorzystać  isinstance do sprawdzenia czy argument jest typu tuple, a przeciwnym wypadku założyć, że 'konstruktor' otrzymał w argumencie poprawną listę list.
Niech 'konstruktor' posiada także domyślny parametr (o wartości 0) wykorzystywany do wypełniania stałą wartością macierzy tworzonej przez podanie jej rozmiarów.
"""

class Matrix:
    def __init__(self, param, element=0):
        self.matrix: list[list[int]] = []
        if isinstance(param, tuple):
            self.matrix = [[element for i in range(param[1])] for j in range(param[0])]
        else:
            self.matrix = param

    def __getitem__(self, i):
        return self.matrix[i]

    def __str__(self):
        string = "[ "
        for i in range(self.size()[0]):
            string += "["
            for j in range(self.size()[1]):
                string += "{:2d}".format(self[i][j])
                if j != self.size()[1] - 1:
                    string += ", "
                else:
                    if i < self.size()[0] - 1:
                        string += "],\n  "
                    else:
                        string += "] ]\n"
        return string

    def size(self):
        return len(self.matrix), len(self.matrix[0])

    def __add__(self, other):
        if self.size() == other.size():
            new_matrix = Matrix(self.size())
            for i in range(self.size()[0]):
                for j in range(self.size()[1]):
                    new_matrix[i][j] = self[i][j] + other[i][j]
            return new_matrix
        else:
            raise ValueError("Matrix dimensions invalid!")

    def __mul__(self, other):
        if self.size()[1] == other.size()[0]:
            new_matrix = Matrix((self.size()[0], other.size()[1]))
            for i in range(self.size()[0]):
                for j in range(other.size()[1]):
                    for k in range(self.size()[1]):
                        new_matrix[i][j] += self[i][k] * other[k][j]
            return new_matrix
        else:
            raise ValueError("Matrix dimensions invalid!")

    def transpose(self):
        new_mat = [[self[j][i] for j in range(self.size()[0])] for i in range(self.size()[1])]
        return Matrix(new_mat)
      
