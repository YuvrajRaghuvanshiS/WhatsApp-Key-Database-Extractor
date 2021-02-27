import os
import re
from subprocess import check_output, getoutput

try:
    import wget
    from packaging import version
except ImportError:
    try:
        os.system('pip3 install wget packaging')
    except:
        os.system('python3 -m pip install wget packaging')

from CustomCI import CustomPrint

# Global variables
appURLWhatsAppCDN = 'https://www.cdn.whatsapp.net/android/2.11.431/WhatsApp.apk'
appURLWhatsCryptCDN = 'https://whatcrypt.com/WhatsApp-2.11.431.apk'


def AfterConnect(ADBSerialId):
    SDKVersion = int(getoutput('adb -s ' + ADBSerialId +
                               ' shell getprop ro.build.version.sdk'))
    if (SDKVersion <= 13):
        CustomPrint(
            'Unsupported device. This method only works on Android v4.0 or higer.', 'red')
        CustomPrint('Cleaning up temporary direcory.', 'red')
        os.system('rm -rf tmp/*')
        Exit()
    _waPathText = 'adb -s ' + ADBSerialId + ' shell pm path com.whatsapp'
    WhatsAppapkPath = re.search(
        '(?<=package:)(.*)(?=apk)', str(check_output(_waPathText.split()))).group(1) + 'apk'
    if not (WhatsAppapkPath):
        CustomPrint('Looks like WhatsApp is not installed on device.', 'red')
        Exit()
    sdPath = getoutput('adb -s ' + ADBSerialId +
                       ' shell "echo $EXTERNAL_STORAGE"') or '/sdcard'
    # To check if APK even exists at a given path to download!
    contentLength = int(re.search("(?<=Content-Length:)(.*[0-9])(?=)", str(check_output(
        'curl -sI http://www.cdn.whatsapp.net/android/2.11.431/WhatsApp.apk'.split()))).group(1))
    _versionNameText = 'adb -s ' + ADBSerialId + \
        ' shell dumpsys package com.whatsapp'
    versionName = re.search("(?<=versionName=)(.*?)(?=\\\\n)",
                            str(check_output(_versionNameText.split()))).group(1)
    CustomPrint('WhatsApp V' + versionName + ' installed on device')
    downloadAppFrom = appURLWhatsAppCDN if(
        contentLength == 18329558) else appURLWhatsCryptCDN
    if (version.parse(versionName) > version.parse('2.11.431')):
        if not (os.path.isfile('helpers/LegacyWhatsApp.apk')):
            CustomPrint(
                'Downloading legacy WhatsApp V2.11.431 to helpers folder')
            wget.download(downloadAppFrom, 'helpers/LegacyWhatsApp.apk')
            print('\n')
        else:
            CustomPrint(
                'Found legacy WhatsApp V2.11.431 apk in helpers folder')

    return 1, SDKVersion, WhatsAppapkPath, versionName, sdPath


def Exit():
    print('\n')
    CustomPrint('Exiting...')
    os.system('adb kill-server')
    quit()


def LinuxUSB(ADBSerialId):
    CustomPrint('Connected to ' + getoutput('adb -s ' +
                                            ADBSerialId + ' shell getprop ro.product.model'))
    return AfterConnect(ADBSerialId)
