import pytest
from to_test import Shop
from to_test import Product


@pytest.fixture
def my_product():
    return Product("Water", 2, 1000)


@pytest.fixture
def my_shop():
    return Shop()


@pytest.fixture
def filled_my_shop(my_shop):
    my_shop.add_product(Product("Potato", 1, 5000))
    my_shop.add_product(Product("Water", 3, 1000))
    my_shop.add_product(Product("Chocolate", 7, 1300))

    return my_shop


def test_add_product(my_shop, my_product):

    my_shop.add_product(my_product)
    assert my_shop.products[-1] == my_product

    with pytest.raises(TypeError):
        my_shop.add_product('')


def test_get_product_index(filled_my_shop):

    assert filled_my_shop._get_product_index("Chocolate") == 2


def test_sell_product(filled_my_shop):

    old_money = filled_my_shop.money

    assert filled_my_shop.sell_product("Chocolate") == 7.0
    assert filled_my_shop.money == old_money + 7.0
    assert filled_my_shop.sell_product("Fish") is None

    with pytest.raises(ValueError):
        filled_my_shop.sell_product("Chocolate", 100000)


def test_sell_product_subtract_quantity(filled_my_shop):

    old_quantity = filled_my_shop.products[2].quantity

    filled_my_shop.sell_product("Chocolate", 10)
    assert filled_my_shop.products[2].quantity == old_quantity - 10

    filled_my_shop.sell_product("Water", 1000)
    assert filled_my_shop._get_product_index("Water") is None
