"""Module contains 5 data structures: Graph, LinkedList, Queue, Stack, HashTable."""

from abc import ABC


class ABCLinkedList(ABC):
    """Abstract class for creating data structures on LinkedList base."""

    def __init__(self, *args):
        self._head = None
        self._tail = None
        self._length = 0

        for data in args:
            self._append(data)

    class Node:
        """Node of linked list."""

        def __init__(self, data, next_node=None):
            self.data = data
            self.next_node = next_node

        def __repr__(self):
            return f"Node({self.data})"

        __str__ = __repr__

    def __len__(self):
        return self._length

    def _get_item(self, index):
        """Returns node by index."""

        check = index > self._length-1 if index > 0 else index > self._length
        if check:
            raise ValueError(f"Index {index} is out of range!")

        # turn negative index in positive
        if index < 0:
            index = self._length + index

        node = self._head
        for _ in range(index):
            node = node.next_node

        return node

    def _append(self, data):
        """Adds new item in the end of the linked list."""

        self._length += 1
        new_node = self.Node(data, None)

        if not self._head:
            self._head = new_node
            self._tail = new_node
        else:
            self._tail.next_node = new_node
            self._tail = new_node

    def _prepend(self, data):
        """Adds new item in the start of the linked list."""

        self._length += 1
        new_node = self.Node(data, None)

        if not self._head:
            self._head = new_node
            self._tail = new_node
        else:
            old_head = self._head
            self._head = new_node
            self._head.next_node = old_head

    def _lookup(self, data):
        """Returns index of node with specified data."""

        for index in range(self._length):
            if self._get_item(index).data == data:
                return index

        raise ValueError(f"{data} is not in LinkedList!")

    def _insert(self, data, index):
        """Inserts data in specified index."""

        if index == 0:
            self._prepend(data)
        else:
            self._length += 1

            old_node = self._get_item(index)
            new_node = self.Node(data, old_node)
            self._get_item(index-1).next_node = new_node

    def _delete(self, index):
        """Deletes node by index."""

        if index in [0, -self._length]:

            if self._length == 1:
                self._head, self._tail = None, None
            else:
                self._head = self._get_item(1)

        else:
            old_next = self._get_item(index).next_node
            self._get_item(index-1).next_node = old_next

            if index in [self._length-1, -1]:
                self._tail = self._get_item(index-1)

        self._length -= 1


class LinkedListIterator:
    """Iterator for linked list."""

    def __init__(self, head, length):

        self.head = head
        self.length = length
        self.nodes_gen_attr = self.nodes_gen()

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.nodes_gen_attr)

    def nodes_gen(self):
        """Generator for linked list nodes iteration."""

        node = self.head

        for _ in range(self.length):
            yield node
            node = node.next_node


class LinkedList(ABCLinkedList):
    """ABCLinkedList implementation"""

    def __init__(self, *args):
        super().__init__(*args)
        self._update_attributes()

    def _update_attributes(self):
        """Updates public attributes"""

        self.head = self._head
        self.length = self._length
        self.tail = self._tail

    def __getitem__(self, index):
        return self._get_item(index)

    def __iter__(self):
        return LinkedListIterator(self.head, self.length)

    def __add__(self, other):
        for value in other:
            self.append(value)

    def __repr__(self):
        str_list = ""
        for node in self:
            str_list += f"{str(node)}"
        return f"LinkedList({str_list})"

    def append(self, data):
        self._append(data)
        self._update_attributes()

    def insert(self, data, index):
        self._insert(data, index)
        self._update_attributes()

    def lookup(self, data):
        return self._lookup(data)

    def prepend(self, data):
        self._prepend(data)
        self._update_attributes()

    def delete(self, index):
        self._delete(index)
        self._update_attributes()


class Graph(ABCLinkedList):
    """Implementation of graph based on linked list."""

    def __init__(self):
        super().__init__(None)
        self.peaks_linked_list = LinkedList()
        self.size = len(self.peaks_linked_list)

    class Peak:
        """Peak of graph. Have value and connections list."""

        def __init__(self, data, *args):
            self.data = data
            self.connections = LinkedList()
            for peak in args:
                self.connections.append(peak)

        def __repr__(self):
            connections_str = ""
            for node in self.connections:
                connections_str += f"Peak({node.data.data}) "

            return f"(Peak ({self.data}, connections:{connections_str}))"

        def __eq__(self, other):
            if not isinstance(other, self.__class__):
                return self.data == other

            return id(self) == id(other)

    def __iter__(self):
        return self.peaks_linked_list.__iter__()

    def insert(self, data, *args):
        """Adds new peak with specified data.

        First argument is value of new peak, all others args should be instances of Peak class.
        They will be added at new peaks connection list.

        You can make connection only with peaks that exist in 'peaks_linked_list'"""

        self._check_args(*args)

        new_peak = self.Peak(data, *args)
        self.peaks_linked_list.append(new_peak)

        for peak in args:
            peak.connections.append(new_peak)

    def _check_args(self, *args):
        """Check args for 'insert' and 'delete' functions."""

        for value in args:
            if not isinstance(value, self.Peak):
                raise ValueError("You should enter Peaks!")

            for node in self.peaks_linked_list:
                if value == node.data:
                    return True
            raise ValueError(f"{value} does not exist in Graph!")

    def lookup(self, data):
        """Returns peak with specified data."""

        return self.peaks_linked_list[self.peaks_linked_list.lookup(data)].data

    def delete(self, delete_peak: Peak):
        """Deletes peak from 'peaks_linked_list' and from 'connection' list
        is all other peaks."""

        self._check_args(delete_peak)

        for node in delete_peak.connections:
            index = node.data.connections.lookup(delete_peak)
            node.data.connections.delete(index)

        index = self.peaks_linked_list.lookup(delete_peak)
        self.peaks_linked_list.delete(index)


class HashTableIterator:
    """Iterator for HashTable."""

    def __init__(self, hash_table, length):

        self.hash_table = hash_table
        self.length = length
        self.nodes_gen_attr = self.nodes_gen()

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.nodes_gen_attr)

    def nodes_gen(self):
        """Return cells that not empy."""

        for index in range(self.length):
            for node in self.hash_table._get_item(index).data:
                yield node.data, index


class HashTable(ABCLinkedList):
    """Implementation of hash table based on linked list."""

    def __init__(self, *args):
        super().__init__()
        self._create_table_list()

        for value in args:
            self.insert(value)

    def __iter__(self):
        return HashTableIterator(self, self._length)

    @staticmethod
    def _make_hash(data):
        """Makes hash for value."""

        if isinstance(data, str):
            result = sum([ord(char) for char in data])
        elif isinstance(data, int):
            result = data
        elif isinstance(data, tuple):
            result = hash(tuple)
        else:
            raise ValueError(f"Hash is not supported for {type(data)}")

        return result % 30

    def _create_table_list(self):
        """Creates 30 cells (linked list with 30 linked lists) for hash table."""

        for _ in range(30):
            self._append(LinkedList())

    def insert(self, data):
        """Makes hash for data add puts it in appropriate cell. """

        index = self._make_hash(data)

        self._get_item(index).data.append(data)

    def lookup(self, index):
        """Returns values with specified key."""

        for value in self._get_item(index).data:
            yield value.data

    def delete(self, index):
        """Deletes all values with specified index."""

        self._get_item(index).data = LinkedList()


class Stack(ABCLinkedList):
    """Implementation of stack based on linked list."""

    def __init__(self, *args):
        super().__init__(*args)
        self.length = self._length

    def __iter__(self):
        return self

    def __next__(self):
        try:
            data = self.pop()
            return data
        except ValueError:
            raise StopIteration

    def __len__(self):
        return self.length

    def push(self, data):
        """Push new item on the end of the stack."""
        self._append(data)
        self.length = self._length

    def pop(self):
        """Returns last item end deletes it from the stack."""

        if self._length == 0:
            raise ValueError("Stack is empty!")

        data = self._get_item(-1).data
        super()._delete(-1)
        self.length = self._length
        return data

    def peek(self):
        """Return last item without deleting."""

        return self._tail.data


class Queue(ABCLinkedList):
    """Implementation of queue based on linked list."""

    def __init__(self, *args):
        super().__init__(*args)
        self.length = self._length

    def __iter__(self):
        return self

    def __len__(self):
        return self.length

    def __next__(self):
        try:
            data = self.dequeue()
            return data
        except ValueError:
            raise StopIteration

    def enqueue(self, data):
        """Appends item to queue"""

        self._append(data)
        self.length = self._length

    def dequeue(self):
        """Returns first item end deletes it from the queue."""

        if self._length == 0:
            raise ValueError("Queue is empty")
        data = self._get_item(0).data
        self._delete(0)

        self.length = self._length
        return data

    def peek(self):
        """Returns first item without deleting."""

        return self._head.data


class BSTIterator:
    """Iterator for BinarySearchTree"""

    def __init__(self, root):
        self.root = root
        self.gen = self.traversal_gen(self.root)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.gen)

    def traversal_gen(self, node):
        """In order binary tree traversal"""

        if node:
            yield from self.traversal_gen(node.left_child)
            yield node.value
            yield from self.traversal_gen(node.right_child)


class BinarySearchTree:
    """Implementation of binary sort tree."""

    def __init__(self, *args):
        self.root = None
        self.size = 0

        for value in args:
            self.add_node(value)

    class BSTNode:
        """Node of binary search tree."""

        def __init__(self, value):
            self.value = value
            self.left_child = None
            self.right_child = None
            self.parent = None

        def __repr__(self):
            return f"BST node({self.value})"

    def __iter__(self):
        return BSTIterator(self.root)

    def add_node(self, value):
        """Adds value to the tree."""

        new_node = self.BSTNode(value)

        if not self.root:
            self.root = new_node
        else:
            node = self.root
            while True:
                side = self._find_side(node.value, value)
                node_side = getattr(node, side)

                if node_side is None:
                    new_node.parent = node
                    setattr(node, side, new_node)
                    self.size += 1
                    break

                node = node_side

    def find(self, value):
        """Finds value in tree"""

        node = self.root

        while True:
            if node.value == value:
                return node

            side = self._find_side(node.value, value)
            node_side = getattr(node, side)

            if node_side is None:
                break
            node = node_side
        raise ValueError("Value is not in tree.")

    def delete(self, value):
        """Deletes value from tree. Uses 3 different algorithms for each case:
        1. If node doesn't have children
        2. If node have one child
        3. If node have 2 children"""

        node = self.find(value)
        if not node:
            raise ValueError(f"There are node with {value} value!")

        if not node.left_child and not node.right_child:
            self._delete_no_child(node)
        elif (not node.left_child and node.right_child or
              node.left_child and not node.right_child):
            self._delete_one_child(node)
        else:
            self._delete_two_child(node)

        self.size -= 1

    def _delete_two_child(self, node):
        """Algorithm for deleting node with two children"""

        heir = node.right_child

        while heir.left_child:
            heir = heir.left_child

        node.value = heir.value

        if heir.right_child:
            self._delete_one_child(heir)
        else:
            self._delete_no_child(heir)

    def _delete_one_child(self, node: BSTNode):
        """Algorithm for deleting node with one child"""

        child = node.left_child if node.left_child else node.right_child

        if node.value == self.root.value:
            self.root = child
        else:
            side = self._find_side(node.parent.value, node.value)
            setattr(node.parent, side, child)

    def _delete_no_child(self, node: BSTNode):
        """Algorithm for deleting node with no children"""

        if self.root.value == node.value:
            self.root = None
        else:
            side = self._find_side(node.parent.value, node.value)
            setattr(node.parent, side, None)

    @staticmethod
    def _find_side(value1, value2):
        """Compares values and returns what child should the element be"""

        return "left_child" if value1 >= value2 else "right_child"
