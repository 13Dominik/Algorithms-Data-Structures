# Graph structure
# Dominik Tomalczyk

import turtle
import polska


# This graph is UNDIRECTED!!!
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


class Edge:
    pass


class GraphMatrix:
    def __init__(self):
        self.vertex_list = []
        self.vertex_dict = {}
        self.neighbours_matrix = [[]]

    def insertVertex(self, vertex: Vertex):
        self.vertex_dict[vertex] = self.order()
        for row in self.neighbours_matrix:
            row.append(0)
        if self.order() != 0:
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


class GraphList:
    def __init__(self):
        self.vertex_list = []
        self.vertex_dict = {}
        self.neighbours_list = {}

    def insertVertex(self, vertex: Vertex):
        self.vertex_dict[vertex] = self.order()
        self.neighbours_list[self.order()] = []
        self.vertex_list.append(vertex)

    def insertEdge(self, vertex1, vertex2, egde=1):
        id_1 = self.getVertexIdx(vertex1)
        id_2 = self.getVertexIdx(vertex2)
        self.neighbours_list[id_1].append(id_2)
        self.neighbours_list[id_2].append(id_1)
        self.neighbours_list[id_1] = sorted(set(self.neighbours_list[id_1]))
        self.neighbours_list[id_2] = sorted(set(self.neighbours_list[id_2]))

    def deleteVertex(self, vertex):
        id_vertex = self.getVertexIdx(vertex)
        self.vertex_list.remove(vertex)  # remove from list
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

        # recreating neighbours list:
        new_neigh_list = {}
        for key in self.neighbours_list.keys():
            new_values = []  # new list of values for every key
            for value in self.neighbours_list[key]:
                if value == id_vertex:  # delete node
                    continue
                if value > id_vertex:  # add reindexed node
                    new_values.append(value - 1)
                else:
                    new_values.append(value)  # if node < deleting node dont change anything
            if key > id_vertex:
                new_neigh_list[key - 1] = new_values  # if key > deleting node reindex it
                continue
            if key == id_vertex:  # skip this key (node is deleted)
                continue
            else:
                new_neigh_list[key] = new_values  # if node < deleting node dont change anything
        self.neighbours_list = new_neigh_list

    def deleteEdge(self, vertex1, vertex2):
        id_1 = self.getVertexIdx(vertex1)
        id_2 = self.getVertexIdx(vertex2)
        self.neighbours_list[id_1].remove(id_2)
        self.neighbours_list[id_2].remove(id_1)

    def getVertexIdx(self, vertex):
        return self.vertex_dict[vertex]

    def getVertex(self, vertex_idx):
        for k, v in self.vertex_dict.items():
            if v == vertex_idx:
                return k

    def neighbours(self, vertex_idx):
        return self.vertex_dict[self.getVertex(vertex_idx)]

    def order(self):
        return len(self.vertex_list)

    def size(self):
        edges = 0
        for v in self.neighbours_list.values():
            edges += len(v)
        return int(edges / 2)

    def edges(self):
        edges_ = []
        for key in self.neighbours_list.keys():
            for value in self.neighbours_list[key]:
                if (key, value) and (value, key) not in edges_:
                    edges_.append((key, value))
        return [(str(self.getVertex(pair[0])), str(self.getVertex(pair[1]))) for pair in edges_]

    def __str__(self):
        return "\n".join([str(k) + " : " + str(v) for k, v in self.neighbours_list.items()])


if __name__ == '__main__':
    vertices = [Vertex('Z'), Vertex('G'), Vertex('N'), Vertex('B'),
                Vertex('F'), Vertex('P'), Vertex('C'), Vertex('E'),
                Vertex('W'), Vertex('L'), Vertex('D'), Vertex('O'),
                Vertex('S'), Vertex('T'), Vertex('K'), Vertex('R')]
    edges = [('Z', 'G'), ('Z', 'P'), ('Z', 'F'),
             ('G', 'Z'), ('G', 'P'), ('G', 'C'), ('G', 'N'),
             ('N', 'G'), ('N', 'C'), ('N', 'W'), ('N', 'B'),
             ('B', 'N'), ('B', 'W'), ('B', 'L'),
             ('F', 'Z'), ('F', 'P'), ('F', 'D'),
             ('P', 'F'), ('P', 'Z'), ('P', 'G'), ('P', 'C'), ('P', 'E'), ('P', 'O'), ('P', 'D'),
             ('C', 'P'), ('C', 'G'), ('C', 'N'), ('C', 'W'), ('C', 'E'),
             ('E', 'P'), ('E', 'C'), ('E', 'W'), ('E', 'T'), ('E', 'S'), ('E', 'O'),
             ('W', 'C'), ('W', 'N'), ('W', 'B'), ('W', 'L'), ('W', 'T'), ('W', 'E'),
             ('L', 'W'), ('L', 'B'), ('L', 'R'), ('L', 'T'),
             ('D', 'F'), ('D', 'P'), ('D', 'O'),
             ('O', 'D'), ('O', 'P'), ('O', 'E'), ('O', 'S'),
             ('S', 'O'), ('S', 'E'), ('S', 'T'), ('S', 'K'),
             ('T', 'S'), ('T', 'E'), ('T', 'W'), ('T', 'L'), ('T', 'R'), ('T', 'K'),
             ('K', 'S'), ('K', 'T'), ('K', 'R'),
             ('R', 'K'), ('R', 'T'), ('R', 'L')]
    gl = GraphList()
    gm = GraphMatrix()
    for vertex in vertices:
        gl.insertVertex(vertex)
        gm.insertVertex(vertex)
    for edge in edges:
        gl.insertEdge(Vertex(str(edge[0])), Vertex(str(edge[1])))
        gm.insertEdge(Vertex(str(edge[0])), Vertex(str(edge[1])))
    gl.deleteVertex(Vertex('K'))
    gm.deleteVertex(Vertex('K'))

    gl.deleteEdge(Vertex('W'), Vertex('E'))
    gm.deleteEdge(Vertex('W'), Vertex('E'))

    polska.draw_map(gm.edges())  # wyrysowanie grafu dla Macierzy sasiedztwa
    polska.draw_map(gl.edges())  # wyrysowanie grafu dla listy sasiedztwa
