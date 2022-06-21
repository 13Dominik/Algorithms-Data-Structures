# Heapsort
# Dominik Tomalczyk
import random
import time
from copy import deepcopy


# Class element (lab 6):
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
    def __init__(self, array=None):
        if array is None:
            self.array = []
        else:
            self.array = array

    @property
    def size(self):
        return len(self.array)

    def right(self, i):
        return 2 * i + 2

    def left(self, i):
        return 2 * i + 1

    def parent(self, i):
        return (i - 1) // 2

    def is_empty(self):
        return not bool(self.array)

    def build_heap(self):
        # Building heap
        for i in range(self.size // 2, -1, -1):
            # For every parent in heap, array_len = len(heap)
            self.__heapify(self.size, i)

    def __heapify(self, array_len, start_idx):
        left = self.left(start_idx)
        right = self.right(start_idx)
        largest = start_idx

        # if left child exists and has highest prio:
        if left <= array_len - 1 and self.array[left] > self.array[largest]:
            largest = left
        # if right child exists and has highest prio
        if right <= array_len - 1 and self.array[right] > self.array[largest]:
            largest = right

        # if something has changed:
        if largest != start_idx:
            self.array[start_idx], self.array[largest] = self.array[largest], self.array[start_idx]
            self.__heapify(array_len, largest)

    def heapsort(self):
        # every iteration we skip last element (wchich is sorted)
        for i in range(self.size - 1, -1, -1):
            self.array[i], self.array[0] = self.array[0], self.array[i]
            self.__heapify(i, 0)

    def print_tab(self):
        if self.is_empty():
            print("{ }")
            return
        print('{', end=' ')
        for i in range(self.size - 1):
            print(self.array[i], end=', ')
        if self.array[self.size - 1]:
            print(self.array[self.size - 1], end=' ')
        print('}')

    def print_tree(self, idx, lvl):
        if idx < self.size:
            self.print_tree(self.right(idx), lvl + 1)
            print(2 * lvl * '  ', self.array[idx] if self.array[idx] else None)
            self.print_tree(self.left(idx), lvl + 1)


def insertion_swap(array):
    for i in range(1, len(array)):
        key = array[i]
        j = i - 1
        while j >= 0 and array[j] > key:
            array[j + 1] = array[j]
            j -= 1
        array[j + 1] = key
    return array


def insertion_shift(array):
    for i in range(1, len(array)):
        key = array[i]
        j = i - 1

        while j >= 0 and array[j] > key:
            j = j - 1
        elem = array.pop(i)
        array.insert(j + 1, elem)
    return array


if __name__ == '__main__':
    l = [(5, 'A'), (5, 'B'), (7, 'C'), (2, 'D'), (5, 'E'), (1, 'F'), (7, 'G'), (5, 'H'), (1, 'I'), (2, 'J')]
    elems = [Element(l[i][1], l[i][0]) for i in range(len(l) - 1)]
    elems2 = deepcopy(elems)
    h = Heap(elems)
    h.build_heap()
    h.print_tab()
    h.print_tree(0, 0)
    h.heapsort()
    h.print_tab()

    rando_numbers = [int(random.random() * 100) for _ in range(10000)]
    h2 = Heap(rando_numbers)

    t_start = time.perf_counter()
    h2.build_heap()
    h2.heapsort()
    t_stop = time.perf_counter()
    print("Czas obliczeń heapsort (tablica 10000 elementów):", "{:.7f}".format(t_stop - t_start))

    # insert sortowanie na  tablicy elementów:
    print(insertion_shift(elems))
    print(insertion_swap(elems2))

    l = [int(random.random() * 1000) for _ in range(10000)]
    t_start_insertionshift = time.perf_counter()
    insertion_shift(l)
    t_stop_insertionshift = time.perf_counter()
    print("Czas obliczeń insertion_shift (tablica 10000 elementów):",
          "{:.7f}".format(t_stop_insertionshift - t_start_insertionshift))

    l = [int(random.random() * 1000) for _ in range(10000)]
    t_start_insertionswap = time.perf_counter()
    insertion_swap(l)
    t_stop_insertionswap = time.perf_counter()
    print("Czas obliczeń insertion_swap (tablica 10000 elementów):",
          "{:.7f}".format(t_stop_insertionswap - t_start_insertionswap))
