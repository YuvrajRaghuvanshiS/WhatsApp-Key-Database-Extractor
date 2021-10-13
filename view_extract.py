import argparse
import datetime
import os
import platform
import re
import shutil
import tarfile
import time
from subprocess import getoutput

import helpers.adb_device_serial_id as adb_device_id
import helpers.tcp_device_serial_id as tcp_device_id
import protect
from helpers.custom_ci import custom_input, custom_print

# Detect OS
is_windows = False
is_linux = False
if platform.system() == 'Windows':
    is_windows = True
if platform.system() == 'Linux':
    is_linux = True

# Global variables
global is_java_installed

# Global command line helpers
tmp = 'tmp/'
helpers = 'helpers/'
bin = 'bin/'
extracted = 'extracted/'
if(is_windows):
    adb = 'bin\\adb.exe -s '
else:
    adb = 'adb -s '


def main():
    custom_print('>>> I am in view_extract.main()', is_print=False)
    os.system('cls' if os.name == 'nt' else 'clear')
    show_banner()
    is_java_installed = check_java()
    global tcp_port
    if(tcp_ip):
        if(not tcp_port):
            tcp_port = '5555'
        adb_device_serial_id = tcp_device_id.init(tcp_ip, tcp_port)
    else:
        adb_device_serial_id = adb_device_id.init()

    if(adb_device_serial_id):
        sdcard_path = getoutput(
            adb + adb_device_serial_id + ' shell "echo $EXTERNAL_STORAGE"') or '/sdcard'
    else:
        sdcard_path = ''
    custom_print('It not necessary to have phone connected unless you want to copy \"msgstore.db\" to \"/sdcard\".\nSo you can ignore above warning.\n')
    extract_self(sdcard_path=sdcard_path,
                 adb_device_serial_id=adb_device_serial_id, is_tar_only=is_tar_only)


def check_java():
    custom_print('>>> I am in view_extract.check_java()', is_print=False)
    # TODO: Variable -s_java_installed scope prblems.
    java_version = ''
    out = getoutput('java -version')
    if(out):
        java_version = re.findall('(?<=version ")(.*)(?=")', out)
    else:
        custom_print(
            'Could not get output of \"java -version\" in \"view_extract.py\"', 'red')
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
        is_no_java_continue = custom_input(
            'It looks like you don\'t have JAVA installed on your system. If you are sure that JAVA is installed you can (C)ontinue with the process or (S)top?: ', 'red') or 's'
        if(is_no_java_continue.upper() == 'C'):
            custom_print(
                'Continuing without detecting JAVA...', 'yellow')
            return is_java_installed
        else:
            kill_me()


def clean_tmp():
    custom_print('>>> I am in view_extract.clean_tmp()', is_print=False)
    if(os.path.isdir(tmp)):
        custom_print('Cleaning up \"' + tmp + '\" folder...', 'yellow')
        shutil.rmtree(tmp)


def kill_me():
    custom_print('>>> I am in view_extract.kill_me()', is_print=False)
    custom_print('\n', is_get_time=False)
    custom_print('Exiting...')
    os.system(
        'bin\\adb.exe kill-server') if(is_windows) else os.system('adb kill-server')
    custom_print(
        'Turn off USB debugging [and USB debugging (Security Settings)] if you\'re done.', 'cyan')
    custom_input('Hit \"Enter\" key to continue....', 'cyan')
    quit()


def extract_ab(is_java_installed, sdcard_path='', adb_device_serial_id='', is_tar_only=False):
    custom_print('>>> I am in view_extract.extract_ab(is_java_installed=' + str(is_java_installed) + ', sdcard_path=' +
                 sdcard_path + ', adb_device_serial_id=' + adb_device_serial_id + ', is_tar_only=' + str(is_tar_only) + ')', is_print=False)
    if not is_java_installed:
        custom_print('\aCan not detect JAVA on system.', 'red')
        # move whatsapp.ab from tmp to user specified folder.
        username = custom_input('Enter a name for this user.: ')
        os.mkdir(extracted) if not (os.path.isdir(extracted)) else custom_print(
            'Folder \"' + extracted + '\" already exists.', 'yellow')
        if not os.path.isdir(extracted + username):
            os.mkdir(extracted + username)
            custom_print('Created folder \"' + extracted + username + '\"')
        else:
            while(os.path.isdir(extracted + username)):
                custom_print('\n', is_get_time=False)
                custom_print('Folder \"' + extracted +
                             username + '\" exists, contents may get overwritten.', 'red')
                username = custom_input('Enter different name of this user.: ')
                if not (os.path.isdir(extracted + username)):
                    os.mkdir(extracted + username)
                    custom_print('Created folder \"' +
                                 extracted + username + '\"')
                    break
        os.rename(tmp + 'whatsapp.ab', extracted + username + '/whatsapp.ab')
        custom_print('Moved \"whatsapp.ab\" to \"' + extracted + username + '\" folder. Size: ' +
                     str(os.path.getsize(extracted + username + '/whatsapp.ab')) + ' bytes.')
        custom_print(
            'Run \"view_extract.py\" after installing Java on system.')
        clean_tmp()
        kill_me()
    if(os.path.isfile(tmp + 'whatsapp.ab')):
        custom_print('Found \"whatsapp.ab\" in \"tmp\" folder. Continuing... Size: ' +
                     str(os.path.getsize(tmp + '/whatsapp.ab')) + ' bytes.')
        username = custom_input(
            'Enter a name for this user (default \"user\").: ') or 'user'
        ab_pass = custom_input(
            'Enter same password which you entered on device when prompted earlier.: ', is_log=False)
        try:
            unpack_out = getoutput('java -jar ' + bin + 'abe.jar unpack ' + tmp +
                                   'whatsapp.ab ' + tmp + 'whatsapp.tar ' + str(ab_pass))
            if('Exception' in unpack_out):
                custom_print('Could not unpack \"' +
                             tmp + 'whatsapp.ab\"', 'red')
                custom_print(unpack_out, 'red')
                kill_me()
            custom_print('Successfully unpacked \"' + tmp + 'whatsapp.ab\" to \"' + tmp +
                         'whatsapp.tar\". Size: ' + str(os.path.getsize(tmp + 'whatsapp.tar')) + ' bytes.')
            if(is_tar_only):
                taking_out_only_tar(username)
            else:
                taking_out_main_files(
                    username, sdcard_path, adb_device_serial_id)
        except Exception as e:
            custom_print(e, 'red')
            kill_me()
    else:
        custom_print(
            '\aCould not find \"whatsapp.ab\" in \"tmp\" folder.', 'red')
        kill_me()


def extract_self(sdcard_path='', adb_device_serial_id='', is_tar_only=False):
    custom_print('>>> I am in view_extract.extract_self(sdcard_path=' + sdcard_path +
                 ', adb_device_serial_id=' + adb_device_serial_id + ', is_tar_only=' + str(is_tar_only) + ')', is_print=False)
    list_user_folders()
    username = custom_input(
        'Enter a name of folder from above (case sensitive): ')
    while(not os.path.isfile(extracted + username + '/whatsapp.ab')):
        if(os.path.isdir(extracted + username) and not os.path.isfile(extracted + username + '/whatsapp.ab')):
            custom_print('Folder \"' + extracted + username +
                         '\" does not even contain whatsapp.ab', 'red')
            kill_me()
        username = custom_input(
            'No such folder: \"' + extracted + username + '\". Enter correct name (case sensitive).: ')
    ab_pass = custom_input(
        'Enter same password which you entered on device when prompted earlier.: ', is_log=False)
    try:
        os.mkdir(tmp) if not (os.path.isdir(tmp)) else custom_print(
            'Folder \"' + tmp + '\" already exists.', 'yellow')
        unpack_out = getoutput('java -jar ' + bin + 'abe.jar unpack ' + extracted +
                               username + '/whatsapp.ab ' + tmp + 'whatsapp.tar ' + str(ab_pass))
        if('Exception' in unpack_out):
            custom_print('Could not unpack \"' +
                         tmp + 'whatsapp.ab\"', 'red')
            custom_print(unpack_out, 'red')
            kill_me()
        custom_print('Successfully unpacked \"' + extracted + username + '/whatsapp.ab\" to ' + '\"' +
                     tmp + 'whatsapp.tar\". Size: ' + str(os.path.getsize(tmp + 'whatsapp.tar')) + ' bytes.')
        if(is_tar_only):
            taking_out_only_tar(username)
        else:
            taking_out_main_files(username, sdcard_path,
                                  adb_device_serial_id)
    except Exception as e:
        custom_print(e, 'red')
        kill_me()


def list_user_folders():
    custom_print('>>> I am in view_extract.list_user_folders()',
                 is_print=False)
    custom_print('\n', is_get_time=False)
    custom_print('Available user folders in extracted directory.')
    all_folders = next(os.walk(extracted))[1]
    if(len(all_folders) == 0):
        custom_print('No folders found in \"' +
                     extracted + '\" folder.', 'red')
        kill_me()
    for folder in all_folders:
        custom_print(folder)
    custom_print('\n', is_get_time=False)


def show_banner():
    custom_print('>>> I am in view_extract.show_banner()', is_print=False)
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


def taking_out_main_files(username, sdcard_path, adb_device_serial_id):
    custom_print('>>> I am in view_extract.taking_out_main_files(username=' + username + ', sdcard_path=' +
                 sdcard_path + ', adb_device_serial_id=' + adb_device_serial_id + ')', is_print=False)
    os.mkdir(extracted) if not (os.path.isdir(extracted)) else custom_print(
        'Folder \"' + extracted + '\" already exists.', 'yellow')
    os.mkdir(extracted + username) if not (os.path.isdir(extracted + username)
                                           ) else custom_print('Folder \"' + extracted + username + '\" already exists.', 'yellow')
    # If user folder already exists ask user to overwrite or skip.
    custom_print('Taking out main files in \"' + tmp + '\" folder temporaily.')
    try:
        tar = tarfile.open(tmp + 'whatsapp.tar')
        all_tar_files = tar.getnames()
        files_to_extract = {'key': 'apps/com.whatsapp/f/key',
                            'msgstore.db': 'apps/com.whatsapp/db/msgstore.db',
                            'wa.db': 'apps/com.whatsapp/db/wa.db',
                            'axolotl.db': 'apps/com.whatsapp/db/axolotl.db',
                            'chatsettings.db': 'apps/com.whatsapp/db/chatsettings.db'}

        for key in files_to_extract:
            if(files_to_extract[key] in all_tar_files):
                tar.extract(files_to_extract[key], tmp)
                os.replace(tmp + files_to_extract[key],
                           extracted + username + '/' + key)
                custom_print('Copied to \"' + extracted +
                             username + '\": ' + key)
            else:
                custom_print(
                    '\"' + key + '\" is not present in tarfile, Go and write to \"https://github.com/YuvrajRaghuvanshiS/WhatsApp-Key-Database-Extractor/issues/73\"', 'red', ['bold'])
        tar.close()
        time.sleep(2)  # So that 'tar' is free to delete.
        try:
            clean_tmp()
        except Exception as e:
            custom_print(e, 'red')
            custom_print('\n', is_get_time=False)
            custom_print('Go & delete \"' + tmp +
                         '\" folder yourself (It\'s important, DO IT.)', 'red')
            custom_print('\n', is_get_time=False)
            # TODO: Major security risk: Data in tmp is not deleted.

        custom_print(
            'You should not leave these extracted database and other files hanging in folder, it is very insecure.')
        is_create_archive = custom_input(
            'Would you like to create a password protected archive? (default y): ') or 'Y'
        if(is_create_archive.upper() == 'Y'):
            custom_print('\n', is_get_time=False)
            custom_print('Now an archive will be created in extracted folder and original files will be deleted. To later \"un-archive\" and access these files you need to run \"python protect.py\" from root directory of this project.', 'yellow')
            protect.compress(username)
        else:
            custom_print('\n', is_get_time=False)
            custom_print('\aYour WhatsApp database along with other files is in \"' +
                         os.path.realpath(extracted + username) + '\" folder.', 'yellow')
            custom_print('\n', is_get_time=False)
            custom_input('Hit \"Enter\" key to continue.')
            if(sdcard_path and adb_device_serial_id):
                is_copy_to_sdcard = custom_input(
                    'Copy \"msgstore.db\" file to phone? (y/n) default \'n\': ') or 'N'
                if(is_copy_to_sdcard.upper() == 'Y'):
                    copy_out = getoutput(adb + adb_device_serial_id + ' push ' + extracted +
                                         username + '/msgstore.db ' + sdcard_path + '/msgstore.db')
                    if('pushed' in copy_out):
                        custom_print('Done copying \"msgstore.db\" to phone.')
                    else:
                        custom_print(
                            'Could not copy \"msgstore.db\" to phone.', 'red')
                        custom_print(copy_out, 'red')
                else:
                    kill_me()
            try:  # Open in explorer.
                if(is_windows):
                    os.startfile(os.path.realpath(extracted + username))
                elif(is_linux):
                    os.system('xdg-open ' +
                              os.path.realpath(extracted + username))
                else:
                    try:
                        os.system(
                            'open ' + os.path.realpath(extracted + username))
                    except Exception as e:
                        custom_print(e, is_print=False)
            except Exception as e:
                custom_print(e, is_print=False)
                kill_me()
    except Exception as e:
        custom_print(e, 'red')
        clean_tmp()
        kill_me()


def taking_out_only_tar(username):
    custom_print('>>> I am in view_extract.taking_out_only_tar(username=' +
                 username + ')', is_print=False)
    os.mkdir(extracted) if not (os.path.isdir(extracted)) else custom_print(
        'Folder \"' + extracted + '\" already exists.', 'yellow')
    try:
        custom_print('Moving \"tmp/whatsapp.tar\" to \"' +
                     extracted + username + '.tar\"')
        os.replace(tmp + 'whatsapp.tar', extracted + username + '.tar')
    except Exception as e:
        custom_print('\a' + e, 'red')
        kill_me()

    clean_tmp()
    custom_print('\n', is_get_time=False)
    custom_print('\aYour \"' + username + '.tar\" is in \"' +
                 os.path.realpath(extracted) + '\" folder.', 'yellow')

    custom_print('\n', is_get_time=False)
    custom_input('Hit \"Enter\" key to continue.')

    try:  # Open in explorer.
        if(is_windows):
            os.startfile(os.path.realpath(extracted))
        elif(is_linux):
            os.system('xdg-open ' +
                      os.path.realpath(extracted))
        else:
            try:
                os.system('open ' + os.path.realpath(extracted))
            except Exception as e:
                custom_print(e, is_print=False)
    except Exception as e:
        custom_print(e, is_print=False)
        kill_me()


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

    tcp_ip = args.tcp_ip
    tcp_port = args.tcp_port
    is_tar_only = args.tar_only

    main()
