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

# Global Variables
app_url_whatsapp_cdn = 'https://web.archive.org/web/20141111030303if_/http://www.whatsapp.com/android/current/WhatsApp.apk'
app_url_whatscrypt_cdn = 'https://whatcrypt.com/WhatsApp-2.11.431.apk'

# Global command line helpers
tmp = 'tmp/'
helpers = 'helpers/'


def after_connect(adb):
    sdk_version = int(getoutput(
        adb + ' shell getprop ro.build.version.sdk'))
    if (sdk_version <= 13):
        custom_print(
            'Unsupported device. This method only works on Android v4.0 or higer.', 'red')
        custom_print('Cleaning up \"tmp\" folder.', 'red')
        os.remove(tmp)
        kill_me()
    _wa_path_text = adb + ' shell pm path com.whatsapp'
    proc = subprocess.Popen(_wa_path_text.split(), stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    out, err = proc.communicate()
    out = out.decode('utf-8')
    if(not out):
        custom_print('Looks like WhatsApp is not installed on device.', 'red')
        kill_me()
    whatsapp_apk_path_in_device = re.search('(?<=package:)(.*)(?=apk)', str(check_output(
        adb + ' shell pm path com.whatsapp'))).group(1) + 'apk'
    sdcard_path = getoutput(adb + ' shell "echo $EXTERNAL_STORAGE"')
    # To check if APK even exists at a given path to download!
    # Since that obviously is not available at whatsapp cdn defaulting that to 0 for GH #46
    # Using getoutput instead of this to skip getting data like 0//n//r or whatever was getting recieved on GH #46 bcz check_output returns a byte type object and getoutput returns a str type .
    content_length = int((re.findall("(?<=content-length:)(.*[0-9])(?=)", getoutput(
        'curl -sI https://web.archive.org/web/20141111030303if_/http://www.whatsapp.com/android/current/WhatsApp.apk')) or ['0'])[0])
    version_name = re.search("(?<=versionName=)(.*?)(?=\\\\r)", str(check_output(
        adb + ' shell dumpsys package com.whatsapp'))).group(1)
    custom_print('WhatsApp V' + version_name + ' installed on device')
    download_app_from = app_url_whatsapp_cdn if(
        content_length == 18329558) else app_url_whatscrypt_cdn
    if (version.parse(version_name) > version.parse('2.11.431')):
        if not (os.path.isfile(helpers + 'LegacyWhatsApp.apk')):
            custom_print(
                'Downloading legacy WhatsApp V2.11.431 to \"' + helpers + '\" folder')
            download_apk(download_app_from, 'helpers/LegacyWhatsApp.apk')
            # wget.download(downloadAppFrom, helpers + 'LegacyWhatsApp.apk')
            custom_print('\n', is_get_time=False)
        else:
            custom_print(
                'Found legacy WhatsApp V2.11.431 apk in \"' + helpers + '\" folder')
    else:
        # Version lower than 2.11.431 installed on device.
        pass

    return 1, sdk_version, whatsapp_apk_path_in_device, version_name, sdcard_path


def download_apk(url, file_name):
    # Streaming, so we can iterate over the response.
    response = requests.get(url, stream=True)
    # For WayBackMachine only.
    total_size_in_bytes = response.headers.get(
        'x-archive-orig-content-length') or response.headers.get('content-length', 0)
    if(total_size_in_bytes):
        # Fixed where it stuck on "Downloading legacy WhatsApp V2.11.431 to helpers folder"
        total_size_in_bytes = int(total_size_in_bytes)
    else:
        # totalSizeInBytes must be null
        custom_print(
            '\aFor some reason I could not download Legacy WhatsApp, you need to download it on your own now from either of the links given below: ', 'red')
        custom_print('\n', is_get_time=False)
        custom_print('1. \"' + app_url_whatsapp_cdn +
                     '\" (official\'s archive)', 'red')
        custom_print('2. \"' + app_url_whatscrypt_cdn +
                     '\" unofficial website.', 'red')
        custom_print('\n', is_get_time=False)
        custom_print(
            'Once downloaded rename it to \"LegacyWhatsApp.apk\" exactly and put in \"helpers\" folder.', 'red')
        kill_me()
    block_size = 1024  # 1 Kibibyte
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    with open('helpers/temp.apk', 'wb') as f:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            f.write(data)
    progress_bar.close()
    os.rename('helpers/temp.apk', file_name)
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        custom_print('\aSomething went during downloading LegacyWhatsApp.apk')
        kill_me()


def kill_me():
    custom_print('\n', is_get_time=False)
    custom_print('Exiting...')
    os.system('bin\\adb.exe kill-server')
    custom_input('Hit \"Enter\" key to continue....', 'cyan')
    quit()


def windows_handler(adb):
    custom_print('Connected to ' + getoutput(adb +
                                             ' shell getprop ro.product.model'))
    return after_connect(adb)
