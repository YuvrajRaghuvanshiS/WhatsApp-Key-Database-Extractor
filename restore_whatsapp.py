import argparse
import os
import platform

import helpers.ADBDeviceSerialId as deviceId
import helpers.TCPDeviceSerialId as tcpDeviceId
from helpers.CustomCI import CustomPrint

# Detect OS
isWindows = False
isLinux = False
if platform.system() == 'Windows':
    isWindows = True
if platform.system() == 'Linux':
    isLinux = True

# Global command line helpers
adb = 'bin\\adb.exe -s '
tmp = 'tmp/'
if(isLinux):
    adb = 'adb -s '


def ReinstallWhatsApp(ADBSerialId):
    CustomPrint('Reinstallting original WhatsApp.')
    if(os.path.isfile(tmp + 'WhatsAppbackup.apk')):
        try:
            os.system(adb + ADBSerialId + ' install -r -d ' +
                      tmp + 'WhatsAppbackup.apk')
        except Exception as e:
            print(e)
            CustomPrint('Could not restore WhatsApp, install from Play Store.\nHowever if it crashes then you have to clear storage/clear data from settings => app settings => WhatsApp.')
    else:
        CustomPrint('Could not find backup APK, install from play store.\nHowever if it crashes then you have to clear storage/clear data from settings => app settings => WhatsApp.', 'red')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--tcp-ip', help='Connects to a remote device via TCP mode.')
    parser.add_argument(
        '--tcp-port', help='Port number to connect to. Default : 5555')
    args = parser.parse_args()
    # args = parser.parse_args(['--allow-reboot --tcp-ip 192.168.43.130'.split())

    tcpIP = args.tcp_ip
    tcpPort = args.tcp_port
    if(tcpIP):
        ADBSerialId = tcpDeviceId.init(tcpIP, tcpPort)
    else:
        ADBSerialId = deviceId.init()
    if(not ADBSerialId):
        quit()
    ReinstallWhatsApp(ADBSerialId)
