import datetime
import os

try:
    from termcolor import colored, cprint
except ImportError:
    try:
        os.system('pip3 install termcolor')
    except:
        os.system('python3 -m pip install termcolor')


def custom_input(text_to_input, color='green', attr=[], get_time=True):
    time = get_current_time() if get_time else ''
    return input(colored(time + text_to_input, color, attrs=attr))


def custom_print(text_to_print, color='green', attr=[], get_time=True):
    time = get_current_time() if get_time else ''
    text_to_print = str(text_to_print)
    cprint(time + text_to_print, color, attrs=attr)
    # cprint((time + textToPrint).center(shutil.get_terminal_size().columns), color, attrs = attr) to print in center. Later.


def get_current_time():
    return '[' + str(datetime.datetime.now().time()) + '] '
