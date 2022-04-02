
"""
Celem ćwiczenia jest wykorzystanie realokowalnej tablicy jako 'bazy' do stworzenia kolejki. Ze względu na to, że Python ma wbudowaną obsługę tablic dynamicznych i sam zarządza pamięcią,
stworzenie w nim tablicy z 'ręczną' realokacją wymaga przyjęcia pewnych ograniczeń:
tablicę implementujemy jako listę o zadanym rozmiarze np:
tab = [None for i in range(size)]
Poza tym wprowadzimy 'protezę' na funkcję realloc:
def realloc(tab, size):
    oldSize = len(tab)
    return [tab[i] if i<oldSize else None  for i in range(size)]

Używając powyższych konstrukcji zaimplementuj kolejkę wykorzystując tablicę cykliczną.
Zdefiniuj klasę reprezentującą kolejkę.  Reprezentacja kolejki powinna zawierać pola przechowujące:  tablicę, jej aktualny rozmiar, indeks miejsca zapisu do kolejki i indeks miejsca odczytu z kolejki.
Następnie należy zaimplementować metody:
konstruktor tworzący pustą kolejkę - ALE ma tu powstać  5-cio elementowa tablica  (na razie pusta), rozmiar będzie ustawiony na 5 a oba indeksy na 0.
is_empty - zwracająca True jeżeli indeks miejsca odczytu jest równy indeksowi miejsca zapisu
peek - zwracająca daną z miejsca odczytu lub None dla pustej kolejki
dequeue - zwracająca None jeżeli kolejka jest pusta lub daną z miejsca odczytu (wtedy przed zwróceniem danej przesuwa się indeks miejsca odczytu o 1 z uwzględnieniem ewentualnego 
zapętlenia na końcu tablicy).
enqueue - otrzymująca dane do wstawienia do kolejki, po wstawieniu której należy przesunąć indeks miejsca zapisu o 1 z uwzględnieniem ewentualnego zapętlenia na końcu tablicy.
Jeżeli po przesunięciu oba indeksy są takie same należy dwukrotnie powiększyć tablicę przez realokację oraz odpowiednio rozsunąć dane - wszystko od od miejsca 'spotkania' indeksów do 'starego'
końca tablicy musi być przemieszczone na koniec powiększonej tablicy. Należy pamiętać o odpowiednim uaktualnieniu rozmiaru tablicy oraz indeksu miejsca odczytu.
"""

def realloc(tab, size):
    oldSize = len(tab)
    return [tab[i] if i<oldSize else None  for i in range(size)]

class Queue:
    def __init__(self):
        self.queue_ = [None] * 5
        self.len_ = 5
        self.write_ = 0
        self.read_ = 0

    def is_empty(self):
        return self.write_ == self.read_

    def peek(self):
        if self.is_empty():
            return None
        else:
            return self.queue_[self.read_]

    def dequeue(self):
        if self.is_empty():
            return None
        else:
            ind = self.read_
            self.read_ += 1
            #Overload
            if self.read_ >= self.len_:
                self.read_ -= self.len_
            return self.queue_[ind]

    def enqueue(self, new_data_):
        self.queue_[self.write_] = new_data_
        self.write_ += 1
        #Overload
        if self.write_ >= self.len_:
            self.write_ -= self.len_
        #Increase size
        if self.read_ == self.write_:
            self.queue_ = realloc(self.queue_, self.len_ * 2)
            for i in range(self.len_):
                if self.len_ - (i + 1) >= self.write_:
                    self.queue_[self.len_ * 2 - (i + 1)] = self.queue_[self.len_ - (i + 1)]
                else:
                    self.queue_[self.len_ * 2 - (i + 1)] = None
            self.read_ += self.len_
            self.len_ *= 2

    def print_tab(self):
        print(self.queue_)

    def print_queue(self):
        ind_start = self.read_
        ind_end = self.write_
        print('[', end=' ')
        if not self.is_empty():
            if ind_end <= ind_start:
                ind_end += self.len_
            for i in range(ind_end - ind_start):
                if ind_start + i >= self.len_:
                    print(self.queue_[i + ind_start - self.len_], end=' ')
                else:
                    print(self.queue_[i + ind_start], end=' ')
        print(']')
