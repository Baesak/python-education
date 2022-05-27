"""Module stores controller for tic-tac-toe."""

from views import View
from abc import abstractmethod, ABC
from tic_tac_toe import GameSession, Logs


class AbcController(ABC):
    """Abstract class for views for tic-tac-toe"""

    @abstractmethod
    def print_message(self, message):
        ...

    @abstractmethod
    def show_field(self, field):
        ...

    @abstractmethod
    def input_from_user(self, message):
        ...


class Controller(AbcController):
    """Controller for tic-tac-toe views and models."""

    def __init__(self, view: View):
        self.view = view

    def menu(self):
        """Menu of tic-tac-toe game."""

        choice = self.view.menu()

        if choice == "1":
            GameSession(self)
        elif choice == "2":
            Logs.show_logs(self)
        elif choice == "3":
            Logs.clear_logs()
            self.print_message("Score table was cleaned.")
        elif choice == "4":
            exit()

        self.view.menu()

    def print_message(self, message):
        """Prints message."""

        self.view.print_message(message)

    def show_field(self, field):
        """Prints field."""

        self.view.show_field(field)

    def input_from_user(self, message):
        """Takes and returns input from user."""

        return self.view.input_from_user(message)
