"""With this module you can create different types of transport."""


from abc import ABC, abstractmethod
from re import match
from descriptors import NonNegative, BoolOnly, StringOnly


class Engine:
    """Creates engine for Transport. Engine may break, and can be repaired with own repair
    method."""

    def __init__(self):
        self.engine_condition = BoolOnly()
        self.engine_condition = True

    def start_engine(self):
        """Starts engine if it is in good condition"""

        print("Starting the engine...")
        if self.engine_condition:
            print("Engine is working.")
        else:
            print("Engine doesn't starts!")

    def break_engine(self):
        """Breaks engine"""

        self.engine_condition = False
        print("Engine is broken!")

    def repair_engine(self):
        """Repairs engine if it in bad condition"""

        self.engine_condition = True
        print("Engine has been repaired.")


class Transport(Engine, ABC):
    """Abstract class for different transport types."""

    def __init__(self, model, price, year, velocity):

        super().__init__()
        self.model = StringOnly()
        self.price = NonNegative()
        self.year = NonNegative()
        self.velocity = NonNegative()

        self.model = model
        self.price = price
        self.year = year
        self.velocity = velocity

    @abstractmethod
    def move(self):
        """Makes transport move."""

        ...

    def __int__(self):
        return self.price

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return self.price + other.price
        if isinstance(other, int):
            return self.price + other

        raise TypeError(f"TypeError: unsupported operand type(s) for +: "
                        f"'{self.__class__}' and '{type(other)}'")

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return self.price - other.price
        if isinstance(other, int):
            return self.price - other

        raise TypeError(f"TypeError: unsupported operand type(s) for +: "
                        f"'{self.__class__}' and '{type(other)}'")

    __radd__ = __add__
    __rsub__ = __sub__


class GroundTransport(Transport, ABC):
    """Can create some different ground vehicles. Saves each new vehicle by number
    in '_taken_numbers'."""

    _taken_numbers = {}

    class Wheel:
        """Creates wheels for ground vehicles."""

        def __init__(self):
            self.tire = BoolOnly()
            self.tire = True

        def change_tire(self):
            """Changing tire if it in bad condition."""

            self.tire = True
            print("Tire changed")

        def break_tire(self):
            """Breaks tire"""

            self.tire = False
            print("Tire broken")

    def __init__(self, model, price, year, velocity, number):
        super().__init__(model, price, year, velocity)
        self._number = ""
        self.number = number
        self._taken_numbers[number] = self

    @property
    def number(self):
        """Returns '_number' attribute"""

        return self._number

    @number.setter
    def number(self, value):
        """Sets '_number' attribute. Number should be in ukrainian
        vehicle numbers format. Also updates number in '_taken_numbers'.
        Each name in '_taken_numbers' should be unique."""

        if not isinstance(value, str):
            raise TypeError(f"'number' cannot be {type(value)}")

        if not bool(match(r"[A-Z]{2}\d{4}[A-Z]{2}", value)):
            raise ValueError(f"{value} - wrong numbers format! Right format: 'AA1234AA'")

        if value in self._taken_numbers.keys():
            raise ValueError(f"{value} is already taken!")

        self._taken_numbers[value] = self._taken_numbers.pop(self._number)
        self._number = value

    @number.deleter
    def number(self):
        del self._number

    @classmethod
    def print_taken_numbers(cls):
        """Print taken numbers list"""

        print(cls._taken_numbers)

    @classmethod
    def remove_from_taken_numbers(cls, key):
        """Remove vehicle from list of taken numbers"""

        cls._taken_numbers.pop(key)

    def move(self):
        """Make vehicle move"""

        print(f"{self} is riding forward!")

    def beep(self):
        """Make vehicle beep"""

        print(f"{self} Beeps")

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.number == other.number
        raise TypeError(f"TypeError: unsupported operand type(s) for ==: "
                        f"'{self.__class__}' and '{type(other)}'")

    def __str__(self):
        return self.model


class WaterTransport(Transport, ABC):
    """Can create some different water transport. Saves each new transport by name
    in '_taken_names'."""

    _taken_names = {}

    def __init__(self, model, price, year, velocity, name, load_limit):
        super().__init__(model, price, year, velocity)

        self.load_limit = NonNegative()
        self.load_limit = load_limit

        self._name = ""
        self.name = name
        self._taken_names[name] = self

    @property
    def name(self):
        """Returns '_name' attribute"""

        return self._name

    @name.setter
    def name(self, value):
        """Sets '_name' attribute.
        Name could be only string type. Also updates name in '_taken_names'.
        Each name in '_taken_names' should be unique."""

        if not isinstance(value, str):
            raise TypeError(f"'number' cannot be {type(value)}")

        if value in self._taken_names.keys():
            raise ValueError(f"{value} is already taken!")

        self._taken_names[value] = self._taken_names.pop(self._name)
        self._name = value

    @name.deleter
    def name(self):
        del self._name

    @classmethod
    def print_taken_names(cls):
        """Print taken names list"""

        print(cls._taken_names)

    @classmethod
    def remove_from_taken_names(cls, key):
        """Remove water transport from list of taken names"""

        cls._taken_names.pop(key)

    def move(self):
        print("The ship is sailing forward!")

    @staticmethod
    def lower_the_anchor():
        """Makes water transport low the anchor"""

        print("The ship dropped anchor!")

    @staticmethod
    def hum_in_horn():
        """Makes water transport hum in horn"""

        print("The ship hums in horn!")

    def __str__(self):
        return self.name


class Car(GroundTransport):
    """Creates car. Have 4 wheels."""

    def __init__(self, model, price, year, velocity, number):
        super().__init__(model, price, year, velocity, number)

        self.wheels = [self.Wheel() for _ in range(4)]


class Motorcycle(GroundTransport):
    """Creates motorcycle. Have 2 wheels"""

    def __init__(self, model, price, year, velocity, number):
        super().__init__(model, price, year, velocity, number)

        self.wheels = [self.Wheel() for _ in range(2)]


class PassengerShip(WaterTransport):
    """Creates Passenger ship. The passenger ship must carry at least 12 passengers"""

    def __init__(self, model, price, year, velocity, name, load_limit, passengers):
        super().__init__(model, price, year, velocity, name, load_limit)

        self._passengers = None
        self.passengers = passengers

    @property
    def passengers(self):
        """Returns 'passengers' attribute"""

        return self._passengers

    @passengers.setter
    def passengers(self, value):
        """Sets 'passengers' attribute. Should be only integer, and at least 12."""

        if not isinstance(value, int):
            raise TypeError(f"'passengers' cannot be {type(value)}")
        if value < 12:
            raise ValueError("The number of passengers on a passenger"
                             " ship must be at least 12.")
        self._passengers = value

    @passengers.deleter
    def passengers(self):
        del self._passengers


my_car = Car("Toyota", 10000, 2018, 320, "AC2345BB")
my_moto = Motorcycle("Suzuki", 234, 2000, 400, "AX2345BB")
my_ship = PassengerShip("Ship", 50000, 1999, 100, "Titanic", 1600, 200)
