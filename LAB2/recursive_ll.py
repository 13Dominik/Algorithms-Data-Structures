# Recursive Linked List
# Dominik Tomalczyk
from copy import deepcopy
from typing import Tuple


# class representing node (from first exercise)
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


# interface :
def nil():
    return None


def cons(el: Node, lst):
    el = deepcopy(el)
    if lst is None:
        lst = el
        return lst
    el.next = lst
    return el


def first(lst):
    """  Create copy of first element and return it"""
    lst = deepcopy(lst)
    if lst is None:
        return None
    lst.next = None
    return lst


def rest(lst):
    if lst is None:
        return None
    return lst.next


# implementing linked list using interface above
def create():
    return nil()


def destroy(lst: Node):
    return None


def add(el, lst):
    return cons(el, lst)


def remove(lst):
    return rest(lst)


def is_empty(lst):
    return lst is None


def length(lst):
    if lst is None:
        return 0
    else:
        return 1 + length(rest(lst))


def get(lst):
    _first = first(lst)
    return _first


def get_last(lst):
    if lst is None:
        return None
    if rest(lst) is None:
        return lst
    else:
        return get_last(rest(lst))


def show_list(lst):
    if lst is None:
        return " << TAIL >> "
    else:
        return str(lst) + "\n" + show_list(rest(lst))


def add_end(el, lst):
    if is_empty(lst):
        return cons(el, lst)
    else:
        first_el = first(lst)  # first element of list
        rest_lst = rest(lst)  # rest of list
        recreated_lst = add_end(el, rest_lst)
        return cons(first_el, recreated_lst)


def remove_last(lst):
    if is_empty(rest(lst)):
        return None
    else:
        first_el = first(lst)
        rest_lst = rest(lst)
        recreated_lst = remove_last(rest_lst)

        return cons(first_el, recreated_lst)


def take(n, lst, new_lst):
    """ Create a new linked list from n last elements """
    if n > length(lst):
        return deepcopy(lst)
    else:
        return take_recursive(n, lst, new_lst)


def take_recursive(n, lst, new_lst):
    """ Create a new Linked list from first n elements """
    if n < 1:
        raise Exception("Can't take less than one node!")

    lst = deepcopy(lst)
    # if new_list took n elements from lst, return
    if length(new_lst) == n:
        return new_lst

    else:
        lst_without_head = rest(lst)  # lst without head
        new_lst = add_end(get(lst), new_lst)  # add head to new list
        return take_recursive(n, lst_without_head,
                              new_lst)  # call take, with the same n, old list without head, and new list


def drop(n, lst, new_lst):
    """ Create a new linked list from n last elements """
    if n > length(lst):
        return None
    else:
        return drop_recursive(length(lst) - n, lst, new_lst)


def drop_recursive(n, lst, new_lst):
    if n < 1:
        raise Exception("Can't take less than one node!")

    lst = deepcopy(lst)
    # if new_list took n elements from lst, return
    if length(new_lst) == n:
        return new_lst

    new_lst = add(get_last(lst), new_lst)
    lst_without_tail = remove_last(lst)  # lst without tail
    return drop_recursive(n, lst_without_tail, new_lst)


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
    head = create()
    head = add(n0, head)
    head = add(n1, head)
    print(show_list(head))
    print("Wyciąganie ostatniego elementu z listy:")
    print(get_last(head))

    print("Dodawanie elementu na koniec:")
    head = add_end(n2, head)
    print(show_list(head))
    print("Usuwanie ostatniego elementu:")
    head = remove_last(head)
    print(show_list(head))

    print("Wyciąganie pierwsego elementu listy:")
    first_node = first(head)
    print(first_node)

    print("Usuwanie pierwszego elementu:")
    head = remove(head)
    print(show_list(head))
    print("Sprawdzanie czy lista jest pusta:")
    print(is_empty(head))
    print("Sprawdzanie długości listy:")
    print(length(head))
    print("Niszczenie listy:")
    head = destroy(head)
    print(is_empty(head))

    head = create()
    for node in nodes:
        head = add(Node(node), head)
    print("Lista ze wszystkich elementow")
    print(show_list(head))

    print("Kopiowanie listy z pominięciem 2 pierwszych elementów")
    new_head = create()
    new_head = drop(2, head, new_head)
    print(show_list(new_head))

    new_head = destroy(head)
    print("Kopiowanie 4 pierwszych elementow listy:")
    new_head = take(4, head, new_head)
    print(show_list(new_head))
