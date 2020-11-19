from os import system
from termcolor import colored, cprint
import os
import platform

# Detect OS
isWindows = False
isLinux = False
if platform.system() == 'Windows' : isWindows = True 
if platform.system() == 'Linux' : isLinux = True

def main() :
    
    ShowBanner()
    CheckJAVA()

def ShowBanner() : 
    banner_path = 'non_essentials/banner.txt'
    banner = open(banner_path,'r')
    banner_content = banner.read()
    CustomPrint(banner_content, 'green', ['bold'])
    banner.close()
    CustomPrint('============ WhatsApp Key / Database Extrator on non-rooted Android ============', 'green', ['bold'])
    CustomPrint('\n================================================================================\n===     This script can extract your WhatsApp msgstore.db (non crypt12,      ===\n===   unencrypted file) and your \'key\' file from \'\\data\\data\\com.whatsapp\'   ===\n===  directory in Android 4.0+ device without root access. However you need  ===\n===   to have JAVA installed on your system in order to \'view the  extract\'. ===\n===  If you don\'t have JAVA installed then you can \'view extract\' later by   ===\n===   running \'view_extract.py\'. The idea is to install a \'Legacy WhatsApp\'  ===\n===       temporarily on your device in order to get the android backup      ===\n===     permission. You WILL NOT lose any data and your current WhatsApp     ===\n===   version will be installed after this process so don\'t panic and don\'t  ===\n=== stop this script while it\'s working. However if something fails you can  ===\n===    run \'restore_whatsapp.py\' and reinstall current WhatsApp or simply    ===\n=== update that from Google Play Store. But it\'s always a good idea to take  ===\n===  a backup. For that go to \'WhatsApp settings\\Chat Settings\\Chat Backup\'  ===\n===              here take a local bacakup. Prepare for Worst.               ===\n===                      Script by : Yuvraj Raghuvanshi                      ===\n===                      Github.com/YuvrajRaghuvanshiS                       ===\n================================================================================', 'green')

def CheckJAVA() : 
    isJAVAInstalled = False
    # after checking if false returns
    noJAVAContinue = CustomInput('\nIt looks like you don\'t have JAVA installed on your system. Would you like to (C)ontinue with the process and \'view extract\' later? or (S)top? : ', 'green')
    if(noJAVAContinue=='c') : 
        CustomPrint('\nContinuing without JAVA, once JAVA is installed on system run \'view_extract.py\'', 'green')
        TCPorUSB()
    else : 
        CustomPrint('\nExiting...', 'green')
        quit()

def TCPorUSB() : 
    isTCP = CustomInput('\nUse (T)CP or (U)SB? : ', 'green')
    if(isTCP=='t') : TCPMode()
    else : USBMode()

def TCPMode() : 
    deviceIP = CustomInput('\nEnter IP address of target device : ', 'green')
    devicePort = CustomInput('\nEnter port number, leave empty for default : ', 'green')
    if(devicePort=='') : devicePort = '5555'
    CustomPrint(deviceIP,'green')
    CustomPrint(devicePort,'green')
    if(isLinux) : LinuxMode()

def USBMode() : 
    pass
    
def LinuxMode() : 
    CustomPrint('Installing dependencies for linux systems...', 'green')
    os.popen('sudo bash bin/linux_dependencies.sh')

def CustomPrint(textToPrint, color, attr=[]) : 
    if(isWindows) : 
        print(textToPrint)
    else : 
        cprint(textToPrint, color, attrs=attr)

def CustomInput(textToInput, color, attr=[]) : 
    if(isWindows) : 
        return input(textToInput).casefold()
    else : 
        return input(colored(textToInput, color, attrs=attr)).casefold()


if __name__ == "__main__":
    main()