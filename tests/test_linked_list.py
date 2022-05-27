import pytest
from data_structures import LinkedList


@pytest.fixture
def empty_linked_list():
    return LinkedList()


@pytest.fixture
def filled_linked_list(values_list):
    return LinkedList(*values_list)


def test_append(empty_linked_list, values_list):

    for value in values_list:
        empty_linked_list.append(value)

    result = [node.data for node in empty_linked_list]
    assert result == values_list


def test_prepend(empty_linked_list, values_list):

    for value in values_list:
        empty_linked_list.prepend(value)

    result = [node.data for node in empty_linked_list]

    assert result == list(reversed(values_list))


def test_lookup(filled_linked_list):

    assert filled_linked_list.lookup([]) == 2
    assert filled_linked_list.lookup(()) == 4
    assert filled_linked_list.lookup(5) == 0


def test_insert(filled_linked_list):

    filled_linked_list.insert("check", 4)
    filled_linked_list.insert(22, 0)
    filled_linked_list.insert([2, 3], 2)

    result = [node.data for node in filled_linked_list]

    assert result == [22, 5, [2, 3], {}, [], "sa", "check", ()]


def test_delete(filled_linked_list):

    filled_linked_list.delete(0)
    filled_linked_list.delete(3)

    result = [node.data for node in filled_linked_list]

    assert result == [{}, [], "sa"]


def test_get_item(filled_linked_list):

    assert filled_linked_list[0].data == 5
    assert filled_linked_list[-1].data == ()
    assert filled_linked_list[-2].data == "sa"
    assert filled_linked_list[1].data == {}

