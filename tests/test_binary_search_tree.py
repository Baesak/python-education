from data_structures import BinarySearchTree
import pytest


@pytest.fixture
def binary_tree():
    tree = BinarySearchTree(20, 50, 30, 15, 7, 17, 60)
    return tree


def test_add(binary_tree):

    expected = [20, 50, 30, 15, 7, 17, 60]
    expected.sort()
    result = [value for value in binary_tree]

    assert result == expected


def test_find(binary_tree):

    assert binary_tree.find(7).value == 7

    with pytest.raises(ValueError):
        binary_tree.find(1)


def test_delete(binary_tree):

    expected = [20, 15, 7, 17, 60]
    expected.sort()

    binary_tree.delete(30)
    binary_tree.delete(50)
    result = [value for value in binary_tree]

    assert result == expected


