import argparse
import datetime
import os
import platform

import helpers.ADBDeviceSerialId as deviceId
import helpers.TCPDeviceSerialId as tcpDeviceId
from helpers.CustomCI import CustomInput, CustomPrint

# Detect OS
isWindows = False
isLinux = False
if platform.system() == 'Windows':
    isWindows = True
if platform.system() == 'Linux':
    isLinux = True


def Exit():
    print('\n')
    CustomPrint('Exiting...')
    os.system(
        'bin\\adb.exe kill-server') if(isWindows) else os.system('adb kill-server')
    CustomInput('Hit \"Enter\" key to continue....', 'cyan')
    quit()


def ReinstallWhatsApp(adb):
    CustomPrint('Reinstallting original WhatsApp.')
    if(os.path.isfile(helpers + 'WhatsAppbackup.apk')):
        try:
            os.system(adb + ' install -r -d ' +
                      helpers + 'WhatsAppbackup.apk')
        except Exception as e:
            CustomPrint(e, 'red')
            CustomPrint('Could not restore WhatsApp, install from Play Store.\nHowever if it crashes then you have to clear storage/clear data from \"Settings \u2192 App Settings \u2192 WhatsApp\".', 'red')
            Exit()
    else:
        CustomPrint('Could not find backup APK, install from play store.\nHowever if it crashes then you have to clear storage/clear data from \"Settings \u2192 App Settings \u2192 WhatsApp\".', 'red')
        Exit()


if __name__ == "__main__":

    CustomPrint('\n\n\n====== Logging start here. ====== \nFile: ' + os.path.basename(__file__) + '\nDate: ' +
                str(datetime.datetime.now()) + '\nIf you see any password here then do let know @github.com/YuvrajRaghuvanshiS/WhatsApp-Key-Database-Extractor\n\n\n', is_get_time=False, is_print=False)
    os.system('cls' if os.name == 'nt' else 'clear')

    parser = argparse.ArgumentParser()
    parser.add_argument('-tip',
                        '--tcp-ip', help='Connects to a remote device via TCP mode.')
    parser.add_argument('-tp',
                        '--tcp-port', help='Port number to connect to. Default: 5555')
    args = parser.parse_args()
    #args = parser.parse_args('--tcp-ip 192.168.43.130'.split())

    tcpIP = args.tcp_ip
    tcpPort = args.tcp_port
    if(tcpIP):
        if(not tcpPort):
            tcpPort = '5555'
        ADBSerialId = tcpDeviceId.init(tcpIP, tcpPort)
    else:
        ADBSerialId = deviceId.init()
    if(not ADBSerialId):
        Exit()

    # Global command line helpers
    helpers = 'helpers/'
    if(isWindows):
        adb = 'bin\\adb.exe -s ' + ADBSerialId
    else:
        adb = 'adb -s ' + ADBSerialId

    ReinstallWhatsApp(adb)
