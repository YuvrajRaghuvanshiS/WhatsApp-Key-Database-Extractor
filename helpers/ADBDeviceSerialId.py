from CustomCI import CustomInput, CustomPrint
import os
import platform
import subprocess as sp

def init() : 
    # Detect OS
    isWindows = False
    isLinux = False
    if platform.system() == 'Windows' : isWindows = True 
    if platform.system() == 'Linux' : isLinux = True

    # Global command line helpers
    currDir = os.path.dirname(os.path.realpath(__file__))
    rootDir = os.path.abspath(os.path.join(currDir, '..'))

    adb = rootDir + '\\bin\\adb.exe'
    if(isLinux) : 
        adb = 'adb'
    
    cmd = adb + ' devices'
    os.system(adb + ' kill-server') # Start server before getting list to avoid daemon texts.
    os.system(adb + ' start-server')
    proc = sp.Popen(cmd.split(),stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE, shell=False)
    output, error = proc.communicate(); output = output.decode('utf-8'); error = error.decode('utf-8')
    # TODO : Show error and exit.
    # TODO : Autoconnect if only one device.
    if len(output) == 0 or error : 
        output = None
        CustomPrint(error, 'red')
        Exit()

    else : 
        output = [x.strip() for x in output.split('\n') if len(x.strip()) > 0]
    deviceToConnect = None
    CustomPrint(output[0] + '\n')
    i = 1
    for device in output[1:] : 
        name = adb + ' -s ' + device.split()[0] + ' shell getprop ro.product.model'
        CustomPrint(str(i) + '. ' + device.split()[0] + '  ' + device.split()[1] + '  ' + sp.getoutput(name).strip()) ; i += 1

    while deviceToConnect is None : 
        deviceIndex = int(CustomInput('Enter device number (for ex : 2) : '))
        if deviceIndex <= 0 or deviceIndex + 1 > len(output) : 
            continue
        deviceToConnect = output[deviceIndex]

    return deviceToConnect.split()[0]
    
# TODO : Check if device is device, offline, or unauthorised

def Exit():
    CustomPrint('\nExiting...')
    quit()