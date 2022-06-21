# Linked List
# Dominik Tomalczyk
from copy import deepcopy
from typing import Tuple


class Node:
    def __init__(self, node_as_tuple: Tuple[str, str, int]):
        self.university = node_as_tuple[0]
        self.city = node_as_tuple[1]
        self.date = node_as_tuple[2]
        self.next = None

    def __str__(self):
        return f"{self.university} {self.city} {self.date}"

    def __repr__(self):
        return f"{self.university} {self.city} {self.date}"


class LinkedList:
    def __init__(self):
        self.head = None

    def destroy(self) -> None:
        """ Delete all nodes """
        self.head = None

    def add(self, node: Node) -> None:
        """ Add element as first (head) """
        # add to empty list:
        node = deepcopy(node)
        if self.head is None:
            self.head = node
            return
        # add as first element:
        node.next = self.head
        self.head = node

    def remove(self) -> None:
        """ Removes first element """
        if self.is_empty():
            raise IndexError("List is empty!")
        self.head = self.head.next

    def is_empty(self) -> bool:
        return self.head is None

    def length(self) -> int:
        lenght = 0
        current = self.head
        while current is not None:
            lenght += 1
            current = current.next
        return lenght

    def get(self) -> Node:
        """ Return first element (head) """
        if self.is_empty():
            raise IndexError("List is empty!")
        return self.head

    def add_to_end(self, node: Node) -> None:
        node = deepcopy(node)
        # add to empty list:
        if self.head is None:
            self.head = node
            return
        # add as last element:
        current = self.head
        while current.next is not None:
            current = current.next
        current.next = node

    def remove_last(self) -> None:
        if self.is_empty():
            raise IndexError("List is empty!")
        if self.length() == 1:
            self.head = None
            return
        current = self.head
        while current.next.next is not None:
            current = current.next
        current.next = None

    def show_list(self) -> None:
        current = self.head
        i = 1
        print("<< HEAD >>")
        while current is not None:
            print(f"{i} - {current}")
            i += 1
            current = current.next

    def take(self, n):
        """ Create a new Linked list from first n elements """
        if n < 1:
            raise Exception("Can't take less than one node!")

        if n >= self.length():
            return deepcopy(self)  # copy whole linked list
        # when n < length copy n elements
        copied_list = deepcopy(self)
        current = copied_list.head
        for i in range(n - 1):
            current = current.next
        current.next = None
        return copied_list

    def drop(self, n):
        """ Create a new linked list from n last elements """
        if n < 1:
            raise Exception("Can't take less than one node!")

        if n >= self.length():  # return empty list
            return LinkedList()

        new_lst = LinkedList()
        current = self.head
        # skipping first elements
        for i in range(n):  # numbers of elements to skip during copying
            current = current.next
        # adding last elements
        for i in range(self.length() - n):
            new_node = deepcopy(current)
            new_node.next = None
            new_lst.add_to_end(deepcopy(new_node))
            current = current.next
        return new_lst


if __name__ == '__main__':
    nodes = [('AGH', 'Kraków', 1919),
             ('UJ', 'Kraków', 1364),
             ('PW', 'Warszawa', 1915),
             ('UW', 'Warszawa', 1915),
             ('UP', 'Poznań', 1919),
             ('PG', 'Gdańsk', 1945)]
    n0 = Node(nodes[0])
    n1 = Node(nodes[1])
    n2 = Node(nodes[2])
    n3 = Node(nodes[3])
    n4 = Node(nodes[4])
    n5 = Node(nodes[5])
    print("Tworzenie pustej listy i dodawanie dwóch elementów na początek:")
    ll = LinkedList()
    ll.add(n0)
    ll.add(n1)
    ll.show_list()
    print("Dodawanie elementu na koniec:")
    ll.add_to_end(n2)
    ll.show_list()
    print("Usuwanie ostatniego elementu:")
    ll.remove_last()
    ll.show_list()

    print("Wyciąganie pierwsego elementu listy:")
    print(ll.get())

    print("Usuwanie pierwszego elementu:")
    ll.remove()
    ll.show_list()
    print("Sprawdzanie czy lista jest pusta:")
    print(ll.is_empty())
    print("Sprawdzanie długości listy:")
    print(ll.length())
    print("Niszczenie listy:")
    ll.destroy()
    print(ll.is_empty())

    for node in nodes:
        ll.add(Node(node))
    print("Lista ze wszystkich elementow")
    ll.show_list()

    print("Kopiowanie listy z pominięciem 3 pierwszych elementów:")
    new_ll = ll.drop(3)
    new_ll.show_list()

    print("Kopiowanie 4 pierwszych elementow listy:")
    new_ll2 = ll.take(4)
    new_ll2.show_list()
