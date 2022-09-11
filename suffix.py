
"""
Jednym ze sposobów bardzo szybkiego wyszukiwania wzorców w tekście jest wykorzystanie drzewa sufiksowego. Otrzymujemy je poprzez odpowiednie 
przekształcenie tekstu, w którym ma się odbywać poszukiwanie. Można wtedy znaleźć w tym tekście dowolny wzorzec w czasie proporcjonalnym do jego długości, 
co jest zwykle bardzo szybkie. Przetwarzanie tekstu może natomiast zająć więcej czasu.

Drzewo sufiksowe to skompresowane drzewo Trie dla wszystkich sufiksów występujących w tekście. Aby zbudować drzewo sufiksowe, należy najpierw wygenerować 
sufiksy dla całego tekstu. Następnie otrzymane sufiksy potraktować jako oddzielne słowa i zbudować dla nich skompresowane drzewo Trie, tzn. takie, 
że połączone są fragmenty, w których węzły mają tylko jednego potomka. W ogólności można najpierw zbudować zwykłe drzewo Trie, a dopiero potem je 
skompresować. Przykładowo, mając tekst “banana\0”, otrzymujemy sufiksy:

banana\0
anana\0
nana\0
ana\0
na\0
a\0
\0

Tablica sufiksowa to posortowana tablica wszystkich sufiksów danego ciągu. Przewaga tablic nad drzewami sprowadza się do łatwiejszej konstrukcji w 
czasie O(n) i mniejszych wymagań pamięciowych. 

Metoda naiwna budowy tablicy sufiksowej: wyznacz wszystkie sufiksy ciągu i oznacz je indeksami, wpisz do tablicy, a następnie posortuj w kolejności 
alfabetycznej. Tablicę sufiksową stanowią indeksy kolejnych sufiksów po posortowaniu.

Przykład dla „banana\0”:

0 banana\0                                6 \0
1 anana\0     Posortuj sufiksy             5 a\0
2 nana\0      ---------------->             3 ana\0
3 ana\0        alfabetycznie                 1 anana\0
4 na\0                                        0 banana\0
5 a\0                                          4 na\0  
6 \0                                            2 nana\0

Tablica sufiksowa dla "banana\0" to {6, 5, 3, 1, 0, 4, 2}. 

Następnie można zastosować przeszukiwanie binarne do znalezienia wybranego wzorca, przechodząc za każdym razem do prawej lub lewej połowy tablicy, 
w zależności od kolejności alfabetycznej między sufiksami a poszukiwanym wzorcem.

Skonstruuj tablicę sufiksową dla wybranego ciągu (może być „banana\0”) i wyszukaj przykładowy wzorzec.

Taką tablicę można również skonstruować z drzewa sufiksowego poprzez przejście po nim DFS w kolejności alfabetycznej. Indeksy 0...N-1 w tablicy 
odpowiadają liściom w kolejności odwiedzenia. Natomiast wartości przechowywane w tych liściach (a zatem i w elementach tablicy) to indeksy kolejnych 
sufiksów od 0 (dla całego tekstu, np. banana\0) do N-1 (dla ostatniego znaku, np. \0) - jak w przykładzie powyżej.
"""

from typing import List, Dict

class Node:
    def __init__(self, key: str, index: int, branches: list = None):
        self.key = key  # str
        self.index = index
        self.branches = branches


def get_suffixes(word: str) -> List[str]:
    # Ustawienie suffixów
    suffixes = []
    for i in range(len(word)):
        suffixes.append(word[i:])
    return suffixes


def get_common(suffixes):
    # Szukanie części wspólnej
    common = ''
    j = 0
    while True:
        for i in range(1, len(suffixes)):
            if suffixes[i][j] != suffixes[i - 1][j]:
                return [suff[j:] for suff in suffixes], common
        common += suffixes[0][j]
        j += 1


class Trie:
    def __init__(self, word: str):
        self.head = Node('', 0)
        self.set_branches(get_suffixes(word), self.head)
        return

    def set_branches(self, suffixes: List[str] = None, node: Node = None):
        # Przypisanie tekstu i indexu do gałęzi
        n = len(suffixes)
        if node != self.head:
            if n > 1:
                suffixes, common = get_common(suffixes)
                node.key = common
            else:
                node.key = suffixes[0]

        if n > 1:
            # Szukanie gałęzi i ich indexu
            branches = []
            idxs = []
            idx = node.index
            for suff in suffixes:
                if suff[0] not in branches:
                    branches.append(suff[0])
                    idxs.append(idx)
                idx += 1

            # Ustawianie kolejnych podgałęzi
            node.branches = []
            for i in range(len(branches)):
                node.branches.append(Node(branches[i], idxs[i]))
                branch_suffixes = []
                for suff in suffixes:
                    if suff[0] == branches[i]:
                        branch_suffixes.append(suff)
                self.set_branches(branch_suffixes, node.branches[i])

    def print_trie(self, node=None, acc=0):
        if node is None:
            print('---Head---')
            node = self.head
        if node.branches:
            print('     ' * acc, '->', node.key, end='')
            for branch in node.branches:
                self.print_trie(branch, acc + 1)
        else:
            print('     ' * acc, '->', node.key)


class SuffixTab:
    def __init__(self, word: str):
        self.key = word
        self.tab = []
        unsorted_suff = get_suffixes(word)

        # Przypisanie indexów
        idx_dict = {}
        idx = 0
        for suff in unsorted_suff:
            idx_dict[suff] = idx
            idx += 1

        # Sortowanie
        self.tab = sort_suffixes(idx_dict)
        # print(unsorted_suff[self.tab[1]])

    def print_tab(self):
        print(self.tab)
        return


def sort_suffixes(idx_dict):
    suffixes = [key for key in idx_dict.keys()]
    suffixes.sort()
    sorted_idxs = []
    for suff in suffixes:
        sorted_idxs.append(idx_dict[suff])
    return sorted_idxs

def compute_leaves(trie, node=None, acc=0):
    if node is None:
        node = trie.head
    for branch in node.branches:
        if not branch.branches:
            acc += 1
        else:
            acc += compute_leaves(trie, branch, acc)
    return acc

def match_trie(trie, word, node=None, acc=0):
    if node is None:
        node = trie.head
    for branch in node.branches:
        if branch.key[0] == word[0]:
            # flag = False
            acc += 1
            i = 1
            while i < len(branch.key) and i < len(word):
                if branch.key[i] != word[i]:
                    return 0
                else:
                    i += 1
                    acc += 1
            if i == len(word):
                if branch.branches:
                    # Licz liście
                    return compute_leaves(trie, branch)
                else:
                    return 1
            elif i == len(branch.key):
                if branch.branches:
                    return match_trie(trie, word[acc:], branch, acc)
                else:
                    return 0

def match_tab(tab, word):
    start, end = 0, len(tab.tab) - 1
    result = 0
    while start <= end:
        i = (start + end) // 2
        if tab.key[tab.tab[i]][0] < word[0]:
            start = i + 1
        elif tab.key[tab.tab[i]][0] > word[0]:
            end = i - 1
        else:
            # Szukanie pierwszego, który się zgadza
            while i > 0 and tab.key[tab.tab[i - 1]][0] == word[0]:
                i -= 1
            while i < len(tab.tab) and tab.key[tab.tab[i]][0] == word[0]:
                if word == tab.key[tab.tab[i]: tab.tab[i] + len(word)]:
                    result += 1
                i += 1
            return result
    return 0

def main():
    word = 'banana\0'
    trie = Trie(word)
    trie.print_trie()
    print(match_trie(trie, 'na'))
    tab = SuffixTab(word)
    tab.print_tab()
    print(match_tab(tab, 'na'))


main()
