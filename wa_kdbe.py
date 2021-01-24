from packaging.version import parse
import helpers.ADBDeviceSerialId as deviceId
import os
import subprocess
import platform
from helpers.CustomCI import CustomInput, CustomPrint
from view_extract import ExtractAB
from helpers.WIndowsUSB import WindowsUSB
from helpers.LinuxUSB import LinuxUSB
import re
import argparse

# Detect OS
isWindows = False
isLinux = False
if platform.system() == 'Windows' : isWindows = True 
if platform.system() == 'Linux' : isLinux = True

# Global Variables
appURLWhatsAppCDN = 'https://www.cdn.whatsapp.net/android/2.11.431/WhatsApp.apk'
appURLWhatsCryptCDN = 'https://whatcrypt.com/WhatsApp-2.11.431.apk'
isJAVAInstalled = False

def main() :
    os.system('cls' if os.name == 'nt' else 'clear')
    CheckBinIfWindows()
    ShowBanner()
    global isJAVAInstalled
    isJAVAInstalled = CheckJAVA()
    # TODO : use -y flag to assume readinstruction read automatically.
    readInstruction = CustomInput('Please read above instructions carefully. Continue? (default y) : ') or 'y'
    if(readInstruction.upper() == 'Y') : 
        USBMode()
    else : 
        Exit()

def BackupWhatsAppApk(SDKVersion, versionName, WhatsAppapkPath):
    os.system(adb + ' shell am force-stop com.whatsapp') if(SDKVersion > 11) else os.system(adb + ' shell am kill com.whatsapp')
    CustomPrint('Backing up WhatsApp ' + versionName + ' apk, the one installed on device to ' + tmp + 'WhatsAppbackup.apk')
    os.mkdir(tmp) if not (os.path.isdir(tmp)) else CustomPrint('Folder ' + tmp + ' already exists.')
    os.system(adb + ' pull ' + WhatsAppapkPath + ' ' + tmp + 'WhatsAppbackup.apk')
    CustomPrint('Apk backup complete.')

def BackupWhatsAppDataasAb(SDKVersion):
    CustomPrint('Backing up WhatsApp data as ' + tmp + 'whatsapp.ab. May take time, don\'t panic.')
    CustomPrint('Enter \'' + abPass + '\' as password when promted on device.', 'yellow')
    try : 
        os.system(adb + ' backup -f '+ tmp + 'whatsapp.ab com.whatsapp') if(SDKVersion >= 23) else os.system(adb + ' backup -f '+ tmp + 'whatsapp.ab -noapk com.whatsapp')
    except Exception as e : 
        CustomPrint(e)
    CustomPrint('Done backing up data.')

def CheckBinIfWindows() : 
    if (isWindows and not os.path.isdir('bin')) : 
        CustomPrint('I can not find bin folder, check again...', 'red')
        Exit()
    pass

def CheckJAVA() : 
    JAVAVersion = re.search('(?<=version ")(.*)(?=")', str(subprocess.check_output('java -version'.split(), stderr=subprocess.STDOUT))).group(1)
    isJAVAInstalled = True if(JAVAVersion) else False
    if (isJAVAInstalled) : 
        CustomPrint('Found Java installed on system.')
        return isJAVAInstalled
    else : 
        noJAVAContinue = CustomInput('It looks like you don\'t have JAVA installed on your system. Would you like to (C)ontinue with the process and \'view extract\' later? or (S)top? : ', 'red') or 'c'
        if(noJAVAContinue=='c') : 
            CustomPrint('Continuing without JAVA, once JAVA is installed on system run \'view_extract.py\'', 'yellow')
            return isJAVAInstalled
        else : 
            Exit()

def Exit():
    CustomPrint('\nExiting...')
    os.system('bin\\adb.exe kill-server') if(isWindows) else os.system('adb kill-server')
    quit()

def InstallLegacy(SDKVersion):
    CustomPrint("installing Legacy WhatsApp V2.11.431, hold tight now.")
    if(SDKVersion >= 17) :
        os.system(adb + ' install -r -d '+ helpers + 'LegacyWhatsApp.apk')
    else : 
        os.system(adb + ' install -r '+ helpers + 'LegacyWhatsApp.apk')
    CustomPrint('Installation Complete.')

def RealDeal(SDKVersion, WhatsAppapkPath, versionName) : 
    BackupWhatsAppApk(SDKVersion, versionName, WhatsAppapkPath)
    UninstallWhatsApp(SDKVersion)
    InstallLegacy(SDKVersion)
    BackupWhatsAppDataasAb(SDKVersion)
    ReinstallWhatsApp()
    CustomPrint('Our work with device has finished, it is safe to remove it now.', 'yellow')
    ExtractAB(isJAVAInstalled, abPass, userName, protectPass)

def ReinstallWhatsApp():
    CustomPrint('Reinstallting original WhatsApp.')
    try : 
        os.system(adb + ' install -r -d ' + tmp + 'WhatsAppbackup.apk')
    except Exception as e : 
        print(e)
        CustomPrint('Could not install WhatsApp, install by running \'restore_whatsapp.py\' or manually installing from Play Store.\nHowever if it crashes then you have to clear storage/clear data from settings => app settings => WhatsApp.')

def ShowBanner() : 
    banner_path = 'non_essentials/banner.txt'
    try : 
        banner = open(banner_path,'r')
        banner_content = banner.read()
        CustomPrint(banner_content, 'green', ['bold'])
        banner.close()
    except Exception as e : 
        CustomPrint(e)
    CustomPrint('============ WhatsApp Key / Database Extrator for non-rooted Android ============\n', 'green', ['bold'])
    intro_path = 'non_essentials/intro.txt'
    try : 
        intro = open(intro_path,'r')
        intro_content = intro.read()
        CustomPrint(intro_content, 'green', ['bold'])
        intro.close()
    except Exception as e : 
        CustomPrint(e)

def UninstallWhatsApp(SDKVersion):
    if(SDKVersion >= 23) :
        try : 
            CustomPrint('Uninstalling WhatsApp, skipping data.')
            os.system(adb + ' shell pm uninstall -k com.whatsapp')
            CustomPrint('Uninstalled.')
        except Exception as e : 
            CustomPrint('Could not uninstall WhatsApp.')
            CustomPrint(e)
            Exit()

def USBMode() : 
    if(isWindows) : 
        ACReturnCode, SDKVersion, WhatsAppapkPath, versionName = WindowsUSB(ADBSerialId)
        RealDeal(SDKVersion, WhatsAppapkPath, versionName) if ACReturnCode==1 else Exit()
    else : 
        ACReturnCode, SDKVersion, WhatsAppapkPath, versionName =  LinuxUSB(ADBSerialId)
        RealDeal(SDKVersion, WhatsAppapkPath, versionName) if ACReturnCode==1 else Exit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('abPass', help='Password for whatsapp.ab.')
    parser.add_argument('userName', help='Reference name of this user.')
    parser.add_argument('-p', '--protect', help='Password to compress database into encrypted archive format.')
    # parser.add_argument('-s', '--save', help='Save to log file.', action='store_true') TODO : add a logger later.

    # args=parser.parse_args('qqqq yuvraj -p 1234'.split())
    args = parser.parse_args()
    abPass = args.abPass
    userName = args.userName
    protectPass = args.protect
    
    ADBSerialId = deviceId.init()

    # Global command line helpers
    adb = 'bin\\adb.exe -s ' + ADBSerialId
    tmp = 'tmp/'
    grep = 'bin\\grep.exe'
    curl = 'bin\\curl.exe'
    helpers = 'helpers/'
    if(isLinux) : 
        adb = 'adb -s ' + ADBSerialId
        grep = 'grep'
        curl = 'curl'

    main()