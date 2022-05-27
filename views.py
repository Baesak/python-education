"""Module stores different views for tic-tac-toe"""

from abc import ABC, abstractmethod


class View(ABC):
    """Abstract class for views for tic-tac-toe"""

    @abstractmethod
    def show_field(self, field: str):
        ...

    @abstractmethod
    def print_message(self, message):
        ...

    @abstractmethod
    def input_from_user(self, message):
        ...

    @abstractmethod
    def menu(self):
        ...


class TerminalView(View):
    """View for terminal"""

    def menu(self):
        """Menu of tic-tac-toe game."""

        while True:
            choice = self.input_from_user("TIC-TAC-TOE\nChoose option:\n"
                                          "1-play\n2-show scores table\n3-clean scores table\n"
                                          "4-exit\n"
                                          ">")
            if self.choice_validation(choice):
                return choice

    def choice_validation(self, choice):
        """Validates user choices."""

        if choice not in ["1", "2", "3", "4"]:
            self.print_message("You should enter only one number from 1 to 4!")
            return False

        return True

    def show_field(self, field: str):
        """Shows field"""

        for row in field:
            print(f"|{' '.join(row)}|")

    def print_message(self, message):
        """Prints message"""
        print(message)

    def input_from_user(self, message: str):
        """Takes input from user and returns it"""

        value = input(message)

        return value

