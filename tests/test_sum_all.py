import pytest
from to_test import sum_all


def test_sum_all():
    assert sum_all(5, 2, 124221, -4, 0) == 124224
