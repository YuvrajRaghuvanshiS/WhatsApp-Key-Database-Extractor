import re
from .CustomCI import CustomInput, CustomPrint
import os
from subprocess import check_output

# Global variables
delete = 'rm -rf'
confirmDelete = ''
helpers = 'helpers/'

def Exit():
    CustomPrint('\nExiting...', 'green')
    os.system('bin\\adb.exe kill-server')
    quit()

def LinuxTCP(deviceIP, devicePort) : 
    CustomPrint('Connecting to device', 'green')
    try : 
        os.system('adb kill-server')
        os.system('adb connect ' + deviceIP + ':' + devicePort)
        os.system('adb wait-for-device')
    except Exception as e : 
        CustomPrint(e)
        Exit()
    deviceName= 'adb shell getprop ro.product.model'
    CustomPrint('Connected to ' + re.search("(?<=b')(.*)(?=\\\\n)", str(check_output(deviceName.split()))).group(1) , 'green')
    return 1

def LinuxUSB() : 
    try : 
        os.system('adb kill-server')
        os.system('adb start-server')
        CustomPrint('Plug device via USB now..', 'green')
        os.system('adb wait-for-device')
    except Exception as e : 
        CustomPrint(e)
        Exit()
    deviceName= 'adb shell getprop ro.product.model'
    CustomPrint('Connected to ' + re.search("(?<=b')(.*)(?=\\\\n)", str(check_output(deviceName.split()))).group(1) , 'green')
    return 1
