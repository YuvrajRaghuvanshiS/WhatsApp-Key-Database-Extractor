import argparse
import datetime
import os
import platform
import re
import shutil
import tarfile
import time
from subprocess import check_output, getoutput

import helpers.adb_device_serial_id as deviceId
import helpers.tcp_device_serial_id as tcpDeviceId
import protect
from helpers.custom_ci import custom_input, custom_print

# Detect OS
isWindows = False
isLinux = False
if platform.system() == 'Windows':
    isWindows = True
if platform.system() == 'Linux':
    isLinux = True

# Global variables
is_java_installed = False

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
    isJAVAInstalled = check_java()
    global tcpPort
    if(tcpIP):
        if(not tcpPort):
            tcpPort = '5555'
        ADBSerialId = tcpDeviceId.init(tcpIP, tcpPort)
    else:
        ADBSerialId = deviceId.init()

    if(ADBSerialId):
        sdPath = getoutput(
            adb + ADBSerialId + ' shell "echo $EXTERNAL_STORAGE"') or '/sdcard'
    else:
        sdPath = ''
    custom_print('It not necessary to have phone connected unless you want to copy \"msgstore.db\" to \"/sdcard\".\nSo you can ignore above warning.\n')
    ExtractAB(isJAVAInstalled, sdPath=sdPath,
              ADBSerialId=ADBSerialId, callingFromOtherModule=False, isTarOnly=isTarOnly)


def check_java():
    java_version = ''
    out = getoutput('java -version')
    if(out):
        java_version = re.findall('(?<=version ")(.*)(?=")', out)
    else:
        custom_print(
            'Could not get output of \"java -version\" in \"view_extract.py\"', 'red')
        custom_print('Continuing without JAVA...', 'red')
        return False
    if(java_version):
        is_java_installed = True
    else:
        is_java_installed = False
    if is_java_installed:
        custom_print('Found Java v' + java_version[0] +
                     ' installed on system. Continuing...')
        return is_java_installed
    else:
        noJAVAContinue = custom_input(
            'It looks like you don\'t have JAVA installed on your system. Would you like to (C)ontinue with the process and \"view extract\" later? or (S)top?: ', 'red') or 'C'
        if(noJAVAContinue.upper() == 'C'):
            custom_print(
                'Continuing without JAVA, once JAVA is installed on system run \"view_extract.py\"', 'yellow')
            return is_java_installed
        else:
            Exit()


def CleanTmp():
    if(os.path.isdir(tmp)):
        custom_print('Cleaning up \"' + tmp + '\" folder...', 'yellow')
        shutil.rmtree(tmp)


def Exit():
    custom_print('\n', is_get_time=False)
    custom_print('Exiting...')
    os.system(
        'bin\\adb.exe kill-server') if(isWindows) else os.system('adb kill-server')
    custom_input('Hit \"Enter\" key to continue....', 'cyan')
    quit()


def ExtractAB(isJAVAInstalled, sdPath='', ADBSerialId='', callingFromOtherModule=True, isTarOnly=False):
    if not (isJAVAInstalled):
        custom_print('\aCan not detect JAVA on system.', 'red')
        # move whatsapp.ab from tmp to user specified folder.
        username = custom_input('Enter a name for this user.: ')
        os.mkdir(extracted) if not (os.path.isdir(extracted)) else custom_print(
            'Folder \"' + extracted + '\" already exists.', 'yellow')
        os.mkdir(extracted + username) if not (os.path.isdir(extracted + username)
                                               ) else custom_print('Folder \"' + extracted + username + '\" exists.')
        os.rename(tmp + 'whatsapp.ab', extracted + username + '/whatsapp.ab')
        custom_print('Moved \"whatsapp.ab\" to \"' + extracted + username + '\" folder. Size: ' +
                     str(os.path.getsize(extracted + username + '/whatsapp.ab')) + ' bytes.')
        custom_print(
            'Run \"view_extract.py\" after installing Java on system.')
        CleanTmp()
        Exit()
    if(not callingFromOtherModule):
        if(custom_input('Have you already made whatsapp.ab and just extracting it now ?: ').upper() == 'Y'):
            ListUserFolders()
            username = custom_input(
                'Enter a name of folder from above (case sensitive): ')
            while(not os.path.isfile(extracted + username + '/whatsapp.ab')):
                if(os.path.isdir(extracted + username) and not os.path.isfile(extracted + username + '/whatsapp.ab')):
                    custom_print('Folder \"' + extracted + username +
                                 '\" does not even contain whatsapp.ab')
                    Exit()
                username = custom_input(
                    'No such folder: \"' + extracted + username + '\". Enter correct name (case sensitive).: ')
            abPass = custom_input(
                'Enter same password which you entered on device when prompted earlier.: ', is_log=False)
            try:
                os.mkdir(tmp) if not (os.path.isdir(tmp)) else custom_print(
                    'Folder \"' + tmp + '\" already exists.', 'yellow')
                os.system('java -jar ' + bin + 'abe.jar unpack ' + extracted +
                          username + '/whatsapp.ab ' + tmp + 'whatsapp.tar ' + str(abPass))
                custom_print('Successfully unpacked \"' + extracted + username + '/whatsapp.ab\" to ' + '\"' +
                             tmp + 'whatsapp.tar\". Size: ' + str(os.path.getsize(tmp + 'whatsapp.tar')) + ' bytes.')
                if(isTarOnly):
                    TakingOutOnlyTar(username)
                else:
                    TakingOutMainFiles(username, sdPath, ADBSerialId)
            except Exception as e:
                custom_print(e, 'red')
                Exit()
        else:
            Exit()
    if(os.path.isfile(tmp + 'whatsapp.ab')):
        custom_print('Found \"whatsapp.ab\" in \"tmp\" folder. Continuing... Size: ' +
                     str(os.path.getsize(tmp + '/whatsapp.ab')) + ' bytes.')
        username = custom_input(
            'Enter a name for this user (default \"user\").: ') or 'user'
        abPass = custom_input(
            'Enter same password which you entered on device when prompted earlier.: ', is_log=False)
        try:
            os.system('java -jar ' + bin + 'abe.jar unpack ' + tmp +
                      'whatsapp.ab ' + tmp + 'whatsapp.tar ' + str(abPass))
            custom_print('Successfully unpacked \"' + tmp + 'whatsapp.ab\" to \"' + tmp +
                         'whatsapp.tar\". Size: ' + str(os.path.getsize(tmp + 'whatsapp.tar')) + ' bytes.')
            if(isTarOnly):
                TakingOutOnlyTar(username)
            else:
                TakingOutMainFiles(username, sdPath, ADBSerialId)
        except Exception as e:
            custom_print(e, 'red')
            Exit()
    else:
        custom_print('\aCould not find \"whatsapp.ab\" in \"tmp\" folder.')
        Exit()


def ListUserFolders():
    custom_print('\n', is_get_time=False)
    custom_print('Available user folders in extracted directory.')
    allFolders = next(os.walk(extracted))[1]
    if(len(allFolders) == 0):
        custom_print('No folders found in \"' +
                     extracted + '\" folder.', 'red')
        Exit()
    for folder in allFolders:
        custom_print(folder)
    custom_print('\n', is_get_time=False)


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
    custom_print(banner_content, 'green', ['bold'], False)
    custom_print('============ WhatsApp Key / Database Extrator for non-rooted Android ===========\n',
                 'green', ['bold'], False)


def TakingOutMainFiles(username, sdPath, ADBSerialId):
    os.mkdir(extracted) if not (os.path.isdir(extracted)) else custom_print(
        'Folder \"' + extracted + '\" already exists.', 'yellow')
    os.mkdir(extracted + username) if not (os.path.isdir(extracted + username)
                                           ) else custom_print('Folder \"' + extracted + username + '\" already exists.', 'yellow')
    # If user folder already exists ask user to overwrite or skip.
    custom_print('Taking out main files in \"' + tmp + '\" folder temporaily.')
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
                custom_print('Copied to \"' + extracted +
                             username + '\": ' + key)
            else:
                custom_print(
                    '\"' + key + '\" is not present in tarfile, Go and write to \"https://github.com/YuvrajRaghuvanshiS/WhatsApp-Key-Database-Extractor/issues/73\"', 'red', ['bold'])
        tar.close()
        time.sleep(2)  # So that 'tar' is free to delete.
        try:
            CleanTmp()
        except Exception as e:
            custom_print(e, 'red')
            custom_print('\n', is_get_time=False)
            custom_print('Go & delete \"' + tmp +
                         '\" folder yourself (It\'s important, DO IT.)', 'red')
            custom_print('\n', is_get_time=False)
            # TODO: Major security risk: Data in tmp is not deleted.

        custom_print(
            'You should not leave these extracted database and other files hanging in folder, it is very insecure.')
        createArchive = custom_input(
            'Would you like to create a password protected archive? (default y): ') or 'Y'
        if(createArchive.upper() == 'Y'):
            custom_print('\n', is_get_time=False)
            custom_print('Now an archive will be created in extracted folder and original files will be deleted. To later \"un-archive\" and access these files you need to run \"python protect.py\" from root directory of this project.', 'yellow')
            protect.compress(username)
        else:
            custom_print('\n', is_get_time=False)
            custom_print('\aYour whatsapp database along with other files is in \"' +
                         os.path.realpath(extracted + username) + '\" folder.', 'yellow')
            custom_print('\n', is_get_time=False)
            custom_input('Hit \"Enter\" key to continue.')
            if(sdPath and ADBSerialId):
                copyTosdCard = custom_input(
                    'Copy \"msgstore.db\" file to phone? (y/n) default \'n\': ') or 'N'
                if(copyTosdCard.upper() == 'Y'):
                    os.system(adb + ADBSerialId + ' push ' + extracted +
                              username + '/msgstore.db ' + sdPath + '/msgstore.db')
                    custom_print('Done copying \"msgstore.db\" to phone.')
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
        custom_print(e, 'red')
        CleanTmp()
        Exit()


def TakingOutOnlyTar(username):
    os.mkdir(extracted) if not (os.path.isdir(extracted)) else custom_print(
        'Folder \"' + extracted + '\" already exists.', 'yellow')
    try:
        custom_print('Moving \"tmp/whatsapp.tar\" to \"' +
                     extracted + username + '.tar\"')
        os.replace(tmp + 'whatsapp.tar', extracted + username + '.tar')
    except Exception as e:
        custom_print('\a' + e, 'red')
        Exit()

    CleanTmp()
    custom_print('\n', is_get_time=False)
    custom_print('\aYour \"' + username + '.tar\" is in \"' +
                 os.path.realpath(extracted) + '\" folder.', 'yellow')

    custom_print('\n', is_get_time=False)
    custom_input('Hit \"Enter\" key to continue.')

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

    custom_print('\n\n\n====== Logging start here. ====== \nFile: ' + os.path.basename(__file__) + '\nDate: ' +
                 str(datetime.datetime.now()) + '\nIf you see any password here then do let know @github.com/YuvrajRaghuvanshiS/WhatsApp-Key-Database-Extractor\n\n\n', is_get_time=False, is_print=False)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-tip', '--tcp-ip', help='Connects to a remote device via TCP mode.')
    parser.add_argument('-tp', '--tcp-port',
                        help='Port number to connect to. Default: 5555')

    parser.add_argument('-to', '--tar-only', action='store_true',
                        help='Get entire WhatsApp\'s data in \"<username>.tar\" file instead of just getting few important files.')
    args = parser.parse_args()
    # args = parser.parse_args('--tcp-ip 192.168.43.130 -tp 555'.split())

    tcpIP = args.tcp_ip
    tcpPort = args.tcp_port
    isTarOnly = args.tar_only

    main()
