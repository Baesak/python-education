import pytest
from algorithms import quick_sort, binary_search
from random import randint


@pytest.mark.parametrize("sorted_list", (quick_sort([randint(-1000, 1000) for _ in range(30)])
                         for _ in range(30)))
def test_binary_search(sorted_list):

    index = randint(0, len(sorted_list)-1)
    value = sorted_list[index]

    assert binary_search(sorted_list, value) == sorted_list.index(value)

    with pytest.raises(ValueError):
        binary_search(sorted_list, 1001)
