# Auto Requirements installer.
import datetime
import json
import os
import socket

try:
    import packaging
    import psutil
    import requests
    import termcolor
    from tqdm import tqdm
except ImportError:
    print('\nFirst run: Auto installing python requirements.\n')
    try:
        # Trying both methods of installations
        os.system('pip3 install --upgrade packaging psutil termcolor requests tqdm')
    except:
        os.system(
            'python3 -m pip install --upgrade packaging psutil termcolor requests tqdm')


import argparse
import concurrent.futures
import platform
import re
import subprocess
import time

import helpers.adb_device_serial_id as adb_device_id
import helpers.tcp_device_serial_id as tcp_device_id
from helpers.custom_ci import custom_input, custom_print
from helpers.linux_handler import linux_handler
from helpers.windows_handler import windows_handler
from view_extract import extract_ab

# Detect OS
is_windows = False
is_linux = False
if platform.system() == 'Windows':
    is_windows = True
if platform.system() == 'Linux':
    is_linux = True

# Global Variables
app_url_whatsapp_cdn = 'https://www.cdn.whatsapp.net/android/2.11.431/WhatsApp.apk'
app_url_whatscrypt_cdn = 'https://whatcrypt.com/WhatsApp-2.11.431.apk'


def main():
    custom_print('>>> I am in wa_kdbe.main()', is_print=False)
    os.system('cls' if os.name == 'nt' else 'clear')
    check_bin()
    show_banner()
    global is_java_installed
    is_java_installed = check_java()
    custom_print('\n', is_get_time=False)
    try:
        custom_print('Arguments passed: ' + str(args), is_print=False)
    except Exception as e:
        custom_print(e, is_print=False)

    try:
        custom_print('System Info: ' +
                     json.dumps(get_sys_info(), indent=2, default=str), is_print=False)
    except Exception as e:
        custom_print(
            'Can\'t get system information. Continuing anyway...', 'yellow')
        custom_print(e, is_print=False)
    try:
        release_date_file = open('non_essentials/DATE', 'r')
        release_date = release_date_file.readline()
        release_date_file.close()
        custom_print('Current release date: ' + release_date, 'cyan')
    except Exception as e:
        custom_print(e, is_print=False)
    is_read_instructions = custom_input(
        '\aPlease read above instructions carefully \u2191 . Continue? (default y): ', 'yellow') or 'Y'
    if(is_read_instructions.upper() == 'Y'):
        custom_print('\n', is_get_time=False)
        custom_input(
            '\aIf you haven\'t already, it is adviced to take a WhatsApp chat backup by going to \"WhatsApp settings \u2192 Chat Settings \u2192 Chat Backup". Hit \"Enter\" key to continue.', 'yellow')
        usb_mode()
    else:
        kill_me()


def animate(message):
    frames = [
        "| o    |",
        "|  o   |",
        "|   o  |",
        "|    o |",
        "|     o|",
        "|    o |",
        "|   o  |",
        "|  o   |",
        "| o    |",
        "|o     |"
    ]
    message = message + ' '
    is_log_only_one_instance = True
    while(subprocess.getoutput(adb + ' get-state') != 'device'):
        # 6 iterations of 0.8 seconds sleep before checking again.
        temp = 6
        while(temp >= 0):
            for frame in frames:
                custom_print(message + frame,
                             is_log=is_log_only_one_instance, end='\r')
                is_log_only_one_instance = False
                # 0.8 seconds sleep: 0.08 * 10(frames)
                time.sleep(0.08)
            temp -= 1


def backup_whatsapp_apk(sdk_version, version_name, whatsapp_apk_path_in_device):
    custom_print('>>> I am in wa_kdbe.backup_whatsapp_apk(sdk_version=' + str(sdk_version) + ', version_name=' +
                 version_name + ', whatsapp_apk_path_in_device=' + whatsapp_apk_path_in_device + ')', is_print=False)
    os.system(adb + ' shell am force-stop com.whatsapp') if(sdk_version >
                                                            11) else os.system(adb + ' shell am kill com.whatsapp')
    custom_print('Backing up WhatsApp ' + version_name +
                 ' apk, the one installed on device to \"/data/local/tmp/WhatsAppbackup.apk\" in your phone.')
    os.system(adb + ' shell cp ' + whatsapp_apk_path_in_device +
              ' /data/local/tmp/WhatsAppbackup.apk')
    custom_print('Apk backup is completed.')


def backup_whatsapp_data_as_ab(sdk_version):
    custom_print('>>> I am in wa_kdbe.backup_whatsapp_data_as_ab(sdk_version=' +
                 str(sdk_version) + ')', is_print=False)
    os.mkdir(tmp) if not (os.path.isdir(tmp)) else custom_print(
        'Folder ' + tmp + ' already exists.', 'yellow')
    custom_print('Backing up WhatsApp data as \"' + tmp +
                 'whatsapp.ab\". May take time, don\'t panic.')
    try:
        os.system(adb + ' backup -f ' + tmp + 'whatsapp.ab com.whatsapp') if(sdk_version >=
                                                                             23) else os.system(adb + ' backup -f ' + tmp + 'whatsapp.ab -noapk com.whatsapp')
    except Exception as e:
        custom_print(e, 'red')
        kill_me()
    custom_print('Done backing up data. Size: ' +
                 str(os.path.getsize(tmp + 'whatsapp.ab')) + ' bytes.')


def check_bin():
    custom_print('>>> I am in wa_kdbe.check_bin()', is_print=False)
    if (not os.path.isdir('bin')):
        custom_print('I can not find \"bin\" folder, check again...', 'red')
        kill_me()
    else:
        pass


def check_java():
    custom_print('>>> I am in wa_kdbe.check_java()', is_print=False)
    java_version = ''
    out = subprocess.getoutput('java -version')
    if(out):
        java_version = re.findall('(?<=version ")(.*)(?=")', out)
    else:
        custom_print(
            'Could not get output of \"java -version\" in \"wa_kdbe.py\"', 'red')
        custom_print('Continuing without JAVA...', 'red')
        return False
    if(java_version):
        is_java_installed = True
    else:
        is_java_installed = False
    if is_java_installed:
        custom_print('Found Java v' + java_version[0] +
                     ' installed on system. Continuing...')
        return is_java_installed
    else:
        is_no_java_continue = custom_input(
            'It looks like you don\'t have JAVA installed on your system. Would you like to (C)ontinue with the process and \"view extract\" later? or (S)top?: ', 'red') or 'C'
        if(is_no_java_continue.upper() == 'C'):
            custom_print(
                'Continuing without JAVA, once JAVA is installed on system run \"view_extract.py\"', 'yellow')
            return is_java_installed
        else:
            kill_me()


def countdown(message, time_sec):
    while time_sec:
        mins, secs = divmod(time_sec, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        custom_print(message + timeformat + '.', end='\r')
        time.sleep(1)
        time_sec -= 1
    custom_print('', is_get_time=False)


def kill_me():
    custom_print('>>> I am in wa_kdbe.kill_me()', is_print=False)
    custom_print('\n', is_get_time=False)
    custom_print('Exiting...')
    os.system(
        'bin\\adb.exe kill-server') if(is_windows) else os.system('adb kill-server')
    custom_print(
        'Turn off USB debugging [and USB debugging (Security Settings)] if you\'re done.', 'cyan')
    custom_input('Hit \"Enter\" key to continue....', 'cyan')
    quit()


def get_sys_info():
    custom_print('>>> I am in wa_kdbe.get_sys_info()', is_print=False)
    info = {}
    info['Platform'] = platform.system()
    info['Platform Release'] = platform.release()
    info['Platform Version'] = platform.version()
    info['Architecture'] = platform.machine()
    info['Hostname'] = socket.gethostname()
    info['Processor'] = platform.processor()
    info['RAM'] = str(
        round(psutil.virtual_memory().total / (1024.0 ** 3)))+" GB"
    return info


def install_legacy(sdk_version):
    custom_print('>>> I am in wa_kdbe.install_legacy(sdk_version=' +
                 str(sdk_version) + ')', is_print=False)
    custom_print('Installing legacy WhatsApp V2.11.431, hold tight now.')
    if(sdk_version >= 17):
        install_legacy_out = subprocess.getoutput(
            adb + ' install -r -d ' + helpers + 'LegacyWhatsApp.apk')
        if('Success' in install_legacy_out):
            custom_print('Installation Complete.')
        else:
            custom_print('Could not install legacy WhatsApp', 'red')
            custom_print(install_legacy_out, 'red')
            countdown('Trying to restore WhatsApp in ', 10)
            reinstall_whatsapp()
            kill_me()

    else:
        install_legacy_out = subprocess.getoutput(
            adb + ' install -r ' + helpers + 'LegacyWhatsApp.apk')
        if('Success' in install_legacy_out):
            custom_print('Installation Complete.')
        else:
            custom_print('Could not install legacy WhatsApp', 'red')
            custom_print(install_legacy_out, 'red')
            kill_me()


def real_deal(sdk_version, whatsapp_apk_path_in_device, version_name, sdcard_path):
    custom_print('>>> I am in wa_kdbe.real_deal(sdk_version=' + str(sdk_version) + ', whatsapp_apk_path_in_device=' +
                 whatsapp_apk_path_in_device + ', version_name=' + version_name + ', sdcard_path=' + sdcard_path + ')', is_print=False)
    backup_whatsapp_apk(sdk_version, version_name, whatsapp_apk_path_in_device)
    uninstall_whatsapp(sdk_version)
    # Reboot here.
    if(is_allowed_reboot):
        if(not tcp_ip):
            custom_print('\n', is_get_time=False)
            custom_print('Rebooting device, please wait.', 'yellow')
            os.system(adb + ' reboot')
            animate('Waiting for device to get online')
            custom_input('Hit \"Enter\" key after unlocking device.', 'yellow')
        else:
            custom_print(
                'Rebooting device in TCP mode break the connection and won\'t work until explicitly turned on in device and/or in PC. Skipping...', 'yellow')

    install_legacy(sdk_version)
    # Before backup run app
    custom_print(subprocess.getoutput(
        adb + ' shell am start -n com.whatsapp/.Main'))
    custom_input(
        '\aHit \"Enter\" key after running Legacy WhatsApp for a while. Ignore invalid date warning.', 'yellow')
    backup_whatsapp_data_as_ab(sdk_version)
    reinstall_whatsapp()
    custom_print('\n', is_get_time=False)
    custom_print(
        '\aOur work with device has finished, it is safe to remove it now.', 'yellow')
    custom_print('\n', is_get_time=False)
    extract_ab(is_java_installed, sdcard_path=sdcard_path,
               adb_device_serial_id=adb_device_serial_id, is_tar_only=is_tar_only)


def reinstall_whatsapp():
    custom_print('>>> I am in wa_kdbe.reinstall_whatsapp()', is_print=False)
    custom_print('Reinstalling original WhatsApp.')
    try:
        reinstall_whatsapp_out = subprocess.getoutput(
            adb + ' shell pm install /data/local/tmp/WhatsAppbackup.apk')
        if('Success' in reinstall_whatsapp_out):
            custom_print('Reinstallation complete.')
        else:
            custom_print('Could not install WhatsApp, install by running \"restore_whatsapp.py\" or manually installing from Play Store.\nHowever if it crashes then you have to clear storage/clear data from \"Settings \u2192 App Settings \u2192 WhatsApp\".', 'red')
            custom_print(reinstall_whatsapp_out, 'red')
    except Exception as e:
        custom_print(e, 'red')
        kill_me()


def run_scrcpy(_is_scrcpy):
    custom_print('>>> I am in wa_kdbe.run_scrcpy(_is_scrcpy=' +
                 str(_is_scrcpy) + ')', is_print=False)
    if(_is_scrcpy):
        cmd = 'bin\scrcpy.exe --max-fps 15 -b 4M --always-on-top' if(
            is_windows) else 'scrcpy --max-fps 15 -b 4M --always-on-top'
        proc = subprocess.Popen(cmd.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, shell=False)
        proc.communicate()


def show_banner():
    custom_print('>>> I am in wa_kdbe.show_banner()', is_print=False)
    banner_content = '''
================================================================================
========                                                                ========
========  db   d8b   db  .d8b.         db   dD d8888b. d8888b. d88888b  ======== 
========  88   I8I   88 d8' `8b        88 ,8P' 88  `8D 88  `8D 88'      ======== 
========  88   I8I   88 88ooo88        88,8P   88   88 88oooY' 88ooooo  ======== 
========  Y8   I8I   88 88~~~88 C8888D 88`8b   88   88 88~~~b. 88~~~~~  ======== 
========  `8b d8'8b d8' 88   88        88 `88. 88  .8D 88   8D 88.      ======== 
========   `8b8' `8d8'  YP   YP        YP   YD Y8888D' Y8888P' Y88888P  ======== 
========                                                                ========
================================================================================'''

    intro_a = '''
============ WhatsApp Key / Database Extrator for non-rooted Android ===========\n
================================================================================
===                                                                          ==='''

    intro_b = '''===  xxxxx  PLEASE TAKE WHATSAPP CHAT BACKUP BEFORE GETTING STARTED.  xxxxx  ==='''

    intro_c = '''===                                                                          ===
===     For that go to \"WhatsApp settings \u2192 Chat Settings \u2192 Chat Backup\"     ===
===              here take a local backup. Prepare for Worst.                ===
===                                                                          ==='''

    intro_d = '''===  Also if you see a folder \"Android/media/com.whatsapp\" copy it somewhere ===
===   safe. New versions of WhatsApp are saving data here INCLUDING IMAGES   ===
===       AND VIDEOS. I try to save it while uninstalling WhatsApp but       ===
===                        YOU CAN NEVER BE TOO SAFE.                        ==='''

    intro_e = '''===                                                                          ===
===     This script can extract your WhatsApp msgstore.db (non crypt12,      ===
===   un-encrypted file) and your \"key\" file from \"/data/data/com.whatsapp\"  ===
===  directory in Android 4.0+ device without root access. However you need  ===
===   to have JAVA installed on your system in order to \"view the extract\".  ===
===  If you don't have JAVA installed then you can \"view extract\" later by   ===
===   running \"view_extract.py\". The idea is to install a \"Legacy WhatsApp\"  ===
===       temporarily on your device in order to get the android backup      ===
===    permission. You should not lose any data and your current WhatsApp    ===
===   version will be installed after this process so don't panic and don't  ===
=== stop this script while it's working. However if something fails you can  ===
===    run \"restore_whatsapp.py\" and reinstall current WhatsApp or simply    ===
===                    update that from Google Play Store.                   ===
===                                                                          ===
===                      Script by: Yuvraj Raghuvanshi                       ===
===                      Github.com/YuvrajRaghuvanshiS                       ===
================================================================================
    '''
    custom_print(banner_content, 'green', ['bold'], False)
    custom_print(intro_a, 'green', ['bold'], False)
    custom_print(intro_b, 'red', ['bold'], False)
    custom_print(intro_c, 'green', ['bold'], False)
    custom_print(intro_d, 'red', ['bold'], False)
    custom_print(intro_e, 'green', ['bold'], False)


def uninstall_whatsapp(sdk_version):
    custom_print('>>> I am in wa_kdbe.uninstall_whatsapp(sdk_version=' +
                 str(sdk_version) + ')', is_print=False)
    if(sdk_version >= 23):
        try:
            custom_print('Uninstalling WhatsApp, skipping data.')
            uninstall_out = subprocess.getoutput(
                adb + ' shell pm uninstall -k com.whatsapp')
            if('Success' in uninstall_out):
                custom_print('Uninstalled.')
            else:
                custom_print('Could not uninstall WhatsApp.', 'red')
                custom_print(uninstall_out, 'red')
                kill_me()
        except Exception as e:
            custom_print(e, 'red')
            kill_me()


def usb_mode():
    custom_print('>>> I am in wa_kdbe.usb_mode()', is_print=False)
    if(is_windows):
        after_connect_return_code, sdk_version, whatsapp_apk_path_in_device, version_name, sdcard_path = windows_handler(
            adb)
        real_deal(sdk_version, whatsapp_apk_path_in_device, version_name,
                  sdcard_path) if after_connect_return_code == 1 else kill_me()
    else:
        after_connect_return_code, sdk_version, whatsapp_apk_path_in_device, version_name, sdcard_path = linux_handler(
            adb_device_serial_id)
        real_deal(sdk_version, whatsapp_apk_path_in_device, version_name,
                  sdcard_path) if after_connect_return_code == 1 else kill_me()


if __name__ == "__main__":

    custom_print('\n\n\n====== Logging start here. ====== \nFile: ' + os.path.basename(__file__) + '\nDate: ' +
                 str(datetime.datetime.now()) + '\nIf you see any password here then do let know @github.com/YuvrajRaghuvanshiS/WhatsApp-Key-Database-Extractor\n\n\n', is_get_time=False, is_print=False)

    parser = argparse.ArgumentParser()
    parser.add_argument('-ar', '--allow-reboot', action='store_true',
                        help='Allow reboot of device before installation of LegacyWhatsApp.apk to prevent some issues like [INSTALL_FAILED_VERSION_DOWNGRADE]')
    parser.add_argument('-tip', '--tcp-ip',
                        help='Connects to a remote device via TCP mode.')
    parser.add_argument('-tp', '--tcp-port',
                        help='Port number to connect to. Default: 5555')
    parser.add_argument('-s', '--scrcpy', action='store_true',
                        help='Run ScrCpy to see and control Android device.')
    parser.add_argument('-to', '--tar-only', action='store_true',
                        help='Get entire WhatsApp\'s data in \"<username>.tar\" file instead of just getting few important files.')
    args = parser.parse_args()
    # args = parser.parse_args('--tcp-ip 192.168.43.130 --scrcpy'.split())

    is_allowed_reboot = args.allow_reboot
    tcp_ip = args.tcp_ip
    tcp_port = args.tcp_port
    is_scrcpy = args.scrcpy
    is_tar_only = args.tar_only
    if(tcp_ip):
        if(not tcp_port):
            tcp_port = '5555'
        adb_device_serial_id = tcp_device_id.init(tcp_ip, tcp_port)
    else:
        adb_device_serial_id = adb_device_id.init()
    if(not adb_device_serial_id):
        kill_me()

    # Global command line helpers
    tmp = 'tmp/'
    helpers = 'helpers/'
    if(is_windows):
        adb = 'bin\\adb.exe -s ' + adb_device_serial_id
    else:
        adb = 'adb -s ' + adb_device_serial_id

    with concurrent.futures.ThreadPoolExecutor() as executor:
        f1 = executor.submit(main)
        time.sleep(1)
        f2 = executor.submit(run_scrcpy, is_scrcpy)
