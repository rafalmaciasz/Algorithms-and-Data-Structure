
"""
Problem maksymalnego przepływu polega na znalezieniu dla danej sieci przepływowej dopuszczalnego przepływu o maksymalnej wartości.
Sieć przepływowa to graf skierowany, w którym każda krawędź ma nieujemną przepustowość oraz występują dwa specjalne wierzchołki s i t.
Twierdzenie maksymalny przepływ/minimalne cięcie mówi, że w sieci przepływowej maksymalna wartość przepływu od źródła (source - s) do ujścia (sink - t) 
równa się łącznej wadze krawędzi w minimalnym cięciu, tzn. najmniejszej łącznej wadze krawędzi, która spowoduje oddzielenie źródła od ujścia. 

Koncepcja i realizacja. Jak już wszystko przygotowaliśmy, to możemy złożyć gotowy algorytm. Zaczynamy od przeszukania BFS grafu, sprawdzenia, 
czy istnieje ścieżka od wierzchołka początkowego do końcowego, oraz obliczenia dla niej minimalnego przepływu. Potem w pętli while, jeśli minimalny 
przepływ > 0, będą się wykonywać następujące kroki:

augmentacja ścieżki,

BFS,

obliczanie nowej wartości minimalnego przepływu.

Na koniec należy zwrócić sumę przepływów przez krawędzie wchodzące do wierzchołka końcowego.

W main-ie proszę utworzyć grafy dla poniższych przykładów testowych. Dla każdego proszę wypisać:
- znaleziony przepływ
- graf po operacji znajdowania przepływu (funkcją printGraph)
"""

from typing import List, Dict, Union

class Vertex:
    def __init__(self, id_: str):
        self.id = id_

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)


class Edge:
    def __init__(self, ver1: Vertex, ver2: Vertex, weight: int = 1,  res: bool = False):
        self.ver1 = ver1
        self.ver2 = ver2
        self.weight = weight
        self.flow = 0
        self.residual = weight
        self.isResidual = res

    def __eq__(self, other):
        return self.ver1 == other.ver1 and self.ver2 == other.ver2

    def __hash__(self):
        return hash(self.ver2)

    def __str__(self):
        return str(self.weight) + str(self.flow) + str(self.residual) + str(self.isResidual)

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

    def insertEdge(self, ver1_id: str, ver2_id: str, weight: int = 1, res: bool = False):
        if ver1_id not in self.id_dict:
            self.insertVertex(ver1_id)
        if ver2_id not in self.id_dict:
            self.insertVertex(ver2_id)
        idx1 = self.getVertexIdx(ver1_id)
        # idx2 = self.getVertexIdx(ver2_id)
        self.vertex_list[idx1].append(Edge(Vertex(ver1_id), Vertex(ver2_id), weight, res))
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
        return [(self.getVertexIdx(edge.ver2.id), edge.residual)
                for edge in self.vertex_list[idx] if not edge.isResidual]

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

    def get_weight(self, ver_idx1: int, ver_idx2: int, res: bool):
        for edge in self.vertex_list[ver_idx1]:
            if self.getVertexIdx(edge.ver2.id) == ver_idx2 and res == edge.isResidual:
                return edge.get_weight()
        else:
            return None


def bfs_traverse(graph: AdjacencyList):
    n = graph.order()
    stock = [0]
    visited = [0] * n
    parent = [None] * n
    visited[0] = 1
    while stock:
        next_ver_idx = stock.pop(0)
        next_ver_neigh = graph.neighbours(next_ver_idx)
        for neigh in next_ver_neigh:
            if not visited[neigh[0]] and neigh[1] > 0:
                stock.append(neigh[0])
                visited[neigh[0]] = 1
                parent[neigh[0]] = next_ver_idx
    return parent

def min_capacity(graph: AdjacencyList, s: int, t: int, parent: List[Union[int, None]]):
    if parent[t] is None:
        return 0
    else:
        current_ver = t
        min_cap = 100000
        while current_ver != s:
            current_neigh = graph.neighbours(parent[current_ver])
            for neigh in current_neigh:
                if neigh[0] == current_ver:
                    if neigh[1] < min_cap:
                        min_cap = neigh[1]
                    current_ver = parent[current_ver]
        return min_cap

def augmentation(graph: AdjacencyList, s: int, t: int, parent: List[Union[int, None]], min_cap: int):
    if not min_cap:
        return
    else:
        current_ver = t
        while current_ver != s:
            current_neigh = graph.neighbours(parent[current_ver])
            for neigh in current_neigh:
                if neigh[0] == current_ver:
                    for edge in graph.vertex_list[parent[current_ver]]:
                        if graph.getVertexIdx(edge.ver2.id) == current_ver:
                            if edge.isResidual:
                                edge.residual += min_cap
                            else:
                                edge.flow += min_cap
                                edge.residual -= min_cap
                    current_ver = parent[current_ver]
        return

def ford_fulkerson(graph: AdjacencyList, s, t):
    if isinstance(s, str) and isinstance(t, str):
        s, t = graph.id_dict[s], graph.id_dict[t]
    max_flow = 0
    parent = bfs_traverse(graph)
    if parent[t] is None:
        raise ValueError("Nie istnieje śćieżka łącząca podane wierzchołki")
    else:
        min_cap = min_capacity(graph, s, t, parent)
        max_flow += min_cap
        while min_cap > 0:
            augmentation(graph, s, t, parent, min_cap)
            parent = bfs_traverse(graph)
            min_cap = min_capacity(graph, s, t, parent)
            max_flow += min_cap
        return max_flow

def printGraph(g: AdjacencyList):
    n = g.order()
    print("------GRAPH------", n)
    for i in range(n):
        v = g.getVertex(i)
        print(v, end=" -> ")
        nbrs = g.neighbours(i)
        for j, _ in nbrs:
            print(g.getVertex(j), g.get_weight(i, j, res=False), end=";")
        print()
    print("-------------------")

def main():
    graf_0 = [('s', 'u', 2), ('u', 't', 1), ('u', 'v', 3), ('s', 'v', 1), ('v', 't', 2)]
    graf_1 = [('s', 'a', 16), ('s', 'c', 13), ('a', 'c', 10), ('c', 'a', 4), ('a', 'b', 12), ('b', 'c', 9),
              ('b', 't', 20), ('c', 'd', 14), ('d', 'b', 7), ('d', 't', 4)]
    graf_2 = [('s', 'a', 3), ('s', 'c', 3), ('a', 'b', 4), ('b', 's', 3), ('b', 'c', 1), ('b', 'd', 2), ('c', 'e', 6),
              ('c', 'd', 2), ('d', 't', 1), ('e', 't', 9)]
    graf_3 = [('s', 'a', 8), ('s', 'd', 3), ('a', 'b', 9), ('b', 'd', 7), ('b', 't', 2), ('c', 't', 5), ('d', 'b', 7),
              ('d', 'c', 4)]
    G = [graf_0, graf_1, graf_2, graf_3]
    for graf in G:
        graph = AdjacencyList()
        for edge in graf:
            graph.insertEdge(edge[0], edge[1], edge[2])
            graph.insertEdge(edge[1], edge[0], edge[2], res=True)
        max_flow = ford_fulkerson(graph, 's', 't')
        print(max_flow)
        printGraph(graph)


main()
