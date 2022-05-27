import pytest


@pytest.fixture(scope="package")
def values_list():
    return [5, {}, [], "sa", ()]