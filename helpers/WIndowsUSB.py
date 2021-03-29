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

# Global Variables
appURLWhatsAppCDN = 'https://www.cdn.whatsapp.net/android/2.11.431/WhatsApp.apk'
appURLWhatsCryptCDN = 'https://whatcrypt.com/WhatsApp-2.11.431.apk'

# Global command line helpers
tmp = 'tmp/'
grep = 'bin\\grep.exe'
curl = 'bin\\curl.exe'
helpers = 'helpers/'


def AfterConnect(adb):
    pdb.set_trace()
    SDKVersion = int(getoutput(
        adb + ' shell getprop ro.build.version.sdk'))
    if (SDKVersion <= 13):
        CustomPrint(
            'Unsupported device. This method only works on Android v4.0 or higer.', 'red')
        CustomPrint('Cleaning up temporary direcory.', 'red')
        os.remove(tmp)
        Exit()
    WhatsAppapkPath = re.search('(?<=package:)(.*)(?=apk)', str(check_output(
        adb + ' shell pm path com.whatsapp'))).group(1) + 'apk'
    if not (WhatsAppapkPath):
        CustomPrint('Looks like WhatsApp is not installed on device.', 'red')
        Exit()
    sdPath = getoutput(adb + ' shell "echo $EXTERNAL_STORAGE"')
    # To check if APK even exists at a given path to download!
    contentLength = int(re.search("(?<=Content-Length:)(.*[0-9])(?=)", str(check_output(
        curl + ' -sI http://www.cdn.whatsapp.net/android/2.11.431/WhatsApp.apk'))).group(1))
    versionName = re.search("(?<=versionName=)(.*?)(?=\\\\r)", str(check_output(
        adb + ' shell dumpsys package com.whatsapp'))).group(1)
    CustomPrint('WhatsApp V' + versionName + ' installed on device')
    downloadAppFrom = appURLWhatsAppCDN if(
        contentLength == 18329558) else appURLWhatsCryptCDN
    if (version.parse(versionName) > version.parse('2.11.431')):
        if not (os.path.isfile(helpers + 'LegacyWhatsApp.apk')):
            CustomPrint(
                'Downloading legacy WhatsApp V2.11.431 to helpers folder')
            DownloadApk(downloadAppFrom, 'helpers/LegacyWhatsApp.apk')
            # wget.download(downloadAppFrom, helpers + 'LegacyWhatsApp.apk')
            print('\n')
        else:
            CustomPrint('Found legacy WhatsApp V2.11.431 apk in ' +
                        helpers + ' folder')

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
    CustomPrint('\nExiting...')
    os.system('bin\\adb.exe kill-server')
    quit()


def WindowsUSB(adb):
    pdb.set_trace()
    CustomPrint('Connected to ' + getoutput(adb +
                                            ' shell getprop ro.product.model'))
    return AfterConnect(adb)
