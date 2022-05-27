class NonNegative:

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, val):
        if val < 0:
            raise ValueError(f"{self.name} cannot be negative!")
        instance.__dict__[self.name] = val


class StringOnly:

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, val):
        if not isinstance(val, str):
            raise TypeError(f"{self.name} should be string!")

        instance.__dict__[self.name] = val


class BoolOnly:

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, val):
        if not isinstance(val, bool):
            raise ValueError(f"{self.name} cannot be boolean!")

        instance.__dict__[self.name] = val