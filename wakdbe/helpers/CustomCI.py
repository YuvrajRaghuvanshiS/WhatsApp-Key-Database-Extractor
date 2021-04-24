import datetime
import os

try:
    from termcolor import colored, cprint
except ImportError:
    try:
        os.system('pip3 install termcolor')
    except:
        os.system('python3 -m pip install termcolor')


def CustomInput(textToInput, color='green', attr=[], getTime=True):
    time = GetTime() if getTime else ''
    return input(colored(time + textToInput, color, attrs=attr))


def CustomPrint(textToPrint, color='green', attr=[], getTime=True):
    time = GetTime() if getTime else ''
    textToPrint = str(textToPrint)
    cprint(time + textToPrint, color, attrs=attr)
    # cprint((time + textToPrint).center(shutil.get_terminal_size().columns), color, attrs = attr) to print in center. Later.


def GetTime():
    return '[' + str(datetime.datetime.now().time()) + '] '
