from random import randint
from re import match
from colorama import init, deinit, Fore, Back, Style


class Hangman:

    words_list = ['python', 'javascript', 'django', 'sql', 'education', 'pycharm']
    chosen_word = ''
    hidden_word = ''
    chosen_letters = []

    def main(self):
        init()
        self.menu()
        deinit()

    def menu(self):
        while True:
            choice = input(Back.GREEN + Fore.RED + Style.BRIGHT + "H A N G M A N" + Style.RESET_ALL + Back.GREEN +
                           Fore.BLACK + "\n\nEnter your choice:\n1-Start game\n2-See previous words\n3-Exit\n>")

            if choice == "1":
                self.start_game()
            elif choice == "2":
                self.show_previous_words()
            elif choice == "3":
                exit()

    def start_game(self):

        lives = 7
        chosen_letters = []
        self.choose_word()
        self.hidden_word_gen()
        self.write_in_file()

        while lives != 0 and '_' in self.hidden_word:
            self.show_hangman_pic(lives)
            choice = input(f"{lives} lives left\n\n{self.hidden_word}\nChoose letter:")
            if self.choice_checker(choice, chosen_letters):
                chosen_letters.append(choice)
                if choice in self.chosen_word:
                    self.update_hidden_word(choice)
                else:
                    print('Letter does not appear in the word')
                    lives -= 1
        if lives != 0:
            print(f"{self.hidden_word}\n\nYou win!")
        else:
            print("You loose!")

    def write_in_file(self):
        with open("previous_words", "r+") as file:
            if self.chosen_word not in file.read().split("\n"):
                file.write(self.chosen_word + "\n")

    @staticmethod
    def show_previous_words():
        with open("previous_words", "r") as file:
            print(file.read())

    def update_hidden_word(self, choice):
        for i in range(len(self.chosen_word)):
            if self.chosen_word[i] == choice:
                hidden_word_list = list(self.hidden_word)
                hidden_word_list[i] = choice
                self.hidden_word = ''.join(hidden_word_list)

    @staticmethod
    def choice_checker(choice, chosen_letters):

        if len(choice) != 1:
            print("You should enter 1 letter!")
            return False
        elif not bool(match("[a-z]", choice)):
            print("You should enter only lowercase english letters")
            return False
        elif choice in chosen_letters:
            print("You already had chosen this letter")
            return False
        else:
            return True

    def hidden_word_gen(self):
        self.hidden_word = '_' * len(self.chosen_word)

    def choose_word(self):
        self.chosen_word = self.words_list[randint(0, len(self.words_list)-1)]

    @staticmethod
    def show_hangman_pic(lives):
        pics = ['''
      +---+
      |   |
          |
          |
          |
          |
    =========''', '''
      +---+
      |   |
      O   |
          |
          |
          |
    =========''', '''
      +---+
      |   |
      O   |
      |   |
          |
          |
    =========''', '''
      +---+
      |   |
      O   |
     /|   |
          |
          |
    =========''', r'''
      +---+
      |   |
      O   |
     /|\  |
          |
          |
    =========''', r'''
      +---+
      |   |
      O   |
     /|\  |
     /    |
          |
    =========''', r'''
      +---+
      |   |
      O   |
     /|\  |
     / \  |
          |
    =========''']
        print(pics[7 - lives])


# my_hangman = Hangman()
# my_hangman.main()