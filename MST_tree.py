
"""
Nasza implementacja:

potrzebujemy trzy dodatkowe listy: intree - czy wierzchołek jest w drzewie, distance - minimalna waga krawędzi dla danego wierzchołka, 
parent - “rodzic”/poprzedni wierzchołek w drzewie (do opisu krawędzi). Rozmiar n, inicjalizacja  odpowiednio: 0, duża liczba (np. float('inf')), -1.

potrzebujemy też struktury na nasze drzewo (MST) - proponuje się utworzyć graf o identycznych wierzchołkach jak wejściowy, ale na razie bez krawędzi,

startujemy z dowolnego wierzchołka,

całość działa w pętli while wykonywanej dopóki bieżący wierzchołek v jest poza drzewem tj. intree[v] == 0,

dodajemy wierzchołek do drzewa tj. intree[v]=1,

przeglądamy otoczenie aktualnie rozważanego wierzchołka:

sprawdzamy, czy waga krawędzi jest mniejsza od tej zapisanej w tablicy distance oraz czy wierzchołek nie jest już w drzewie,

jeśli warunek jest spełniony, to uaktualniamy tablicę distance oraz zapamiętujemy rodzica (parent),

szukamy kolejnego wierzchołka, który dodamy do drzewa:

musimy wykonać przegląd po wszystkich wierzchołkach (technicznie po tych, które nie są w drzewie),

szukamy takiego, który nie jest w MST oraz ma najmniejszą wartość w tablicy distance - czyli poszukiwana krawędź o najmniejszej wadze,

dodajemy do drzewa MST krawędź - technicznie dwie krawędzie - tu używamy informacji z listy parent,

warto też wyznaczyć sumę krawędzi tworzących drzewo - “długość” drzewa rozpinającego.


Weryfikacja:

Wczytujemy graf - dostarczony w pliku graf_mst.py. Uwaga. W odróżnieniu od wcześniej wykorzystywanej “mapy Polski”, tu nie mamy podwójnych 
krawędzi - zatem trzeba je dodać “ręcznie” tj. wczytujemy kolejne połączenie, np. krotkę (‘A’,’B’,4). Tworzymy wierzchołki ‘A’, ‘B’ oraz dwie 
krawędzie pomiędzy A->B i B->A obie z wagą 4.
Na rysunku mamy podane MST dla danego grafu. Wystarczy tylko sprawdzić, czy np. lista krawędzi w naszym MST jest identyczna.
"""

import graf_mst
from typing import List, Dict


class Vertex:
    def __init__(self, id: str, color=0):
        self.id = id
        self.color = color

    def set_color(self, color):
        self.color = color
        return

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
        for ver in self.id_dict:
            for edge in self.vertex_list[self.getVertexIdx(ver)]:
                if edge.ver2.id not in visited:
                    edges.append((ver, edge.ver2.id))
            visited.append(ver)
        return edges

    def get_weight(self, ver_idx1, ver_idx2):
        for edge in self.vertex_list[ver_idx1]:
            if self.getVertexIdx(edge.ver2.id) == ver_idx2:
                return edge.get_weight()
        else:
            return None


def prim(graph):
    n = graph.order()
    MST_tree = AdjacencyList()
    for ver_id in graph.id_dict:
        MST_tree.insertVertex(ver_id)
    intree = [0] * n
    distance = [1000] * n
    parent = [-1] * n
    v = 0
    while intree[v] == 0:
        intree[v] = 1
        neighbours = graph.neighbours(v)
        for neigh_idx in neighbours:
            w = graph.get_weight(v, neigh_idx)
            if intree[neigh_idx] == 0 and w < distance[neigh_idx]:
                distance[neigh_idx] = w
                parent[neigh_idx] = v
        min_distance = 1000
        min_distance_ver1 = 0
        min_distance_ver2 = 0
        for i in range(n):
            if distance[i] < min_distance and intree[i] == 0:
                min_distance = distance[i]
                min_distance_ver1 = parent[i]
                min_distance_ver2 = i
        if min_distance < 1000:
            MST_tree.insertEdge(MST_tree.getVertex(min_distance_ver2), MST_tree.getVertex(min_distance_ver1), min_distance)
            MST_tree.insertEdge(MST_tree.getVertex(min_distance_ver1), MST_tree.getVertex(min_distance_ver2), min_distance)
            v = min_distance_ver2
    return MST_tree

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
    G = graf_mst.graf
    graph = AdjacencyList()
    for edge in G:
        graph.insertEdge(edge[0], edge[1], edge[2])
        graph.insertEdge(edge[1], edge[0], edge[2])
    mst_tree = prim(graph)
    printGraph(mst_tree)


main()
