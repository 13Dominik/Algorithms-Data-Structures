# Hash table
# DOMINIK TOMALCZYK

from typing import Union, TypeVar, Any

DELETED = TypeVar("DELETED")
KEY = TypeVar("KEY", str, int)


class FullListException(Exception):
    """Raised when the list is full, and can not add new element"""
    pass


class ElementNotInList(Exception):
    """Raised when the element is not in list"""
    pass


class Element:
    def __init__(self, key: KEY, value: Any):
        self.key = key
        self.value = value

    def __str__(self):
        return f"{self.key} : {self.value}"

    def __repr__(self):
        return f"{self.key} : {self.value}"


class HashTable:
    def __init__(self, size: int, c1: int = 1, c2: int = 0):
        self.tab: list = [None for _ in range(size)]
        self.c1 = c1
        self.c2 = c2

    def do_hash(self, key: KEY) -> int:
        """ Hash element key and return position in self.tab to put a element """
        if isinstance(key, str):
            key = sum([ord(char) for char in key])
        return key % len(self.tab)

    def search(self, key: KEY):
        """ Returns value of a key, if not found None"""
        idx = self.do_hash(key)
        # if element is empty
        if self.tab[idx] is None:
            return None
        # if element is on index
        if isinstance(self.tab[idx], Element) and self.tab[idx].key == key:
            return self.tab[idx].value

        # look for conflict
        for i in range(1, len(self.tab)):
            new_index = (idx + self.c1 * i + self.c2 * i ** 2) % len(self.tab)
            if self.tab[new_index] is not None and self.tab[new_index] is not DELETED:
                if self.tab[new_index].key == key:
                    return self.tab[new_index].value
        # element not found
        return None

    def insert(self, elem: Element):
        idx: int = self.do_hash(elem.key)
        # if there is no element or element have the same key -> overwrite it
        if self.tab[idx] is None or self.tab[idx] is DELETED:
            self.tab[idx] = elem
            return
        if isinstance(self.tab[idx], Element) and self.tab[idx].key == elem.key:
            self.tab[idx] = elem
            return
        self.solve_conflict(elem)

    def remove(self, key: KEY):
        idx = self.do_hash(key)
        if self.tab[idx] is None:
            return None
        if isinstance(self.tab[idx], Element) and self.tab[idx].key == key:
            self.tab[idx] = DELETED
            return
        for i in range(1, len(self.tab)):
            new_index = (idx + self.c1 * i + self.c2 * i ** 2) % len(self.tab)
            if isinstance(self.tab[new_index], Element) and self.tab[new_index].key == key:
                self.tab[new_index] = DELETED
                return
                # element not found
        raise ElementNotInList

    def solve_conflict(self, elem):
        """ solve problem with open addressing method """
        idx = self.do_hash(elem.key)
        for i in range(1, len(self.tab)):
            # New index, square probing
            new_index = (idx + self.c1 * i + self.c2 * i ** 2) % len(self.tab)
            # if new space is empty or have the same key -> overwrite it
            if isinstance(self.tab[new_index], Element) and self.tab[new_index].key == elem.key:
                self.tab[new_index] = elem
                return
            if self.tab[new_index] is None or self.tab[new_index] is DELETED:
                self.tab[new_index] = elem
                return
        raise FullListException

    def __str__(self):
        s = "{"
        for elem in self.tab:
            s += str(elem)
            s += ", "
        return s + "}"


if __name__ == '__main__':
    def test_first_case(c1=0, c2=1):
        ht = HashTable(13, c1, c2)
        letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"]
        for i in range(1, 16):
            try:
                if i == 6:
                    ht.insert(Element(18, "F"))
                    continue
                if i == 7:
                    ht.insert(Element(31, "G"))
                    continue
                ht.insert(Element(i, letters[i - 1]))
            except FullListException:
                print(f"Brak miejsca! Element: {i} nie został dodany!")
        print(ht)
        print(ht.search(5))
        print(ht.search(14))
        ht.insert(Element(5, "Z"))
        print(ht.search(5))
        ht.remove(5)
        print(ht)
        print(ht.search(31))
        # Problem z szukaniem elementow po usunieciu innych został rozwiązany stosując specjalne oznacznie "DELETED"
        ht.insert(Element("W", "test"))
        print(ht)


    def test_second_case(c1=1, c2=0):
        ht = HashTable(13, c1, c2)
        letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"]
        for i in range(1, 14):
            try:
                ht.insert(Element(i * 13, letters[i - 1]))
            except FullListException:
                print(f"Nie znaleziono miejsca! Element: {i * 13} nie został dodany!")
        print(ht)


    test_first_case(1, 0)

    test_second_case(1, 0)  # probkowanie liniowe

    test_second_case(0, 1)  # ponowne wywolanie drugiej funkcji z probkowaniem kwadratowym

    test_first_case(0, 1)  # pierwsza funkcja z probkowaniem kwadratowym
