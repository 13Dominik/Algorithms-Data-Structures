# Ford Fulkerson algorithm
# Dominik Tomalczyk

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
        self.neighbours_list = []

    def insertVertex(self, vertex: Vertex):
        self.vertex_dict[vertex] = self.order()
        self.neighbours_list.append([])
        self.vertex_list.append(vertex)

    def insertEdge(self, vertex1, vertex2, edge):
        id_1 = self.getVertexIdx(vertex1)
        id_2 = self.getVertexIdx(vertex2)
        self.neighbours_list[id_1].append((id_2, edge))  # adding with weight of edge
        self.neighbours_list[id_1] = self.neighbours_list[id_1]

        # GRAPH IS NOW DIRECTED !!!
        # self.neighbours_list[id_2].append((id_1, edge))
        # self.neighbours_list[id_2] = sorted(set(self.neighbours_list[id_2]))

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
        # GRAPH IS NOW DIRECTED !!!
        # for edge in self.neighbours_list[id_2]:
        #    if edge[0] == id_1:
        #        self.neighbours_list[id_2].remove(edge)
        #        break

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

    def __str__(self):
        return "\n".join([str(k) + " : " + str(v) for k, v in self.neighbours_list.items()])

    def getEdge(self, v1, v2):
        for edge in self.neighbours_list[v1]:
            if edge[0] == v2:
                return edge[1]

    def bfs_search(self, start):
        visited = []
        parent = [None for _ in range(self.order())]
        stack = [start]
        while stack:
            s = stack.pop(0)
            neighs = self.neighbours(s)
            for u in neighs:
                # extra condition (instruction point 5)
                if u[0] not in visited and self.getEdge(s, u[0]).residual > 0:
                    stack.append(u[0])
                    visited.append(u[0])
                    parent[u[0]] = s
        return parent

    def calculate_flow(self, start, end, parent):
        current = end
        min_capacity = float('inf')

        if parent[end] is None:
            return 0

        while current is not start:
            edge_ = self.getEdge(parent[current], current)
            if min_capacity > edge_.residual:
                min_capacity = edge_.residual
            current = parent[current]

        return min_capacity

    def path_augmentation(self, start, end, parent, min_capacity):
        current = end
        while current is not start:
            self.getEdge(parent[current], current).flow += min_capacity
            self.getEdge(parent[current], current).residual -= min_capacity
            self.getEdge(current, parent[current]).residual += min_capacity

            current = parent[current]

    def ford_fulkerson(self, start, end):
        start = self.getVertexIdx(start)
        end = self.getVertexIdx(end)

        result = 0
        parent = self.bfs_search(start)
        min_capacity = self.calculate_flow(start, end, parent)
        while min_capacity > 0:
            result += min_capacity
            self.path_augmentation(start, end, parent, min_capacity)
            parent = self.bfs_search(start)
            min_capacity = self.calculate_flow(start, end, parent)
        return result


class Edge:
    def __init__(self, capacity, isresidual):
        self.capacity = capacity
        self.flow = 0
        self.residual = capacity
        self.isresidual = isresidual

    def __str__(self):
        return f"{self.capacity} {self.flow} {self.residual} {self.isresidual}"

    def __repr__(self):
        return f"{self.capacity} {self.flow} {self.residual} {self.isresidual}"


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
    # 3
    # 23
    # 5
    # 6

    graf_0 = [('s', 'u', 2), ('u', 't', 1), ('u', 'v', 3), ('s', 'v', 1), ('v', 't', 2)]
    graf_1 = [('s', 'a', 16), ('s', 'c', 13), ('a', 'c', 10), ('c', 'a', 4), ('a', 'b', 12), ('b', 'c', 9),
              ('b', 't', 20), ('c', 'd', 14), ('d', 'b', 7), ('d', 't', 4)]
    graf_2 = [('s', 'a', 3), ('s', 'c', 3), ('a', 'b', 4), ('b', 's', 3), ('b', 'c', 1), ('b', 'd', 2), ('c', 'e', 6),
              ('c', 'd', 2), ('d', 't', 1), ('e', 't', 9)]
    graf_3 = [('s', 'a', 8), ('s', 'd', 3), ('a', 'b', 9), ('b', 'd', 7), ('b', 't', 2), ('c', 't', 5), ('d', 'b', 7),
              ('d', 'c', 4)]
    for i in range(4):
        gl = GraphList()
        for elem in eval('graf_' + str(i)):
            if Vertex(elem[0]) not in gl.vertex_list:
                gl.insertVertex(Vertex(elem[0]))
            if Vertex(elem[1]) not in gl.vertex_list:
                gl.insertVertex(Vertex(elem[1]))
            gl.insertEdge(Vertex(elem[0]), Vertex(elem[1]), Edge(elem[2], False))
            gl.insertEdge(Vertex(elem[1]), Vertex(elem[0]), Edge(0, True))
        print(f"Max przepływ dla grafu numer {i}:")
        print(gl.ford_fulkerson(Vertex('s'), Vertex('t')))
        printGraph(gl)
