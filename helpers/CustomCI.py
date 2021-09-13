import datetime
import logging
import os

try:
    from termcolor import colored, cprint
except ImportError:
    try:
        os.system('pip3 install termcolor')
    except:
        os.system('python3 -m pip install termcolor')

if not (os.path.isdir('log')):
    os.mkdir('log')
logging.basicConfig(filename='log/wa_kdbe.log', level=logging.DEBUG, format='')
masked = []


def CustomInput(textToInput, color='green', attr=[], getTime=True, log=True):
    time = GetTime() if getTime else ''
    data = input(colored(time + textToInput, color, attrs=attr))
    if(log):
        logging.debug(time + textToInput + data)
    else:
        logging.debug(time + textToInput + '********')
        # Add that password in list, and mask that while printing also.
        masked.append(data)
    return data


def CustomPrint(textToPrint, color='green', attr=[], getTime=True, log=True):
    time = GetTime() if getTime else ''
    textToPrint = str(textToPrint)
    cprint(time + textToPrint, color, attrs=attr)
    if(log):
        logging.debug(time + textToPrint)
    else:
        # Search for password and mask.
        for i in masked:
            if i in textToPrint:
                logging.debug(time + textToPrint.replace(i, '********'))

    # cprint((time + textToPrint).center(shutil.get_terminal_size().columns), color, attrs = attr) to print in center. Later.


def GetTime():
    return '[' + str(datetime.datetime.now().time()) + '] '
