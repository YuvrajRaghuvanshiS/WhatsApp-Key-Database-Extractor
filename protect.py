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
    custom_print('This utility is for archiving your output folder with password to enchance it\'s security. Secure is a relative term. Choose longer password.')
    is_compressing = custom_input(
        'Are you (C)ompressing or (D)ecompressing? : ')
    while(True):
        if(is_compressing.upper() == 'C'):
            list_user_folders()
            print('\n')
            user_folder = custom_input(
                'Enter a name of folder from above (case sensitive) : ')
            compress(user_folder)
            break
        elif(is_compressing.upper() == 'D'):
            list_user_files()
            print('\n')
            user_zip = custom_input(
                'Enter a name of file from above (case sensitive) : ')
            uncompress(user_zip)
            break
        else:
            is_compressing = custom_input('Choose either \'c\' or \'d\' : ')
            continue


def compress(user_folder):
    if(not os.path.isdir(extracted + user_folder)):
        custom_print('Could not find directory \"' +
                     extracted + user_folder + '\"')
        exit()
    elif(len(os.listdir(extracted + user_folder)) == 0):
        custom_print('User folder is empty.')
        exit()
    else:
        password = custom_input('Choose a password for zip : ')
        if(password):
            password = ' -p' + password
        os.system(seven_zip + ' a -t7z -mhe ' + extracted +
                  user_folder + ' ' + extracted + user_folder + '/* ' + password)
        print('\n')
        custom_print(
            'If you see \"Everything is OK\" in above line then it is recommended to delete user folder.')
        is_delelte_user_folder = custom_input(
            'Delete \"' + user_folder + '\" folder? (default y) : ') or 'y'
        print('\n')
        custom_print('\aYour \"' + user_folder + '.7z\" file is in \"' + os.path.realpath(extracted) + '\" folder. Password is : ' +
                     password.replace(' -p', ''), 'yellow')
        print('\n')
        custom_input('Hit \"Enter\" key to continue.')
        if(is_delelte_user_folder.upper() == 'Y'):
            delete_user_folder(user_folder)
        else:
            exit()


def delete_user_folder(user_folder):
    custom_print('Deleting...')
    try:
        shutil.rmtree(extracted + user_folder)
    except Exception as e:
        custom_print(e, 'red')
        custom_print('Please manually delete it.', 'red')
    exit()


def delete_user_zip(user_zip):
    custom_print('Deleting...')
    try:
        os.remove(extracted + user_zip)
    except Exception as e:
        custom_print(e, 'red')
        custom_print('Please manually delete it.', 'red')
    exit()


def exit():
    print('\n')
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
    print('\n')
    custom_print('Available user files in extracted directory.')
    print('\n')
    all_files = next(os.walk(extracted))[2]
    if(len(all_files) == 1 and os.path.isfile(extracted + '.placeholder')):
        custom_print('No user files found in \"' +
                     extracted + '\" folder.', 'red')
        exit()
    for file in all_files:
        if(file != '.placeholder'):
            custom_print(file)


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


def uncompress(user_zip):
    if(not str(user_zip).endswith('7z')):
        user_zip = user_zip + '.7z'
    if(not os.path.isfile(extracted + user_zip)):
        custom_print('Could not find ' + extracted + user_zip)
        exit()
    elif(os.path.getsize(extracted + user_zip) <= 0):
        custom_print(extracted + user_zip + ' is empty.')
        exit()
    else:
        password = custom_input('Enter password, leave empty for none : ')
        if(password):
            password = ' -p' + password
        os.system(seven_zip + ' e -aot ' + extracted + user_zip +
                  ' -o' + extracted + user_zip.replace('.7z', '') + password)
        print('\n')
        custom_print(
            'If you see \"Everything is OK\" in above line then you can delete user zip file.')
        is_delete_user_zip = custom_input(
            'Delete ' + user_zip + ' ? (default n) : ') or 'n'
        print('\n')
        custom_print('\aYour extracted \"' + user_zip.replace('.7z',
                                                              '') + '\" folder is in \"' + os.path.realpath(extracted + user_zip.replace('.7z', '')) + '\" folder.', 'yellow')
        print('\n')
        custom_input('Hit \"Enter\" key to continue.')
        if(is_delete_user_zip.upper() == 'Y'):
            delete_user_zip(user_zip)
        else:
            exit()


if __name__ == "__main__":
    main()


# For zipping and unzipping the extracted folder.
# .\bin\7za.exe a      -t7z     .\extracted\yuvraj    .\extracted\yuvraj\*    -p1234 -mhe
#             (add) (type 7z) (name of ouput archive) (what to archive)  (passowrd) (header ecnryption)
# check if already exists.
# .\bin\7za.exe e -aot .\extracted\yuvraj.7z -oextracted\yuvraj -p1234
