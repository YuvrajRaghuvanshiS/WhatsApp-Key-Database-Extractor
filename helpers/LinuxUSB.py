import os
import pdb
import re
from subprocess import check_output, getoutput

try:
    from packaging import version
    import requests
    from tqdm import tqdm
except ImportError:
    try:
        os.system('pip3 install packaging requests tqdm')
    except:
        os.system('python3 -m pip install packaging requests tqdm')

from CustomCI import CustomPrint

# Global variables
appURLWhatsAppCDN = 'https://www.cdn.whatsapp.net/android/2.11.431/WhatsApp.apk'
appURLWhatsCryptCDN = 'https://whatcrypt.com/WhatsApp-2.11.431.apk'


def AfterConnect(ADBSerialId):
    pdb.set_trace()
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
    # Since that obviously is not available at whatsapp cdn defaulting that to 0 for GH #46
    try:
        contentLength = int(re.search("(?<=Content-Length:)(.*[0-9])(?=)", str(check_output(
            'curl -sI http://www.cdn.whatsapp.net/android/2.11.431/WhatsApp.apk'.split()))).group(1))
    except ValueError:
        contentLength = 0
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
            DownloadApk(downloadAppFrom, 'helpers/LegacyWhatsApp.apk')
            # wget.download(downloadAppFrom, 'helpers/LegacyWhatsApp.apk')
            print('\n')
        else:
            CustomPrint(
                'Found legacy WhatsApp V2.11.431 apk in helpers folder')

    return 1, SDKVersion, WhatsAppapkPath, versionName, sdPath


def DownloadApk(url, fileName):
    # Streaming, so we can iterate over the response.
    response = requests.get(url, stream=True)
    totalSizeInBytes = int(response.headers.get('content-length', 0))
    blockSize = 1024  # 1 Kibibyte
    progressBar = tqdm(total=totalSizeInBytes, unit='iB', unit_scale=True)
    with open(fileName, 'wb') as file:
        for data in response.iter_content(blockSize):
            progressBar.update(len(data))
            file.write(data)
    progressBar.close()
    if totalSizeInBytes != 0 and progressBar.n != totalSizeInBytes:
        CustomPrint('\aSomething went during downloading LegacyWhatsApp.apk')


def Exit():
    print('\n')
    CustomPrint('Exiting...')
    os.system('adb kill-server')
    quit()


def LinuxUSB(ADBSerialId):
    pdb.set_trace()
    CustomPrint('Connected to ' + getoutput('adb -s ' +
                                            ADBSerialId + ' shell getprop ro.product.model'))
    return AfterConnect(ADBSerialId)
