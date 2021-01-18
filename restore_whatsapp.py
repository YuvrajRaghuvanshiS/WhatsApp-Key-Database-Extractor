from helpers.CustomCI import CustomPrint
import helpers.ADBDeviceSerialId as deviceId
import os

# Global command line helpers 
adb = 'adb -s '
tmp = 'tmp/'

def ReinstallWhatsApp(ADBSerialId):
    CustomPrint('Reinstallting original WhatsApp.')
    if(os.path.isfile(tmp + 'WhatsAppbackup.apk')) :
        try : 
            os.system(adb + ADBSerialId + ' install -r -d ' + tmp + 'WhatsAppbackup.apk')
        except Exception as e : 
            print(e)
            CustomPrint('Could not restore WhatsApp, install from Play Store.\nHowever if it crashes then you have to clear storage/clear data from settings => app settings => WhatsApp.')
    else : 
        CustomPrint('Could not find backup APK, install from play store.\nHowever if it crashes then you have to clear storage/clear data from settings => app settings => WhatsApp.','red')

if __name__ == "__main__":
    ADBSerialId = deviceId.init()
    ReinstallWhatsApp(ADBSerialId)