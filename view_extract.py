import argparse
import os
import platform
import re
import shutil
import subprocess
import tarfile
import time

import helpers.ADBDeviceSerialId as deviceId
import helpers.TCPDeviceSerialId as tcpDeviceId
import protect
from helpers.CustomCI import CustomInput, CustomPrint

# Detect OS
isWindows = False
isLinux = False
if platform.system() == 'Windows':
    isWindows = True
if platform.system() == 'Linux':
    isLinux = True

# Global variables
isJAVAInstalled = False

# Global command line helpers
tmp = 'tmp/'
helpers = 'helpers/'
bin = 'bin/'
extracted = 'extracted/'
if(isWindows):
    adb = 'bin\\adb.exe -s '
else:
    adb = 'adb -s '


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    ShowBanner()
    global isJAVAInstalled
    isJAVAInstalled = CheckJAVA()
    global tcpPort
    if(tcpIP):
        if(not tcpPort):
            tcpPort = '5555'
        ADBSerialId = tcpDeviceId.init(tcpIP, tcpPort)
    else:
        ADBSerialId = deviceId.init()

    if(ADBSerialId):
        sdPath = subprocess.getoutput(
            adb + ADBSerialId + ' shell "echo $EXTERNAL_STORAGE"') or '/sdcard'
    else:
        sdPath = ''
    ExtractAB(isJAVAInstalled, sdPath=sdPath,
              ADBSerialId=ADBSerialId, callingFromOtherModule=False, isTarOnly=isTarOnly)


def CheckJAVA():
    JAVAVersion = re.search('(?<=version ")(.*)(?=")', str(subprocess.check_output(
        'java -version'.split(), stderr=subprocess.STDOUT))).group(1)
    isJAVAInstalled = True if(JAVAVersion) else False
    if (isJAVAInstalled):
        CustomPrint('Found Java installed on system. Continuing...')
        return isJAVAInstalled
    else:
        noJAVAContinue = CustomInput(
            'It looks like you don\'t have JAVA installed on your system. Would you like to (C)ontinue with the process and \"view extract\" later? or (S)top? : ', 'red') or 'C'
        if(noJAVAContinue.upper() == 'C'):
            CustomPrint(
                'Continuing without JAVA, once JAVA is installed on system run \"view_extract.py\"', 'yellow')
            return isJAVAInstalled
        else:
            Exit()


def CleanTmp():
    if(os.path.isdir(tmp)):
        CustomPrint('Cleaning up \"' + tmp + '\" folder...', 'yellow')
        shutil.rmtree(tmp)


def Exit():
    print('\n')
    CustomPrint('Exiting...')
    os.system(
        'bin\\adb.exe kill-server') if(isWindows) else os.system('adb kill-server')
    CustomInput('Hit \"Enter\" key to continue....', 'cyan')
    quit()


def ExtractAB(isJAVAInstalled, sdPath='', ADBSerialId='', callingFromOtherModule=True, isTarOnly=False):
    if not (isJAVAInstalled):
        CustomPrint('\aCan not detect JAVA on system.', 'red')
        # move whatsapp.ab from tmp to user specified folder.
        username = CustomInput('Enter a name for this user. : ')
        os.mkdir(extracted) if not (os.path.isdir(extracted)) else CustomPrint(
            'Folder \"' + extracted + '\" already exists.', 'yellow')
        os.mkdir(extracted + username) if not (os.path.isdir(extracted + username)
                                               ) else CustomPrint('Folder \"' + extracted + username + '\" exists.')
        os.rename(tmp + 'whatsapp.ab', extracted + username + '/whatsapp.ab')
        CustomPrint('Moved \"whatsapp.ab\" to \"' + extracted + username + '\" folder. Size : ' +
                    str(os.path.getsize(extracted + username + '/whatsapp.ab')) + ' bytes.')
        CustomPrint('Run \"view_extract.py\" after installing Java on system.')
        CleanTmp()
        Exit()
    if(not callingFromOtherModule):
        if(CustomInput('Have you already made whatsapp.ab and just extracting it now ? : ').upper() == 'Y'):
            ListUserFolders()
            print('\n')
            username = CustomInput(
                'Enter a name of folder from above (case sensitive) : ') or 'user'
            abPass = CustomInput(
                'Enter same password which you entered on device when prompted earlier. : ')
            if(os.path.isfile(extracted + username + '/whatsapp.ab')):
                try:
                    CustomPrint('Found \"whatsapp.ab\" in \"' + extracted + username + '\" folder. Size : ' + str(
                        os.path.getsize(extracted + username + '/whatsapp.ab')) + ' bytes. Unpacking...')
                    os.mkdir(tmp) if not (os.path.isdir(tmp)) else CustomPrint(
                        'Folder \"' + tmp + '\" already exists.', 'yellow')
                    os.system('java -jar ' + bin + 'abe.jar unpack ' + extracted +
                              username + '/whatsapp.ab ' + tmp + 'whatsapp.tar ' + str(abPass))
                    CustomPrint('Successfully unpacked \"' + extracted + username + '/whatsapp.ab\" to ' + '\"' +
                                tmp + 'whatsapp.tar\". Size : ' + str(os.path.getsize(tmp + 'whatsapp.tar')) + ' bytes.')
                    if(isTarOnly):
                        TakingOutOnlyTar(username)
                    else:
                        TakingOutMainFiles(username, sdPath, ADBSerialId)
                except Exception as e:
                    CustomPrint(e, 'red')
                    Exit()
            else:
                CustomPrint('Could not find \"whatsapp.ab\" in \"' + extracted +
                            username + '\" folder, did you name your user properly?')
                Exit()
        else:
            Exit()
    if(os.path.isfile(tmp + 'whatsapp.ab')):
        CustomPrint('Found \"whatsapp.ab\" in \"tmp\" folder. Continuing... Size : ' +
                    str(os.path.getsize(tmp + '/whatsapp.ab')) + ' bytes.')
        username = CustomInput(
            'Enter a name for this user (default \"user\"). : ') or 'user'
        abPass = CustomInput(
            'Enter same password which you entered on device when prompted earlier. : ')
        try:
            os.system('java -jar ' + bin + 'abe.jar unpack ' + tmp +
                      'whatsapp.ab ' + tmp + 'whatsapp.tar ' + str(abPass))
            CustomPrint('Successfully unpacked \"' + tmp + 'whatsapp.ab\" to \"' + tmp +
                        'whatsapp.tar\". Size : ' + str(os.path.getsize(tmp + 'whatsapp.tar')) + ' bytes.')
            if(isTarOnly):
                TakingOutOnlyTar(username)
            else:
                TakingOutMainFiles(username, sdPath, ADBSerialId)
        except Exception as e:
            CustomPrint(e, 'red')
            Exit()
    else:
        CustomPrint('\aCould not find \"whatsapp.ab\" in \"tmp\" folder.')
        Exit()


def ListUserFolders():
    print('\n')
    CustomPrint('Available user folders in extracted directory.')
    print('\n')
    allFolders = next(os.walk(extracted))[1]
    if(len(allFolders) == 0):
        CustomPrint('No folders found in \"' + extracted + '\" folder.', 'red')
        Exit()
    for folder in allFolders:
        CustomPrint(folder)


def ShowBanner():
    banner_content = '''
================================================================================
========                                                                ========
========  db   d8b   db  .d8b.         db   dD d8888b. d8888b. d88888b  ======== 
========  88   I8I   88 d8' `8b        88 ,8P' 88  `8D 88  `8D 88'      ======== 
========  88   I8I   88 88ooo88        88,8P   88   88 88oooY' 88ooooo  ======== 
========  Y8   I8I   88 88~~~88 C8888D 88`8b   88   88 88~~~b. 88~~~~~  ======== 
========  `8b d8'8b d8' 88   88        88 `88. 88  .8D 88   8D 88.      ======== 
========   `8b8' `8d8'  YP   YP        YP   YD Y8888D' Y8888P' Y88888P  ======== 
========                                                                ========
================================================================================
    '''
    CustomPrint(banner_content, 'green', ['bold'], False)
    CustomPrint('============ WhatsApp Key / Database Extrator for non-rooted Android ===========\n',
                'green', ['bold'], False)


def TakingOutMainFiles(username, sdPath, ADBSerialId):
    os.mkdir(extracted) if not (os.path.isdir(extracted)) else CustomPrint(
        'Folder \"' + extracted + '\" already exists.', 'yellow')
    os.mkdir(extracted + username) if not (os.path.isdir(extracted + username)
                                           ) else CustomPrint('Folder \"' + extracted + username + '\" already exists.', 'yellow')
    # If user folder already exists ask user to overwrite or skip.
    CustomPrint('Taking out main files in \"' + tmp + '\" folder temporaily.')
    try:
        tar = tarfile.open(tmp + 'whatsapp.tar')
        allTarFiles = tar.getnames()
        filesToExtract = {'key': 'apps/com.whatsapp/f/key',
                          'msgstore.db': 'apps/com.whatsapp/db/msgstore.db',
                          'wa.db': 'apps/com.whatsapp/db/wa.db',
                          'axolotl.db': 'apps/com.whatsapp/db/axolotl.db',
                          'chatsettings.db': 'apps/com.whatsapp/db/chatsettings.db'}

        for key in filesToExtract:
            if(filesToExtract[key] in allTarFiles):
                tar.extract(filesToExtract[key], tmp)
                os.replace(tmp + filesToExtract[key],
                           extracted + username + '/' + key)
                CustomPrint('Copied to \"' + extracted +
                            username + '\" : ' + key)
            else:
                CustomPrint(
                    '\"' + key + '\" is not present in tarfile, Go and write to \"https://github.com/YuvrajRaghuvanshiS/WhatsApp-Key-Database-Extractor/issues/73\"', 'red', ['bold'])
        tar.close()
        time.sleep(2)  # So that 'tar' is free to delete.
        try:
            CleanTmp()
        except Exception as e:
            CustomPrint(e, 'red')
            print('\n')
            CustomPrint('Go & delete \"' + tmp +
                        '\" folder yourself (It\'s important, DO IT.)', 'red')
            print('\n')
            # TODO : Major security risk : Data in tmp is not deleted.

        CustomPrint(
            'You should not leave these extracted database and other files hanging in folder, it is very insecure.')
        createArchive = CustomInput(
            'Would you like to create a password protected archive? (default y) : ') or 'y'
        if(createArchive.upper() == 'Y'):
            print('\n')
            CustomPrint('Now an archive will be created in extracted folder and original files will be deleted. To later \"un-archive\" and access these files you need to run \"python protect.py\" from root directory of this project.', 'yellow')
            protect.Compress(username)
        else:
            print('\n')
            CustomPrint('\aYour whatsapp database along with other files is in \"' +
                        os.path.realpath(extracted + username) + '\" folder.', 'yellow')
            print('\n')
            CustomInput('Hit \"Enter\" key to continue.')
            if(sdPath and ADBSerialId):
                copyTosdCard = CustomInput(
                    'Copy \"msgstore.db\" file to phone? (y/n) default \'n\' : ') or 'n'
                if(copyTosdCard.upper() == 'Y'):
                    os.system(adb + ADBSerialId + ' push ' + extracted +
                              username + '/msgstore.db ' + sdPath + '/msgstore.db')
                    CustomPrint('Done copying \"msgstore.db\" to phone.')
            try:  # Open in explorer.
                if(isWindows):
                    os.startfile(os.path.realpath(extracted + username))
                elif(isLinux):
                    os.system('xdg-open ' +
                              os.path.realpath(extracted + username))
                else:
                    try:
                        os.system(
                            'open ' + os.path.realpath(extracted + username))
                    except:
                        pass
            except:
                Exit()
    except Exception as e:
        CustomPrint(e, 'red')
        CleanTmp()
        Exit()


def TakingOutOnlyTar(username):
    os.mkdir(extracted) if not (os.path.isdir(extracted)) else CustomPrint(
        'Folder \"' + extracted + '\" already exists.', 'yellow')
    try:
        CustomPrint('Moving \"tmp/whatsapp.tar\" to \"' +
                    extracted + username + '.tar\"')
        os.replace(tmp + 'whatsapp.tar', extracted + username + '.tar')
    except Exception as e:
        CustomPrint('\a' + e, 'red')
        Exit()

    CleanTmp()
    print('\n')
    CustomPrint('\aYour \"' + username + '.tar\" is in \"' +
                os.path.realpath(extracted) + '\" folder.', 'yellow')

    print('\n')
    CustomInput('Hit \"Enter\" key to continue.')

    try:  # Open in explorer.
        if(isWindows):
            os.startfile(os.path.realpath(extracted))
        elif(isLinux):
            os.system('xdg-open ' +
                      os.path.realpath(extracted))
        else:
            try:
                os.system('open ' + os.path.realpath(extracted))
            except:
                pass
    except:
        Exit()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-tip', '--tcp-ip', help='Connects to a remote device via TCP mode.')
    parser.add_argument('-tp', '--tcp-port',
                        help='Port number to connect to. Default : 5555')

    parser.add_argument('-to', '--tar-only', action='store_true',
                        help='Get entire WhatsApp\'s data in \"<username>.tar\" file instead of just getting few important files.')
    args = parser.parse_args()
    # args = parser.parse_args('--tcp-ip 192.168.43.130 -tp 555'.split())

    tcpIP = args.tcp_ip
    tcpPort = args.tcp_port
    isTarOnly = args.tar_only

    main()
