import datetime

from termcolor import colored, cprint


def CustomInput(textToInput, color = 'green', attr=[], getTime = True) : 
    time = GetTime() if getTime else ''
    return input(colored(time + textToInput, color, attrs=attr))

def CustomPrint(textToPrint, color = 'green', attr=[], getTime = True) : 
    time = GetTime() if getTime else ''
    cprint(time + textToPrint, color, attrs=attr)

def GetTime() : 
    return '[' + str(datetime.datetime.now().time()) + '] '
