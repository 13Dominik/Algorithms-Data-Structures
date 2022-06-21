# Skipping list
# Dominik Tomalczyk

from random import random
from typing import Any, Optional, Union


class Element:
    def __init__(self, key: Union[int, str], value: Any, maxlevel: int, levels: Optional[int] = 0):
        """
        Creating a element of skip list
        :param key: key of a element (int) or head (str)
        :param value: value of a element
        :param maxlevel:  number of maximum possible levels in every element
        :param levels: # if levels is passed (it means initialize a HEAD list) create a self.head of
        levels height. If not passed create a list of random (1, maxlevel) height (initializing a element, not a HEAD)
        """
        self.key = key
        self.value = value
        self.maxlevel = maxlevel  # max number of levels (must be the same as SkipList maxheight)
        self.levels = levels  # current number of levels (random)
        self.next = [None for _ in range(self.levels)]

    @property
    def levels(self):
        return self.__levels

    @levels.setter
    def levels(self, levels):
        if levels == 0:
            p = 0.5
            lvl = 1
            while random() < p and lvl < self.maxlevel:
                lvl += 1
            self.__levels = lvl
        else:
            self.__levels = levels

    def __str__(self):
        return f"{self.key} : {self.value}"

    def __repr__(self):
        return f"{self.key} : {self.value}"


class SkipList:
    def __init__(self, maxheight: int):
        self.maxheight = maxheight  # max height of every element
        self.head = Element("HEAD", "HEAD", maxheight, maxheight)  # initalize a head list of maxheight height

    def search(self, key):
        current = self.head
        for i in range(self.maxheight - 1, -1, -1):  # for every lvl from up to down
            # for every lvl move forward
            while current.next[i] and current.next[i].key < key:
                current = current.next[i]

        current = current.next[0]
        if current is None or current.key != key:  # if element not found
            return None

        return f"{current}"

    def insert(self, elem: Element):
        if self.search(elem.key) is not None:  # If element with this key in list, remove it and add as new
            self.remove(elem.key)
        previous = [None for _ in range(self.maxheight)]  # previous array (path to node)
        current = self.head

        # start from highest level, skipping nodes
        for i in range(self.maxheight - 1, -1, -1):
            while current.next[i] and current.next[i].key < elem.key:
                current = current.next[i]
            previous[i] = current  # save path to array of paths

        # reached level 0 and forward reference to right, which is correct position to insert key.
        current = current.next[0]
        # if end of list or correct position
        if current is None or current.key != elem.key:
            n = elem
            # now it looks: old1 -> new -> old2
            for i in range(n.levels):

                previous[i].next[i] = n  # old1 -> new

    def remove(self, search_key):
        # create update array and initialize it
        previous = [None for _ in range(self.maxheight)]
        current = self.head

        # start from highest level, skipping nodes
        for i in range(self.maxheight - 1, -1, -1):
            while current.next[i] and current.next[i].key < search_key:
                current = current.next[i]
            previous[i] = current  # save path to array of paths

        # reached level 0 and forward reference to right, which is desired position to insert key.
        current = current.next[0]

        # If current node is target node
        if current is not None and current.key == search_key:

            # starts from lowest level to highest
            for i in range(self.maxheight):

                # if previous not points to current (it means we remove all levels from current)
                # and now previous looks for current.next
                # reached highest level of current
                if previous[i].next[i] != current:
                    break
                # if previous looks for current remove one level:
                # skipping current element prev now points to next (similar to Linked list)
                previous[i].next[i] = current.next[i]

    def __str__(self):
        s = "<<HEAD>> "
        current = self.head.next[0]
        s += str(current)
        s += ", "
        while current:
            if current.next[0] is None:
                break
            s += str(current.next[0])
            s += ", "
            current = current.next[0]

        return f"{s[:-2]}"

    def displayList_(self):
        node = self.head.next[0]  # first element on level 0
        keys = []  # list of keys on this level
        while node is not None:
            keys.append(node.key)
            node = node.next[0]

        for lvl in range(self.maxheight - 1, -1, -1):
            print("{}: ".format(lvl), end=" ")
            node = self.head.next[lvl]
            idx = 0
            while node is not None:
                while node.key > keys[idx]:
                    print("  ", end=" ")
                    idx += 1
                idx += 1
                print("{:2d}".format(node.key), end=" ")
                node = node.next[lvl]
            print("")


if __name__ == '__main__':
    HEIGHT = 6
    skip_list = SkipList(HEIGHT)
    letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"]
    for i in range(1, 16):
        skip_list.insert(Element(i, letters[i - 1], HEIGHT))
    skip_list.displayList_()
    print(skip_list.search(2))
    skip_list.insert(Element(2, "Z", HEIGHT))
    print(skip_list.search(2))
    skip_list.remove(5)
    skip_list.remove(6)
    skip_list.remove(7)
    skip_list.displayList_()
    skip_list.insert(Element(6, "W", HEIGHT))
    skip_list.displayList_()
