import argparse
import shutil
from helpers.CustomCI import CustomInput, CustomPrint
import os
import subprocess
import platform
import re
import protect


# Detect OS
isWindows = False
isLinux = False
if platform.system() == 'Windows' : isWindows = True 
if platform.system() == 'Linux' : isLinux = True

# Global variables
isJAVAInstalled = False

# Global command line helpers
adb = 'bin\\adb.exe'
tmp = 'tmp/'
grep = 'bin\\grep.exe'
curl = 'bin\\curl.exe'
helpers = 'helpers/'
bin = 'bin/'
extracted = 'extracted/'
tar = 'tar.exe'
if(isLinux) : 
    adb = 'adb'
    grep = 'grep'
    curl = 'curl'
    tar = 'tar'


def main() : 
    os.system('cls' if os.name == 'nt' else 'clear')
    ShowBanner()
    global isJAVAInstalled
    isJAVAInstalled = CheckJAVA()
    ExtractAB(isJAVAInstalled, abPass, userName, protectPass, False)

def CheckJAVA() : 
    JAVAVersion = re.search('(?<=version ")(.*)(?=")', str(subprocess.check_output('java -version'.split(), stderr=subprocess.STDOUT))).group(1)
    isJAVAInstalled = True if(JAVAVersion) else False
    if (isJAVAInstalled) : 
        CustomPrint('Found Java installed on system. Continuing...')
        return isJAVAInstalled
    else : 
        noJAVAContinue = CustomInput('It looks like you don\'t have JAVA installed on your system. Would you like to (C)ontinue with the process and \'view extract\' later? or (S)top? : ', 'red') or 'c'
        if(noJAVAContinue=='c') : 
            CustomPrint('Continuing without JAVA, once JAVA is installed on system run \'view_extract.py\'', 'yellow')
            return isJAVAInstalled
        else : 
            Exit()

def CleanTmp() :
        if(os.path.isdir(tmp)) : 
            CustomPrint('Cleaning up tmp folder...')
            shutil.rmtree(tmp)

def Exit():
    CustomPrint('\nExiting...')
    os.system('bin\\adb.exe kill-server') if(isWindows) else os.system('adb kill-server')
    quit()

def ExtractAB(isJAVAInstalled, abPass, userName, protectPass, callingFromOtherModule = True) :
    if not (isJAVAInstalled) : 
        CustomPrint('Can not detect JAVA on system.')
        os.mkdir(extracted + userName) if not (os.path.isdir(extracted + userName)) else CustomPrint('Folder ' + extracted + userName + ' exists.')
        os.rename(tmp + 'whatsapp.ab', extracted + userName + '/whatsapp.ab')
        CustomPrint('Moved whatsapp.ab to ' + extracted + userName + ' folder. Run view_extract.py after installing Java on system.')
        Exit()
    if(not callingFromOtherModule) : 
        if(CustomInput('Have you already made whatsapp.ab and just extracting it now ? : ').upper() == 'Y') : 
            if(os.path.isfile(extracted + userName + '/whatsapp.ab')) : 
                try : 
                    CustomPrint('Fluffing whatsapp.ab file, may take some time. Be patient.')
                    os.system('java -jar ' + bin + 'abe.jar unpack ' + extracted + userName + '/whatsapp.ab ' + tmp + 'whatsapp.tar ' + str(abPass))
                    CustomPrint('Successfully \'fluffed\' '+ extracted + userName + '/whatsapp.ab ' + tmp + 'whatsapp.tar ')
                    TakingOutMainFiles(userName, protectPass)
                except Exception as e : 
                    CustomPrint(e)
            else : 
                CustomPrint('Could not find whatsapp.ab in ' + extracted + userName + ' folder, did you name your user properly?')
                CustomPrint('May be that \'whatsapp.ab\' file is still in ' + tmp +' folder. Enter \'n\' next time.')
                Exit()
    if(os.path.isfile(tmp + 'whatsapp.ab')) :
        CustomPrint('Found whatsapp.ab in tmp folder. Continuing')
        try : 
            CustomPrint('Fluffing whatsapp.ab file, may take some time. Be patient.')
            os.system('java -jar ' + bin + 'abe.jar unpack ' + tmp + 'whatsapp.ab ' + tmp + 'whatsapp.tar ' + str(abPass))
            CustomPrint('Successfully \'fluffed\' '+ tmp + 'whatsapp.ab to ' + tmp + 'whatsapp.tar ')
            TakingOutMainFiles(userName, protectPass)
        except Exception as e : 
            CustomPrint(e)

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
    
def TakingOutMainFiles(userName, protectPass) : 
    os.mkdir(extracted + userName) if not (os.path.isdir(extracted + userName)) else CustomPrint('Folder already exists.')
    CustomPrint('Taking out main files in ' + tmp + ' folder temporaily.')
    try : 
        bin = '' if(isLinux) else 'bin\\'
        os.system(bin + tar + ' xvf ' + tmp + 'whatsapp.tar -C ' + tmp + ' apps/com.whatsapp/f/key') ; os.replace('tmp/apps/com.whatsapp/f/key', extracted + userName + '/key')
        os.system(bin + tar + ' xvf ' + tmp + 'whatsapp.tar -C ' + tmp + ' apps/com.whatsapp/db/msgstore.db') ; os.replace('tmp/apps/com.whatsapp/db/msgstore.db', extracted + userName + '/msgstore.db')
        os.system(bin + tar + ' xvf ' + tmp + 'whatsapp.tar -C ' + tmp + ' apps/com.whatsapp/db/wa.db') ; os.replace('tmp/apps/com.whatsapp/db/wa.db', extracted + userName + '/wa.db')
        os.system(bin + tar + ' xvf ' + tmp + 'whatsapp.tar -C ' + tmp + ' apps/com.whatsapp/db/axolotl.db') ; os.replace('tmp/apps/com.whatsapp/db/axolotl.db' , extracted + userName + '/axolotl.db')
        os.system(bin + tar + ' xvf ' + tmp + 'whatsapp.tar -C ' + tmp + ' apps/com.whatsapp/db/chatsettings.db') ; os.replace('tmp/apps/com.whatsapp/db/chatsettings.db', extracted + userName + '/chatsettings.db')
        
        # TODO : use -y flag to cleantmp automatically.
        CustomPrint('\nIf you do not see any errors in above lines in extracting/fluffing whatsapp.ab you SHOULD choose to clean temporary folder. It contains your chats in UN-ENCRYPTED format.','yellow')
        _cleanTemp = CustomInput('Would you like to clean tmp folder? (default y) : ') or 'y'
        if(_cleanTemp.upper() == 'Y') : 
            CleanTmp()
        
        if(protectPass) : 
            CustomPrint('Now an archive will be created in extracted folder with password \'' + protectPass + '\' and original files will be deleted. To later \'un-archive\' and access these files you need to run \'python protect.py\' from root directory of this project.', 'yellow')
            protect.Compress(userName, protectPass)

    except Exception as e : 
        CustomPrint(e)
        CleanTmp()

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
    main()