import pytest
from algorithms import recursive_factorial
from math import factorial
from random import randint


@pytest.mark.parametrize("num", [randint(0, 100) for _ in range(100)])
def test_recursive_factorial(num):
    assert recursive_factorial(num) == factorial(num)
