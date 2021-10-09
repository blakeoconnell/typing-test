import random

with open ('data.txt') as data:
    lines = data.readlines()

class Data:
    def __init__(self):
        self.words = lines

    def get_words(self, num):
        words_string = ""
        words_list = []
        for _ in range(num):
            random_word = random.choice(self.words).replace("\n", "")
            words_list.append(random_word)
            words_string += random_word + " "
        return words_string, words_list
