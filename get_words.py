from random import choice, shuffle


class Text:
    def __init__(self, numbers_of_words):
        self.list_of_words = []
        self.text = []
        self.numbers_of_words = numbers_of_words

    def get_some_words(self):
        with open("ListOfWords.txt", "r") as file:
            for words in file.readlines():
                self.list_of_words.append(words.strip())
            shuffle(self.list_of_words)
            for i in range(self.numbers_of_words):
                self.text.append(choice(self.list_of_words))
        return self.text
