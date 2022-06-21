# Coloring graph
# Dominik Tomalczyk

from polska import draw_map, graf
from typing import List


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

    def greedyColoring(self, start_vertex, method):
        """
        Coloring the graph
        :param start_vertex: vertex which from we want to start coloring
        :param method: DFS or BFS (methods of going to another vertices)
        :return: Lists of tuples ("Vertex", color) needed to draw_map
        """
        if method == "DFS":
            list_to_visit = self.__DFS(start_vertex)
        else:
            list_to_visit = self.__BFS(start_vertex)
        neigh_list = self.neighbours_list  # needed to mark neighbours
        V = self.order()  # represents number of vertices

        result = [-1 for _ in range(V)]

        result[list_to_visit[0]] = 0  # first (in order of visiting) vertex has a 0 color

        # A temporary array to store the available colors.
        # True value of available[cr] would mean that the
        # color cr is assigned to one of its adjacent vertices
        available = [True for _ in range(V)]

        for vertex in list_to_visit:
            # Process all adjacent vertices and
            # flag their colors as unavailable
            for i in neigh_list[vertex]:
                if result[i] != -1:
                    available[result[i]] = False

            # searching for first available color
            available_color = 0
            while available_color < V:
                if available[available_color] is True:
                    break
                available_color += 1

            result[vertex] = available_color  # Assign the found color

            for i in neigh_list[vertex]:  # Reset the values back to false for the next iteration
                if result[i] != -1:
                    available[result[i]] = True

        return [(str(self.getVertex(u)), result[u]) for u in range(V)]  # return list of tuples needed to draw_map

    def __BFS(self, s) -> List[int]:
        visited = [False] * self.order()
        queue = []
        queue.append(s)
        visited[s] = True

        result = []
        while queue:
            s = queue.pop(0)
            result.append(s)
            for i in self.neighbours_list[s]:
                if visited[i] is False:
                    queue.append(i)
                    visited[i] = True
        return result

    def __DFS(self, s) -> List[int]:
        visited = []
        S = [s]
        while S:
            v = S.pop(-1)
            if v not in visited:
                visited.append(v)
                if v in self.neighbours_list.keys():
                    self.neighbours_list[v].reverse()
                    for u in self.neighbours_list[v]:
                        S.append(u)
        return visited


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
    for vertex in vertices:
        gl.insertVertex(vertex)
    for edge in edges:
        gl.insertEdge(Vertex(str(edge[0])), Vertex(str(edge[1])))

    draw_map(gl.edges(), gl.greedyColoring(5, "DFS"))  # dla przykładu wywołuje z DFS zaczynając od wierzchołka 5
    draw_map(gl.edges(), gl.greedyColoring(3, "BFS"))  # tymrazem dla metody BFS z wierzchołka 3
