
"""With this module you can create different types of transport."""

from re import match
from descriptors import NonNegative, BoolOnly, StringOnly


class Engine:
    """Creates engine for transport. Engine may break, and can be repaired by own repair
    method."""

    def __init__(self):
        self.engine_condition = BoolOnly()
        self.engine_condition = True

    def move(self):
        """Makes vehicle move!"""

        if self._start_engine():
            print(f"{self} is moving forward!")

    def _start_engine(self):
        """Starts engine if it is in good condition"""

        print("Starting the engine...")
        if self.engine_condition:
            print("Engine is working.")
            return True
        else:
            print("Engine doesn't starts!")
            return False

    def break_engine(self):
        """Breaks engine"""

        self.engine_condition = False
        print("Engine is broken!")

    def repair_engine(self):
        """Repairs engine if it in bad condition"""

        self.engine_condition = True
        print("Engine has been repaired.")


class Transport:
    """Class for different transport types."""

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

    @staticmethod
    def beep():
        """Make transport beep"""

        print(f"Transport Beeps")

    @staticmethod
    def move():
        """Makes transport move."""
        print(f"Transport is moving forward!")

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


class Numbers:
    """Allows you to add numbers attribute to your vehicle"""

    _taken_numbers = {}

    def __init__(self, number):
        self._number = ''
        self.number = number

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


class Car(Engine, Transport, Numbers):
    """Creates car."""

    def __init__(self, model, price, year, velocity, number):
        super().__init__()
        Transport.__init__(self, model, price, year, velocity)
        Numbers.__init__(self, number)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.number == other.number
        raise TypeError(f"TypeError: unsupported operand type(s) for ==: "
                        f"'{self.__class__}' and '{type(other)}'")

    def __str__(self):
        return self.model


class Motorcycle(Transport, Engine, Numbers):
    """Creates motorcycle. Have 2 wheels"""

    def __init__(self, model, price, year, velocity, number):
        super().__init__(model, price, year, velocity)
        Engine.__init__(self)
        Numbers.__init__(self, number)

    def move(self):
        if self.engine_condition:
            print(f"{self} motorcycle is starting its loud engine and fastly moving forward!")
        else:
            print("Something wrong with engine.")

    def do_olly(self):
        print(f"{self} has done olly!"
              f"Looks like the engine has overheated...")
        self.break_engine()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.number == other.number
        raise TypeError(f"TypeError: unsupported operand type(s) for ==: "
                        f"'{self.__class__}' and '{type(other)}'")

    def __str__(self):
        return self.model


class Ship(Transport, Engine):
    """Creates ship"""

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
        """Remove ship from list of taken names"""

        cls._taken_names.pop(key)

    def move(self):
        """Makes ship move"""

        if self.engine_condition:
            print(f"'{self.name}' ship is sailing forward!")
        else:
            print("Something wrong with engine.")

    def lower_the_anchor(self):
        """Makes ship low the anchor"""

        print(f"The {self} ship dropped anchor!")

    def beep(self):
        """Makes ship hum in horn"""

        print(f"The {self} ship hums in horn!")

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.name == other.name
        raise TypeError(f"TypeError: unsupported operand type(s) for ==: "
                        f"'{self.__class__}' and '{type(other)}'")


class Helicopter(Transport, Engine, Numbers):
    """Makes Helicopter"""

    def __init__(self, model, price, year, velocity, number):
        super().__init__(model, price, year, velocity)
        Engine.__init__(self)
        Numbers.__init__(self, number)

        self.in_air = BoolOnly()
        self.condition = BoolOnly()

    def move(self):
        """Makes helicopter move and rise in the air"""

        if self.condition:
            print(f"{self} helicopter is flying forward!")
            self.in_air = True
        else:
            print("Your helicopter is broken!")

    def sit_down(self):
        """Makes helicopter land"""

        if self.in_air:
            print("Helicopter has landed.")
            self.in_air = False
        else:
            print("Helicopter is landed already")

    def break_engine(self):
        """Breaks engine"""

        self.engine_condition = False
        print("Engine is broken!")

        if self.in_air:
            self.condition = False
            print("Helicopter fall down and crushed! It is useless now.")

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.number == other.number
        raise TypeError(f"TypeError: unsupported operand type(s) for ==: "
                        f"'{self.__class__}' and '{type(other)}'")

    def __str__(self):
        return self.model

