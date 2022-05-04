from random import randint
import pytest
from algorithms import quick_sort


@pytest.mark.parametrize("unsorted_list", ([randint(-1000, 1000) for _ in range(100)] for _ in range(100)))
def test_quick_sort(unsorted_list):
    """Compares the result of my quick sort function and the built-in function sort"""
    unsorted_list.sort()
    assert quick_sort(unsorted_list) == unsorted_list
