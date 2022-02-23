"""This module has one class - 'Calculator'. It can be used to do simple
 arithmetic operations"""


class Calculator:
    """Class supports 4 simple arithmetic operation: addition, subtraction, multiplication
    and division."""

    @staticmethod
    def addition(first_num, second_num):
        """Addition operation. Arguments can be any positive or negative numbers. """
        return first_num + second_num

    @staticmethod
    def subtraction(first_num, second_num):
        """Subtraction operation. Arguments can be any positive or negative numbers."""
        return first_num - second_num

    @staticmethod
    def multiplication(first_num, second_num):
        """Multiplications operation. Arguments can be any positive or negative numbers. """
        return first_num * second_num

    @staticmethod
    def division(first_num, second_num):
        """Division operation. First argument can be any positive or negative number,
        second argument can be any number except 0."""
        return first_num / second_num
