import argparse
import os
import platform
import re
import shutil
import subprocess
import tarfile
import time

import helpers.adb_device_serial_id as deviceId
import helpers.tcp_device_serial_id as tcpDeviceId
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
is_java_installed = False

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
    os.system('cls' if os.name == 'nt' else 'clear')
    show_banner()
    global is_java_installed
    is_java_installed = check_java()
    global tcp_port
    if(tcp_ip):
        if(not tcp_port):
            tcp_port = '5555'
        adb_serial_id = tcpDeviceId.init(tcp_ip, tcp_port)
    else:
        adb_serial_id = deviceId.init()

    if(adb_serial_id):
        sd_path = subprocess.getoutput(
            adb + adb_serial_id + ' shell "echo $EXTERNAL_STORAGE"') or '/sdcard'
    else:
        sd_path = ''
    extract_ab(is_java_installed, sd_path=sd_path,
               adb_serial_id=adb_serial_id, calling_from_other_module=False, is_tar_only=is_tar_only)


def check_java():
    java_version = re.search('(?<=version ")(.*)(?=")', str(subprocess.check_output(
        'java -version'.split(), stderr=subprocess.STDOUT))).group(1)
    is_java_installed = True if(java_version) else False
    if is_java_installed:
        custom_print('Found Java installed on system. Continuing...')
        return is_java_installed
    else:
        continue_without_java = custom_input(
            'It looks like you don\'t have JAVA installed on your system. Would you like to (C)ontinue with the process and \"view extract\" later? or (S)top? : ', 'red') or 'C'
        if(continue_without_java.upper() == 'C'):
            custom_print(
                'Continuing without JAVA, once JAVA is installed on system run \"view_extract.py\"', 'yellow')
            return is_java_installed
        else:
            exit()


def clean_tmp():
    if(os.path.isdir(tmp)):
        custom_print('Cleaning up \"' + tmp + '\" folder...', 'yellow')
        shutil.rmtree(tmp)


def exit():
    print('\n')
    custom_print('Exiting...')
    os.system(
        'bin\\adb.exe kill-server') if(is_windows) else os.system('adb kill-server')
    custom_input('Hit \"Enter\" key to continue....', 'cyan')
    quit()


def extract_ab(is_java_installed, sd_path='', adb_serial_id='', calling_from_other_module=True, is_tar_only=False):
    if not is_java_installed:
        custom_print('\aCan not detect JAVA on system.', 'red')
        # move whatsapp.ab from tmp to user specified folder.
        username = custom_input('Enter a name for this user. : ')
        os.mkdir(extracted) if not (os.path.isdir(extracted)) else custom_print(
            'Folder \"' + extracted + '\" already exists.', 'yellow')
        os.mkdir(extracted + username) if not (os.path.isdir(extracted + username)
                                               ) else custom_print('Folder \"' + extracted + username + '\" exists.')
        os.rename(tmp + 'whatsapp.ab', extracted + username + '/whatsapp.ab')
        custom_print('Moved \"whatsapp.ab\" to \"' + extracted + username + '\" folder. Size : ' +
                     str(os.path.getsize(extracted + username + '/whatsapp.ab')) + ' bytes.')
        custom_print(
            'Run \"view_extract.py\" after installing Java on system.')
        clean_tmp()
        exit()
    if(not calling_from_other_module):
        if(custom_input('Have you already made whatsapp.ab and just extracting it now ? : ').upper() == 'Y'):
            list_user_folders()
            print('\n')
            username = custom_input(
                'Enter a name of folder from above (case sensitive) : ') or 'user'
            ab_pass = custom_input(
                'Enter same password which you entered on device when prompted earlier. : ')
            if(os.path.isfile(extracted + username + '/whatsapp.ab')):
                try:
                    custom_print('Found \"whatsapp.ab\" in \"' + extracted + username + '\" folder. Size : ' + str(
                        os.path.getsize(extracted + username + '/whatsapp.ab')) + ' bytes. Unpacking...')
                    os.mkdir(tmp) if not (os.path.isdir(tmp)) else custom_print(
                        'Folder \"' + tmp + '\" already exists.', 'yellow')
                    os.system('java -jar ' + bin + 'abe.jar unpack ' + extracted +
                              username + '/whatsapp.ab ' + tmp + 'whatsapp.tar ' + str(ab_pass))
                    custom_print('Successfully unpacked \"' + extracted + username + '/whatsapp.ab\" to ' + '\"' +
                                 tmp + 'whatsapp.tar\". Size : ' + str(os.path.getsize(tmp + 'whatsapp.tar')) + ' bytes.')
                    if(is_tar_only):
                        taking_out_only_tar(username)
                    else:
                        taking_out_main_files(username, sd_path, adb_serial_id)
                except Exception as e:
                    custom_print(e, 'red')
                    exit()
            else:
                custom_print('Could not find \"whatsapp.ab\" in \"' + extracted +
                             username + '\" folder, did you name your user properly?')
                exit()
        else:
            exit()
    if(os.path.isfile(tmp + 'whatsapp.ab')):
        custom_print('Found \"whatsapp.ab\" in \"tmp\" folder. Continuing... Size : ' +
                     str(os.path.getsize(tmp + '/whatsapp.ab')) + ' bytes.')
        username = custom_input(
            'Enter a name for this user (default \"user\"). : ') or 'user'
        ab_pass = custom_input(
            'Enter same password which you entered on device when prompted earlier. : ')
        try:
            os.system('java -jar ' + bin + 'abe.jar unpack ' + tmp +
                      'whatsapp.ab ' + tmp + 'whatsapp.tar ' + str(ab_pass))
            custom_print('Successfully unpacked \"' + tmp + 'whatsapp.ab\" to \"' + tmp +
                         'whatsapp.tar\". Size : ' + str(os.path.getsize(tmp + 'whatsapp.tar')) + ' bytes.')
            if(is_tar_only):
                taking_out_only_tar(username)
            else:
                taking_out_main_files(username, sd_path, adb_serial_id)
        except Exception as e:
            custom_print(e, 'red')
            exit()
    else:
        custom_print('\aCould not find \"whatsapp.ab\" in \"tmp\" folder.')
        exit()


def list_user_folders():
    print('\n')
    custom_print('Available user folders in extracted directory.')
    print('\n')
    all_folders = next(os.walk(extracted))[1]
    if(len(all_folders) == 0):
        custom_print('No folders found in \"' +
                     extracted + '\" folder.', 'red')
        exit()
    for folder in all_folders:
        custom_print(folder)


def show_banner():
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


def taking_out_main_files(username, sd_path, adb_serial_id):
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
                             username + '\" : ' + key)
            else:
                custom_print(
                    '\"' + key + '\" is not present in tarfile, Go and write to \"https://github.com/YuvrajRaghuvanshiS/WhatsApp-Key-Database-Extractor/issues/73\"', 'red', ['bold'])
        tar.close()
        time.sleep(2)  # So that 'tar' is free to delete.
        try:
            clean_tmp()
        except Exception as e:
            custom_print(e, 'red')
            print('\n')
            custom_print('Go & delete \"' + tmp +
                         '\" folder yourself (It\'s important, DO IT.)', 'red')
            print('\n')
            # TODO : Major security risk : Data in tmp is not deleted.

        custom_print(
            'You should not leave these extracted database and other files hanging in folder, it is very insecure.')
        create_archive = custom_input(
            'Would you like to create a password protected archive? (default y) : ') or 'y'
        if(create_archive.upper() == 'Y'):
            print('\n')
            custom_print('Now an archive will be created in extracted folder and original files will be deleted. To later \"un-archive\" and access these files you need to run \"python protect.py\" from root directory of this project.', 'yellow')
            protect.compress(username)
        else:
            print('\n')
            custom_print('\aYour whatsapp database along with other files is in \"' +
                         os.path.realpath(extracted + username) + '\" folder.', 'yellow')
            print('\n')
            custom_input('Hit \"Enter\" key to continue.')
            if(sd_path and adb_serial_id):
                copy_to_sdcard = custom_input(
                    'Copy \"msgstore.db\" file to phone? (y/n) default \'n\' : ') or 'n'
                if(copy_to_sdcard.upper() == 'Y'):
                    os.system(adb + adb_serial_id + ' push ' + extracted +
                              username + '/msgstore.db ' + sd_path + '/msgstore.db')
                    custom_print('Done copying \"msgstore.db\" to phone.')
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
                    except:
                        pass
            except:
                exit()
    except Exception as e:
        custom_print(e, 'red')
        clean_tmp()
        exit()


def taking_out_only_tar(username):
    os.mkdir(extracted) if not (os.path.isdir(extracted)) else custom_print(
        'Folder \"' + extracted + '\" already exists.', 'yellow')
    try:
        custom_print('Moving \"tmp/whatsapp.tar\" to \"' +
                     extracted + username + '.tar\"')
        os.replace(tmp + 'whatsapp.tar', extracted + username + '.tar')
    except Exception as e:
        custom_print('\a' + e, 'red')
        exit()

    clean_tmp()
    print('\n')
    custom_print('\aYour \"' + username + '.tar\" is in \"' +
                 os.path.realpath(extracted) + '\" folder.', 'yellow')

    print('\n')
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
            except:
                pass
    except:
        exit()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-tip', '--tcp-ip', help='Connects to a remote device via TCP mode.')
    parser.add_argument('-tp', '--tcp-port',
                        help='Port number to connect to. Default : 5555')

    parser.add_argument('-to', '--tar-only', action='store_true',
                        help='Get entire WhatsApp\'s data in \"<username>.tar\" file instead of just getting few important files.')
    # args = parser.parse_args()
    args = parser.parse_args('--tcp-ip 192.168.43.130 -tp 555'.split())

    tcp_ip = args.tcp_ip
    tcp_port = args.tcp_port
    is_tar_only = args.tar_only

    main()
