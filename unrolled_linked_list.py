
"""
Zaimplementuj  rozwiniętą listę wiązaną (ang. unrolled linked list).  Zdefiniuj klasę reprezentującą element takiej listy - powinien on zawierać 'stałą' tablicę
(stworzoną analogicznie jak w poprzednim zadaniu - jej rozmiar może być pamiętany w zmiennej globalnej), jej aktualne wypełnienie (czyli liczbę aktualnie
znajdujących się w niej elementów) oraz wskazanie na następny element listy. Dodatkowo przydatne będą metody wstawiająca i usuwająca w miejscu wskazanym przez
indeks (z przesunięciem pozostałych elementów).

Następnie należy zaimplementować klasę reprezentującą listę, zawierającą metody:
konstruktor tworzący pustą listę
get - pobierająca daną spod podanego indeksu
insert - wstawiająca daną w miejscu wskazanym przez podany indeks, przesuwając istniejące elementy w prawo;  jeżeli tablica elementu w którym ma nastąpić wstawienie
jest pełna to do listy dokładany jest nowy element, połowa zapełnionej tablicy jest przenoszona do nowego elementu i wstawienie danej zachodzi albo w opróżnianym
elemencie albo we wstawianym (w zależności gdzie 'wypada' miejsce wskazane przez indeks). Podanie indeksu większego od aktualnej liczby elementów listy skutkuje
dodaniem elementu na końcu listy.
delete - usuwająca  daną spod podanego indeksu - dodatkowo jeżeli tablica jest zapełniona mniej niż w połowie z następnego elementu
listy jest do niej przenoszony pierwszy element tablicy; jeżeli to przeniesienie spowoduje, że zapełnienie tablicy w tym następnym elemencie
spadnie poniżej połowy wtedy wszystkie je elementy są przenoszone do tablicy we wcześniejszym elemencie listy (tej, z której usuwana była dana), a element listy
z pustą już tablicą jest usuwany.
"""

class Element:
    def __init__(self, size, next = None):
        self.tab_ = [None for _ in range(size)]
        self.wyp_ = 0
        self.next_ = next

    def insert(self, data, ind):
        if ind < self.wyp_:
            for i in range(ind, self.wyp_ + 1):
                if not self.tab_[i]:
                    tab_ = self.tab_[ind:i]
                    for j in range(len(tab_)):
                        self.tab_[ind + j + 1] = tab_[j]
        self.tab_[ind] = data
        self.wyp_ += 1

    def delete(self, ind):
        self.tab_[ind] = None
        for j in range(ind, self.wyp_ - 1):
            self.tab_[j] = self.tab_[j + 1]
            if j == self.wyp_ - 2:
                self.tab_[j + 1] = None
        self.wyp_ -= 1


class UnrolledLinkedList:
    def __init__(self, size):
        self.head_ = None
        self.size_ = size

    def get(self, ind):
        if self.head_:
            element = self.head_
            num_of_el = 0
            while element:
                new_ind = ind - num_of_el
                if new_ind < element.wyp_:
                    return element.tab_[new_ind]
                else:
                    element = element.next_
            return None
        else:
            raise ValueError("Empty list!")

    def insert(self, data, ind):
        if not self.head_:
            self.head_ = Element(self.size_)
        element = self.head_
        num_of_el = 0
        added = False
        last_el = False
        while element and not added:
            new_ind = ind - num_of_el
            if not element.next_:
                last_el = True
            if last_el and new_ind > element.wyp_ != self.size_:
                #Add to end
                element.insert(data, element.wyp_)
                added = True
            if last_el and new_ind == self.size_ == element.wyp_:
                element.next_ = Element(self.size_)
            if new_ind < element.wyp_ == self.size_:
                #Move half to next element and add
                rest = element.tab_[int(self.size_/2):]
                element.tab_[int(self.size_ / 2):] = [None for _ in range(int(self.size_ / 2))]
                num_of_rest = len(rest)
                #Add new element of the list
                new_elem = Element(self.size_)
                new_elem.next_ = element.next_
                element.next_ = new_elem
                new_elem.tab_[:num_of_rest] = rest
                element.wyp_ = self.size_ - num_of_rest
                new_elem.wyp_ = num_of_rest
                if new_ind <= element.wyp_:
                    #Add to first element
                    element.insert(data, new_ind)
                else:
                    #Add to new element
                    new_elem.insert(data, new_ind - element.wyp_)
                added = True
            elif new_ind <= element.wyp_ < self.size_:
                #Move rest right and add
                element.insert(data, new_ind)
                added = True
            if not added:
                num_of_el += element.wyp_
            element = element.next_

    def delete(self, ind):
        num_of_el = 0
        element = self.head_
        last_elem = False
        deleted = False
        while element and not deleted:
            new_ind = ind - num_of_el
            if not element.next_:
                last_elem = True
            if last_elem and new_ind >= element.wyp_:
                #Delete last element
                element.delete(element.wyp_ - 1)
                deleted = True
            if new_ind < element.wyp_:
                #Delete
                element.delete(new_ind)
                deleted = True
                if element.wyp_ <= int(self.size_/2) and not last_elem:
                    #Move one from next element
                    next_elem = element.next_
                    moved_ind = next_elem.tab_[0]
                    next_elem.delete(0)
                    element.insert(moved_ind, element.wyp_)
                    if next_elem.wyp_ <= int(self.size_/2):
                        #Move all from next to previous element
                        for i in next_elem.tab_:
                            if i:
                                element.insert(i, element.wyp_)
                        #Delete empty element
                        element.next_ = next_elem.next_
            if deleted:
                num_of_el -= element.wyp_
            element = element.next_

    def print_list(self):
        str = '[ '
        element = self.head_
        while element:
            for i in element.tab_:
                if i:
                    str += '{} '.format(i)
            element = element.next_
        str += ']'
        print(str)
