
"""
Zaimplementuj w języku Python drzewo AVL przerabiając program z poprzedniego zadania (np. przez dziedziczenie).
Klasa reprezentująca węzeł drzewa powinna zawierać dodatkowe pole określające współczynnik wyważenia (lub pola pamiętające wysokość poddrzew).
Klasa reprezentująca drzewo powinna mieć zmodyfikowane metody dodawania i usuwania węzłów (szczegóły poniżej).

Drzewo AVL zachowuje własności BST i posiada dodatkową cechę, która określa uporządkowanie węzłów w określony sposób. 
Każdy węzeł posiada wspólczynnik wyważenia, który jest równy różnicy wysokości lewego i prawego poddrzewa. Może wynosić 0, +1 lub -1.
 Po wykonaniu operacji dodawania lub usuwania węzłów odbywa się określona operacja rotacji węzłów, która przywraca zrównoważenie drzewa binarnego.

Zaimplementuj funkcjonalności takie jak w drzewie BST w poprzednim zadaniu. Należy jednak tym razem przy dodawaniu i usuwaniu węzłów uwzględnić
równoważenie drzewa. Przykładowo - jeśli węzeł jest dodany do lewego rozgałęzienia to współczynnik wyważenia jest zwiększany o  1, a jeśli do prawego
zmniejszany o 1 (tak przyjęto w poniższym przykładzie, ale kwestia kiedy stosować -1 a kiedy +1 jest umowna). W przypadku braku zrównoważenia drzewa AVL 
(współczynnik mniejszy od -1 lub większy od 1) konieczna jest odpowiednia rotacja odpowiednich węzłów. W tym celu należy zaimplementować funkcje,
które będą realizować rotację w lewo oraz rotację w prawo. 

Będą one przydatne w uwzględnieniu czterech przypadków:
pojedyczna rotacja LL (ang. left-left)
pojedyncza rotacja RR (ang. right-right)
podwójna rotacja RL (ang. right-left)
podwójna rotacja LR (ang. left-right)
Oznaczenia RR, LL, RL i LR określają sposób połączenia węzłów przed wykonaniem rotacji.

W przypadku braku zrównoważenia drzewa AVL konieczna jest odpowiednia rotacja konkretnych węzłów.

Współczynnik wyważenia korzenia jest mniejszy od zera, więc wymaga rotacji w lewo. Dodatkowo sprawdzany jest współczynnik wyważenia prawego dziecka.
Jeśli dziecko ma współczynnik wyważenia większy od zera (dłuższa lewa gałąź) to rotuj w prawo względem dziecka a następnie w lewo względem korzenia.

Podczas aktualizacji współczynnika wyważenia możliwe jest wywoływanie funkcji zwracającej wysokość poddrzewa (jest to opcja nieefektywna obliczeniowo, 
lecz dozwolona do tego zadania). 
"""

class Node:
    def __init__(self, key, value, left=None, right=None):
        self.key_ = key
        self.value_ = value
        self.left_ = left
        self.right_ = right
        self.balance_ = 0
    def __str__(self):
        return str(self.key_)


class TreeBST:
    def __init__(self):
        self.head_ = None

    def search(self, key, node='unset'):
        if isinstance(node, str):
            node = self.head_
        if node:
            result = None
            if key < node.key_:
                result = self.search(key, node.left_)
            elif key > node.key_:
                result = self.search(key, node.right_)
            else:
                return node.value_
            return result
        else:
            raise ValueError("Drzewo jest puste")

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
        hs = [0]
        if node.left_:
            hs.append(self.height(node.left_, h + 1))
        if node.right_:
            hs.append(self.height(node.right_, h + 1))
        if not node.left_ and not node.right_:
            hs.append(h)
        if any(hs):
            return max(hs)
        else:
            return 0

class TreeAVL(TreeBST):
    def __init__(self):
        super().__init__()

    def left_rotation(self, node):
        node.right_.left_ = node
        node.right_.balance_ += 1
        return node.right_

    def right_rotation(self, node):
        node.left_.right_ = node
        node.left_.balance_ -= 1
        return node.left_

    def actual_balance(self, node):
        if node.left_ and node.right_:
            return self.height(node.left_) - self.height(node.right_)
        elif node.left_:
            return self.height(node.left_) + 1
        elif node.right_:
            return -self.height(node.right_) - 1
        else:
            return 0

    def rotate(self, node):
        if node.balance_ > 0:
            # xR
            if node.left_.balance_ > 0:
                # RR
                if node.left_.right_:
                    acc = node.left_.right_
                else:
                    acc = None
                if self.head_.key_ == node.key_:
                    self.head_ = self.right_rotation(node)
                    node = self.head_
                else:
                    node = self.right_rotation(node)
                node.right_.left_ = acc
                node.balance_ = self.actual_balance(node)
                node.right_.balance_ = self.actual_balance(node.right_)
            else:
                # LR
                if node.left_.right_.left_:
                    acc = node.left_.right_.left_
                else:
                    acc = None
                node.left_ = self.left_rotation(node.left_)
                node.left_.left_.right_ = acc
                if node.left_.right_:
                    acc2 = node.left_.right_
                else:
                    acc2 = None
                if self.head_.key_ == node.key_:
                    self.head_ = self.right_rotation(node)
                    node = self.head_
                else:
                    node = self.right_rotation(node)
                node.right_.left_ = acc2
                node.balance_ = self.actual_balance(node)
                node.left_.balance_ = self.actual_balance(node.left_)
                node.right_.balance_ = self.actual_balance(node.right_)
                if node.right_.left_:
                    node.right_.left_.balance_ = self.actual_balance(node.right_.left_)
        else:
            # xL
            if node.right_.balance_ > 0:
                # RL
                if node.right_.left_.right_:
                    acc = node.right_.left_.right_
                else:
                    acc = None
                node.right_ = self.right_rotation(node.right_)
                node.right_.right_.left_ = acc
                if node.right_.left_:
                    acc2 = node.right_.left_
                else:
                    acc2 = None
                if self.head_.key_ == node.key_:
                    self.head_ = self.left_rotation(node)
                    node = self.head_
                else:
                    node = self.left_rotation(node)
                node.left_.right_ = acc2
                node.balance_ = self.actual_balance(node)
                node.left_.balance_ = self.actual_balance(node.left_)
                node.right_.balance_ = self.actual_balance(node.right_)
                if node.left_.right_:
                    node.left_.right_.balance_ = self.actual_balance(node.left_.right_)
            else:
                # LL
                if node.right_.left_:
                    acc = node.right_.left_
                else:
                    acc = None
                if self.head_.key_ == node.key_:
                    self.head_ = self.left_rotation(node)
                    node = self.head_
                else:
                    node = self.left_rotation(node)
                node.left_.right_ = acc
                node.balance_ = self.actual_balance(node)
                node.left_.balance_ = self.actual_balance(node.left_)
        return node

    def insert_(self, key, value, node='unset'):
        if isinstance(node, str):
            if not self.head_:
                #Add first node
                self.head_ = Node(key, value)
                return
            node = self.head_
        if not node:
            return Node(key, value)
        if key < node.key_:
            node.left_ = self.insert_(key, value, node.left_)
            node.balance_ = self.actual_balance(node)
            new_node = node
            if node.balance_ >= 2 or node.balance_ <= -2:
                new_node = self.rotate(node)
            return new_node
        elif key > node.key_:
            node.right_ = self.insert_(key, value, node.right_)
            node.balance_ = self.actual_balance(node)
            new_node = node
            if node.balance_ >= 2 or node.balance_ <= -2:
                new_node = self.rotate(node)
            return new_node
        else:
            node.value_ = value
            return node

    def delete_(self, key, node='unset'):
        if isinstance(node, str):
            node = self.head_
        if node:
            if key > node.key_:
                node.right_ = self.delete_(key, node.right_)
                node.balance_ = self.actual_balance(node)
                new_node = node
                if node.balance_ >= 2 or node.balance_ <= -2:
                    new_node = self.rotate(node)
                return new_node
            elif key < node.key_:
                node.left_ = self.delete_(key, node.left_)
                node.balance_ = self.actual_balance(node)
                new_node = node
                if node.balance_ >= 2 or node.balance_ <= -2:
                    new_node = self.rotate(node)
                return new_node
            else:
                # Found
                if not node.left_ and not node.right_:
                    # Node without child nodes
                    return None
                elif not node.left_ and node.right_:
                    # Node with one child node on right side
                    return node.right_
                elif node.left_ and not node.right_:
                    # Node with one child node on left side
                    return node.left_
                else:
                    # Node with two child nodes
                    parent = node.right_
                    if parent.left_:
                        child = parent.left_
                        while child.left_:
                            parent = child
                            child = child.left_
                        node.value_ = child.value_
                        node.key_ = child.key_
                        if child.right_:
                            parent.left_ = child.right_
                        else:
                            parent.left_ = None
                    else:
                        parent.left_ = node.left_
                        node = parent

                    node.balance_ = self.actual_balance(node)
                    new_node = node
                    if node.balance_ >= 2 or node.balance_ <= -2:
                        new_node = self.rotate(node)
                    return new_node

        else:
            return None

def main():
    dict = {50:'A', 15:'B', 62:'C', 5:'D', 2:'E', 1:'F', 11:'G', 100:'H', 7:'I', 6:'J', 55:'K', 52:'L', 51:'M', 57:'N', 8:'O', 9:'P', 10:'R', 99:'S', 12:'T'}
    tree = TreeAVL()
    for key in dict:
        tree.insert_(key, dict[key])
    tree.print_tree()
    tree.print()
    print(tree.search(10))
    tree.delete_(50)
    tree.delete_(52)
    tree.delete_(11)
    tree.delete_(57)
    tree.delete_(1)
    tree.delete_(12)
    tree.insert_(3, 'AA')
    tree.insert_(4, 'BB')
    tree.delete_(7)
    tree.delete_(8)
    tree.print_tree()
    tree.print()

main()