
class TextStyle:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    INVERSE = '\033[7m'
    HIDDEN = '\033[8m'
    STRIKETHROUGH = '\033[9m'
    NORMAL = '\033[22m'


class FgColors:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'

    @staticmethod
    def rbg2ansi(r, g, b):
        return f'\033[38;2;{r};{b};{g}m'


class BgColors:
    BLACK = '\033[40m'
    RED = '\033[41m'
    GREEN = '\033[42m'
    YELLOW = '\033[43m'
    BLUE = '\033[44m'
    MAGENTA = '\033[45m'
    CYAN = '\033[46m'
    WHITE = '\033[47m'
    BRIGHT_BLACK = '\033[100m'
    BRIGHT_RED = '\033[101m'
    BRIGHT_GREEN = '\033[102m'
    BRIGHT_YELLOW = '\033[103m'
    BRIGHT_BLUE = '\033[104m'
    BRIGHT_MAGENTA = '\033[105m'
    BRIGHT_CYAN = '\033[106m'
    BRIGHT_WHITE = '\033[107m'

    @staticmethod
    def rbg2ansi(r, g, b):
        return f'\033[48;2;{r};{b};{g}m'


class Utils:
    CURSOR_INVISIBLE = '\033[?25l'  # make cursor invisible
    CURSOR_VISIBLE = '\033[?25h'  # make cursor visible
    ERASE_TO_END = '\033[0J'  # erase from cursor until end of screen
    ERASE_TO_BEGINNING = '\033[1J'  # erase from cursor to beginning of screen
    ERASE_SCREEN = '\033[2J'  # erase entire screen
    ERASE_SAVED_LINES = '\033[3J'  # erase saved lines
    ERASE_TO_END_OF_LINE = '\033[0K'  # erase from cursor to end of line
    ERASE_TO_START_OF_LINE = '\033[1K'  # erase start of line to the cursor
    ERASE_LINE = '\033[2K'  # erase the entire line
    MOVE_CURSOR_HOME = '\033[H'  # moves cursor to home position (0, 0)
    MOVE_CURSOR_NEXT_LINE_BEGIN = '\033[E'  # moves cursor to beginning of next line, # lines down
    MOVE_CURSOR_PREV_LINE_BEGIN = '\033[F'  # moves cursor to beginning of previous line, # lines up
    REQUEST_CURSOR_POSITION = '\033[6n'  # request cursor position (reports as ESC[#;#R)
    SAVE_CURSOR_POSITION = '\033[s'  # save cursor position (SCO)
    RESTORE_CURSOR_POSITION = '\033[u'  # restores the cursor to the last saved position (SCO)

    @staticmethod
    def move_cursor(line=0, column=0):
        return '\033[{};{}H'.format(line, column)

    @staticmethod
    def move_from_location(lines=0, columns=0):
        move_up = '\033[{}A'.format(lines) if lines > 0 else ''
        move_down = '\033[{}B'.format(abs(lines)) if lines < 0 else ''
        move_right = '\033[{}C'.format(columns) if columns > 0 else ''
        move_left = '\033[{}D'.format(abs(columns)) if columns < 0 else ''

        return '{}{}{}{}'.format(move_up, move_down, move_right, move_left)


