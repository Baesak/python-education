import pytest
from data_structures import HashTable


@pytest.fixture
def filled_hash_table():
    return HashTable("lies", "foes", (4, 1, "sa"),
                     33, (4, 1, "sa"))


def test_insert():
    hash_table = HashTable("lies", "foes", (4, 1, "sa"),
                           33, (4, 1, "sa"))

    result = [value for value in hash_table]
    expected = [(33, 3), ('lies', 9), ('foes', 9), ((4, 1, 'sa'),
                12), ((4, 1, 'sa'), 12)]

    assert result == expected


def test_lookup(filled_hash_table):

    result = [value for value in filled_hash_table.lookup(9)]

    assert result == ['lies', 'foes']


def test_delete(filled_hash_table):

    filled_hash_table.delete(9)

    expected = [(33, 3), ((4, 1, 'sa'), 12), ((4, 1, 'sa'), 12)]
    result = [value for value in filled_hash_table]

    assert result == expected
