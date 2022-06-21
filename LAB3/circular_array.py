# Circular array
# Dominik Tomalczyk

from typing import Optional


class Queue:
    def __init__(self):
        self.__array = [None for _ in range(5)]
        self.idx_enq = 0
        self.idx_deq = 0

    @property
    def size(self) -> int:
        return len(self.__array)

    def is_empty(self) -> bool:
        return self.idx_enq == self.idx_deq

    def peek(self) -> Optional[int]:
        """ Returns current element to dequeue (only showing element) """
        return self.__array[self.idx_deq]

    def dequeue(self) -> Optional[int]:
        """ Dequeue current element """
        current = self.__array[self.idx_deq]

        if current is None:  # If list is empty
            return None

        self.__array[self.idx_deq] = None  # pop value

        if self.idx_deq == self.size - 1:
            self.idx_deq = 0
        else:
            self.idx_deq += 1
        return current

    def enqueue(self, value) -> None:
        """ Add new element to queue """
        self.__array[self.idx_enq] = value
        if self.idx_enq == self.size - 1:
            self.idx_enq = 0
        else:
            self.idx_enq += 1
        if self.idx_enq == self.idx_deq:
            self.realloc(self.idx_enq)

    def realloc(self, idx) -> None:
        """ Allocate 2 times bigger new array """
        new_list = [None for _ in range(self.size * 2)]
        new_list[0:idx] = self.__array[0:idx]  # first elements
        new_list[-(self.size - idx):] = self.__array[idx:]  # lasts elements
        self.idx_deq += self.size  # new deq index
        self.__array = new_list

    def show_queue(self) -> str:
        s = "Current Queue: "

        current_element = self.idx_deq
        while self.__array[current_element] is not None:
            s += f"{str(self.__array[current_element])} "
            if current_element == self.size - 1:
                current_element = 0
            else:
                current_element += 1

        return s

    def __str__(self):
        return f"{self.__array}"


if __name__ == '__main__':

    q = Queue()
    for i in range(1, 5):
        q.enqueue(i)
    print(q)
    print(q.show_queue())
    print(q.dequeue())
    print(q.peek())
    print(q.show_queue())

    for i in range(5, 9):
        q.enqueue(i)
    print(q)

    elem = q.dequeue()
    while elem is not None:
        print(elem)
        elem = q.dequeue()

    print(q.show_queue())

