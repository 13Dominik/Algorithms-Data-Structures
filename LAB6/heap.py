# Heap
# DOMINIK TOMALCZYK

class Element:
    def __init__(self, data, prio):
        self.data = data
        self.prio = prio

    def __str__(self):
        return f"{self.prio} : {self.data}"

    def __repr__(self):
        return f"{self.prio} : {self.data}"

    def __gt__(self, other):
        return self.prio > other.prio

    def __lt__(self, other):
        return self.prio < other.prio


class Heap:
    def __init__(self):
        self.queue = []

    @property
    def size(self):
        return len(self.queue)

    def right(self, i):
        return 2 * i + 2

    def left(self, i):
        return 2 * i + 1

    def parent(self, i):
        return (i - 1) // 2

    def is_empty(self):
        return not bool(self.queue)

    def peek(self):
        """ Does not modify heap just only display element with highest priority """
        return self.queue[0]

    def dequeue(self):
        if not self.queue:
            return None
        node_to_pick = self.queue[0]
        self.queue[0] = self.queue[-1]  # last element is now first
        self.queue = self.queue[:-1]  # remove last element

        self.__heapify(0)
        return node_to_pick

    def __heapify(self, start):
        left = self.left(start)
        right = self.right(start)
        largest = start

        # if left child exists and has highest prio:
        if left <= self.size - 1 and self.queue[left] > self.queue[largest]:
            largest = left
        # if right child exists and has highest prio
        if right <= self.size - 1 and self.queue[right] > self.queue[largest]:
            largest = right

        # if something has changed:
        if largest != start:
            self.queue[start], self.queue[largest] = self.queue[largest], self.queue[start]
            self.__heapify(largest)

    def enqueue(self, element: Element):
        self.queue.append(element)  # Add as last element
        current = self.size - 1  # index of last element

        while current > 0 and self.queue[current] > self.queue[self.parent(current)]:
            self.queue[current], self.queue[self.parent(current)] = self.queue[self.parent(current)], self.queue[current]
            current = self.parent(current)

    def print_tab(self):
        if self.is_empty():
            print("{ }")
            return
        print('{', end=' ')
        for i in range(self.size - 1):
            print(self.queue[i], end=', ')
        if self.queue[self.size - 1]:
            print(self.queue[self.size - 1], end=' ')
        print('}')

    def print_tree(self, idx, lvl):
        if idx < self.size:
            self.print_tree(self.right(idx), lvl + 1)
            print(2 * lvl * '  ', self.queue[idx] if self.queue[idx] else None)
            self.print_tree(self.left(idx), lvl + 1)


if __name__ == '__main__':

    h = Heap()
    l = [4, 7, 6, 7, 5, 2, 2, 1]
    algo = "ALGORYTM"
    for i in range(len(l)):
        h.enqueue(Element(algo[i], l[i]))
    h.print_tree(0, 0)
    h.print_tab()
    print(h.dequeue())
    print(h.peek())
    h.print_tab()
    while True:
        el = h.dequeue()
        if el is None:
            break
        print(el)
    h.print_tab()
