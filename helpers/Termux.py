import os
import re
from subprocess import check_output, getoutput

try:
    import wget
    from packaging import version
except ImportError:
    try:
        os.system('pip install wget packaging')
    except:
        os.system('python -m pip install wget packaging')

from CustomCI import CustomPrint

# Global variables
appURLWhatsAppCDN = 'https://www.cdn.whatsapp.net/android/2.11.431/WhatsApp.apk'
appURLWhatsCryptCDN = 'https://whatcrypt.com/WhatsApp-2.11.431.apk'


def AfterConnect(adb):
    SDKVersion = int(getoutput(
        adb + ' shell getprop ro.build.version.sdk'))
    if (SDKVersion <= 13):
        CustomPrint(
            'Unsupported device. This method only works on Android v4.0 or higer.', 'green')
        CustomPrint('Cleaning up temporary direcory.', 'green')
        os.system('rm -rf tmp/*')
        Exit()
    WhatsAppapkPath = re.search('(?<=package:)(.*)(?=apk)', str(check_output(
        adb + ' shell pm path com.whatsapp'))).group(1) + 'apk'
    if not (WhatsAppapkPath):
        CustomPrint('Looks like WhatsApp is not installed on device.')
        Exit()
    sdPath = getoutput(adb + ' shell "echo $EXTERNAL_STORAGE"')
    contentLength = int(re.search("(?<=Content-Length:)(.*[0-9])(?=)", str(check_output(
        'curl -sI http://www.cdn.whatsapp.net/android/2.11.431/WhatsApp.apk'.split()))).group(1))
    versionName = re.search("(?<=versionName=)(.*?)(?=\\\\r)", str(check_output(
        adb + ' shell dumpsys package com.whatsapp'))).group(1)
    CustomPrint('WhatsApp V' + versionName + ' installed on device')
    downloadAppFrom = appURLWhatsAppCDN if(
        contentLength == 18329558) else appURLWhatsCryptCDN
    if (version.parse(versionName) > version.parse('2.11.431')):
        if not (os.path.isfile('helpers/LegacyWhatsApp.apk')):
            CustomPrint(
                'Downloading legacy WhatsApp V2.11.431 to helpers folder')
            wget.download(downloadAppFrom, 'helpers/LegacyWhatsApp.apk')
        else:
            CustomPrint(
                'Found legacy WhatsApp V2.11.431 apk in helpers folder')

    return 1, SDKVersion, WhatsAppapkPath, versionName, sdPath


def Exit():
    CustomPrint('\nExiting...', 'green')
    os.system('adb kill-server')
    quit()


def TermuxMode(adb):
    CustomPrint('Connected to ' + getoutput(adb +
                                            ' shell getprop ro.product.model'))
    return AfterConnect(adb)
