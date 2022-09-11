
"""
Problem dokładnego dopasowania dwóch grafów stanowi w istocie pytanie o to, czy są one względem siebie izomorficzne. Jest to specjalny przypadek problemu izomorfizmu podgrafu, który stanowi NP-zupełny problem decyzyjny określony w następujący sposób: dla danych grafów G i P sprawdzić, czy istnieje podgraf G izomorficzny z P.

Wyrażając to jeszcze inaczej - chodzi o to, aby jakiś podgraf G miał identyczną liczbę wierzchołków i układ krawędzi jak wzorzec P.

Implementacja:

używamy reprezentacji w postaci macierzy sąsiedztwa wykorzystując kod stworzony w ramach ćwiczenia "Klasyczne implementacje grafu",

jedyne co nam będzie potrzebne, oprócz standardowych funkcjonalności, to dostęp (pobranie) macierzy sąsiedztwa,

wczytujemy poniższe grafy (warto je sobie narysować). Proszę zadbać o to, aby macierz sąsiedztwa była symetryczna,


graph_G = [ ('A','B',1), ('B','F',1), ('B','C',1), ('C','D',1), ('C','E',1), ('D','E',1)]
graph_P = [ ('A','B',1), ('B','C',1), ('A','C',1)]


pobieramy z grafów macierze sąsiedztwa i zapisujemy je w postaci tablic numpy

inicjujemy M - określamy jej rozmiar i wypełniamy zgodnie z podanym sposobem (przyda się funkcja zwracająca krawędzie dla wierzchołka),

implementujemy funkcję ullman w wersji 1.0, tj. bez wykorzystania M0 i prune,

dodajemy zliczenie liczby wywołań rekurencji. Schemat:

no_recursion = ullman(......, no_recursion)

            no_recursion = no_recursion +1

            ….

            return no_recursion

sprawdzamy czy nasz kod działa i czy znajdujemy izomorfizmy,

    Poniżej, dla ułatwienia testowania, zamieszona została jedna z macierzy M, dla której powinni Państwo uzyskać izomorfizm (dla wierrzołków dodawanych alfabetycznie):
 [[0. 0. 0. 1. 0. 0.]                                                           
 [0. 0. 1. 0. 0. 0.]                                                            
 [0. 0. 0. 0. 1. 0.]]
    To samo, ale dla wierzchołków dodawanych razem z krawędziami: 
 [[0. 0. 0. 1. 0. 0.]
 [0. 0. 0. 0. 1. 0.]
 [0. 0. 0. 0. 0. 1.]]

implementujemy wersję 2.0 z uwzględnieniem M0. Sprawdzamy czy wynik jest poprawny (nadal) oraz czy spadła liczba iteracji.

w wersji 3.0 dodajemy funkcję prune. Dla wskazanego przykładu liczba iteracji powinna nieznacznie zmaleć
"""

from typing import List, Dict
import numpy as np

class Vertex:
    def __init__(self, id_: str):
        self.id = id_

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

class Edge:
    def __init__(self, ver1: str, ver2: str, priority: int = 1):
        self.ver1 = ver1
        self.ver2 = ver2
        self.priority = priority


class AdjacencyMatrix:
    def __init__(self, id_dict: Dict = None, vertex_matrix: List[List[int]] = None):
        if vertex_matrix is None:
            vertex_matrix = []
        if id_dict is None:
            id_dict = {}
        self.id_dict = id_dict
        self.vertex_matrix = vertex_matrix

    def insertVertex(self, ver_id: str):
        new_idx = self.order()
        self.vertex_matrix.append([0] * new_idx)
        for row in self.vertex_matrix:
            row.append(0)
        self.id_dict[ver_id] = new_idx
        return

    def insertEdge(self, ver1_id: str, ver2_id: str, priority: int = 1):
        if ver1_id not in self.id_dict and priority != 0:
            self.insertVertex(ver1_id)
        if ver2_id not in self.id_dict and priority != 0:
            self.insertVertex(ver2_id)
        idx1 = self.getVertexIdx(ver1_id)
        idx2 = self.getVertexIdx(ver2_id)
        self.vertex_matrix[idx1][idx2] = priority
        return

    def deleteVertex(self, ver_id):
        deleted_idx = self.getVertexIdx(ver_id)
        self.vertex_matrix.pop(deleted_idx)
        for row in self.vertex_matrix:
            row.pop(deleted_idx)
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
        if ver1_id in self.id_dict and ver2_id in self.id_dict:
            self.insertEdge(ver1_id, ver2_id, priority=0)
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
        neighbours = self.vertex_matrix[idx]
        return [i for i, weight in enumerate(neighbours) if weight != 0]

    def order(self):
        return len(self.vertex_matrix)

    def size(self):
        return len(self.edges())

    def edges(self):
        # [(X, Y), ...]
        edges = []
        for i in range(self.order()):
            for j in range(i):
                if self.vertex_matrix[i][j] != 0:
                    edges.append(Edge(self.getVertex(i), self.getVertex(j), self.vertex_matrix[i][j]))
        return edges

    def get_matrix(self):
        return self.vertex_matrix

def M0(P: AdjacencyMatrix, G: AdjacencyMatrix, M: np.ndarray):
    X, Y = len(M), len(M[0])
    matrix_P, matrix_G = P.get_matrix(), G.get_matrix()
    M_copy = M.copy()
    for i in range(X):
        deg_vi = matrix_P[i].count(1)
        for j in range(Y):
            deg_vj = matrix_G[j].count(1)
            if deg_vi <= deg_vj:
                M_copy[i][j] = 1
            else:
                M_copy[i][j] = 0
    return M_copy

def prune(P: AdjacencyMatrix, G: AdjacencyMatrix, M: np.ndarray):
    X, Y = len(M), len(M[0])
    change = True
    while change:
        change = False
        for i in range(X):
            for j in range(Y):
                if M[i][j] == 1:
                    neighbours_y = G.neighbours(j)
                    flag = False
                    for neighbour_x in P.neighbours(i):
                        for neighbour_y in neighbours_y:
                            if M[neighbour_x][neighbour_y] == 1:
                                flag = True
                    if not flag:
                        M[i][j] = 0
                        change = True
    return M

def ullman_v1(P: AdjacencyMatrix, G: AdjacencyMatrix, M: np.ndarray, used_columns=None, current_row=0, iso_list=None,
            counter=0):
    size = len(M[0])
    if not iso_list:
        iso_list = []

    if not used_columns:
        used_columns = [False] * size

    if current_row == len(M):
        matrix_P, matrix_G = np.array(P.get_matrix()), np.array(G.get_matrix())
        iso_candidate = np.array((matrix_P == M @ (M @ matrix_G).T))
        if iso_candidate.all():
            iso_list.append(M.copy())
        return iso_list, counter

    M_copy = M.copy()

    for j in range(size):
        if not used_columns[j]:
            M_copy[current_row][j] = 1
            for k in range(size):
                if k != j:
                    M_copy[current_row][k] = 0
            used_columns[j] = True
            iso_list, counter = ullman_v1(P, G, M_copy, used_columns, current_row + 1, iso_list, counter)
            counter += 1
            used_columns[j] = False
    return iso_list, counter

def ullman_v2(P: AdjacencyMatrix, G: AdjacencyMatrix, M: np.ndarray, used_columns=None, current_row=0, iso_list=None,
            counter=0):
    size = len(M[0])
    if not iso_list:
        iso_list = []

    if not used_columns:
        used_columns = [False] * size

    if current_row == len(M):
        matrix_P, matrix_G = np.array(P.get_matrix()), np.array(G.get_matrix())
        iso_candidate = np.array((matrix_P == M @ (M @ matrix_G).T))
        if iso_candidate.all():
            iso_list.append(M.copy())
        return iso_list, counter

    M_copy = M.copy()

    for j in range(size):
        if not used_columns[j] and M[current_row][j]:
            M_copy[current_row][j] = 1
            for k in range(size):
                if k != j:
                    M_copy[current_row][k] = 0
            used_columns[j] = True
            iso_list, counter = ullman_v2(P, G, M_copy, used_columns, current_row + 1, iso_list, counter)
            counter += 1
            used_columns[j] = False
    return iso_list, counter

def ullman_v3(P: AdjacencyMatrix, G: AdjacencyMatrix, M: np.ndarray, used_columns=None, current_row=0, iso_list=None,
           counter=0):
    size = len(M[0])
    if not iso_list:
        iso_list = []

    if not used_columns:
        used_columns = [False] * size

    if current_row == len(M):
        matrix_P, matrix_G = np.array(P.get_matrix()), np.array(G.get_matrix())
        iso_candidate = np.array((matrix_P == M @ (M @ matrix_G).T))
        if iso_candidate.all():
            iso_list.append(M.copy())
        return iso_list, counter

    M_copy = M.copy()
    M = prune(P, G, M)

    for j in range(size):
        if not used_columns[j] and M[current_row][j]:
            M_copy[current_row][j] = 1
            for k in range(size):
                if k != j:
                    M_copy[current_row][k] = 0
            used_columns[j] = True
            iso_list, counter = ullman_v3(P, G, M_copy, used_columns, current_row + 1, iso_list, counter)
            counter += 1
            used_columns[j] = False
    return iso_list, counter


def main():

    # Tworzenie grafów
    graph_G = [('A', 'B', 1), ('B', 'F', 1), ('B', 'C', 1), ('C', 'D', 1), ('C', 'E', 1), ('D', 'E', 1)]
    graph_P = [('A', 'B', 1), ('B', 'C', 1), ('A', 'C', 1)]
    P, G = AdjacencyMatrix(), AdjacencyMatrix()

    # Układanie wierzchołków alfabetycznie
    vertex_G = []
    for edge in graph_G:
        if edge[0] not in vertex_G:
            vertex_G.append(edge[0])
        if edge[1] not in vertex_G:
            vertex_G.append(edge[1])
    vertex_G.sort(key=ord)

    vertex_P = []
    for edge in graph_P:
        if edge[0] not in vertex_P:
            vertex_P.append(edge[0])
        if edge[1] not in vertex_P:
            vertex_P.append(edge[1])
    vertex_P.sort(key=ord)

    for ver in vertex_G:
        G.insertVertex(ver)
    for ver in vertex_P:
        P.insertVertex(ver)

    # Dodawanie krawędzi
    for edge in graph_G:
        G.insertEdge(edge[0], edge[1], edge[2])
        G.insertEdge(edge[1], edge[0], edge[2])
    for edge in graph_P:
        P.insertEdge(edge[0], edge[1], edge[2])
        P.insertEdge(edge[1], edge[0], edge[2])

    matrix_P, matrix_G = np.array(P.get_matrix()), np.array(G.get_matrix())
    X, Y = matrix_P.shape[1], matrix_G.shape[1]
    matrix_M = np.zeros([X, Y])

    iso_v1, counter_v1 = ullman_v1(P, G, matrix_M)
    print(len(iso_v1), counter_v1)

    iso_v2, counter_v2 = ullman_v2(P, G, M0(P, G, matrix_M))
    print(len(iso_v2), counter_v2)

    iso_v3, counter_v3 = ullman_v3(P, G, M0(P, G, matrix_M))
    print(len(iso_v3), counter_v3)


main()
