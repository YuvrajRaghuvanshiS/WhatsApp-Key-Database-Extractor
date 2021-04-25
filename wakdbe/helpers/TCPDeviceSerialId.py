import os
import platform
import subprocess as sp

from wakdbe.helpers.CustomCI import CustomPrint


def init(tcpIP, tcpPort):
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

    combo = tcpIP + ':' + tcpPort
    cmd = adb + ' connect ' + combo
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
        output = [x.strip() for x in output.split() if len(x.strip()) > 0]

    if('connected' in (x.lower() for x in output)):
        return combo
    if('authenticate' in (x.lower() for x in output)):
        CustomPrint(
            'Device unauthorized. Please check the confirmation dialog on your device.', 'red')
        Exit()
    if('refused' in (x.lower() for x in output)):
        CustomPrint(
            'Could not find any connected device. Either USB Debugging is off or device is not running ADB over TCP', 'red')
        return ''

    ''' Possible outputs
    ['connected', 'to', '192.168.43.130:5555']
    ['failed', 'to', 'authenticate', 'to', '192.168.43.130:5555'] 
    ['cannot', 'connect', 'to', '192.168.43.130:5555:', 'No', 'connection', 'could', 'be', 'made', 'because', 'the', 'target', 'machine', 'actively', 'refused', 'it.', '(10061)']
    '''


def Exit():
    print('\n')
    CustomPrint('Exiting...')
    CustomInput('Hit \'Enter\' key to continue....', 'cyan')
    quit()
