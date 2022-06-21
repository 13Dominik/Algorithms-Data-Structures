# Prim's method to find Minimum spanning tree
# Dominik Tomalczyk

from copy import deepcopy


class Vertex:
    def __init__(self, key):
        self.key = key
        self.color = None

    def __eq__(self, other):
        return self.key == other.key

    def __hash__(self):
        return hash(self.key)

    def __str__(self):
        return f"{self.key}"

    def __repr__(self):
        return f"{self.key}"


class GraphList:
    def __init__(self):
        self.vertex_list = []
        self.vertex_dict = {}
        self.neighbours_list = {}

    def insertVertex(self, vertex: Vertex):
        self.vertex_dict[vertex] = self.order()
        self.neighbours_list[self.order()] = []
        self.vertex_list.append(vertex)

    def insertEdge(self, vertex1, vertex2, edge=1):
        id_1 = self.getVertexIdx(vertex1)
        id_2 = self.getVertexIdx(vertex2)
        self.neighbours_list[id_1].append((id_2, edge))  # adding with weight of edge
        self.neighbours_list[id_2].append((id_1, edge))
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
                if value[0] == id_vertex:  # delete node
                    continue
                if value[0] > id_vertex:  # add reindexed node
                    new_values.append((value[0] - 1, value[1]))
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

        for edge in self.neighbours_list[id_1]:
            if edge[0] == id_2:
                self.neighbours_list[id_1].remove(edge)
                break
        for edge in self.neighbours_list[id_2]:
            if edge[0] == id_1:
                self.neighbours_list[id_2].remove(edge)
                break

    def getVertexIdx(self, vertex):
        return self.vertex_dict[vertex]

    def getVertex(self, vertex_idx):
        for k, v in self.vertex_dict.items():
            if v == vertex_idx:
                return k

    def neighbours(self, vertex_idx):
        return self.neighbours_list[vertex_idx]

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
                if (key, value[0]) and (value[0], key) not in edges_:
                    edges_.append((key, value[0]))
        edges = []
        for pair in edges_:
            weight = 0
            v1 = pair[0]
            v2 = pair[1]
            for edge in self.neighbours_list[v1]:
                if edge[0] == v2:
                    weight = edge[1]
                    break
            edges.append((str(self.getVertex(pair[0])), str(self.getVertex(pair[1])), weight))
        return edges

    def DFS(self, s):
        visited = []
        S = [s]
        while S:
            v = S.pop(-1)
            if v not in visited:
                visited.append(v)
                if v in self.neighbours_list.keys():
                    self.neighbours_list[v].reverse()
                    for u in self.neighbours_list[v]:
                        S.append(u[0])
        return visited

    def __str__(self):
        return "\n".join([str(k) + " : " + str(v) for k, v in self.neighbours_list.items()])


class MST:
    def __init__(self, graph: GraphList):
        self.base_graph = deepcopy(graph)
        self.graph_MST = None
        self.size = self.graph_MST.order()

        self.intree = [0 for _ in range(self.size)]
        self.distance = [float("inf") for _ in range(self.size)]
        self.parent = [-1 for _ in range(self.size)]

    @property
    def graph_MST(self):
        return self.__graph_MST

    @graph_MST.setter
    def graph_MST(self, value):
        self.__graph_MST = GraphList()
        for vertex in self.base_graph.vertex_list:
            self.__graph_MST.insertVertex(vertex)

    def Prim(self, v):
        edge_weights = []
        while self.intree[v] == 0:
            current = v
            self.intree[v] = 1
            for neighbour in self.base_graph.neighbours_list[v]:
                if neighbour[1] < self.distance[neighbour[0]]:
                    self.distance[neighbour[0]] = neighbour[1]  # update cost
                    self.parent[neighbour[0]] = current  # update parent
            min_cost = float("inf")
            for vertex in self.base_graph.neighbours_list.keys():
                if self.intree[vertex] == 0:
                    if self.distance[vertex] < min_cost:  # find lowest weight of edge
                        min_cost = self.distance[vertex]
                        v = vertex  # next step vertex
            edge_weight = 0
            # look for edge weight in basegraph and add it to sum of weights
            for edge in self.base_graph.neighbours_list[self.parent[v]]:
                if edge[0] == v:
                    edge_weight = edge[1]
                    edge_weights.append(edge_weight)
                    break
            self.graph_MST.insertEdge(self.graph_MST.getVertex(self.parent[v]), self.graph_MST.getVertex(v),
                                      edge_weight)
        return sum(edge_weights[:-1])  # returns sum of MST


def printGraph(g):
    n = g.order()
    print("------GRAPH------", n)
    for i in range(n):
        v = g.getVertex(i)
        print(v, end=" -> ")
        nbrs = g.neighbours(i)
        for (j, w) in nbrs:
            print(g.getVertex(j), w, end=";")
        print()
    print("-------------------")


if __name__ == '__main__':
    graf = [('A', 'B', 4), ('A', 'C', 1), ('A', 'D', 4),
            ('B', 'E', 9), ('B', 'F', 9), ('B', 'G', 7), ('B', 'C', 5),
            ('C', 'G', 9), ('C', 'D', 3),
            ('D', 'G', 10), ('D', 'J', 18),
            ('E', 'I', 6), ('E', 'H', 4), ('E', 'F', 2),
            ('F', 'H', 2), ('F', 'G', 8),
            ('G', 'H', 9), ('G', 'J', 8),
            ('H', 'I', 3), ('H', 'J', 9),
            ('I', 'J', 9)
            ]
    gl = GraphList()
    for elem in graf:
        if Vertex(elem[0]) not in gl.vertex_list:
            gl.insertVertex(Vertex(elem[0]))
        if Vertex(elem[1]) not in gl.vertex_list:
            gl.insertVertex(Vertex(elem[1]))
        gl.insertEdge(Vertex(elem[0]), Vertex(elem[1]), elem[2])

    m = MST(gl)
    print(f"Suma MST: {m.Prim(0)}")
    printGraph(m.graph_MST)
