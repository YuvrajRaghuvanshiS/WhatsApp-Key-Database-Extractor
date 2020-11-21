from termcolor import colored, cprint
import platform

# Detect OS
isWindows = False
isLinux = False
if platform.system() == 'Windows' : isWindows = True 
if platform.system() == 'Linux' : isLinux = True

def CustomInput(textToInput, color = 'green', attr=[]) : 
    if(isWindows) : 
        return input(textToInput).casefold()
    else : 
        return input(colored(textToInput, color, attrs=attr)).casefold()

def CustomPrint(textToPrint, color = 'green', attr=[]) : 
    if(isWindows) : 
        print(textToPrint)
    else : 
        cprint(textToPrint, color, attrs=attr)
