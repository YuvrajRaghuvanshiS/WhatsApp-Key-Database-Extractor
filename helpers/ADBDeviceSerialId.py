import os
import platform
import subprocess as sp

from CustomCI import CustomInput, CustomPrint


def init():
    # Detect OS
    isWindows = False
    isLinux = False
    if platform.system() == 'Windows':
        isWindows = True
    if platform.system() == 'Linux':
        isLinux = True

    # Global command line helpers
    currDir = os.path.dirname(os.path.realpath(__file__))
    rootDir = os.path.abspath(os.path.join(currDir, '..'))
    if(isWindows):
        adb = rootDir + '\\bin\\adb.exe'
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
        CustomPrint(error, 'red')
        Exit()
    else:
        output = [x.strip() for x in output.split('\n') if len(x.strip()) > 0]

    if(len(output) == 1):
        CustomPrint(
            'Could not find any connected device. Is USB Debugging on?', 'red')
        return ''

    deviceToConnect = None
    i = 1
    if(len(output) == 2):
        if(output[1].split()[1] == 'offline'):
            CustomPrint(
                'Device is offline, try turning off USB debugging and turn on again.', 'yellow')
            Exit()
        if(output[1].split()[1] == 'unauthorized'):
            CustomPrint(
                'Device unauthorized. Please check the confirmation dialog on your device.', 'red')
            Exit()
        return output[1].split()[0]

    CustomPrint(output[0])
    print('\n')
    if deviceToConnect is None:
        for device in output[1:]:
            name = adb + ' -s ' + \
                device.split()[0] + ' shell getprop ro.product.model'
            CustomPrint(str(i) + '. ' + device.split()
                        [0] + '  ' + device.split()[1] + '  ' + sp.getoutput(name).strip())
            i += 1

    while deviceToConnect is None:
        deviceIndex = int(CustomInput('Enter device number (for ex : 2) : '))
        if deviceIndex <= 0 or deviceIndex + 1 > len(output):
            continue
        deviceToConnect = output[deviceIndex]

    if(deviceToConnect.split()[1] == 'offline'):
        CustomPrint(
            'Device is offline, try turning off USB debugging and turn on again.', 'yellow')
        Exit()
    if(deviceToConnect.split()[1] == 'unauthorized'):
        CustomPrint(
            'Device unauthorized. Please check the confirmation dialog on your device.', 'red')
        Exit()
    return deviceToConnect.split()[0]


def Exit():
    print('\n')
    CustomPrint('Exiting...')
    os.system('pause')
    quit()
