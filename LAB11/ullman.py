# Ullman algorithm
# Dominik Tomalczyk

import numpy as np
from copy import deepcopy


class Vertex:
    def __init__(self, key):
        self.key = key

    def __eq__(self, other):
        return self.key == other.key

    def __hash__(self):
        return hash(self.key)

    def __str__(self):
        return f"{self.key}"

    def __repr__(self):
        return f"{self.key}"


class GraphMatrix:
    def __init__(self):
        self.vertex_list = []
        self.vertex_dict = {}
        self.neighbours_matrix = [[]]

    def insertVertex(self, vertex: Vertex):
        self.vertex_dict[vertex] = self.order()
        # for i in range(len(self.neighbours_matrix[0])):
        #    self.neighbours_matrix[i] = np.append(self.neighbours_matrix[i], 0)
        for row in self.neighbours_matrix:
            row.append(0)
        if self.order() != 0:
            # np.append(self.neighbours_matrix, [0] * (self.order() + 1))
            self.neighbours_matrix.append([0] * (self.order() + 1))
        self.vertex_list.append(vertex)

    def insertEdge(self, vertex1, vertex2, edge=1):
        id_1 = self.getVertexIdx(vertex1)
        id_2 = self.getVertexIdx(vertex2)
        self.neighbours_matrix[id_1][id_2] = edge
        self.neighbours_matrix[id_2][id_1] = edge

    def deleteVertex(self, vertex):
        id_vertex = self.getVertexIdx(vertex)
        for row in self.neighbours_matrix:  # remove from every row
            row.pop(id_vertex)
        self.neighbours_matrix.pop(id_vertex)  # remove row

        self.vertex_list.remove(vertex)  # remove from vertices list

        # reindexing dict:
        new_dict = {}
        for k, v in self.vertex_dict.items():
            if v == id_vertex:
                continue
            if v > id_vertex:
                new_dict[k] = v - 1
            else:
                new_dict[k] = v
        self.vertex_dict = new_dict

    def deleteEdge(self, vertex1, vertex2):
        id_1 = self.getVertexIdx(vertex1)
        id_2 = self.getVertexIdx(vertex2)
        self.neighbours_matrix[id_1][id_2] = 0
        self.neighbours_matrix[id_2][id_1] = 0

    def getVertexIdx(self, vertex: Vertex):
        return self.vertex_dict[vertex]

    def getVertex(self, vertex_idx: int):
        return self.vertex_list[vertex_idx]

    def neighbours(self, vertex_idx):
        neigh = []
        for idx, vertex in enumerate(self.neighbours_matrix[vertex_idx]):
            if vertex != 0:
                neigh.append(idx)
        return neigh

    def order(self):
        """ Returns no. vertices """
        return len(self.vertex_list)

    def size(self):
        """ Returns no. edges """
        edges = 0
        for row in self.neighbours_matrix:
            edges += sum(row)
        return int(edges / 2)

    def edges(self):
        """ Returns vertex key : vertex key of all edges for undirected graph"""
        edges_ = []
        for i in range(self.order()):
            for j in range(i, self.order()):
                if self.neighbours_matrix[i][j] != 0:
                    edges_.append([self.getVertex(j).key, self.getVertex(i).key])

        return [(str(pair[0]), str(pair[1])) for pair in edges_]

    def __str__(self):
        return "\n".join([str(row) for row in self.neighbours_matrix])

def ullman_1(used_cols, curr_row, G, P, M):
    global ullman_1_call, ullman_1_isomorphisms
    ullman_1_call += 1

    if curr_row == M.shape[0]:
        if (P == (M @ np.transpose(M @ G))).all():
            ullman_1_isomorphisms += 1
        return True

    M_prim = deepcopy(M)

    for i in range(M_prim.shape[1]):
        if i not in used_cols:
            for c in range(M_prim.shape[1]):
                if c == i:
                    M_prim[curr_row][c] = 1
                else:
                    M_prim[curr_row][c] = 0

            used_cols.append(i)
            ullman_1(used_cols, curr_row + 1, G, P, M_prim, )
            used_cols.remove(i)

def ullman_2(used_cols, curr_row, G,P,M, M0):
    global ullman_2_call, ullman_2_isomorphisms
    ullman_2_call += 1

    if curr_row == M.shape[0]:
        if (P == (M @ np.transpose(M @ G))).all():
            ullman_2_isomorphisms += 1
        return True

    M_prim = deepcopy(M)

    for i in range(M_prim.shape[1]):
        if i not in used_cols:
            if M0[curr_row][i] == 1:
                for c in range(M_prim.shape[1]):
                    if c == i:
                        M_prim[curr_row][c] = 1
                    else:
                        M_prim[curr_row][c] = 0

                used_cols.append(i)
                ullman_2(used_cols, curr_row + 1, G, P, M_prim, M0)
                used_cols.remove(i)
def prune(M):
    change = True
    while change:
        change = False
        for i in range(M.shape[0]):
            for j in range(M.shape[1]):
                if M[i, j] == 1:
                    neigh_exist = False

                    for x in range(0, len(P[0])):
                        for y in range(0, len(G[0])):
                            if M[x, y] == 1:
                                neigh_exist = True
                                break

                    if not neigh_exist:
                        M[i, j] = 0
                        change = True
                        break

def ullman_3(used_cols, curr_row, G,P,M, M0):
    global ullman_3_call, ullman_3_isomorphisms
    ullman_3_call += 1

    if curr_row == M.shape[0]:
        if (P == (M @ np.transpose(M @ G))).all():
            ullman_3_isomorphisms += 1
        return True

    M_prim = deepcopy(M)
    prune(M_prim)
    for i in range(M_prim.shape[1]):
        if i not in used_cols:
            if M0[curr_row][i] == 1:
                for c in range(M_prim.shape[1]):
                    if c == i:
                        M_prim[curr_row][c] = 1
                    else:
                        M_prim[curr_row][c] = 0

                used_cols.append(i)
                ullman_3(used_cols, curr_row + 1, G, P, M_prim, M0)
                used_cols.remove(i)

if __name__ == '__main__':
    graph_G = [('A', 'B', 1), ('B', 'F', 1), ('B', 'C', 1), ('C', 'D', 1), ('C', 'E', 1), ('D', 'E', 1)]
    graph_P = [('A', 'B', 1), ('B', 'C', 1), ('A', 'C', 1)]
    g1 = GraphMatrix()
    g2 = GraphMatrix()

    for elem in graph_G:
        if Vertex(elem[0]) not in g1.vertex_list:
            g1.insertVertex(Vertex(elem[0]))
        if Vertex(elem[1]) not in g1.vertex_list:
            g1.insertVertex(Vertex(elem[1]))
        g1.insertEdge(Vertex(elem[0]), Vertex(elem[1]))

    for elem in graph_P:
        if Vertex(elem[0]) not in g2.vertex_list:
            g2.insertVertex(Vertex(elem[0]))
        if Vertex(elem[1]) not in g2.vertex_list:
            g2.insertVertex(Vertex(elem[1]))
        g2.insertEdge(Vertex(elem[0]), Vertex(elem[1]))

    G = np.array(g1.neighbours_matrix)
    P = np.array(g2.neighbours_matrix)
    M = np.zeros((P.shape[0], G.shape[0]))

    ullman_1_call = 0
    ullman_1_isomorphisms = 0
    used_cols = []
    ullman_1(used_cols, 0, G, P, M)
    print(f"Liczba wywołań funkcji: {ullman_1_call} liczba znalezionych izomorfizmów: {ullman_1_isomorphisms}")

    ullman_2_call = 0
    ullman_2_isomorphisms = 0
    M0 = np.zeros((M.shape[0], M.shape[1]))
    for i in range(P.shape[0]):
        p_len = np.sum(P[i, :])
        for j in range(G.shape[0]):
            g_len = np.sum(G[j, :])
            if p_len <= g_len:
                M0[i, j] = 1
    used_cols1 = []
    ullman_2(used_cols1, 0, G, P, M, M0)
    print(f"Liczba wywołań funkcji: {ullman_2_call} liczba znalezionych izomorfizmów: {ullman_2_isomorphisms}")

    ullman_3_call = 0
    ullman_3_isomorphisms = 0
    used_cols2 = []
    ullman_3(used_cols2, 0, G, P, M, M0)
    print(f"Liczba wywołań funkcji: {ullman_3_call} liczba znalezionych izomorfizmów: {ullman_3_isomorphisms}")

