from data_structures import Stack


def test_pop_push(values_list):
    stack = Stack()

    for value in values_list:
        stack.push(value)

    result = [value for value in stack]

    assert result == list(reversed(values_list))
    assert len(stack) == 0


