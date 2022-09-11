
"""
Zaimplementuj w języku Python drzewo binarne BST. Niech będzie zaimplementowane za pomocą dwóch klas: pierwsza klasa zawiera pole root wskazujące na 
korzeń drzewa (ang. root node), druga klasa reprezentuje węzeł drzewa i zawiera cztery pola: klucz, wartość oraz wskaźniki na dwa węzły dzieci 
(ang. child node) - prawe i lewe rozgałęzienie.

Zaimplementuj poniższe funkcjonalności:
konstruktor - tworzy obiekt reprezentujący drzewo z polem root ustawionym na None
search - wyszukująca i zwracająca wartość odpowiadającą podanemu kluczowi (lub None)
insert - wstawiająca daną wg podanego klucza, jeżeli element o takim kluczu istnieje, jego wartość powinna zostać nadpisana (funkcja pamięta poprzednika,
patrz wykład)
delete -  usuwająca daną o podanym kluczu
print - wypisująca zawartość drzewa jako listę od najmniejszego do największego klucza w formie klucz:wartość
height - metoda zwracająca wysokość drzewa od podanego węzła do węzła nieposiadającego kolejnych potomków (leaf node)  - najdłuższa ścieżka w drzewie

Funkcja search wykonuje wyszukiwanie elementu w drzewie na podstawie klucza w wersji rekurencyjnej.
Funkcja insert tworzy kolejne elementy drzewa na podstawie podanego klucza, prawe rozgałęzienie zawiera klucze większe niż klucz w węźle rodzic (parent node),
lewe rozgałęzenie zawiera klucze mniejsze niż klucz w węźle rodzic.

Funkcja delete usuwa element drzewa na podstawie podanego klucza. Należy uwzględnić trzy przypadki:
usunięcie węzła, który nie posiada węzłów dzieci (child nodes)
usunięcie węzła z jednym dzieckiem 
usunięcie węzła, który posiada dwa węzły dzieci - usuwany węzeł zastępujemy minimalnym kluczem z prawego poddrzewa (ang. right subtree) - successor node
"""

class Node:
    def __init__(self, key, value, left=None, right=None):
        self.key_ = key
        self.value_ = value
        self.left_ = left
        self.right_ = right


class TreeBST:
    def __init__(self):
        self.head_ = None

    def search(self, key):
        if self.head_:
            node = self.head_
            while node:
                if key < node.key_:
                    node = node.left_
                elif key > node.key_:
                    node = node.right_
                else:
                    return node.value_
            return None
        else:
            raise ValueError("Drzewo jest puste")

    def insert(self, key, value, node='unset'):
        if isinstance(node, str):
            if not self.head_:
                #Add first node
                self.head_ = Node(key, value)
                return
            node = self.head_
        if not node:
            return Node(key, value)
        if key < node.key_:
            node.left_ = self.insert(key, value, node.left_)
            return node
        elif key > node.key_:
            node.right_ = self.insert(key, value, node.right_)
            return node
        else:
            node.value_ = value
            return node

    def delete(self, key, node='unset'):
        if isinstance(node, str):
            node = self.head_
        if node:
            if key > node.key_:
                node.right_ = self.delete(key, node.right_)
                return node
            elif key < node.key_:
                node.left_ = self.delete(key, node.left_)
                return node
            else:
                #Found
                if not node.left_ and not node.right_:
                    #Node without child nodes
                    return None
                elif not node.left_ and node.right_:
                    #Node with one child node on right side
                    return node.right_
                elif node.left_ and not node.right_:
                    #Node with one child node on left side
                    return node.left_
                else:
                    #Node with two child nodes
                    parent = node.right_
                    if parent.left_:
                        child = parent.left_
                    else:
                        parent.left_ = node.left_
                        return parent
                    while child.left_:
                        parent = child
                        child = child.left_
                    node.value_ = child.value_
                    node.key_ = child.key_
                    if child.right_:
                        parent.left_ = child.right_
                    else:
                        parent.left_ = None
                    return node
        else:
            return None

    def print(self, node='unset'):
        str_ = ''
        first = False
        if isinstance(node, str):
            first = True
            node = self.head_
            str_ += '{'
        if node:
            if node.left_:
                str_ += self.print(node.left_)
            str_ += '{}:{} '.format(node.key_, node.value_)
            if node.right_:
                str_ += self.print(node.right_)
            if first:
                print(str_, '}')
            return str_
        else:
            return

    def print_tree(self):
        print("==============")
        self._print_tree(self.head_, 0)
        print("==============")

    def _print_tree(self, node, lvl):
        if node:
            self._print_tree(node.right_, lvl + 5)
            print()
            print(lvl*" ", node.key_, node.value_)
            self._print_tree(node.left_, lvl + 5)


    def height(self, node='unset', h=0):
        if isinstance(node, str):
            node = self.head_
        hs = [1]
        if node.left_:
            hs.append(self.height(node.left_, h + 1))
        if node.right_:
            hs.append(self.height(node.right_, h + 1))
        if not node.left_ and not node.right_:
            hs.append(h)
        if any(hs):
            return max(hs)


def main():
    tree = TreeBST()
    nodes = {
        50:'A',
        15:'B',
        62:'C',
        5:'D',
        20:'E',
        58:'F',
        91:'G',
        3:'H',
        8:'I',
        37:'J',
        60:'K',
        24:'L'
    }

    for key in nodes.keys():
        tree.insert(key, nodes[key])

    tree.print_tree()
    tree.print()
    print(tree.search(24))
    tree.insert(20, 'AA')
    tree.insert(6, 'M')
    tree.delete(62)
    tree.insert(59, 'N')
    tree.insert(100, 'P')
    tree.delete(8)
    tree.delete(15)
    tree.insert(55, 'R')
    tree.delete(50)
    tree.delete(5)
    tree.delete(24)
    print(tree.height())
    tree.print()
    tree.print_tree()

main()



