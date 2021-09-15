import os
import re
from subprocess import check_output, getoutput
import subprocess

try:
    from packaging import version
    import requests
    from tqdm import tqdm
except ImportError:
    try:
        os.system('pip3 install packaging requests tqdm')
    except:
        os.system('python3 -m pip install packaging requests tqdm')

from custom_ci import custom_print, custom_input

# Global variables
appURLWhatsAppCDN = 'https://web.archive.org/web/20141111030303if_/http://www.whatsapp.com/android/current/WhatsApp.apk'
appURLWhatsCryptCDN = 'https://whatcrypt.com/WhatsApp-2.11.431.apk'


def AfterConnect(ADBSerialId):
    SDKVersion = int(getoutput('adb -s ' + ADBSerialId +
                               ' shell getprop ro.build.version.sdk'))
    if (SDKVersion <= 13):
        custom_print(
            'Unsupported device. This method only works on Android v4.0 or higer.', 'red')
        custom_print('Cleaning up \"tmp\" folder.', 'red')
        os.system('rm -rf tmp/*')
        Exit()
    _waPathText = 'adb -s ' + ADBSerialId + ' shell pm path com.whatsapp'
    proc = subprocess.Popen(_waPathText.split(), stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    out, err = proc.communicate()
    out = out.decode('utf-8')
    if(not out):
        custom_print('Looks like WhatsApp is not installed on device.', 'red')
        Exit()
    WhatsAppapkPath = re.search(
        '(?<=package:)(.*)(?=apk)', str(check_output(_waPathText.split()))).group(1) + 'apk'
    sdPath = getoutput('adb -s ' + ADBSerialId +
                       ' shell "echo $EXTERNAL_STORAGE"') or '/sdcard'
    # To check if APK even exists at a given path to download!
    # Since that obviously is not available at whatsapp cdn defaulting that to 0 for GH #46
    # Using getoutput instead of this to skip getting data like 0//n//r or whatever was getting recieved on GH #46 bcz check_output returns a byte type object and getoutput returns a str type .
    contentLength = int((re.findall("(?<=content-length:)(.*[0-9])(?=)", getoutput(
        'curl -sI https://web.archive.org/web/20141111030303if_/http://www.whatsapp.com/android/current/WhatsApp.apk')) or ['0'])[0])
    _versionNameText = 'adb -s ' + ADBSerialId + \
        ' shell dumpsys package com.whatsapp'
    versionName = re.search("(?<=versionName=)(.*?)(?=\\\\n)",
                            str(check_output(_versionNameText.split()))).group(1)
    custom_print('WhatsApp V' + versionName + ' installed on device')
    downloadAppFrom = appURLWhatsAppCDN if(
        contentLength == 18329558) else appURLWhatsCryptCDN
    if (version.parse(versionName) > version.parse('2.11.431')):
        if not (os.path.isfile('helpers/LegacyWhatsApp.apk')):
            custom_print(
                'Downloading legacy WhatsApp V2.11.431 to \"helpers\" folder')
            DownloadApk(downloadAppFrom, 'helpers/LegacyWhatsApp.apk')
            # wget.download(downloadAppFrom, 'helpers/LegacyWhatsApp.apk')
            custom_print('\n', is_get_time=False)
        else:
            custom_print(
                'Found legacy WhatsApp V2.11.431 apk in \"helpers\" folder')
    else:
        # Version lower than 2.11.431 installed on device.
        pass

    return 1, SDKVersion, WhatsAppapkPath, versionName, sdPath


def DownloadApk(url, fileName):
    # Streaming, so we can iterate over the response.
    response = requests.get(url, stream=True)
    totalSizeInBytes = response.headers.get(
        'x-archive-orig-content-length') or response.headers.get('content-length', 0)
    if(totalSizeInBytes):
        # Fixed where it stuck on "Downloading legacy WhatsApp V2.11.431 to helpers folder"
        totalSizeInBytes = int(totalSizeInBytes)
    else:
        # totalSizeInBytes must be null
        custom_print(
            '\aFor some reason I could not download Legacy WhatsApp, you need to download it on your own now from either of the links given below: ', 'red')
        custom_print('\n', is_get_time=False)
        custom_print('1. \"' + appURLWhatsAppCDN +
                     '\" (official\'s archive)', 'red')
        custom_print('2. \"' + appURLWhatsCryptCDN +
                     '\" unofficial website.', 'red')
        custom_print('\n', is_get_time=False)
        custom_print(
            'Once downloaded rename it to \"LegacyWhatsApp.apk\" exactly and put in \"helpers\" folder.', 'red')
        Exit()
    blockSize = 1024  # 1 Kibibyte
    progressBar = tqdm(total=totalSizeInBytes, unit='iB', unit_scale=True)
    with open('helpers/temp.apk', 'wb') as f:
        for data in response.iter_content(blockSize):
            progressBar.update(len(data))
            f.write(data)
    progressBar.close()
    os.rename('helpers/temp.apk', 'helpers/LegacyWhatsApp.apk')
    if totalSizeInBytes != 0 and progressBar.n != totalSizeInBytes:
        custom_print('\aSomething went during downloading LegacyWhatsApp.apk')
        Exit()


def Exit():
    custom_print('\n', is_get_time=False)
    custom_print('Exiting...')
    os.system('adb kill-server')
    custom_input('Hit \"Enter\" key to continue....', 'cyan')
    quit()


def LinuxUSB(ADBSerialId):
    custom_print('Connected to ' + getoutput('adb -s ' +
                                             ADBSerialId + ' shell getprop ro.product.model'))
    return AfterConnect(ADBSerialId)
