import os
import platform
import subprocess as sp

from custom_ci import custom_input, custom_print


def init():
    # Detect OS
    is_windows = False
    is_linux = False
    if platform.system() == 'Windows':
        is_windows = True
    if platform.system() == 'Linux':
        is_linux = True

    # Global command line helpers
    current_directory = os.path.dirname(os.path.realpath(__file__))
    root_directory = os.path.abspath(os.path.join(current_directory, '..'))
    if(is_windows):
        adb = root_directory + '\\bin\\adb.exe'
    else:
        adb = 'adb'

    cmd = adb + ' devices'
    # Kill server before getting list to avoid daemon texts.
    os.system(adb + ' kill-server')
    os.system(adb + ' start-server')
    proc = sp.Popen(cmd.split(), stdin=sp.PIPE, stdout=sp.PIPE,
                    stderr=sp.PIPE, shell=False)
    output, error = proc.communicate()
    output = output.decode('utf-8')
    error = error.decode('utf-8')

    if len(output) == 0 or error:
        output = None
        custom_print(error, 'red')
        exit()
    else:
        output = [x.strip() for x in output.split('\n') if len(x.strip()) > 0]

    if(len(output) == 1):
        custom_print(
            'Could not find any connected device. Is USB Debugging on?', 'red')
        return ''

    device_to_connect = None
    i = 1
    if(len(output) == 2):
        if(output[1].split()[1] == 'offline'):
            custom_print(
                'Device is offline, try turning off USB debugging and turn on again.', 'yellow')
            exit()
        if(output[1].split()[1] == 'unauthorized'):
            custom_print(
                'Device unauthorized. Please check the confirmation dialog on your device.', 'red')
            exit()
        return output[1].split()[0]

    custom_print(output[0])
    print('\n')
    if device_to_connect is None:
        for device in output[1:]:
            name = adb + ' -s ' + \
                device.split()[0] + ' shell getprop ro.product.model'
            custom_print(str(i) + '. ' + device.split()
                         [0] + '  ' + device.split()[1] + '  ' + sp.getoutput(name).strip())
            i += 1

    while device_to_connect is None:
        device_index = int(custom_input('Enter device number (for ex : 2) : '))
        if device_index <= 0 or device_index + 1 > len(output):
            continue
        device_to_connect = output[device_index]

    if(device_to_connect.split()[1] == 'offline'):
        custom_print(
            'Device is offline, try turning off USB debugging and turn on again.', 'yellow')
        exit()
    if(device_to_connect.split()[1] == 'unauthorized'):
        custom_print(
            'Device unauthorized. Please check the confirmation dialog on your device.', 'red')
        exit()
    return device_to_connect.split()[0]


def exit():
    print('\n')
    custom_print('Exiting...')
    custom_input('Hit \"Enter\" key to continue....', 'cyan')
    quit()


print(init())
