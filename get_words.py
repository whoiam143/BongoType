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

    def get_string(self):
        strings = []
        self.get_some_words()
        if self.numbers_of_words == 5 or self.numbers_of_words == 15:
            return self.text
        elif self.numbers_of_words == 25:
            strings.append(list(self.text)[:10])
            strings.append(list(self.text)[10:20])
            strings.append(list(self.text)[20:])
            return strings
        elif self.numbers_of_words == 25:
            strings.append(list(self.text)[:10])
            strings.append(list(self.text)[10:20])
            strings.append(list(self.text)[20:30])
            strings.append(list(self.text)[30:40])
            strings.append(list(self.text)[40:])
            return strings
