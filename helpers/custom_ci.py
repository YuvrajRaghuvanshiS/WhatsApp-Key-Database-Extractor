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


def custom_input(text_to_input, color='green', attr=[], is_get_time=True, is_log=True):
    time = get_time() if is_get_time else ''
    data = input(colored(time + text_to_input, color, attrs=attr))
    if(is_log):
        logging.debug(time + text_to_input + data)
    else:
        logging.debug(time + text_to_input + '********')
        # Add that password in list, and mask that while printing also.
        masked.append(data)
    return data


def custom_print(text_to_print, color='green', attr=[], is_get_time=True, is_log=True, is_print=True, end='\n'):
    time = get_time() if is_get_time else ''
    text_to_print = str(text_to_print)
    if(is_print):
        cprint(time + text_to_print, color, attrs=attr, end=end)
    else:
        pass
    if(is_log):
        logging.debug(time + text_to_print)
    else:
        # Search for password and mask.
        for i in masked:
            if i in text_to_print:
                logging.debug(time + text_to_print.replace(i, '********'))

    # cprint((time + textToPrint).center(shutil.get_terminal_size().columns), color, attrs = attr) to print in center. Later.


def get_time():
    return '[' + str(datetime.datetime.now().time()) + '] '
