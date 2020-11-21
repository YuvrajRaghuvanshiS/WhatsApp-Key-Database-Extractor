import os
from packaging.version import Version
from termcolor import colored, cprint
import subprocess
from subprocess import check_output
import platform
import re
from packaging import version
import wget
from helpers.CustomCI import CustomInput, CustomPrint
from extract_backup import ExtractAB

# Detect OS
isWindows = False
isLinux = False
if platform.system() == 'Windows' : isWindows = True 
if platform.system() == 'Linux' : isLinux = True

# Global Variables
SDKVersion = ''
WhatsAppapkPath = ''
SDPath = '' # Internal storage.
versionName = ''
contentLength = '' # To check if APK even exists at a given path to download!
appURLWhatsAppCDN = 'https://www.cdn.whatsapp.net/android/2.11.431/WhatsApp.apk'
appURLWhatsCryptCDN = 'https://whatcrypt.com/WhatsApp-2.11.431.apk'

# Global command line helpers
adb = 'bin\\adb.exe'
delete = 'del'
tmp = 'tmp\\'
confirmDelete = '/q'
grep = 'bin\\grep.exe'
curl = 'bin\\curl.exe'
helpers = 'helpers\\'
if(isLinux) : 
    adb = 'adb'
    delete = 'rm -rf'
    tmp = 'tmp/'
    confirmDelete = ''
    grep = 'grep'
    curl = 'curl'
    helpers = 'helpers/'

def main() :
    CheckBinIfWindows()
    ShowBanner()
    CheckJAVA()

def AfterConnect() : 
    SDKVersion = int(re.search('[0-9]{2,3}', str(check_output(adb +' shell getprop ro.build.version.sdk'))).group(0))
    if (SDKVersion <= 13) : 
        CustomPrint('Unsupported device. This method only works on Android v4.0 or higer.', 'green')
        CustomPrint('Cleaning up temporary direcory.', 'green')
        os.system(delete + ' ' + confirmDelete + ' '  + tmp + '*')
        Exit()
    WhatsAppapkPath = re.search('(?<=package:)(.*)(?=apk)', str(check_output(adb + ' shell pm path com.whatsapp'))).group(1) + 'apk'
    if not (WhatsAppapkPath) : CustomPrint('Looks like WhatsApp is not installed on device.') ; Exit()
    SDPath = re.search("(?<=b')(.*)(?=\\\\r)", str(check_output(adb + ' shell "echo $EXTERNAL_STORAGE"'))).group(1)
    contentLength = int(re.search("(?<=Content-Length:)(.*[0-9])(?=)", str(check_output(curl + ' -sI http://www.cdn.whatsapp.net/android/2.11.431/WhatsApp.apk'))).group(1))
    downloadAppFrom = appURLWhatsAppCDN if(contentLength == 18329558) else appURLWhatsCryptCDN
    versionName = re.search("(?<=versionName=)(.*?)(?=\\\\r)", str(check_output(adb + ' shell dumpsys package com.whatsapp'))).group(1)
    CustomPrint('WhatsApp V' + versionName + ' installed on device')
    if (version.parse(versionName) > version.parse('2.11.431')) :
        if not (os.path.isfile(helpers + 'LegacyWhatsApp.apk')) : 
            CustomPrint('Downloading legacy WhatsApp V2.11.431 to helpers folder')
            wget.download(downloadAppFrom, helpers + 'LegacyWhatsApp.apk')
        else : 
            CustomPrint('Found legacy WhatsApp V2.11.431 apk in ' + helpers + ' folder')
        
        BackupWhatsAppApk(SDKVersion, versionName, WhatsAppapkPath)
        UninstallWhatsApp(SDKVersion)
        InstallLegacy(SDKVersion)
        BackupWhatsAppDataasAb(SDKVersion)
        ReinstallWhatsApp()
        CustomPrint('Our work with device has finished, it is safe to remove it now.')
        ExtractAB()

def BackupWhatsAppApk(SDKVersion, versionName, WhatsAppapkPath):
    os.system(adb + ' shell am force-stop com.whatsapp') if(SDKVersion > 11) else os.system(adb + ' shell am kill com.whatsapp')
    CustomPrint('Backing up WhatsApp ' + versionName + ' apk, the one installed on device to ' + tmp + 'WhatsAppbackup.apk')
    os.system(adb + ' pull ' + WhatsAppapkPath + ' ' + tmp + 'WhatsAppbackup.apk')
    CustomPrint('Apk backup complete.')

def BackupWhatsAppDataasAb(SDKVersion):
    CustomPrint('Backing up WhatsApp data as ' + tmp + 'whatsapp.ab. May take time, don\'t panic.')
    try : 
        os.system(adb + ' backup -f '+ tmp + 'whatsapp.ab com.whatsapp') if(SDKVersion >= 23) else os.system(adb + ' backup -f '+ tmp + 'whatsapp.ab -noapk com.whatsapp')
    except Exception as e : 
        CustomPrint(e)
    CustomPrint('Done backing up data.')

def CheckBinIfWindows() : 
    if (isWindows and not os.path.isdir('bin')) : 
        CustomPrint('I can not find bin folder, check again...', 'green')
        Exit()
    pass

def CheckJAVA() : 
    isJAVAInstalled = False
    # after checking if false returns
    noJAVAContinue = CustomInput('It looks like you don\'t have JAVA installed on your system. Would you like to (C)ontinue with the process and \'view extract\' later? or (S)top? : ', 'green') or 'c'
    if(noJAVAContinue=='c') : 
        CustomPrint('Continuing without JAVA, once JAVA is installed on system run \'view_extract.py\'', 'green')
        TCPorUSB()
    else : 
        Exit()

def Exit():
    CustomPrint('\nExiting...', 'green')
    os.system('bin\\adb.exe kill-server')
    quit()

def InstallLegacy(SDKVersion):
    CustomPrint("installing Legacy WhatsApp V2.11.431, hold tight now.")
    if(SDKVersion >= 17) :
        os.system(adb + ' install -r -d '+ helpers + 'LegacyWhatsApp.apk')
    else : 
        os.system(adb + ' install -r '+ helpers + 'LegacyWhatsApp.apk')
    CustomPrint('Installation Complete.')

def LinuxBashDependencies():
    CustomPrint('Installing dependencies (if not already installed)...', 'green')
    bashCommand = "bash bin/linux_dependencies.sh"
    # could use os.system but that would affect error output
    # and ye har bar na chle installing dependenciess iska bhi kuch krkna h
    try : 
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    except Exception as e : 
        CustomPrint(e)
        Exit()
    output, error = process.communicate()
    if(error!=None) : 
        CustomPrint(error,'red')
        Exit()
    CustomPrint(output, 'green')

def LinuxTCP(deviceIP, devicePort) : 
    LinuxBashDependencies()
    CustomPrint('Connecting to device', 'green')
    try : 
        os.system(adb + ' kill-server')
        os.system(adb + ' connect ' + deviceIP + ':' + devicePort)
        os.system(adb + ' wait-for-device')
    except Exception as e : 
        CustomPrint(e)
        Exit()
    deviceName= adb + ' shell getprop ro.product.model'
    CustomPrint('Connected to ' + re.search("(?<=b')(.*)(?=\\\\r)", str(check_output(deviceName))).group(1) , 'green')
    AfterConnect()

def LinuxUSB() : 
    LinuxBashDependencies()
    try : 
        os.system(adb + ' kill-server')
        os.system(adb + ' start-server')
        CustomPrint('Plug device via USB now..', 'green')
        os.system(adb + ' wait-for-device')
    except Exception as e : 
        CustomPrint(e)
        Exit()
    deviceName= adb + ' shell getprop ro.product.model'
    CustomPrint('Connected to ' + re.search("(?<=b')(.*)(?=\\\\r)", str(check_output(deviceName))).group(1) , 'green')
    AfterConnect()

def ReinstallWhatsApp():
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
    CustomPrint('============ WhatsApp Key / Database Extrator on non-rooted Android ============', 'green', ['bold'])
    CustomPrint('\n================================================================================\n===     This script can extract your WhatsApp msgstore.db (non crypt12,      ===\n===   unencrypted file) and your \'key\' file from \'\\data\\data\\com.whatsapp\'   ===\n===  directory in Android 4.0+ device without root access. However you need  ===\n===   to have JAVA installed on your system in order to \'view the  extract\'. ===\n===  If you don\'t have JAVA installed then you can \'view extract\' later by   ===\n===   running \'view_extract.py\'. The idea is to install a \'Legacy WhatsApp\'  ===\n===       temporarily on your device in order to get the android backup      ===\n===     permission. You WILL NOT lose any data and your current WhatsApp     ===\n===   version will be installed after this process so don\'t panic and don\'t  ===\n=== stop this script while it\'s working. However if something fails you can  ===\n===    run \'restore_whatsapp.py\' and reinstall current WhatsApp or simply    ===\n=== update that from Google Play Store. But it\'s always a good idea to take  ===\n===  a backup. For that go to \'WhatsApp settings\\Chat Settings\\Chat Backup\'  ===\n===              here take a local bacakup. Prepare for Worst.               ===\n===                                                                          ===\n===                      Script by : Yuvraj Raghuvanshi                      ===\n===                      Github.com/YuvrajRaghuvanshiS                       ===\n================================================================================', 'green')

def TCPMode() : 
    deviceIP = CustomInput('Enter IP address of target device : ', 'green')
    devicePort = CustomInput('Enter port number, leave empty for default (5555) : ', 'green')
    if(devicePort=='') : devicePort = '5555'
    if(isLinux) : LinuxTCP(deviceIP, devicePort)
    else : WindowsTCP(deviceIP, devicePort)

def TCPorUSB() : 
    connectionMode = CustomInput('Use (T)CP or (U)SB? : ', 'green') or 'u'
    if(connectionMode=='t') : TCPMode()
    else : USBMode()

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
    if(isWindows) : WindowsUSB()
    else : LinuxUSB()  

def WindowsTCP(deviceIP, devicePort) : 
    CustomPrint('Connecting to device', 'green')
    try : 
        os.system(adb + ' kill-server')
        os.system(adb + ' connect ' + deviceIP + ':' + devicePort)
        os.system(adb + ' wait-for-device')
    except Exception as e : 
        CustomPrint(e)
        Exit()
    deviceName= adb + ' shell getprop ro.product.model'
    CustomPrint('Connected to ' + re.search("(?<=b')(.*)(?=\\\\r)", str(check_output(deviceName))).group(1) , 'green')
    AfterConnect()

def WindowsUSB() : 
    try : 
        os.system(adb + ' kill-server')
        os.system(adb + ' start-server')
        CustomPrint('Plug device via USB now..', 'green')
        os.system(adb + ' wait-for-device')
    except Exception as e : 
        CustomPrint(e)
        Exit()
    deviceName= adb + ' shell getprop ro.product.model'
    CustomPrint('Connected to ' + re.search("(?<=b')(.*)(?=\\\\r)", str(check_output(deviceName))).group(1) , 'green')
    AfterConnect()

if __name__ == "__main__":
    main()