from helpers.CustomCI import CustomPrint
from helpers.ADBDeviceSerialId import GetASBDeviceSerialId
import platform
import os

# Detect OS
isWindows = False
isLinux = False
if platform.system() == 'Windows' : isWindows = True 
if platform.system() == 'Linux' : isLinux = True

# Global command line helpers
adb = 'bin\\adb.exe -s ' + str(GetASBDeviceSerialId())
tmp = 'tmp\\'
if(isLinux) : 
    adb = 'adb -s ' + str(GetASBDeviceSerialId())
    tmp = 'tmp/'

def ReinstallWhatsApp():
    CustomPrint('Reinstallting original WhatsApp.')
    if(os.path.isfile(tmp + 'WhatsAppbackup.apk')) :
        try : 
            os.system(adb + ' install -r -d ' + tmp + 'WhatsAppbackup.apk')
        except Exception as e : 
            print(e)
            CustomPrint('Could not restore WhatsApp, install from Play Store.\nHowever if it crashes then you have to clear storage/clear data from settings => app settings => WhatsApp.')
    else : 
        CustomPrint('Could not find backup APK, install from play store.\nHowever if it crashes then you have to clear storage/clear data from settings => app settings => WhatsApp.','red')


ReinstallWhatsApp()