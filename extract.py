from termcolor import colored, cprint
import os
import platform

# Detect if Windows.
if platform.system() == 'Windows' : isWindows = True 

def main() :
    
    ShowBanner()
    CheckJAVA()
    TCPorUSB()

def ShowBanner() : 
    banner_path = 'non_essentials/banner.txt'
    banner = open(banner_path,'r')
    banner_content = banner.read()
    CustomPrint(banner_content, 'green', ['bold'])
    banner.close()
    CustomPrint('============ WhatsApp Key / Database Extrator on non-rooted Android ============', 'green', ['bold'])
    CustomPrint('\n================================================================================\n===     This script can extract your WhatsApp msgstore.db (non crypt12,      ===\n===   unencrypted file) and your \'key\' file from \'\\data\\data\\com.whatsapp\'   ===\n===  directory in Android 4.0+ device without root access. However you need  ===\n===   to have JAVA installed on your system in order to \'view the  extract\'. ===\n===  If you don\'t have JAVA installed then you can \'view extract\' later by   ===\n===   running \'view_extract.py\'. The idea is to install a \'Legacy WhatsApp\'  ===\n===       temporarily on your device in order to get the android backup      ===\n===     permission. You WILL NOT lose any data and your current WhatsApp     ===\n===   version will be installed after this process so don\'t panic and don\'t  ===\n=== stop this script while it\'s working. However if something fails you can  ===\n===    run \'restore_whatsapp.py\' and reinstall current WhatsApp or simply    ===\n=== update that from Google Play Store. But it\'s always a good idea to take  ===\n===  a backup. For that go to \'WhatsApp settings\\Chat Settings\\Chat Backup\'  ===\n===              here take a local bacakup. Prepare for Worst.               ===\n===                      Script by : Yuvraj Raghuvanshi                      ===\n===                      Github.com/YuvrajRaghuvanshiS                       ===\n================================================================================', 'green')

def CheckJAVA() : 
    # after checking if false returns
    pass

def TCPorUSB() : 
    pass

def CustomPrint(textToPrint, color, attr=[]) : 
    if(isWindows) : 
        print(textToPrint)
    else : 
        cprint(textToPrint, color, attrs=attr)


if __name__ == "__main__":
    main()