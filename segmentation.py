
"""
Pomysł segmentacji z wykorzystaniem MST polega na wyszukaniu w drzewie krawędzi o największej wadze oraz jej usunięciu. Wtedy uzyskamy dwa odrębne drzewa, 
o potencjalnie różnych właściwościach. 
Zademonstrujemy to na bardzo prostym przykładzie obrazu binarnego sample.png, ponieważ działanie metody na obrazach rzeczywistych nie jest “oczywiste”.
"""

import cv2
from typing import List, Dict
import numpy as np
import matplotlib.pyplot as plt


class Vertex:
    def __init__(self, id_: str, color: int = 0):
        self.id = id_
        self.color = color

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def get_color(self):
        return self.color

    def set_color(self, color):
        self.color = color
        return


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

    def insertEdge(self, ver1_id: str, color1: int, ver2_id: str, color2: int, weight: int = 1):
        if ver1_id not in self.id_dict:
            self.insertVertex(ver1_id)
        if ver2_id not in self.id_dict:
            self.insertVertex(ver2_id)
        idx1 = self.getVertexIdx(ver1_id)
        # idx2 = self.getVertexIdx(ver2_id)
        self.vertex_list[idx1].append(Edge(Vertex(ver1_id, color1), Vertex(ver2_id, color2), weight))
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

    def get_color(self, ver_id):
        edge = self.vertex_list[self.getVertexIdx(ver_id)][0]
        return edge.ver1.get_color()

    def set_color(self, ver_id, color):
        edge = self.vertex_list[self.getVertexIdx(ver_id)][0]
        return edge.ver1.set_color(color)

    def get_weight(self, ver_idx1, ver_idx2):
        for edge in self.vertex_list[ver_idx1]:
            if self.getVertexIdx(edge.ver2.id) == ver_idx2:
                return edge.get_weight()
        else:
            return None

    def find_max_edge(self):
        max_weight = 0
        max_edge = None
        for edges in self.vertex_list:
            for edge in edges:
                if edge.weight > max_weight:
                    max_weight = edge.weight
                    max_edge = edge
        return max_edge

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
            ver1_id = MST_tree.getVertex(min_distance_ver1)
            ver2_id = MST_tree.getVertex(min_distance_ver2)
            ver1_color = graph.get_color(ver1_id)
            ver2_color = graph.get_color(ver2_id)
            MST_tree.insertEdge(ver2_id, ver2_color, ver1_id, ver1_color, min_distance)
            MST_tree.insertEdge(ver1_id, ver1_color, ver2_id, ver2_color, min_distance)
            v = min_distance_ver2
    return MST_tree

def traverse(graph, ver_id, color):
    ver_idx = graph.getVertexIdx(ver_id)
    visited = []
    stock = [ver_idx]
    stock.extend(graph.neighbours(ver_idx))
    while stock:
        current_ver_idx = stock.pop(0)
        if current_ver_idx not in visited:
            visited.append(current_ver_idx)
            current_ver_id = graph.getVertex(current_ver_idx)
            graph.set_color(current_ver_id, color)
            stock.extend(graph.neighbours(current_ver_idx))
    return graph

def seg(img):
    img_graph = AdjacencyList()
    X, Y = img.shape

    # Tworzenie macierzy identyfikatorów
    ids = []
    for i in range(X):
        ids.append([])
        for j in range(Y):
            ids[i].append(X * i + j)

    # Tworzenie połączeń między pikselami
    for i in range(1, X - 1):
        for j in range(1, Y - 1):
            for x in range(i - 1, i + 2):
                for y in range(j - 1, j + 2):
                    if not (x == i and y == j):
                        img_graph.insertEdge(ids[i][j], img[i][j], ids[x][y], img[x][y], abs(img[i][j] - img[x][y]))
                        img_graph.insertEdge(ids[x][y], img[x][y], ids[i][j], img[i][j], abs(img[i][j] - img[x][y]))
    mst_tree = prim(img_graph)
    max_edge = mst_tree.find_max_edge()

    # Podział grafu
    mst_tree.deleteEdge(max_edge.ver1.id, max_edge.ver2.id)
    mst_tree.deleteEdge(max_edge.ver2.id, max_edge.ver1.id)

    # Tworzenie i kolorowanie obrazu
    IS = np.zeros((X, Y), dtype='uint8')
    mst_tree = traverse(mst_tree, max_edge.ver1.id, 100)
    mst_tree = traverse(mst_tree, max_edge.ver2.id, 200)
    for i in range(X):
        for j in range(Y):
            IS[i][j] = mst_tree.get_color(ids[i][j])

    # Wizualizacja obrazu
    plt.imshow(IS, 'gray', vmin=0, vmax=255)
    plt.axis('off')
    plt.show()
    return IS

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
    print(abs(0 - 255))
    I = cv2.imread('sample.png', cv2.IMREAD_GRAYSCALE)
    seg(I)


main()
