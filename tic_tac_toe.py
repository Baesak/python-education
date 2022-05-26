"""With this module you can make own tic-tac-toe game!"""

from abc import ABC
from loggers import file_logger


class FieldChecker(ABC):
    """Class for checking field in Field class."""

    def __init__(self, field: list):
        self.field = field
        self.winner = ""

    def _check_rows(self):
        """Checks rows in field."""

        for row in self.field:
            symbol_set = set(row)
            if self._check_set(symbol_set):
                self.winner = symbol_set.pop()
                return True

        return False

    def _check_diagonals(self):
        """Checks two diagonals is field."""

        symbol_set = set(self.field[0][0] + self.field[1][1] + self.field[2][2])
        if self._check_set(symbol_set):
            self.winner = symbol_set.pop()
            return True

        symbol_set = set(self.field[0][2] + self.field[1][1] + self.field[2][0])
        if self._check_set(symbol_set):
            self.winner = symbol_set.pop()
            return True

        return False

    def _check_columns(self):
        """Checks columns in fields."""

        for index in range(3):
            symbol_set = set(self.field[0][index] + self.field[1][index] + self.field[2][index])

            if self._check_set(symbol_set):
                self.winner = symbol_set.pop()
                return True

        return False

    @staticmethod
    def _check_set(symbol_set: set):
        """Shortcut for condition in checking functions."""

        return "_" not in symbol_set and len(symbol_set) == 1


class Field(FieldChecker):
    """Field for GameSession. Field stored in field attribute,
    which is list with 3 lists. Those 3 lists is representing rows in field."""

    def __init__(self):
        self.field = [
            ["_", "_", "_"],
            ["_", "_", "_"],
            ["_", "_", "_"]
        ]
        self.game_result = ""

        super().__init__(self.field)

    def return_field(self):
        """Shows field."""

        for row in self.field:
            print(f"|{' '.join(row)}|")

    def check_game_state(self):
        """Checks actual game state."""

        if self._check_rows():
            return False
        if self._check_columns():
            return False
        if self._check_diagonals():
            return False

        if "_" not in self.field[0] + self.field[1] + self.field[2]:
            return False

        return True

    def __getitem__(self, index: int):
        return self.field[index]


class Player:
    """Creates player for GameSession."""

    def __init__(self, controller, name: str, symbol: str):
        self.name = name
        self.symbol = symbol
        self.win_count = 0
        self.controller = controller

    def make_move(self, field: Field):
        """Takes coordinates from user and write it down on
         the field."""

        while True:
            cord = self.controller.input_from_user(f"{self.name} move:").split()
            cord = self.cord_validation(cord, field)
            if cord:
                field[cord[0] - 1][cord[1] - 1] = self.symbol
                break

    def cord_validation(self, cord: tuple, field: Field):
        """Validates user coordinates."""

        try:
            cord = tuple(map(int, cord))
        except ValueError:
            self.controller.print_message("You should enter numbers!")
            return False

        if len(cord) != 2:
            self.controller.print_message("You should enter 2 numbers!")
            return False
        if not 1 <= cord[0] <= 3 or not 1 <= cord[1] <= 3:
            self.controller.print_message("Coordinates numbers should be in range 1-3!")
            return False
        if field[cord[0]-1][cord[1]-1] != "_":
            self.controller.print_message("This cell is occupied!")
            return False

        return cord

    def __repr__(self):
        return self.name


class GameSession:
    """Game session of tic-tac-toe."""

    def __init__(self, controller, player1=None, player2=None):

        self.controller = controller
        self.field = Field()
        self.player1, self.player2 = self._set_players(player1, player2)
        self._player_num = 2
        self.winner = ""

        self.play()

    def _set_players(self, player1, player2):
        """Return 2 players. If it's not the first game
        it will take old players and return them. If this is the first game -
        will create new ones."""

        if player1 is None and player2 is None:
            name1 = self.controller.input_from_user("Enter name of player 1:")
            name2 = self.controller.input_from_user("Enter name of player 2:")

            return Player(self.controller, name1, "O"), Player(self.controller, name2, "X")

        return player1, player2

    def _player_iter(self):
        """Alternates '1' and '2' for switching between players
        in 'play' function 'while' cycle"""

        self._player_num = 1 if self._player_num == 2 else 2
        return self._player_num

    def play(self):
        """Starts the game. If user want to play again
        starts the recursion."""

        self.controller.show_field(self.field.field)
        while self.field.check_game_state():
            getattr(self, f"player{self._player_iter()}").make_move(self.field)
            self.controller.show_field(self.field.field)

        self.results()
        repeat = self.controller.input_from_user("Do you wanna play again?(yes/no)\n>")
        if repeat == "yes":
            GameSession(self.controller, self.player1, self.player2)

    def _define_winner(self):
        """Defines what player relates to winner in Field class
        and saves him at winner attribute."""

        self.winner = self.player1 if self.field.winner == "O" else self.player2

    def results(self):
        """Printing results of game session."""

        self._define_winner()

        if not self.field.winner:
            message = "Draw"

        elif self.player1.win_count + self.player2.win_count == 0:
            message = f"{self.winner} wins!"
            self.winner.win_count += 1
        else:
            self.winner.win_count += 1
            message = f"{self.player1} - {self.player1.win_count}\n"\
                      f"{self.player2} - {self.player2.win_count}"

        self.controller.print_message(message)
        file_logger.info(message)


class Logs:
    """Can show or clear logs for tic-tac-toe module."""

    @staticmethod
    def show_logs(controller):
        with open("tic-tac-toe.log", "r", encoding="utf-8") as file:
            controller.print_message(file.read())

    @staticmethod
    def clear_logs():
        with open("tic-tac-toe.log", "w", encoding="utf-8") as file:
            file.write("")

