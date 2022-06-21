# Shellsort
# Dominik Tomalczyk

import random
from copy import deepcopy, copy
import time


def knuth_gap(array):
    """ Returns gap for shellsort Formula: (3^n – 1)/2"""
    gap = 1
    while gap < len(array) / 3:
        gap = gap * 3 + 1
    return gap


def shell(array):
    gap = knuth_gap(array)
    while gap > 0:
        for i in range(gap, len(array)):
            temp = array[i]
            j = i
            # j >= gap needed to end on index 0, dont go for minus
            while j >= gap and array[j - gap] > temp:
                array[j] = array[j - gap]
                j -= gap

            array[j] = temp
        gap //= 3


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


def quicksort(array):
    answear = copy(array)
    part(answear, 0, len(array) - 1)
    return answear


def part(array, start, end) -> None:
    if start >= end:
        return
    i = start
    j = end
    pivot = array[int((i + j) / 2)]

    while i < j:
        while array[i] < pivot:
            i += 1
        while array[j] > pivot:
            j -= 1
        if i <= j:
            array[i], array[j] = array[j], array[i]
            i += 1
            j -= 1
    if start < j:
        part(array, start, j)
    if i < end:
        part(array, i, end)


def median_3(a, b, c):
    return max(min(a, b), min(c, max(a, b)))


def median_1(a):
    return a


def median_2(a, b):
    return a


def median_4(a, b, c, d):
    f = max(min(a, b), min(c, d))  # usuwa najmniejsza z 4
    g = min(max(a, b), max(c, d))  # usuwa największą z 4
    return median_2(f, g)


def median_5(a, b, c, d, e):
    f = max(min(a, b), min(c, d))  # usuwa najmniejsza z 4
    g = min(max(a, b), max(c, d))  # usuwa największą z 4
    return median_3(e, f, g)


def compute_median(array):
    if len(array) == 1:
        return array[0]
    chunks = [array[i: i + 5] for i in range(0, len(array), 5)]
    l = []
    for chunk in chunks:
        if len(chunk) == 5:
            l.append(median_5(chunk[0], chunk[1], chunk[2], chunk[3], chunk[4]))
        elif len(chunk) == 4:
            l.append(median_4(chunk[0], chunk[1], chunk[2], chunk[3]))
        elif len(chunk) == 3:
            l.append(median_3(chunk[0], chunk[1], chunk[2]))
        elif len(chunk) == 2:
            l.append(median_2(chunk[0], chunk[1]))
        elif len(chunk) == 1:
            l.append(median_1(chunk[0]))
    return compute_median(l)


def quicksort_median(array):
    answear = copy(array)
    part_median(answear, 0, len(array) - 1)
    return answear


def part_median(array, start, end) -> None:
    if start >= end:
        return
    i = start
    j = end
    pivot = compute_median(array[i:j + 1])

    while i < j:
        while array[i] < pivot:
            i += 1
        while array[j] > pivot:
            j -= 1
        if i <= j:
            array[i], array[j] = array[j], array[i]
            i += 1
            j -= 1
    if start < j:
        part_median(array, start, j)
    if i < end:
        part_median(array, i, end)


if __name__ == '__main__':
    array_to_sort = [int(random.random() * 100) for _ in range(10000)]
    array_to_sort2 = deepcopy(array_to_sort)
    array_to_sort3 = deepcopy(array_to_sort)
    array_to_sort4 = deepcopy(array_to_sort)
    array_to_sort5 = deepcopy(array_to_sort)

    h = Heap(array_to_sort)
    t_start = time.perf_counter()
    h.build_heap()
    h.heapsort()
    t_stop = time.perf_counter()
    print("Czas sortowania heapsort: ", t_stop - t_start)

    t_start2 = time.perf_counter()
    shell(array_to_sort3)
    t_stop2 = time.perf_counter()
    print("Czas sortowania shellsort: ", t_stop2 - t_start2)

    t_start3 = time.perf_counter()
    insertion_swap(array_to_sort2)
    t_stop3 = time.perf_counter()
    print("Czas sortowania insertion: ", t_stop3 - t_start3)

    t_start4 = time.perf_counter()
    quicksort(array_to_sort4)
    t_stop4 = time.perf_counter()
    print("Czas sortowania quicksort: ", t_stop4 - t_start4)

    t_start5 = time.perf_counter()
    quicksort_median(array_to_sort5)
    t_stop5 = time.perf_counter()
    print("Czas sortowania quicksort z wykorzystaniem mediany: ", t_stop5 - t_start5)
