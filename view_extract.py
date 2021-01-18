from helpers.CustomCI import CustomInput, CustomPrint
import os
import subprocess
import re

# Global variables
isJAVAInstalled = False

# Global command line helpers
adb = 'adb'
delete = 'rm -rf'
tmp = 'tmp/'
confirmDelete = ''
grep = 'grep'
curl = 'curl'
helpers = 'helpers/'
bin = 'bin/'
tar = 'tar'
extracted = 'extracted/'

def main() : 
    os.system('clear')
    ShowBanner()
    global isJAVAInstalled
    isJAVAInstalled = CheckJAVA()
    ExtractAB(isJAVAInstalled)

def CheckJAVA() : 
    JAVAVersion = re.search('(?<=version ")(.*)(?=")', str(subprocess.check_output('java -version'.split(), stderr=subprocess.STDOUT))).group(1)
    isJAVAInstalled = True if(JAVAVersion) else False
    if (isJAVAInstalled) : 
        CustomPrint('Found Java installed on system. Continuing...')
        return isJAVAInstalled
    else : 
        noJAVAContinue = CustomInput('It looks like you don\'t have JAVA installed on your system. Would you like to (C)ontinue with the process and \'view extract\' later? or (S)top? : ', 'green') or 'c'
        if(noJAVAContinue=='c') : 
            CustomPrint('Continuing without JAVA, once JAVA is installed on system run \'view_extract.py\'', 'green')
            return isJAVAInstalled
        else : 
            Exit()

def CleanTmp() :
        if(os.path.isdir(tmp)) : 
            CustomPrint('Cleaning up tmp folder...')
            os.remove('tmp/whatsapp.tar')
            os.remove('tmp/whatsapp.ab')
            #os.remove('tmp\WhatsAppbackup.apk') Not removing backup apk

def Exit():
    CustomPrint('\nExiting...', 'green')
    os.system('adb kill-server')
    quit()

def ExtractAB(isJAVAInstalled) :
    if not (isJAVAInstalled) : 
        CustomPrint('Can not detect JAVA on system.')
        Exit()
    # Ask if already have whatsapp.ab file and continuing the process, if so then check in extracted folder first and continue.
    if(CustomInput('Have you already made whatsapp.ab and just extracting it now ? : ').upper()=='y'.upper()) : 
        userName = CustomInput('Enter name for this user (same as before.) : ') or 'user'
        abPass = CustomInput('Please enter password for backup (leave empty for none) : ')
        if(os.path.isfile(extracted + userName + '/whatsapp.ab')) : 
            try : 
                os.system('java -jar ' + bin + 'abe.jar unpack ' + extracted + userName + '/whatsapp.ab ' + tmp + 'whatsapp.tar ' + str(abPass))
                CustomPrint('Successfully \'fluffed\' '+ extracted + userName + '/whatsapp.ab ' + tmp + 'whatsapp.tar ')
                TakingOutMainFiles(userName)
            except Exception as e : 
                CustomPrint(e)
        else : 
            CustomPrint('Could not find whatsapp.ab in extracted folder, did you name your user properly?')
            Exit()
    if(os.path.isfile(tmp + 'whatsapp.ab')) :
        CustomPrint('Found whatsapp.ab in tmp folder. Continuing')
        userName = CustomInput('Enter a reference name for this user. : ') or 'user'
        abPass = CustomInput('Please enter password for backup (leave empty for none) : ')
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
    CustomPrint('============ WhatsApp Key / Database Extrator on non-rooted Android ============\n', 'green', ['bold'])
    
def TakingOutMainFiles(userName) : 
    os.mkdir(extracted + userName) if not (os.path.isdir(extracted + userName)) else CustomPrint('Folder already exists.')
    CustomPrint('Taking out main files in ' + tmp + ' folder temporaily.')
    try : 
        bin = ''
        os.system(bin + tar + ' xvf ' + tmp + 'whatsapp.tar -C ' + tmp + ' apps/com.whatsapp/f/key') ; os.replace('tmp/apps/com.whatsapp/f/key', extracted + userName + '/key')
        os.system(bin + tar + ' xvf ' + tmp + 'whatsapp.tar -C ' + tmp + ' apps/com.whatsapp/db/msgstore.db') ; os.replace('tmp/apps/com.whatsapp/db/msgstore.db', extracted + userName + '/msgstore.db')
        os.system(bin + tar + ' xvf ' + tmp + 'whatsapp.tar -C ' + tmp + ' apps/com.whatsapp/db/wa.db') ; os.replace('tmp/apps/com.whatsapp/db/wa.db', extracted + userName + '/wa.db')
        os.system(bin + tar + ' xvf ' + tmp + 'whatsapp.tar -C ' + tmp + ' apps/com.whatsapp/db/axolotl.db') ; os.replace('tmp/apps/com.whatsapp/db/axolotl.db' , extracted + userName + '/axolotl.db')
        os.system(bin + tar + ' xvf ' + tmp + 'whatsapp.tar -C ' + tmp + ' apps/com.whatsapp/db/chatsettings.db') ; os.replace('tmp/apps/com.whatsapp/db/chatsettings.db', extracted + userName + '/chatsettings.db')
        # Reset bin here...
        
        CustomPrint('\nIf you do not see any errors in above lines in extracting/fluffing whatsapp.ab you SHOULD choose to clean temporary folder. It contains your chats in UN-ENCRYPTED format.','green')
        _cleanTemp = CustomInput('Would you like to clean tmp folder? (default y) : ','green') or 'y'
        if(_cleanTemp.upper()=='y'.upper()) : 
            CleanTmp()
    except Exception as e : 
        CustomPrint(e)
        CleanTmp()

if __name__ == "__main__":
    main()