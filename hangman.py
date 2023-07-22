import math
import random
import time

import colorama
import pandas as pd
from ansi_codes import FgColors, TextStyle, Utils
import pyfiglet
from animations import take_input, text2drawing, PADDING, FONT, NotAlphabetic, InBlackList

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

settings = TextStyle.BOLD  # default text design
df = pd.read_csv('hangman_dataset.csv')
topics = list(df.keys())

'''
hangman game class, it is responsible for all of the game including displaying the design
'''


class Hangman():
    def __init__(self, lock):
        self.window = []
        """
        window:
        0: Topic\n
        1: drawing
        2: drawing
        3: drawing + \t + used letters title
        4: drawing + \t + used letters
        5: drawing + \t + used letters
        6: drawing + \t + used letters
        7: drawing\n
        8: hidden word
        9: input
        """
        self.lock = lock
        self.alive = True
        self.stage = 0
        self.used_letters = []
        self.topic = "topic"
        self.word = "word"
        self.hidden_word = []
        self.correctly_guessed = []
        self.won = False
        self.flag = False

    '''draw the game logo, 
    get the topic and the word fo the game and
    print the topic'''

    def start_game(self):

        def get_topic(message):
            self.window = [message]
            self.print_window()
            while True:
                try:
                    chosen_topic = take_input().upper()
                    break
                except:
                    pass
            possible_topic = list(
                filter(lambda x: x.upper().startswith(chosen_topic), topics + ['Random']))  # get the topic written
            if len(possible_topic) == 1:  # if the topic exists
                self.topic = possible_topic[0]  # save the topic to self.topic
            if self.topic == 'Random':  # if the topic is random, get a random topic
                self.topic = random.choice(topics)

        get_topic(f"Choose the topic ({', '.join(map(lambda x: x[0] + ' - ' + x, topics + ['Random']))}):")

        while self.topic not in topics:
            get_topic(
                f"Please choose another topic ({', '.join(map(lambda x: x[0] + ' - ' + x, topics + ['Random']))}):")

        self.word = random.choice(df[self.topic].tolist())
        self.flag = True
        self.display()

    def display(self):
        self.hide_word()
        self.window = [f'{TextStyle.UNDERLINE}Topic: {self.topic + TextStyle.RESET + settings}\n'] + hangman_stages[
            self.stage]
        reshaped = [[] for _ in range(math.ceil(len(self.used_letters) / 3))]

        for i in range(len(self.used_letters)):
            reshaped[i // 3].append(self.used_letters[i])
        self.window[3] = self.window[3] + TextStyle.UNDERLINE + "Used Letters" + TextStyle.RESET + settings

        for i in range(len(reshaped)):
            self.window[i + 4] = self.window[i + 4] + '\t' + ', '.join(reshaped[i])

        self.window.append('\n' + PADDING + ' '.join(self.hidden_word))
        self.window.append('Please enter your guess.')

        self.print_window()

    def print_window(self):
        self.lock.acquire()
        new_lines = '\n'.join(self.window).count('\n')
        if self.flag:
            new_lines = 0
            self.flag = False
        print(Utils.MOVE_CURSOR_PREV_LINE_BEGIN * new_lines + Utils.ERASE_TO_END, end='')
        print(PADDING + ('\n' + PADDING).join(self.window), end='')

        self.lock.release()

    def hide_word(self):
        self.hidden_word = [
            TextStyle.UNDERLINE + i + TextStyle.RESET + settings if i.upper() in self.correctly_guessed and i != ' ' else ' ' if i == ' ' else TextStyle.UNDERLINE + ' ' + TextStyle.RESET + settings
            for i in self.word]

    def guess(self):
        while True:
            try:
                guess = take_input(self.used_letters + self.correctly_guessed)
                break
            except NotAlphabetic as e:
                message = f'Your guess({str(e)}) is not alphabetic. Please enter another guess here:'
            except InBlackList as e:
                message = f'Your guess({str(e)}) was already guessed. Please enter another guess here:'
            self.window[-1] = message
            self.print_window()

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


if __name__ == '__main__':
    colorama.init()  # allows the usage of ansi escape codes
    hangman = Hangman()
    while hangman.alive and not hangman.won:
        hangman.display()
        hangman.guess()
        hangman.is_alive()
        hangman.is_won()
    colorama.deinit()
