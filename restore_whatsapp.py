import argparse
import datetime
import os
import platform
import subprocess

import helpers.adb_device_serial_id as adb_device_id
import helpers.tcp_device_serial_id as tcp_device_id
from helpers.custom_ci import custom_input, custom_print

# Detect OS
is_windows = False
is_linux = False
if platform.system() == 'Windows':
    is_windows = True
if platform.system() == 'Linux':
    is_linux = True


def kill_me():
    custom_print('\n', is_get_time=False)
    custom_print('Exiting...')
    os.system(
        'bin\\adb.exe kill-server') if(is_windows) else os.system('adb kill-server')
    custom_input('Hit \"Enter\" key to continue....', 'cyan')
    quit()


def reinstall_whatsapp(adb):
    custom_print('Reinstallting original WhatsApp.')
    if('/data/local/tmp/WhatsAppbackup.apk' in subprocess.getoutput('adb shell ls /data/local/tmp/WhatsAppbackup.apk')):
        try:
            reinstall_whatsapp_out = subprocess.getoutput(
                adb + ' shell pm install /data/local/tmp/WhatsAppbackup.apk')
            if('Success' in reinstall_whatsapp_out):
                custom_print('Reinstallation Complete.')
            else:
                custom_print('Could not install WhatsApp, install by running \"restore_whatsapp.py\" or manually installing from Play Store.\nHowever if it crashes then you have to clear storage/clear data from \"Settings \u2192 App Settings \u2192 WhatsApp\".', 'red')
                custom_print(reinstall_whatsapp_out, 'red')

        except Exception as e:
            custom_print(e, 'red')
            kill_me()
    else:
        custom_print('Could not find backup APK, install from play store.\nHowever if it crashes then you have to clear storage/clear data from \"Settings \u2192 App Settings \u2192 WhatsApp\".', 'red')
        kill_me()


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
    custom_print('============ WhatsApp Key / Database Extrator for non-rooted Android ===========\n',
                 'green', ['bold'], False)


if __name__ == "__main__":

    custom_print('\n\n\n====== Logging start here. ====== \nFile: ' + os.path.basename(__file__) + '\nDate: ' +
                 str(datetime.datetime.now()) + '\nIf you see any password here then do let know @github.com/YuvrajRaghuvanshiS/WhatsApp-Key-Database-Extractor\n\n\n', is_get_time=False, is_print=False)
    os.system('cls' if os.name == 'nt' else 'clear')

    parser = argparse.ArgumentParser()
    parser.add_argument('-tip',
                        '--tcp-ip', help='Connects to a remote device via TCP mode.')
    parser.add_argument('-tp',
                        '--tcp-port', help='Port number to connect to. Default: 5555')
    args = parser.parse_args()
    # args = parser.parse_args('--tcp-ip 192.168.43.130'.split())

    tcp_ip = args.tcp_ip
    tcp_port = args.tcp_port
    if(tcp_ip):
        if(not tcp_port):
            tcp_port = '5555'
        adb_device_serial_id = tcp_device_id.init(tcp_ip, tcp_port)
    else:
        adb_device_serial_id = adb_device_id.init()
    if(not adb_device_serial_id):
        kill_me()

    # Global command line helpers
    helpers = 'helpers/'
    if(is_windows):
        adb = 'bin\\adb.exe -s ' + adb_device_serial_id
    else:
        adb = 'adb -s ' + adb_device_serial_id

    os.system('cls' if os.name == 'nt' else 'clear')
    show_banner()
    reinstall_whatsapp(adb)
