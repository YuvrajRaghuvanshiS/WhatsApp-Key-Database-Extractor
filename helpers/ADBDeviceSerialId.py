from CustomCI import CustomInput
import os
import platform

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

    os.system(adb + ' devices')
    ADBSerialId = CustomInput('Choose device from "List of devices attached"\nFor example : 7835fd84543/emulator-5554 : ', 'green')
    return ADBSerialId
