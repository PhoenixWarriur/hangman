from hangman import Hangman
from animations import center_cmd_window, run_logo_animation
from threading import Thread
import threading

import colorama
from ansi_codes import Utils

PADDING = " \t"
FONT = "big_money-ne"


def game_loop(start, running):
    while not start.is_set():
        pass
    hangman.start_game()
    while hangman.alive and not hangman.won:
        hangman.display()
        hangman.guess()
        hangman.is_alive()
        hangman.is_won()
    running.set()


if __name__ == '__main__':
    lock = threading.Lock()
    start = threading.Event()
    running = threading.Event()
    hangman = Hangman(lock)
    colorama.init()
    center_cmd_window()
    print(Utils.CURSOR_VISIBLE, end='')
    t1 = Thread(target=run_logo_animation, args=(lock, start, running, hangman))
    t2 = Thread(target=game_loop, args=(start, running))

    t1.start()
    t2.start()

    t2.join()

    print(Utils.CURSOR_VISIBLE, end='')
    colorama.deinit()
