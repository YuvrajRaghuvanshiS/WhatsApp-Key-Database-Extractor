from termcolor import colored, cprint
import platform

def CustomInput(textToInput, color = 'green', attr=[]) : 
    return input(colored(textToInput, color, attrs=attr)).casefold()

def CustomPrint(textToPrint, color = 'green', attr=[]) : 
    cprint(textToPrint, color, attrs=attr)
