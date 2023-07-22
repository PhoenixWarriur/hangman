import msvcrt
import time
from threading import Thread

import colorama
import ctypes
from ansi_codes import FgColors, TextStyle, Utils, BgColors
import pyfiglet

FONT = "big_money-ne"
PADDING = " \t"
settings = TextStyle.BOLD  # default text design
color_palette = [(183, 134, 40), (198, 147, 32), (219, 165, 20), (238, 182, 9), (252, 194, 1)]


class InBlackList(Exception):
    def __init__(self, char):
        self.char = char

    def __str__(self):
        return str(self.char)


class NotAlphabetic(Exception):
    def __init__(self, char):
        self.char = char

    def __str__(self):
        return str(self.char)


def text2drawing(text):
    return PADDING + pyfiglet.figlet_format(text, font=FONT).replace('\n', '\n' + PADDING)


def run_logo_animation(lock, start, running, hangman):
    global thread_running
    print(settings + Utils.MOVE_CURSOR_HOME + Utils.ERASE_TO_END + Utils.CURSOR_INVISIBLE, end='')
    max_number = len(color_palette) - 1
    logo = create_logo_color_animation("Hangman") + "\n\n\n\n"
    cnt = 0

    while not running.is_set():
        new_lines = '\n'.join(hangman.window).count('\n') + 1
        colored_logo = logo.replace('>',
                                    FgColors.rbg2ansi(color_palette[abs(cnt % (2 * max_number) - max_number)])).replace(
            '<', FgColors.WHITE)
        lock.acquire()
        print(
            Utils.MOVE_CURSOR_PREV_LINE_BEGIN * new_lines + Utils.ERASE_TO_BEGINNING + Utils.MOVE_CURSOR_HOME + colored_logo + Utils.MOVE_CURSOR_NEXT_LINE_BEGIN * new_lines)
        lock.release()
        start.set()
        cnt += 1
        time.sleep(0.3)


def take_input(black_list=None):
    if black_list is None:
        black_list = []

    while True:  # loop for each character

        try:
            char = msvcrt.getch().decode()
        except:
            continue
        if 32 < ord(char) <= 255 and ord(char) != 127:
            if 'A' <= char <= 'Z' or 'a' <= char <= 'z':
                if char.upper() in black_list:
                    raise InBlackList(char)

                user_input = char
                break

            else:
                raise NotAlphabetic(char)

    # doing something with the input
    # print(Utils.move_from_location(columns=-len(message)) + Utils.ERASE_TO_END + 'The user input is:',
    #       user_input)
    return user_input


def create_logo_color_animation(text):
    hangman_drawing = text2drawing(text)

    clusters = []  # Store clusters of spaces (start, end) positions
    current_cluster_start = None

    for i, char in enumerate(hangman_drawing):
        if char == '$':
            if current_cluster_start is None:
                current_cluster_start = i
        else:
            if current_cluster_start is not None:
                clusters.append((current_cluster_start, i))
                current_cluster_start = None

    # Check if there is a cluster at the end
    if current_cluster_start is not None:
        clusters.append((current_cluster_start, len(hangman_drawing)))
    adder = 0
    # Insert '>' at the beginning and '<' at the end of each cluster
    for start, end in clusters:
        start += adder
        end += adder
        hangman_drawing = hangman_drawing[:start] + '>' + hangman_drawing[start:end] + '<' + hangman_drawing[end:]
        adder += 2
    return hangman_drawing


def center_cmd_window():
    ctypes.windll.kernel32.SetConsoleTitleW("Hangman")  # set cmd window title
    kernel32 = ctypes.WinDLL("kernel32")
    user32 = ctypes.WinDLL("user32")

    sm_cxscreen = 0
    sm_cyscreen = 1

    h_wnd = kernel32.GetConsoleWindow()

    screen_width = user32.GetSystemMetrics(sm_cxscreen)
    screen_height = user32.GetSystemMetrics(sm_cyscreen)

    rect = ctypes.wintypes.RECT()
    user32.GetWindowRect(h_wnd, ctypes.byref(rect))

    window_width = rect.right - rect.left
    window_height = rect.bottom - rect.top

    new_left = max((screen_width - window_width) // 2, 0)
    new_top = max((screen_height - window_height) // 2, 0)

    user32.SetWindowPos(h_wnd, 0, new_left, new_top, 0, 0, 0x0001)


if __name__ == '__main__':
    colorama.init()
    center_cmd_window()

    t1 = Thread(target=run_logo_animation)
    t2 = Thread(target=take_input)

    t1.start()
    t2.start()

    t2.join()

    thread_running = False
    print(Utils.CURSOR_VISIBLE, end='')

    colorama.deinit()
