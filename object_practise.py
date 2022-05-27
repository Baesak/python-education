"""Module haves 3 iteration tools, file manager and generator.."""

from time import time


class FileManager:
    """Allows you to work with file through the context manager."""

    def __init__(self, file_name, mode="r"):
        self.file_name = file_name
        self.mode = mode

    def __enter__(self):
        self.file = open(self.file_name, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()


def exec_speed_decorator_for_gen(func):
    """Implementation of exec_speed_decorator for generators."""

    def check_time(length):

        start_time = time()
        result = func(length)

        try:
            while True:
                next_iter = next(result)
                yield next_iter

        except StopIteration:
            print(f"{func.__name__} executed for {time() - start_time}")

    return check_time


def exec_speed_decorator(func):
    """Prints for how long function was executed. """

    def check_time(length):
        start_time = time()
        result = func(length)

        try:
            while True:
                next_iter = next(result)
                yield next_iter

        except StopIteration:
            print(f"{func.__name__} executed for {time() - start_time}")

    return check_time


@exec_speed_decorator_for_gen
def fibonacci(length: int):
    """Fibonacci Sequence generator."""

    if not isinstance(length, int) or length < 0:
        raise ValueError("You should enter positive numbers!")

    previous1 = 0
    previous2 = 1
    new = None

    for _ in range(length):
        yield previous1

        new = previous1 + previous2
        previous1 = previous2
        previous2 = new


class Chain:
    """Allows you to iterate through multiply iterables in
    one cycle."""

    def __init__(self, *args):
        self.iterables = args
        self.iterables_gen = self.iter_iterables_gen()

    def iter_iterables_gen(self):
        """Returns values from multiple iterables in order."""

        for iterable in self.iterables:
            for val in iterable:
                yield val

    def __next__(self):
        return next(self.iterables_gen)

    def __iter__(self):
        return self


class Zip:
    """Allows you to take values from each iterable
    in one cycle"""

    def __init__(self, *args):
        self.iterables = args
        self.values_gen = self.iter_value_gen()

    def iter_value_gen(self):
        """Return values from each iterable in one cycle.
        Does it in the range of minimum length from the given lists"""

        len_list = [len(iterable) for iterable in self.iterables]

        for index in range(min(len_list)):

            values_list = []
            for iterable in self.iterables:
                values_list.append(iterable[index])

            yield tuple(values_list)

    def __next__(self):
        return next(self.values_gen)

    def __iter__(self):
        return self


class Product:
    """Makes Cartesian Product for specified iterables."""

    def __init__(self, *args):

        self.iterables = list(args)
        self.values_gen = self.iter_values_gen()

    def iter_values_gen(self):
        """Return tuples for each possible permutations."""

        result = [[]]
        for iterable in self.iterables:
            result = [x + [y] for x in result for y in iterable]
        for prod in result:
            yield tuple(prod)

    def __next__(self):
        return next(self.values_gen)

    def __iter__(self):
        return self


with FileManager("example.txt", "w") as file:
    file.write("Sample text")

list_num = [22, 3, 1, 120]
list_bool = [True, True, False]
list_name = ("John", "Fred")

for name, number in Zip(list_num, list_name):
    print(name, number)

print("\n******\n")

for value in Chain(list_bool, list_name, list_num):
    print(value)
