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

from CustomCI import CustomPrint, CustomInput

# Global Variables
appURLWhatsAppCDN = 'https://web.archive.org/web/20141111030303if_/http://www.whatsapp.com/android/current/WhatsApp.apk'
appURLWhatsCryptCDN = 'https://whatcrypt.com/WhatsApp-2.11.431.apk'

# Global command line helpers
tmp = 'tmp/'
helpers = 'helpers/'


def AfterConnect(adb):
    SDKVersion = int(getoutput(
        adb + ' shell getprop ro.build.version.sdk'))
    if (SDKVersion <= 13):
        CustomPrint(
            'Unsupported device. This method only works on Android v4.0 or higer.', 'red')
        CustomPrint('Cleaning up \"tmp\" folder.', 'red')
        os.remove(tmp)
        Exit()
    _waPathText = adb + ' shell pm path com.whatsapp'
    proc = subprocess.Popen(_waPathText.split(), stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    out, err = proc.communicate()
    out = out.decode('utf-8')
    if(not out):
        CustomPrint('Looks like WhatsApp is not installed on device.', 'red')
        Exit()
    WhatsAppapkPath = re.search('(?<=package:)(.*)(?=apk)', str(check_output(
        adb + ' shell pm path com.whatsapp'))).group(1) + 'apk'
    sdPath = getoutput(adb + ' shell "echo $EXTERNAL_STORAGE"')
    # To check if APK even exists at a given path to download!
    # Since that obviously is not available at whatsapp cdn defaulting that to 0 for GH #46
    # Using getoutput instead of this to skip getting data like 0//n//r or whatever was getting recieved on GH #46 bcz check_output returns a byte type object and getoutput returns a str type .
    contentLength = int((re.findall("(?<=content-length:)(.*[0-9])(?=)", getoutput(
        'curl -sI https://web.archive.org/web/20141111030303if_/http://www.whatsapp.com/android/current/WhatsApp.apk')) or ['0'])[0])
    versionName = re.search("(?<=versionName=)(.*?)(?=\\\\r)", str(check_output(
        adb + ' shell dumpsys package com.whatsapp'))).group(1)
    CustomPrint('WhatsApp V' + versionName + ' installed on device')
    downloadAppFrom = appURLWhatsAppCDN if(
        contentLength == 18329558) else appURLWhatsCryptCDN
    if (version.parse(versionName) > version.parse('2.11.431')):
        if not (os.path.isfile(helpers + 'LegacyWhatsApp.apk')):
            CustomPrint(
                'Downloading legacy WhatsApp V2.11.431 to \"' + helpers + '\" folder')
            DownloadApk(downloadAppFrom, 'helpers/LegacyWhatsApp.apk')
            # wget.download(downloadAppFrom, helpers + 'LegacyWhatsApp.apk')
            print('\n')
        else:
            CustomPrint(
                'Found legacy WhatsApp V2.11.431 apk in \"' + helpers + '\" folder')
    else:
        # Version lower than 2.11.431 installed on device.
        pass

    return 1, SDKVersion, WhatsAppapkPath, versionName, sdPath


def DownloadApk(url, fileName):
    # Streaming, so we can iterate over the response.
    response = requests.get(url, stream=True)
    # For WayBackMachine only.
    totalSizeInBytes = response.headers.get(
        'x-archive-orig-content-length') or response.headers.get('content-length', 0)
    if(totalSizeInBytes):
        # Fixed where it stuck on "Downloading legacy WhatsApp V2.11.431 to helpers folder"
        totalSizeInBytes = int(totalSizeInBytes)
    else:
        # totalSizeInBytes must be null
        CustomPrint('\aFor some reason I could not download Legacy WhatsApp, you need to download it on your own now from either of the links given below: ', 'red')
        print('\n')
        CustomPrint('1. \"' + appURLWhatsAppCDN +
                    '\" (official\'s archive)', 'red')
        CustomPrint('2. \"' + appURLWhatsCryptCDN +
                    '\" unofficial website.', 'red')
        print('\n')
        CustomPrint(
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
        CustomPrint('\aSomething went during downloading LegacyWhatsApp.apk')
        Exit()


def Exit():
    print('\n')
    CustomPrint('Exiting...')
    os.system('bin\\adb.exe kill-server')
    CustomInput('Hit \"Enter\" key to continue....', 'cyan')
    quit()


def WindowsUSB(adb):
    CustomPrint('Connected to ' + getoutput(adb +
                                            ' shell getprop ro.product.model'))
    return AfterConnect(adb)
