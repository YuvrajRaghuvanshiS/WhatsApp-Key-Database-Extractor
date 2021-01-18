from CustomCI import CustomInput
import os

def init() : 
    
    # Global command line helpers
    currDir = os.path.dirname(os.path.realpath(__file__))
    rootDir = os.path.abspath(os.path.join(currDir, '..'))
    os.system('proot login')
    adb = 'adb'
    os.system(adb + ' devices')
    ADBSerialId = CustomInput('Choose device from "List of devices attached"\nFor example : 7835fd84543/emulator-5554 : ', 'green')
    return ADBSerialId
