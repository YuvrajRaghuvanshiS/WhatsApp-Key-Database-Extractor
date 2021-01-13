from .CustomCI import CustomInput, CustomPrint
import os
from subprocess import check_output
import re
from packaging import version
import wget

# Global Variables
SDKVersion = ''
WhatsAppapkPath = ''
SDPath = '' # Internal storage.
versionName = ''
contentLength = '' # To check if APK even exists at a given path to download!
appURLWhatsAppCDN = 'https://www.cdn.whatsapp.net/android/2.11.431/WhatsApp.apk'
appURLWhatsCryptCDN = 'https://whatcrypt.com/WhatsApp-2.11.431.apk'

# Global command line helpers
adb = 'bin\\adb.exe'
tmp = 'tmp\\'
grep = 'bin\\grep.exe'
curl = 'bin\\curl.exe'
helpers = 'helpers\\'

def AfterConnect() : 
    SDKVersion = int(re.search('[0-9]{2,3}', str(check_output(adb +' shell getprop ro.build.version.sdk'))).group(0))
    if (SDKVersion <= 13) : 
        CustomPrint('Unsupported device. This method only works on Android v4.0 or higer.', 'green')
        CustomPrint('Cleaning up temporary direcory.', 'green')
        os.system('del /q tmp\\*')
        Exit()
    WhatsAppapkPath = re.search('(?<=package:)(.*)(?=apk)', str(check_output(adb + ' shell pm path com.whatsapp'))).group(1) + 'apk'
    if not (WhatsAppapkPath) : CustomPrint('Looks like WhatsApp is not installed on device.') ; Exit()
    SDPath = re.search("(?<=b')(.*)(?=\\\\r)", str(check_output(adb + ' shell "echo $EXTERNAL_STORAGE"'))).group(1)
    contentLength = int(re.search("(?<=Content-Length:)(.*[0-9])(?=)", str(check_output(curl + ' -sI http://www.cdn.whatsapp.net/android/2.11.431/WhatsApp.apk'))).group(1))
    versionName = re.search("(?<=versionName=)(.*?)(?=\\\\r)", str(check_output(adb + ' shell dumpsys package com.whatsapp'))).group(1)
    CustomPrint('WhatsApp V' + versionName + ' installed on device')
    downloadAppFrom = appURLWhatsAppCDN if(contentLength == 18329558) else appURLWhatsCryptCDN
    if (version.parse(versionName) > version.parse('2.11.431')) :
        if not (os.path.isfile(helpers + 'LegacyWhatsApp.apk')) : 
            CustomPrint('Downloading legacy WhatsApp V2.11.431 to helpers folder')
            wget.download(downloadAppFrom, helpers + 'LegacyWhatsApp.apk')
        else : 
            CustomPrint('Found legacy WhatsApp V2.11.431 apk in ' + helpers + ' folder')
 
    return 1, SDKVersion, WhatsAppapkPath, versionName

def Exit():
    CustomPrint('\nExiting...', 'green')
    os.system('bin\\adb.exe kill-server')
    quit()


def WindowsUSB() : 
    try : 
        os.system(adb + ' kill-server')
        os.system(adb + ' start-server')
        CustomPrint('Plug device via USB now..', 'green')
        os.system(adb + ' wait-for-device')
    except Exception as e : 
        CustomPrint(e)
        Exit()
    deviceName= adb + ' shell getprop ro.product.model'
    CustomPrint('Connected to ' + re.search("(?<=b')(.*)(?=\\\\r)", str(check_output(deviceName))).group(1) , 'green')
    return AfterConnect()
