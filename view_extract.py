import os
import platform
import re
import shutil
import subprocess

import protect
from helpers.CustomCI import CustomInput, CustomPrint

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
    ExtractAB(isJAVAInstalled, False)

def CheckJAVA() : 
    JAVAVersion = re.search('(?<=version ")(.*)(?=")', str(subprocess.check_output('java -version'.split(), stderr=subprocess.STDOUT))).group(1)
    isJAVAInstalled = True if(JAVAVersion) else False
    if (isJAVAInstalled) : 
        CustomPrint('Found Java installed on system. Continuing...')
        return isJAVAInstalled
    else : 
        noJAVAContinue = CustomInput('It looks like you don\'t have JAVA installed on your system. Would you like to (C)ontinue with the process and \'view extract\' later? or (S)top? : ', 'red') or 'c'
        if(noJAVAContinue.upper() == 'C') : 
            CustomPrint('Continuing without JAVA, once JAVA is installed on system run \'view_extract.py\'', 'yellow')
            return isJAVAInstalled
        else : 
            Exit()

def CleanTmp() :
        if(os.path.isdir(tmp)) : 
            CustomPrint('Cleaning up tmp folder...','yellow')
            shutil.rmtree(tmp)
def Exit():
    CustomPrint('\nExiting...')
    os.system('bin\\adb.exe kill-server') if(isWindows) else os.system('adb kill-server')
    quit()

def ExtractAB(isJAVAInstalled, callingFromOtherModule = True) :
    if not (isJAVAInstalled) : 
        CustomPrint('Can not detect JAVA on system.')
        # move whatsapp.ab from tmp to user specified folder.
        userName = CustomInput('Enter a name for this user. : ')
        os.mkdir(extracted) if not (os.path.isdir(extracted)) else CustomPrint('Folder ' + extracted + 'already exists.','yellow')
        os.mkdir(extracted + userName) if not (os.path.isdir(extracted + userName)) else CustomPrint('Folder ' + extracted + userName + ' exists.')
        os.rename(tmp + 'whatsapp.ab', extracted + userName + '/whatsapp.ab')
        CustomPrint('Moved whatsapp.ab to ' + extracted + userName + ' folder. Run view_extract.py after installing Java on system.')
        Exit()
    if(not callingFromOtherModule) : 
        if(CustomInput('Have you already made whatsapp.ab and just extracting it now ? : ').upper()=='y'.upper()) : 
            userName = CustomInput('Enter name for this user (same as before.) : ') or 'user'
            abPass = CustomInput('Enter same password which you entered on device when prompted earlier. : ')
            if(os.path.isfile(extracted + userName + '/whatsapp.ab')) : 
                try : 
                    os.system('java -jar ' + bin + 'abe.jar unpack ' + extracted + userName + '/whatsapp.ab ' + tmp + 'whatsapp.tar ' + str(abPass))
                    CustomPrint('Successfully \'fluffed\' '+ extracted + userName + '/whatsapp.ab ' + tmp + 'whatsapp.tar ')
                    TakingOutMainFiles(userName)
                except Exception as e : 
                    CustomPrint(e)
            else : 
                CustomPrint('Could not find whatsapp.ab in ' + extracted + userName + ' folder, did you name your user properly?')
                Exit()
    if(os.path.isfile(tmp + 'whatsapp.ab')) :
        CustomPrint('Found whatsapp.ab in tmp folder. Continuing')
        userName = CustomInput('Enter a reference name for this user. : ') or 'user'
        abPass = CustomInput('Enter same password which you entered on device when prompted earlier. : ')
        try : 
            os.system('java -jar ' + bin + 'abe.jar unpack ' + tmp + 'whatsapp.ab ' + tmp + 'whatsapp.tar ' + str(abPass))
            CustomPrint('Successfully \'fluffed\' '+ tmp + 'whatsapp.ab ' + tmp + 'whatsapp.tar ')
            TakingOutMainFiles(userName)
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
    CustomPrint('============ WhatsApp Key / Database Extrator for non-rooted Android ===========\n', 'green', ['bold'])
    
def TakingOutMainFiles(userName) : 
    os.mkdir(extracted) if not (os.path.isdir(extracted)) else CustomPrint('Folder ' + extracted + 'already exists.','yellow')
    os.mkdir(extracted + userName) if not (os.path.isdir(extracted + userName)) else CustomPrint('Folder already exists.', 'yellow')
    CustomPrint('Taking out main files in ' + tmp + ' folder temporaily.')
    try : 
        bin = '' if(isLinux) else 'bin\\'
        os.system(bin + tar + ' xvf ' + tmp + 'whatsapp.tar -C ' + tmp + ' apps/com.whatsapp/f/key') ; os.replace('tmp/apps/com.whatsapp/f/key', extracted + userName + '/key')
        os.system(bin + tar + ' xvf ' + tmp + 'whatsapp.tar -C ' + tmp + ' apps/com.whatsapp/db/msgstore.db') ; os.replace('tmp/apps/com.whatsapp/db/msgstore.db', extracted + userName + '/msgstore.db')
        os.system(bin + tar + ' xvf ' + tmp + 'whatsapp.tar -C ' + tmp + ' apps/com.whatsapp/db/wa.db') ; os.replace('tmp/apps/com.whatsapp/db/wa.db', extracted + userName + '/wa.db')
        os.system(bin + tar + ' xvf ' + tmp + 'whatsapp.tar -C ' + tmp + ' apps/com.whatsapp/db/axolotl.db') ; os.replace('tmp/apps/com.whatsapp/db/axolotl.db' , extracted + userName + '/axolotl.db')
        os.system(bin + tar + ' xvf ' + tmp + 'whatsapp.tar -C ' + tmp + ' apps/com.whatsapp/db/chatsettings.db') ; os.replace('tmp/apps/com.whatsapp/db/chatsettings.db', extracted + userName + '/chatsettings.db')
        
        CleanTmp()
        
        CustomPrint('You should not leave these extracted database and other files hanging in folder, it is very insecure.')
        createArchive = CustomInput('Would you like to create a password protected archive? (default y) : ') or 'y'
        if(createArchive.upper() == 'Y') : 
            CustomPrint('\nNow an archive will be created in extracted folder and original files will be deleted. To later \'un-archive\' and access these files you need to run \'python protect.py\' from root directory of this project.','yellow')
            protect.Compress(userName)
        else : 
            CustomPrint('\a\nYour whatsapp database along with other files is in ' + extracted + userName + ' folder.\n','yellow')
            try : # Open in explorer.
                if(isWindows) : 
                    os.startfile(os.path.realpath(extracted + userName))
                else : 
                    os.system('xdg-open ' + os.path.realpath(extracted + userName))
            except Exception as e : 
                pass

    except Exception as e : 
        CustomPrint(e)
        CleanTmp()

if __name__ == "__main__":
    main()
