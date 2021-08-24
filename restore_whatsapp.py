import argparse
import os
import platform

import helpers.adb_device_serial_id as deviceId
import helpers.tcp_device_serial_id as tcpDeviceId
from helpers.custom_ci import custom_print, custom_input

# Detect OS
is_windows = False
is_linux = False
if platform.system() == 'Windows':
    is_windows = True
if platform.system() == 'Linux':
    is_linux = True


def exit():
    print('\n')
    custom_print('Exiting...')
    os.system(
        'bin\\adb.exe kill-server') if(is_windows) else os.system('adb kill-server')
    custom_input('Hit \"Enter\" key to continue....', 'cyan')
    quit()


def reinstall_whatsapp(adb):
    custom_print('Reinstallting original WhatsApp.')
    if(os.path.isfile(helpers + 'WhatsAppbackup.apk')):
        try:
            os.system(adb + ' install -r -d ' +
                      helpers + 'WhatsAppbackup.apk')
            custom_input('Hit \"Enter\" key to continue.')
        except Exception as e:
            custom_print(e, 'red')
            custom_print('Could not restore WhatsApp, install from Play Store.\nHowever if it crashes then you have to clear storage/clear data from \"Settings \u2192 App Settings \u2192 WhatsApp\".', 'red')
            exit()
    else:
        custom_print('Could not find backup APK, install from play store.\nHowever if it crashes then you have to clear storage/clear data from \"Settings \u2192 App Settings \u2192 WhatsApp\".', 'red')
        exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-tip',
                        '--tcp-ip', help='Connects to a remote device via TCP mode.')
    parser.add_argument('-tp',
                        '--tcp-port', help='Port number to connect to. Default : 5555')
    args = parser.parse_args()
    #args = parser.parse_args('--tcp-ip 192.168.43.130'.split())

    tcp_ip = args.tcp_ip
    tcp_port = args.tcp_port
    if(tcp_ip):
        if(not tcp_port):
            tcp_port = '5555'
        adb_serial_id = tcpDeviceId.init(tcp_ip, tcp_port)
    else:
        adb_serial_id = deviceId.init()
    if(not adb_serial_id):
        exit()

    # Global command line helpers
    helpers = 'helpers/'
    if(is_windows):
        adb = 'bin\\adb.exe -s ' + adb_serial_id
    else:
        adb = 'adb -s ' + adb_serial_id

    reinstall_whatsapp(adb)
