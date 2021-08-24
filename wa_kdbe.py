# File: wa_kdbe.py
# Author: Yuvraj Raghuvanshi (YuvrajRaghuvanshi.S@protonmail.com)
# Description: Main file of project.

# Auto requirements installer.
import json
import os
import socket

try:
    import packaging
    import psutil
    import termcolor
    import requests
    from tqdm import tqdm
except ImportError:
    print('\nFirst run : Auto installing python requirements.\n')
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

import helpers.adb_device_serial_id as device_id
import helpers.tcp_device_serial_id as tcp_device_id
from helpers.custom_ci import custom_input, custom_print
from helpers.linux_usb import linux_usb
from helpers.wIndows_usb import windows_usb
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
is_java_installed = False


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    check_bin()
    show_banner()
    global is_java_installed
    is_java_installed = check_java()
    print('\n')
    try:
        custom_print('Arguments passed : ' + str(args))
        print('\n')
    except:
        pass

    try:
        custom_print('System Info : ' +
                     json.dumps(get_sys_info(), indent=2, default=str))
        print('\n')
    except:
        custom_print(
            'Can\'t get system information. Continuing anyway...', 'yellow')
    custom_print('Current release date : 29/06/2021', 'cyan')
    print('\n')
    read_instruction = custom_input(
        '\aPlease read above instructions carefully \u2191 . Continue? (default y) : ', 'yellow') or 'y'
    if(read_instruction.upper() == 'Y'):
        print('\n')
        custom_input(
            '\aIf you haven\'t already, it is adviced to take a WhatsApp chat backup by going to \"WhatsApp settings \u2192 Chat Settings \u2192 Chat Backup". Hit \"Enter\" key to continue.', 'yellow')
        usb_mode()
    else:
        exit()


def backup_whatsapp_apk(sdk_version, version_name, whatsapp_apk_path):
    os.system(adb + ' shell am force-stop com.whatsapp') if(sdk_version >
                                                            11) else os.system(adb + ' shell am kill com.whatsapp')
    custom_print('Backing up WhatsApp ' + version_name +
                 ' apk, the one installed on device to \"' + tmp + 'WhatsAppbackup.apk\".')
    os.mkdir(tmp) if not (os.path.isdir(tmp)) else custom_print(
        'Folder \"' + tmp + '\" already exists.', 'yellow')
    os.system(adb + ' shell cp ' + whatsapp_apk_path +
              ' /sdcard/WhatsAppbackup.apk')
    os.system(adb + ' pull /sdcard/WhatsAppbackup.apk ' +
              helpers + 'WhatsAppbackup.apk')
    # Delete temp apk from /sdcard.
    os.system(adb + ' shell rm -rf /sdcard/WhatsAppbackup.apk')
    custom_print('Apk backup complete.')


def backup_whatsapp_data_as_ab(sdk_version):
    custom_print('Backing up WhatsApp data as \"' + tmp +
                 'whatsapp.ab\". May take time, don\'t panic.')
    try:
        os.system(adb + ' backup -f ' + tmp + 'whatsapp.ab com.whatsapp') if(sdk_version >=
                                                                             23) else os.system(adb + ' backup -f ' + tmp + 'whatsapp.ab -noapk com.whatsapp')
    except Exception as e:
        custom_print(e, 'red')
        exit()
    custom_print('Done backing up data. Size : ' +
                 str(os.path.getsize(tmp + 'whatsapp.ab')) + ' bytes.')


def check_bin():
    if (not os.path.isdir('bin')):
        custom_print('I can not find \"bin\" folder, check again...', 'red')
        exit()
    else:
        pass


def check_java():
    java_version = re.search('(?<=version ")(.*)(?=")', str(subprocess.check_output(
        'java -version'.split(), stderr=subprocess.STDOUT))).group(1)
    is_java_installed = True if(java_version) else False
    if is_java_installed:
        custom_print('Found Java installed on system.')
        return is_java_installed
    else:
        continue_without_java = custom_input(
            'It looks like you don\'t have JAVA installed on your system. Would you like to (C)ontinue with the process and \"view extract\" later? or (S)top? : ', 'red') or 'c'
        if(continue_without_java.upper() == 'C'):
            custom_print(
                'Continuing without JAVA, once JAVA is installed on system run \"view_extract.py\"', 'yellow')
            return is_java_installed
        else:
            exit()


def exit():
    print('\n')
    custom_print('Exiting...')
    os.system(
        'bin\\adb.exe kill-server') if(is_windows) else os.system('adb kill-server')
    custom_input('Hit \"Enter\" key to continue....', 'cyan')
    quit()


def get_sys_info():
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
    custom_print('Installing legacy WhatsApp V2.11.431, hold tight now.')
    if(sdk_version >= 17):
        os.system(adb + ' install -r -d ' + helpers + 'LegacyWhatsApp.apk')
    else:
        os.system(adb + ' install -r ' + helpers + 'LegacyWhatsApp.apk')
    custom_print('Installation Complete.')


def real_deal(sdk_version, whatsapp_apk_path, version_name, sd_path):
    backup_whatsapp_apk(sdk_version, version_name, whatsapp_apk_path)
    uninstall_whatsapp(sdk_version)
    # Reboot here.
    if(is_allow_reboot):
        if(not tcp_ip):
            print('\n')
            custom_print('Rebooting device, please wait.', 'yellow')
            os.system(adb + ' reboot')
            while(subprocess.getoutput(adb + ' get-state') != 'device'):
                custom_print('Waiting for device...')
                time.sleep(5)
            custom_input('Hit \"Enter\" key after unlocking device.', 'yellow')
        else:
            custom_print(
                'Rebooting device in TCP mode break the connection and won\'t work until explicitly turned on in device and/or in PC. Skipping...', 'yellow')

    install_legacy(sdk_version)
    # Before backup run app
    os.system(adb + ' shell am start -n com.whatsapp/.Main')
    custom_input(
        '\aHit \"Enter\" key after running Legacy WhatsApp for a while. Ignore invalid date warning.', 'yellow')
    backup_whatsapp_data_as_ab(sdk_version)
    reinstall_whatsapp()
    print('\n')
    custom_print(
        '\aOur work with device has finished, it is safe to remove it now.', 'yellow')
    print('\n')
    extract_ab(is_java_installed, sd_path=sd_path,
               adb_serial_id=adb_serial_id, is_tar_only=is_tar_only)


def reinstall_whatsapp():
    custom_print('Reinstallting original WhatsApp.')
    try:
        os.system(adb + ' install -r -d ' + helpers + 'WhatsAppbackup.apk')
    except Exception as e:
        custom_print(e, 'red')
        custom_print('Could not install WhatsApp, install by running \"restore_whatsapp.py\" or manually installing from Play Store.\nHowever if it crashes then you have to clear storage/clear data from \"Settings \u2192 App Settings \u2192 WhatsApp\".')
        exit()


def run_scrcpy(_is_scrcpy):
    if(_is_scrcpy):
        cmd = 'bin\scrcpy.exe --max-fps 15 -b 4M --always-on-top' if(
            is_windows) else 'scrcpy --max-fps 15 -b 4M --always-on-top'
        proc = subprocess.Popen(cmd.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, shell=False)
        proc.communicate()


def show_banner():
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
================================================================================
    '''
    custom_print(banner_content, 'green', ['bold'], False)
    custom_print('============ WhatsApp Key / Database Extrator for non-rooted Android ===========',
                 'green', ['bold'], False)
    intro_content = '''
================================================================================
===                                                                          ===
===  xxxxx  PLEASE TAKE WHATSAPP CHAT BACKUP BEFORE GETTING STARTED.  xxxxx  ===
===                                                                          ===
===     For that go to \"WhatsApp settings \u2192 Chat Settings \u2192 Chat Backup\"     ===
===              here take a local backup. Prepare for Worst.                ===
===                                                                          ===
===     This script can extract your WhatsApp msgstore.db (non crypt12,      ===
===   unencrypted file) and your \"key\" file from \"/data/data/com.whatsapp\"   ===
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
    custom_print(intro_content, 'green', ['bold'], False)


def uninstall_whatsapp(sdk_version):
    if(sdk_version >= 23):
        try:
            custom_print('Uninstalling WhatsApp, skipping data.')
            os.system(adb + ' shell pm uninstall -k com.whatsapp')
            custom_print('Uninstalled.')
        except Exception as e:
            custom_print('Could not uninstall WhatsApp.')
            custom_print(e, 'red')
            exit()


def usb_mode():
    if(is_windows):
        afterconnect_return_code, sdk_version, whatsapp_apk_path, version_name, sd_path = windows_usb(
            adb)
        real_deal(sdk_version, whatsapp_apk_path, version_name,
                  sd_path) if afterconnect_return_code == 1 else exit()
    else:
        afterconnect_return_code, sdk_version, whatsapp_apk_path, version_name, sd_path = linux_usb(
            adb_serial_id)
        real_deal(sdk_version, whatsapp_apk_path, version_name,
                  sd_path) if afterconnect_return_code == 1 else exit()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-ar', '--allow-reboot', action='store_true',
                        help='Allow reboot of device before installation of LegacyWhatsApp.apk to prevent some issues like [INSTALL_FAILED_VERSION_DOWNGRADE]')
    parser.add_argument('-tip', '--tcp-ip',
                        help='Connects to a remote device via TCP mode.')
    parser.add_argument('-tp', '--tcp-port',
                        help='Port number to connect to. Default : 5555')
    parser.add_argument('-s', '--scrcpy', action='store_true',
                        help='Run ScrCpy to see and control Android device.')
    parser.add_argument('-to', '--tar-only', action='store_true',
                        help='Get entire WhatsApp\'s data in \"<username>.tar\" file instead of just getting few important files.')
    args = parser.parse_args()
    #args = parser.parse_args('--tcp-ip 192.168.43.130 --scrcpy'.split())

    is_allow_reboot = args.allow_reboot
    tcp_ip = args.tcp_ip
    tcp_port = args.tcp_port
    is_scrcpy = args.scrcpy
    is_tar_only = args.tar_only
    if(tcp_ip):
        if(not tcp_port):
            tcp_port = '5555'
        adb_serial_id = tcp_device_id.init(tcp_ip, tcp_port)
    else:
        adb_serial_id = device_id.init()
    if(not adb_serial_id):
        exit()

    # Global command line helpers
    tmp = 'tmp/'
    helpers = 'helpers/'
    if(is_windows):
        adb = 'bin\\adb.exe -s ' + adb_serial_id
    else:
        adb = 'adb -s ' + adb_serial_id

    with concurrent.futures.ThreadPoolExecutor() as executor:
        f1 = executor.submit(main)
        time.sleep(1)
        f2 = executor.submit(run_scrcpy, is_scrcpy)
