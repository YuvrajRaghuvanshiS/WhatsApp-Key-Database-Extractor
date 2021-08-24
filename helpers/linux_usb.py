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
app_url_whatsapp_cdn = 'https://web.archive.org/web/20141111030303if_/http://www.whatsapp.com/android/current/WhatsApp.apk'
app_url_whatscrypt_cdn = 'https://whatcrypt.com/WhatsApp-2.11.431.apk'


def after_connect(adb_serial_id):
    sdk_version = int(getoutput('adb -s ' + adb_serial_id +
                                ' shell getprop ro.build.version.sdk'))
    if (sdk_version <= 13):
        custom_print(
            'Unsupported device. This method only works on Android v4.0 or higer.', 'red')
        custom_print('Cleaning up \"tmp\" folder.', 'red')
        os.system('rm -rf tmp/*')
        Exit()
    _wa_path_text = 'adb -s ' + adb_serial_id + ' shell pm path com.whatsapp'
    proc = subprocess.Popen(_wa_path_text.split(), stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    out, err = proc.communicate()
    out = out.decode('utf-8')
    if(not out):
        custom_print('Looks like WhatsApp is not installed on device.', 'red')
        Exit()
    whatsapp_apk_path = re.search(
        '(?<=package:)(.*)(?=apk)', str(check_output(_wa_path_text.split()))).group(1) + 'apk'
    sd_path = getoutput('adb -s ' + adb_serial_id +
                        ' shell "echo $EXTERNAL_STORAGE"') or '/sdcard'
    # To check if APK even exists at a given path to download!
    # Since that obviously is not available at whatsapp cdn defaulting that to 0 for GH #46
    # Using getoutput instead of this to skip getting data like 0//n//r or whatever was getting recieved on GH #46 bcz check_output returns a byte type object and getoutput returns a str type .
    content_length = int((re.findall("(?<=content-length:)(.*[0-9])(?=)", getoutput(
        'curl -sI https://web.archive.org/web/20141111030303if_/http://www.whatsapp.com/android/current/WhatsApp.apk')) or ['0'])[0])
    _version_name_text = 'adb -s ' + adb_serial_id + \
        ' shell dumpsys package com.whatsapp'
    version_name = re.search("(?<=versionName=)(.*?)(?=\\\\n)",
                             str(check_output(_version_name_text.split()))).group(1)
    custom_print('WhatsApp V' + version_name + ' installed on device')
    download_app_from = app_url_whatsapp_cdn if(
        content_length == 18329558) else app_url_whatscrypt_cdn
    if (version.parse(version_name) > version.parse('2.11.431')):
        if not (os.path.isfile('helpers/LegacyWhatsApp.apk')):
            custom_print(
                'Downloading legacy WhatsApp V2.11.431 to \"helpers\" folder')
            download_apk(download_app_from, 'helpers/LegacyWhatsApp.apk')
            # wget.download(downloadAppFrom, 'helpers/LegacyWhatsApp.apk')
            print('\n')
        else:
            custom_print(
                'Found legacy WhatsApp V2.11.431 apk in \"helpers\" folder')
    else:
        # Version lower than 2.11.431 installed on device.
        pass

    return 1, sdk_version, whatsapp_apk_path, version_name, sd_path


def download_apk(url, file_name):
    # Streaming, so we can iterate over the response.
    response = requests.get(url, stream=True)
    total_size_in_bytes = response.headers.get(
        'x-archive-orig-content-length') or response.headers.get('content-length', 0)
    if(total_size_in_bytes):
        # Fixed where it stuck on "Downloading legacy WhatsApp V2.11.431 to helpers folder"
        total_size_in_bytes = int(total_size_in_bytes)
    else:
        # totalSizeInBytes must be null
        custom_print('\aFor some reason I could not download Legacy WhatsApp, you need to download it on your own now from either of the links given below : ', 'red')
        print('\n')
        custom_print('1. \"' + app_url_whatsapp_cdn +
                     '\" (official\'s archive)', 'red')
        custom_print('2. \"' + app_url_whatscrypt_cdn +
                     '\" unofficial website.', 'red')
        print('\n')
        custom_print(
            'Once downloaded rename it to \"LegacyWhatsApp.apk\" exactly and put in \"helpers\" folder.', 'red')
        Exit()
    block_size = 1024  # 1 Kibibyte
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    with open('helpers/temp.apk', 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
    os.rename('helpers/temp.apk', file_name)
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        custom_print('\aSomething went during downloading LegacyWhatsApp.apk')
        Exit()


def Exit():
    print('\n')
    custom_print('Exiting...')
    os.system('adb kill-server')
    custom_input('Hit \"Enter\" key to continue....', 'cyan')
    quit()


def linux_usb(ADBSerialId):
    custom_print('Connected to ' + getoutput('adb -s ' +
                                             ADBSerialId + ' shell getprop ro.product.model'))
    return after_connect(ADBSerialId)
