"""This module allows you to create Sentence class for
work with words and chars in sentences"""

from re import match, findall, sub


class MultiplySentenceError(Exception):
    def __init__(self, sentence):
        self.message = f"'{sentence}' have more than 1 sentence!"

    def __str__(self):
        return self.message


class Sentence:
    """Takes sentence. Allows you to get words from sentence by index,
    iterate over words, and see list of words and list of other characters."""

    def __init__(self, sentence):
        if self.sentence_validation(sentence):
            self.sentence = sentence

    @staticmethod
    def sentence_validation(sentence: str):
        """Validates value for 'sentence' input."""

        if not isinstance(sentence, str):
            raise TypeError("Sentence should be string type!")
        if not any(sentence.endswith(symb) for symb in ["!", "?", "."]):
            raise ValueError("Sentence should be ended!")
        if match(r".*[?!.]\s", sentence):
            raise MultiplySentenceError(sentence)

        return True

    @property
    def words(self):
        """Returns list of words without other characters"""

        return [sub(r"[^A-z\d]", " ", word) for word in self.sentence.split()]

    @property
    def other_chars(self):
        """Returns list of other characters than words"""

        return findall(r"[^A-z\d\s]", self.sentence)

    def _words(self):
        """Lazy iterator for words in sentence."""

        for word in self.words:
            yield word

    def __iter__(self):
        return SentenceIterator(self.words)

    def __repr__(self):
        return f"Sentence(words={len(self.words)}," \
               f"other_chars={len(self.other_chars)})"

    def __getitem__(self, index):
        return " ".join(self.sentence.split()[index])


class SentenceIterator:
    """Iterator for Sentence class"""

    def __init__(self, words):
        self._words = words
        self._max_index = len(words) - 1
        self._index = 0

    def __next__(self):
        if self._index != self._max_index:
            self._index += 1
            return self._words[self._index]
        raise StopIteration

    def __iter__(self):
        return self


try:
    my_sentence = Sentence("You can eat some more of those soft French rolls. Also, you can have some tea!")
except MultiplySentenceError as error:
    print(error)

try:
    my_sentence = Sentence("Eat some more of those soft French rolls, and have some tea")
except ValueError as error:
    print(error)

try:
    my_sentence = Sentence(123)
except TypeError as error:
    print(error)

my_sentence = Sentence("Eat some more of those soft French rolls, and have some tea!")

print(my_sentence)
print(my_sentence.words)
print(my_sentence.other_chars)

for word in my_sentence:
    print(word)
