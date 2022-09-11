
"""
Kruskal-MST(G)

Umieść krawędzie w kolejce priorytetowej posortowane po wadze

    licznik = 0

    while (licznik < n-1 )

            pobierz następny wierzchołek (v,w)

            if (component(v) ≠ component(w))

                    dodaj do Tkruskal

                    połącz component(v) oraz component(w)


Analiza tego krótkiego kodu pokazuje, że jedyna “niewiadoma” to component. Pod tym skrótem kryje się operacja sprawdzenia, czy wierzchołki (v,w) 
należą do tego samego pod-drzewa - bo łączymy przecież w każdym kroku krawędź z drzewa Tkruskal z krawędzią spoza drzewa. Zatem zadanie musimy rozpocząć 
od struktury Union-Find (struktura zbiorów rozłącznych). Uwaga. Oczywiście algorytm można zaimplementować bez tego typu struktury, jednak nie będzie to 
rozwiązanie specjalnie efektywne.

Union-Find

Potrzebujemy struktury, która dla ustalonego zbioru (tu grafu/drzewa) przechowuje podział na mniejsze, rozłączne zbiory (sub-grafy/sub-drzewa). Opis 
problemu można również znaleźć na Wikipedii. W kontekście algorytmu Kruskala potrzebne są dwie operacje:
same_component(v,w) - czy wierzchołki v i w są w tym samym sub-drzewie,
merge_component(C1,C2) - połączyć dwa pod-drzewa (zbiory) poprzez dodanie łączącej ich krawędzi.

Na początek rozważmy dwa proste, narzucające się rozwiązania:

możemy poetykietować każdy z wierzchołków (elementów zbioru). Wtedy łatwo (szybko) sprawdzimy, czy dwa wierzchołki są w tym samym zbiorze. Problem 
pojawi się natomiast przy łączeniu - “przeetykietowanie” wymaga przejścia po strukturze (zatem czas liniowy).

możemy traktować łączenie jako wstawianie krawędzi do grafu, ale wtedy pojawia się problem przy pierwszym teście - musimy “zwiedzić” graf.


Potrzebujemy zatem czegoś innego - właśnie struktury zbiorów rozłącznych (Union-Find). W tym przypadku każdy z pod-zbiorów reprezentowany jest jako 
“wsteczne” drzewo - poszczególne elementy wskazują “w stronę” korzenia. Jednocześnie etykieta korzenia (root) jest też etykietą całego pod-drzewa. 
Dodatkowo, każdy element “pamięta” rozmiar pod-drzewa, którego jest lokalnym korzeniem. Wymienione funkcjonalności można uzyskać z wykorzystaniem 
dwóch tablic (list).


Struktura Union-Find udostępnia dwie operacje (jak sama nazwa wskazuje:)):

Find(v) - znajdź korzeń dla elementu v (co oznacza przejście od elementu “w górę” do korzenia)

Union(u,v) - połącz korzeń elementu u z korzeniem elementu v.


Musimy teraz zadbać o to, aby czas dla dowolnej liczby operacji Find i Union był jak najmniejszy. Wpływ na to ma wysokość drzewa. Należy przy tym z
wrócić uwagę, że drzewa mogą dość łatwo stać się niezrównoważone, a kontrolę nad tym mamy poprzez wybór, który z dwóch dotychczasowych korzeni, 
będzie korzeniem połączonego drzewa.

Tu ustalamy, że mniejsze pod-drzewo stanie się elementem większego pod-drzewa. Dlaczego? Dla większego pod-drzewa wysokość (poziom) wszystkich 
elementów zostaje taki sam, a dla mniejszego zwiększa się o jeden (dodajemy korzeń). Stąd wysokość zmienia się dla mniejszej liczby elementów.


Implementacja:

tworzymy klasę, w trakcie inicjalizacji tworzymy trzy zmienne - dwie wspomniane listy (wskaźnik na rodzica - p, oraz wielkość - size) oraz n - 
rozmiar struktury. Listy inicjujemy: p - numerem wierzchołka, size - 1.

implementujemy metodę find(v) - jeśli root(v) == v to znaczy, że v jest korzeniem i zwracamy v, w przeciwnym wypadku, rekurencyjnie szukamy korzenia,

implementujemy metodę union_sets(s1,s2) - na początku wyznaczamy korzenie dla s1 i s2, jeśli są one równe, oznacza to, że elementy są w tym samym 
pod-zbiorze i nic nie musimy robić. W przeciwnym przypadku sprawdzamy rozmiary pod-drzew, które mamy łączyć - zgodnie z opisem, mniejsze podpinamy 
pod większe (odpowiedni zapis w p) oraz uaktualniamy size.

implementujemy metodę same_component(s1,s2) - sprawdzamy, czy korzeń s1 == korzeń s2.


Prosty test:

Stwórzmy sobie zbiór 5 wierzchołków i przeprowadźmy kilka testów. Połączmy np. 1-2 i 4-5. Sprawdźmy, czy są połączone 1-2, 2-3, 4-5. 
Połączmy 3-1 i ponownie sprawdźmy. Jeśli wszystko działa poprawnie, to przechodzimy do kolejnego kroku.


Implementacja algorytmu Kruskala:

tworzymy graf testowy (podobnie jak w podstawowym zadaniu), wykorzystujemy rozwijaną strukturę - można przenieść do osobnego pliku,

pobieramy listę krawędzi i sortujemy ją - tym razem malejąco,

tworzymy strukturę Union-Find o takiej liczbie wierzchołków jak mamy w grafie - tu ew. może być potrzebne dodanie prostej funkcji do klasy opisującej graf,

w pętli po liście krawędzi:

pobieramy kolejną krawędź i sprawdzamy, czy wierzchołki są w tym samym pod-zbiorze,

jeśli nie, to łączymy oba pod-drzewa.


Uwaga. Należy zaimplementować “przekodowanie” etykiet z grafu (duże litery alfabetu) na liczby - np. wykorzystać wartość kodu ASCII. Sprawdźmy, 
czy otrzymaliśmy poszukiwaną listę krawędzi.
"""

from typing import List, Dict, Tuple
import graf_mst

class Vertex:
    def __init__(self, id_: str):
        self.id = id_

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)


class Edge:
    def __init__(self, ver1: Vertex, ver2: Vertex, weight: int = 1):
        self.ver1 = ver1
        self.ver2 = ver2
        self.weight = weight

    def __eq__(self, other):
        return self.ver1 == other.ver1 and self.ver2 == other.ver2

    def __hash__(self):
        return hash(self.ver2)

    def get_weight(self):
        return self.weight


class AdjacencyList:
    def __init__(self, id_dict: Dict = None, vertex_list: List[List[Edge]] = None):
        if vertex_list is None:
            vertex_list = []
        if id_dict is None:
            id_dict = {}
        self.id_dict = id_dict
        self.vertex_list = vertex_list

    def insertVertex(self, ver_id: str):
        new_idx = self.order()
        self.vertex_list.append([])
        self.id_dict[ver_id] = new_idx
        return

    def insertEdge(self, ver1_id: str, ver2_id: str, weight: int = 1):
        if ver1_id not in self.id_dict:
            self.insertVertex(ver1_id)
        if ver2_id not in self.id_dict:
            self.insertVertex(ver2_id)
        idx1 = self.getVertexIdx(ver1_id)
        # idx2 = self.getVertexIdx(ver2_id)
        self.vertex_list[idx1].append(Edge(Vertex(ver1_id), Vertex(ver2_id), weight))
        return

    def deleteVertex(self, ver_id: str):
        # Delete vertex from adjacency list
        self.vertex_list.pop(self.getVertexIdx(ver_id))
        for idx, neighbours in enumerate(self.vertex_list):
            neighbours2 = [edge.ver2.id for edge in neighbours]
            if ver_id in neighbours2:
                self.deleteEdge(self.getVertex(idx), ver_id)
        deleted = False
        for ver in self.id_dict:
            if not deleted:
                if ver == ver_id:
                    deleted = True
            else:
                self.id_dict[ver] -= 1
        self.id_dict.pop(ver_id)
        return

    def deleteEdge(self, ver1_id: str, ver2_id: str):
        idx1 = self.getVertexIdx(ver1_id)
        # idx2 = self.getVertexIdx(ver2_id)
        self.vertex_list[idx1].remove(Edge(Vertex(ver1_id), Vertex(ver2_id)))
        return

    def getVertexIdx(self, ver_id: str):
        if ver_id in self.id_dict:
            return self.id_dict[ver_id]
        else:
            raise ValueError('Invalid vertex id')

    def getVertex(self, idx: int):
        for ver in self.id_dict:
            if self.getVertexIdx(ver) == idx:
                return ver
        else:
            raise ValueError('Invalid index')

    def neighbours(self, idx: int):
        neighbours = self.vertex_list[idx]
        return [self.getVertexIdx(edge.ver2.id) for edge in neighbours]

    def order(self):
        return len(self.vertex_list)

    def size(self):
        return len(self.edges())

    def edges(self):
        # [(X, Y), ...]
        visited = []
        edges = []
        for ver in self.id_dict.values():
            for edge in self.vertex_list[ver]:
                if edge.ver2.id not in visited:
                    edges.append((edge.ver1.id, edge.ver2.id, edge.weight))
            visited.append(ver)
        return edges

    def vertexes(self):
        return list(self.id_dict.keys())

    def get_weight(self, ver_idx1, ver_idx2):
        for edge in self.vertex_list[ver_idx1]:
            if self.getVertexIdx(edge.ver2.id) == ver_idx2:
                return edge.get_weight()
        else:
            return None


class UnionFind:
    def __init__(self, vertexes):
        n = max(vertexes) + 1
        self.parent: List[int] = [0] * n
        for i in vertexes:
            self.parent[i] = i
        self.size: List[int] = [1] * n
        self.n = n

    def __repr__(self):
        return str(self.parent)

    def find(self, v):
        if self.parent[v] == v:
            return v
        else:
            return self.find(self.parent[v])

    def same_components(self, s1, s2):
        if self.find(s1) == self.find(s2):
            return True
        else:
            return False

    def union_sets(self, s1, s2):
        print(convert2str(s1), convert2str(s2))
        p1, p2 = self.find(s1), self.find(s2)
        if self.size[p1] >= self.size[p2]:
            self.parent[p2] = p1
            self.size[p1] += 1
        else:
            self.parent[p1] = p2
            self.size[p2] += 1
        return


def convert2int(letter: str):
    # Tylko duże litery, ale żeby zaczynało się od zera
    return ord(letter) - 65

def convert2str(digit: int):
    return chr(digit + 65)

def third_elem(tup: Tuple):
    return tup[2]

def kruskal(edges: List[Tuple]):
    graph = AdjacencyList()
    for edge in edges:
        graph.insertEdge(edge[0], edge[1], edge[2])
    edges2 = graph.edges()
    edges2.sort(key=third_elem, reverse=True)
    vertexes = graph.vertexes()
    if isinstance(vertexes[0], str):
        for i in range(len(vertexes)):
            vertexes[i] = convert2int(vertexes[i])
    union_find = UnionFind(vertexes)
    while edges2:
        edge = edges2.pop()
        ver1, ver2 = edge[0], edge[1]
        if isinstance(ver1, str) and isinstance(ver2, str):
            ver1, ver2 = convert2int(ver1), convert2int(ver2)
        if not union_find.same_components(ver1, ver2):
            union_find.union_sets(ver1, ver2)
    return union_find

def printGraph(g):
    n = g.order()
    print("------GRAPH------", n)
    for i in range(n):
        v = g.getVertex(i)
        print(v, end=" -> ")
        nbrs = g.neighbours(i)
        for j in nbrs:
            print(g.getVertex(j), g.get_weight(i, j), end=";")
        print()
    print("-------------------")

def main():
    vertexes = graf_mst.graf
    print("Dodane krawędzie:")
    print(kruskal(vertexes))


main()
