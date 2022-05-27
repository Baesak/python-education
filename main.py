from views import TerminalView
from controllers import Controller


def main():
    """Starts tic-tac-toe menu."""

    view = TerminalView()
    controller = Controller(view)
    controller.menu()


main()
