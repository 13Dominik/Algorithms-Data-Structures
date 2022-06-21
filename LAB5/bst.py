# Binary search tree
# Dominik Tomalczyk

class Node:
    def __init__(self, key, data):
        self.key = key
        self.data = data
        self.left = None
        self.right = None

    def __str__(self):
        return f"{self.key} : {self.data} "


class BST:
    def __init__(self):
        self.root = None

    def search(self, key):
        current = self.root

        if current is None:
            raise Exception("Element not found!")
        if current.key == key:
            return current.data
        else:
            return self.__search_recu(key, current)

    def __search_recu(self, key, current):
        if current is None:
            raise Exception("Element not found!")

        if current.key == key:
            return current.data
        if key > current.key:
            return self.__search_recu(key, current.right)
        return self.__search_recu(key, current.left)

    def insert(self, node: Node):
        if self.root is None:
            self.root = node
            return
        return self.__insert_recu(new_node=node, parent_node=self.root)

    def __insert_recu(self, new_node, parent_node):
        # overwrite node
        if new_node.key == parent_node.key:
            parent_node.data = new_node.data
            return
        # insert on left
        if new_node.key < parent_node.key and parent_node.left is None:
            parent_node.left = new_node
            return
        # insert on right
        if new_node.key > parent_node.key and parent_node.right is None:
            parent_node.right = new_node
            return
        # go left
        if new_node.key < parent_node.key:
            return self.__insert_recu(new_node, parent_node.left)
        # go right
        if new_node.key > parent_node.key:
            return self.__insert_recu(new_node, parent_node.right)

    def height(self, start_key=None):
        """ Compute (the greatest) height from node with start_key to end of tree"""
        if start_key is None:
            start_key = self.root.key
        current = self.root
        if current.key != start_key:
            return self.__height_recu(self.__go_to_node(start_key, current))  # go to correct node and start computing
        return self.__height_recu(current)  # if we start from root

    def __height_recu(self, node):
        """ Compute height from node to end """
        if node is None:
            return -1
        else:
            # Compute the depth of each subtree
            left_height = self.__height_recu(node.left)
            right_height = self.__height_recu(node.right)
            # Use the larger number
            if left_height > right_height:
                return left_height + 1
            else:
                return right_height + 1

    def __go_to_node(self, start_key, current):
        """ Go to correct node from wchich we should start counting """
        if current.key == start_key:
            return current
        # go left
        if start_key < current.key:
            return self.__go_to_node(start_key, current.left)
        # go right
        if start_key > current.key:
            return self.__go_to_node(start_key, current.right)

    def delete(self, key):
        current = self.root
        if current is None:
            raise Exception("Tree does not exist!")
        return self.__delete(current, key)

    def __delete(self, current, key):

        # go left
        if key < current.key:
            current.left = self.__delete(current.left, key)

        # go right
        elif key > current.key:
            current.right = self.__delete(current.right, key)

        # If current.key == key
        else:

            # Node with 0 or 1 child
            if current.left is None:
                temp = current.right
                return temp  # None or one (only) child
            # Node with 0 or 1 child
            elif current.right is None:
                temp = current.left
                return temp  # None or one (only) child

            # Node with two children:
            # find the lowest in right subtree:
            temp = current.right
            while temp.left is not None:
                temp = temp.left

            # Copy the lowest to current
            current.key = temp.key
            current.data = temp.data

            # Delete current
            current.right = self.__delete(current.right, temp.key)

        return current

    def print(self):
        """ Print sorted values from tree key: value"""
        return self.__print(self.root)

    def __print(self, current):
        if current.left:
            self.__print(current.left)
        print(f"{current.key} : {current.data}", end=', ')
        if current.right:
            self.__print(current.right)

    def print_tree(self):
        print("==============")
        self._print_tree(self.root, 0)
        print("==============")

    def _print_tree(self, node, lvl):
        if node is not None:
            self._print_tree(node.right, lvl + 5)

            print()
            print(lvl * " ", node.key, node.data)

            self._print_tree(node.left, lvl + 5)


if __name__ == '__main__':
    b = BST()
    for k, v in {50: 'A', 15: 'B', 62: 'C', 5: 'D', 20: 'E', 58: 'F', 91: 'G', 3: 'H', 8: 'I', 37: 'J', 60: 'K',
                 24: 'L'}.items():
        b.insert(Node(k, v))
    b.print_tree()
    b.print()
    b.search(24)
    b.insert(Node(20, "AA"))
    b.insert(Node(6, "M"))
    b.delete(62)
    b.insert(Node(59, "N"))
    b.insert(Node(100, "P"))
    b.delete(8)
    b.delete(15)
    b.insert(Node(55, "R"))
    b.delete(50)
    b.delete(5)
    b.delete(24)
    print()
    print(b.height())
    print()
    b.print()
    print()
    b.print_tree()
