import math
import random
import colorama
import pandas as pd
import ansi_codes
from ansi_codes import FgColors, TextStyle, Utils
import pyfiglet

colorama.init()  # allows the usage of ansi escape codes

hangman_stages = [
    ['   ┬───────┬  ', '   │       │  ', '   │          ', '   │          ', '   │          ', '   │          ',
     '───┴──────────'],
    ['   ┬───────┬  ', '   │       │  ', '   │       O  ', '   │          ', '   │          ', '   │          ',
     '───┴──────────'],
    ['   ┬───────┬  ', '   │       │  ', '   │       O  ', '   │       |  ', '   │          ', '   │          ',
     '───┴──────────'],
    ['   ┬───────┬  ', '   │       │  ', '   │       O  ', '   │      /|  ', '   │          ', '   │          ',
     '───┴──────────'],
    ['   ┬───────┬  ', '   │       │  ', '   │       O  ', '   │      /|\\ ', '   │          ', '   │          ',
     '───┴──────────'],
    ['   ┬───────┬  ', '   │       │  ', '   │       O  ', '   │      /|\\ ', '   │       |  ', '   │          ',
     '───┴──────────'],
    ['   ┬───────┬  ', '   │       │  ', '   │       O  ', '   │      /|\\ ', '   │       |  ', '   │      /   ',
     '───┴──────────'],
    ['   ┬───────┬  ', '   │       │  ', '   │       O  ', '   │      /|\\ ', '   │       |  ', '   │      / \\ ',
     '───┴──────────']]

LINE_UP = Utils.MOVE_CURSOR_PREV_LINE_BEGIN
LINE_CLEAR = Utils.ERASE_TO_END
PADDING = " \t"
FONT = "big"

settings = TextStyle.BOLD  # default text design
lines = len(hangman_stages[0]) + 2  # window lines to delete
df = pd.read_csv('hangman_dataset.csv')

'''
hangman game class, it is responsible for all of the game including displaying the design
'''


def text2drawing(text):
    return PADDING + pyfiglet.figlet_format(text, font=FONT).replace('\n', '\n' + PADDING)


class Hangman():
    def __init__(self):
        self.alive = True
        self.stage = 0
        self.used_letters = []
        self.topic = "topic"
        self.word = "word"
        self.hidden_word = []
        self.correctly_guessed = []
        self.won = False
        self.first = True

    '''draw the game logo, 
    get the topic and the word fo the game and
    print the topic'''

    def start_game(self):
        print(Utils.MOVE_CURSOR_HOME + Utils.ERASE_TO_END)
        print(settings + text2drawing("Hangman") + "\n\n\n\n")  # print the game logo
        topics = list(df.keys())
        print(
            f"{PADDING}Choose the topic ({', '.join(map(lambda x: x[0] + ' - ' + x, topics + ['Random']))}):")  # print the topics and add a random topic

        def get_topic():
            chosen_topic = input(PADDING+"Please enter your chosen topic here: ").upper()
            possible_topic = list(
                filter(lambda x: x.upper().startswith(chosen_topic), topics + ['Random']))  # get the topic written
            if len(possible_topic) == 1:  # if the topic exists
                self.topic = possible_topic[0]  # save the topic to self.topic
            if self.topic == 'Random':  # if the topic is random, get a random topic
                self.topic = random.choice(topics)

        get_topic()

        while self.topic not in topics:
            print(LINE_UP * lines, end=LINE_CLEAR)  # delete the line above
            get_topic()

        self.word = random.choice(df[self.topic].tolist())  # get a random word
        print(LINE_UP * 2, end=LINE_CLEAR)  # delete two lines above
        print(f'{PADDING}Topic: {self.topic}\n')
        self.display()

    def display(self):
        self.hide_word()
        if self.first:
            self.first = False

        else:
            print(LINE_UP * lines, end=LINE_CLEAR)

        window = hangman_stages[self.stage].copy()
        reshaped = [[] for _ in range(math.ceil(len(self.used_letters) / 3))]

        for i in range(len(self.used_letters)):
            reshaped[i // 3].append(self.used_letters[i])
        window[2] = window[2] + TextStyle.UNDERLINE + "Used Letters" + TextStyle.RESET + settings

        for i in range(len(reshaped)):
            window[i + 3] = window[i + 3] + '\t' + ', '.join(reshaped[i])

        window.append('\n' + PADDING + ' '.join(self.hidden_word))
        print(PADDING + ('\n' + PADDING).join(window))

    def hide_word(self):
        self.hidden_word = [
            TextStyle.UNDERLINE + i + TextStyle.RESET + settings if i.upper() in self.correctly_guessed and i != ' ' else ' ' if i == ' ' else TextStyle.UNDERLINE + ' ' + TextStyle.RESET + settings
            for i in self.word]

    def guess(self, guess):
        while not guess.isalpha() or guess.upper() in self.correctly_guessed + self.used_letters or len(guess) != 1:
            print(LINE_UP, end=LINE_CLEAR + PADDING)
            if not guess.isalpha():
                guess = input('Your guess is not alphabetic. Please enter another guess here:')

            elif guess.upper() in self.correctly_guessed + self.used_letters:
                guess = input('Your guess was already guessed. Please enter another guess here:')

            elif len(guess) != 1:
                guess = input('You must enter 1 digit. Please enter another guess here:')

        guess = guess.upper()
        if guess in self.word.upper():
            self.correctly_guessed.append(guess)
        else:
            self.used_letters.append(guess)
            self.stage += 1

    def is_alive(self):
        if not (self.stage < len(hangman_stages) - 1):
            self.alive = False
            print(Utils.MOVE_CURSOR_HOME + Utils.ERASE_TO_END)
            print(
                f'\n{FgColors.RED}{text2drawing("YOU    DIED !")}\n{PADDING}your topic was {self.topic} and your word was {self.word}')

    def is_won(self):
        if len(set(self.correctly_guessed)) == len(set(self.word.replace(' ', '').upper())):
            self.won = True
            print(Utils.MOVE_CURSOR_HOME + Utils.ERASE_TO_END)
            print(
                f'\n{FgColors.GREEN}{text2drawing("YOU    WON !")}\n{PADDING}your topic was {self.topic} and your word was {self.word}')

    def game_loop(self):
        self.start_game()
        while self.alive and not self.won:
            self.guess(input(PADDING + 'Please enter you guess here: '))
            print(LINE_UP, end=LINE_CLEAR)
            self.display()
            self.is_alive()
            self.is_won()


hangman = Hangman()
hangman.game_loop()
print(TextStyle.RESET, sep='')
colorama.deinit()
