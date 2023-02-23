# Implements a sorted list.
# CSC 202, Lab 5
# Given code, Summer '19

class SortedList:
    """
    A sorted collection of elements
    NOTE: Do not alter this class.
    """

    def __init__(self):
        # The length of the backing array:
        self.capacity = 4
        # The backing array:
        self.array = [None] * self.capacity
        # The number of elements in this sorted list:
        self.size = 0

    def __eq__(self, other):
        if type(other) != SortedList or self.size != other.size:
            return False

        for idx in range(self.size):
            if self.array[idx] != other.array[idx]:
                return False

        return True

    def __repr__(self):
        return "SortedList(%d, %r, %d)" \
               % (self.capacity, self.array, self.size)


def size(lst):
    """
    Count the number of elements in a sorted list.
    TODO: Implement this function. It must have O(1) complexity.

    :param lst: A SortedList
    :return: The number of elements in the sorted list
    """
    return lst.size


def get(lst, idx):
    """
    Get the element at an index.
    TODO: Implement this function. It must have O(1) complexity.

    :param lst: A SortedList
    :param idx: An index at which to get an element
    :return: The element in the sorted list at the index
    :raise IndexError: If the index is out-of-bounds
    """
    if idx < 0 or idx >= lst.size:
        raise IndexError

    return lst.array[idx]


def insert(lst, value):
    """
    Insert an element in sorted order, doubling capacity first if necessary.
    TODO: Implement this function. It must have O(n) complexity.

    :param lst: A SortedList
    :param value: A comparable value to insert as an element
    """
    if lst.size == lst.capacity:
        lst.capacity *= 2
        temp = lst.array
        lst.array = [None] * lst.capacity
        for i in range(lst.size):
            lst.array[i] = temp[i]
    for i in range(lst.size - 1, -1, -1):
        if lst.array[i] < value or lst.array[i] == value:
            lst.array[i + 1] = value
            lst.size += 1
            return
        else:
            lst.array[i + 1] = lst.array[i]
    lst.array[0] = value
    lst.size += 1
    return


def remove(lst, idx):
    """
    Remove the element at an index.
    TODO: Implement this function. It must have O(n) complexity.

    :param lst: A SortedList
    :param idx: An index at which to remove an element
    :return: The removed element
    :raise IndexError: If the index is out-of-bounds
    """
    if idx < 0 or idx >= lst.size:
        raise IndexError
    temp = lst.array[idx]
    if idx == lst.size - 1:
        lst.array[idx] = lst.array[idx-1]
    lst.size -= 1
    i = idx
    while i <= lst.size - 1:
        lst.array[i] = lst.array[i+1]
        i += 1
    return temp


def find(lst, value):
    """
    Find the index of an element.
    TODO: Implement this function. It must have O(log n) complexity.

    :param lst: A SortedList
    :param value: A comparable value to find as an element
    :return: The index of an element equal to the value
    :raise ValueError: If no element is equal to the value
    """
    low = 0
    high = lst.size - 1
    while low <= high:
        mid = (low+high) // 2
        if lst.array[mid] < value:
            low = mid + 1
        elif lst.array[mid] > value:
            high = mid - 1
        else:
            return mid
    raise ValueError


def create(array, size):
    """
    Create a new sorted list from an array.
    TODO: Implement this function. It must have O(n log n) complexity.
    :param array: An unsorted array of comparable values
    :param size: A length of a given array
    :return: A new SortedList containing the array's values in sorted order
    """
    new = SortedList()
    for i in range(size):
        insert(new, array[i])
    return new


def merge(lst_a, size_a, lst_b, size_b):
    new = SortedList()
    new.capacity = size_a + size_b
    new.array = [None] * new.capacity
    new.size = 0
    i = 0
    j = 0
    while i < size_a or j < size_b:
        if i >= size_a:
            insert(new, lst_b.array[j])
            j += 1
        elif j >= size_b:
            insert(new, lst_a.array[i])
            i += 1
        elif lst_a.array[i] < lst_b.array[j]:
            insert(new, lst_a.array[i])
            i += 1
        else:
            insert(new, lst_b.array[j])
            j += 1
    return new    return new
