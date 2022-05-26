"""Modules stores 3 algorithms: Binary Search, Recursion Factorial and Quick Sort."""


from data_structures import Stack


def permutation(iterable, start, end):
    """Function for 'quick sort' function.
    Makes permutation and returns new index of the axis."""

    axis = iterable[end]
    axis_index = start

    for index in range(start, end):
        if iterable[index] <= axis:
            iterable[index], iterable[axis_index] = iterable[axis_index], iterable[index]
            axis_index = axis_index + 1

    iterable[end], iterable[axis_index] = iterable[axis_index], iterable[end]

    return axis_index


def quick_sort(iterable):
    """Quick Sort implementation."""

    stack = Stack()

    start = 0
    end = len(iterable) - 1
    stack.push((start, end))

    while stack:
        start, end = stack.pop()
        axis_index = permutation(iterable, start, end)

        if axis_index - 1 > start:
            stack.push((start, axis_index - 1))

        if axis_index + 1 < end:
            stack.push((axis_index + 1, end))

    return iterable


def binary_search(iterable, value):
    """Implementation of Binary Search"""

    start = 0
    end = len(iterable)-1

    while start <= end:
        middle = (start + end) // 2

        if iterable[middle] == value:
            return middle
        if iterable[middle] > value:
            end = middle - 1
        else:
            start = middle + 1
    raise ValueError(f"Value {value} is not in the iterable!")


def recursive_factorial(num):
    """Recursive implementation of factorial"""

    if num in (0, 1):
        return 1

    return num*recursive_factorial(num-1)
