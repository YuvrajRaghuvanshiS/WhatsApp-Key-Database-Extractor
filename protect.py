import datetime
import os
import platform
import shutil

from helpers.custom_ci import custom_input, custom_print

# Detect OS
is_windows = False
is_linux = False
if platform.system() == 'Windows':
    is_windows = True
if platform.system() == 'Linux':
    is_linux = True

# Global command line helpers
extracted = 'extracted/'
bin = 'bin/'
if(is_windows):
    seven_zip = 'bin\\7za.exe'
else:
    seven_zip = '7z'


def main():
    custom_print('>>> I am in protect.main()', is_print=False)
    custom_print('This utility is for archiving your output folder with password to enchance it\'s security. Secure is a relative term. Choose longer password.')
    is_compressing = custom_input(
        'Are you (C)ompressing or (D)ecompressing?: ')
    while(True):
        if(is_compressing.upper() == 'C'):
            list_user_folders()
            custom_print('\n', is_get_time=False)
            user_folder = custom_input(
                'Enter a name of folder from above (case sensitive): ')
            compress(user_folder)
            break
        elif(is_compressing.upper() == 'D'):
            list_user_files()
            custom_print('\n', is_get_time=False)
            user_zip = custom_input(
                'Enter a name of file from above (case sensitive): ')
            uncompress(user_zip)
            break
        else:
            is_compressing = custom_input('Choose either \'c\' or \'d\': ')
            continue


def compress(user_folder):
    custom_print('>>> I am in protect.compress(user_folder=' +
                 user_folder + ')', is_print=False)
    if(not os.path.isdir(extracted + user_folder)):
        custom_print('Could not find directory \"' +
                     extracted + user_folder + '\"')
        kill_me()
    elif(len(os.listdir(extracted + user_folder)) == 0):
        custom_print('User folder is empty.')
        kill_me()
    else:
        password = custom_input('Choose a password for zip: ', is_log=False)
        if(password):
            password = ' -p' + password
        os.system(seven_zip + ' a -t7z -mhe ' + extracted +
                  user_folder + ' ' + extracted + user_folder + '/* ' + password)
        custom_print('\n', is_get_time=False)
        custom_print(
            'If you see \"Everything is OK\" in above line then it is recommended to delete user folder.')
        is_delete_user_folder = custom_input(
            'Delete \"' + user_folder + '\" folder? (default y): ') or 'Y'
        custom_print('\n', is_get_time=False)
        custom_print('\aYour \"' + user_folder + '.7z\" file is in \"' + os.path.realpath(extracted) + '\" folder. Password is: ' +
                     password.replace(' -p', ''), 'yellow', is_log=False)
        custom_print('\n', is_get_time=False)
        custom_input('Hit \"Enter\" key to continue.')
        if(is_delete_user_folder.upper() == 'Y'):
            delete_user_folder(user_folder)
        else:
            kill_me()


def delete_user_folder(user_folder):
    custom_print('>>> I am in protect.delete_user_folder(user_folder=' +
                 user_folder + ')', is_print=False)
    custom_print('Deleting...')
    try:
        shutil.rmtree(extracted + user_folder)
    except Exception as e:
        custom_print(e, 'red')
        custom_print('Please manually delete it.', 'red')
    kill_me()


def delete_user_zip(user_zip):
    custom_print('>>> I am in protect.delete_user_zip(user_zip=' +
                 user_zip + ')', is_print=False)
    custom_print('Deleting...')
    try:
        os.remove(extracted + user_zip)
    except Exception as e:
        custom_print(e, 'red')
        custom_print('Please manually delete it.', 'red')
    kill_me()


def kill_me():
    custom_print('>>> I am in protect.kill_me()', is_print=False)
    custom_print('\n', is_get_time=False)
    custom_print('Exiting...')
    try:  # Open in explorer.
        if(is_windows):
            os.startfile(os.path.realpath(extracted))
        elif(is_linux):
            os.system('xdg-open ' + os.path.realpath(extracted))
        else:
            try:
                os.system('open ' + os.path.realpath(extracted))
            except:
                pass
    except:
        pass
    custom_input('Hit \"Enter\" key to continue....', 'cyan')
    quit()


def list_user_files():
    custom_print('>>> I am in protect.list_user_files()', is_print=False)
    custom_print('\n', is_get_time=False)
    custom_print('Available user files in extracted directory.')
    custom_print('\n', is_get_time=False)
    all_files = next(os.walk(extracted))[2]
    if(len(all_files) == 1 and os.path.isfile(extracted + '.placeholder')):
        custom_print('No user files found in \"' +
                     extracted + '\" folder.', 'red')
        kill_me()
    for f in all_files:
        if(f != '.placeholder'):
            custom_print(f)


def list_user_folders():
    custom_print('>>> I am in protect.list_user_folders()', is_print=False)
    custom_print('\n', is_get_time=False)
    custom_print('Available user folders in extracted directory.')
    custom_print('\n', is_get_time=False)
    all_folders = next(os.walk(extracted))[1]
    if(len(all_folders) == 0):
        custom_print('No folders found in \"' +
                     extracted + '\" folder.', 'red')
        kill_me()
    for folder in all_folders:
        custom_print(folder)


def show_banner():
    custom_print('>>> I am in protect.show_banner()', is_print=False)
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


def uncompress(user_zip):
    custom_print('>>> I am in protect.uncompress(user_zip=' +
                 user_zip + ')', is_print=False)
    if(not str(user_zip).endswith('7z')):
        user_zip = user_zip + '.7z'
    if(not os.path.isfile(extracted + user_zip)):
        custom_print('Could not find ' + extracted + user_zip)
        kill_me()
    elif(os.path.getsize(extracted + user_zip) <= 0):
        custom_print(extracted + user_zip + ' is empty.')
        kill_me()
    else:
        password = custom_input(
            'Enter password, leave empty for none: ', is_log=False)
        if(password):
            password = ' -p' + password
        os.system(seven_zip + ' e -aot ' + extracted + user_zip +
                  ' -o' + extracted + user_zip.replace('.7z', '') + password)
        custom_print('\n', is_get_time=False)
        custom_print(
            'If you see \"Everything is OK\" in above line then you can delete user zip file.')
        is_delete_user_zip = custom_input(
            'Delete ' + user_zip + ' ? (default n): ') or 'N'
        custom_print('\n', is_get_time=False)
        custom_print('\aYour extracted \"' + user_zip.replace('.7z',
                                                              '') + '\" folder is in \"' + os.path.realpath(extracted + user_zip.replace('.7z', '')) + '\" folder.', 'yellow')
        custom_print('\n', is_get_time=False)
        custom_input('Hit \"Enter\" key to continue.')
        if(is_delete_user_zip.upper() == 'Y'):
            delete_user_zip(user_zip)
        else:
            kill_me()


if __name__ == "__main__":

    custom_print('\n\n\n====== Logging start here. ====== \nFile: ' + os.path.basename(__file__) + '\nDate: ' +
                 str(datetime.datetime.now()) + '\nIf you see any password here then do let know @github.com/YuvrajRaghuvanshiS/WhatsApp-Key-Database-Extractor\n\n\n', is_get_time=False, is_print=False)
    os.system('cls' if os.name == 'nt' else 'clear')
    show_banner()
    main()


# For zipping and unzipping the extracted folder.
# .\bin\7za.exe a      -t7z     .\extracted\yuvraj    .\extracted\yuvraj\*    -p1234 -mhe
#             (add) (type 7z) (name of ouput archive) (what to archive)  (passowrd) (header ecnryption)
# check if already exists.
# .\bin\7za.exe e -aot .\extracted\yuvraj.7z -oextracted\yuvraj -p1234
