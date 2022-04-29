import pytest
from to_test import Product


@pytest.fixture
def my_product():
    return Product("Water", 2, 1000)


def test_subtract_quantity(my_product):
    old_quantity = my_product.quantity

    my_product.subtract_quantity()
    assert my_product.quantity == old_quantity - 1

    my_product.subtract_quantity(10)
    assert my_product.quantity == old_quantity - 11


def test_zero_quantity(my_product):

    with pytest.raises(ValueError):
        my_product.subtract_quantity(1230)


def test_add_quantity(my_product):

    old_quantity = my_product.quantity

    my_product.add_quantity(73)
    assert my_product.quantity == old_quantity + 73


def test_change_price(my_product):

    my_product.change_price(30)

    assert my_product.price == 30


def test_zero_price(my_product):

    with pytest.raises(ValueError):
        my_product.change_price(-10)

