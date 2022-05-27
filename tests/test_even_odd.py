import pytest
from to_test import even_odd


@pytest.mark.parametrize("num", [2, 22, 100, 1500])
def test_even_number(num: int):

    assert even_odd(2) == "even"


@pytest.mark.parametrize("num", [13, 1, 3, 6653])
def test_odd_number(num: int):

    assert even_odd(num) == "odd"

