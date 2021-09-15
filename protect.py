import datetime
import os
import platform
import shutil

from helpers.custom_ci import custom_input, custom_print

# Detect OS
isWindows = False
isLinux = False
if platform.system() == 'Windows':
    isWindows = True
if platform.system() == 'Linux':
    isLinux = True

# Global command line helpers
extracted = 'extracted/'
bin = 'bin/'
if(isWindows):
    sevenZip = 'bin\\7za.exe'
else:
    sevenZip = '7z'


def main():
    custom_print('This utility is for archiving your output folder with password to enchance it\'s security. Secure is a relative term. Choose longer password.')
    isCompressing = custom_input('Are you (C)ompressing or (D)ecompressing?: ')
    while(True):
        if(isCompressing.upper() == 'C'):
            ListUserFolders()
            custom_print('\n', is_get_time=False)
            userFolder = custom_input(
                'Enter a name of folder from above (case sensitive): ')
            Compress(userFolder)
            break
        elif(isCompressing.upper() == 'D'):
            ListUserFiles()
            custom_print('\n', is_get_time=False)
            userZip = custom_input(
                'Enter a name of file from above (case sensitive): ')
            Uncompress(userZip)
            break
        else:
            isCompressing = custom_input('Choose either \'c\' or \'d\': ')
            continue


def Compress(userFolder):
    if(not os.path.isdir(extracted + userFolder)):
        custom_print('Could not find directory \"' +
                     extracted + userFolder + '\"')
        Exit()
    elif(len(os.listdir(extracted + userFolder)) == 0):
        custom_print('User folder is empty.')
        Exit()
    else:
        password = custom_input('Choose a password for zip: ', is_log=False)
        if(password):
            password = ' -p' + password
        os.system(sevenZip + ' a -t7z -mhe ' + extracted +
                  userFolder + ' ' + extracted + userFolder + '/* ' + password)
        custom_print('\n', is_get_time=False)
        custom_print(
            'If you see \"Everything is OK\" in above line then it is recommended to delete user folder.')
        deleteUserFolder = custom_input(
            'Delete \"' + userFolder + '\" folder? (default y): ') or 'Y'
        custom_print('\n', is_get_time=False)
        custom_print('\aYour \"' + userFolder + '.7z\" file is in \"' + os.path.realpath(extracted) + '\" folder. Password is: ' +
                     password.replace(' -p', ''), 'yellow', is_log=False)
        custom_print('\n', is_get_time=False)
        custom_input('Hit \"Enter\" key to continue.')
        if(deleteUserFolder.upper() == 'Y'):
            DeleteUserFolder(userFolder)
        else:
            Exit()


def DeleteUserFolder(userFolder):
    custom_print('Deleting...')
    try:
        shutil.rmtree(extracted + userFolder)
    except Exception as e:
        custom_print(e, 'red')
        custom_print('Please manually delete it.', 'red')
    Exit()


def DeleteUserZip(userZip):
    custom_print('Deleting...')
    try:
        os.remove(extracted + userZip)
    except Exception as e:
        custom_print(e, 'red')
        custom_print('Please manually delete it.', 'red')
    Exit()


def Exit():
    custom_print('\n', is_get_time=False)
    custom_print('Exiting...')
    try:  # Open in explorer.
        if(isWindows):
            os.startfile(os.path.realpath(extracted))
        elif(isLinux):
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


def ListUserFiles():
    custom_print('\n', is_get_time=False)
    custom_print('Available user files in extracted directory.')
    custom_print('\n', is_get_time=False)
    allFiles = next(os.walk(extracted))[2]
    if(len(allFiles) == 1 and os.path.isfile(extracted + '.placeholder')):
        custom_print('No user files found in \"' +
                     extracted + '\" folder.', 'red')
        Exit()
    for f in allFiles:
        if(f != '.placeholder'):
            custom_print(f)


def ListUserFolders():
    custom_print('\n', is_get_time=False)
    custom_print('Available user folders in extracted directory.')
    custom_print('\n', is_get_time=False)
    allFolders = next(os.walk(extracted))[1]
    if(len(allFolders) == 0):
        custom_print('No folders found in \"' +
                     extracted + '\" folder.', 'red')
        Exit()
    for folder in allFolders:
        custom_print(folder)


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


def Uncompress(userZip):
    if(not str(userZip).endswith('7z')):
        userZip = userZip + '.7z'
    if(not os.path.isfile(extracted + userZip)):
        custom_print('Could not find ' + extracted + userZip)
        Exit()
    elif(os.path.getsize(extracted + userZip) <= 0):
        custom_print(extracted + userZip + ' is empty.')
        Exit()
    else:
        password = custom_input(
            'Enter password, leave empty for none: ', is_log=False)
        if(password):
            password = ' -p' + password
        os.system(sevenZip + ' e -aot ' + extracted + userZip +
                  ' -o' + extracted + userZip.replace('.7z', '') + password)
        custom_print('\n', is_get_time=False)
        custom_print(
            'If you see \"Everything is OK\" in above line then you can delete user zip file.')
        deleteUserZip = custom_input(
            'Delete ' + userZip + ' ? (default n): ') or 'N'
        custom_print('\n', is_get_time=False)
        custom_print('\aYour extracted \"' + userZip.replace('.7z',
                                                             '') + '\" folder is in \"' + os.path.realpath(extracted + userZip.replace('.7z', '')) + '\" folder.', 'yellow')
        custom_print('\n', is_get_time=False)
        custom_input('Hit \"Enter\" key to continue.')
        if(deleteUserZip.upper() == 'Y'):
            DeleteUserZip(userZip)
        else:
            Exit()


if __name__ == "__main__":

    custom_print('\n\n\n====== Logging start here. ====== \nFile: ' + os.path.basename(__file__) + '\nDate: ' +
                 str(datetime.datetime.now()) + '\nIf you see any password here then do let know @github.com/YuvrajRaghuvanshiS/WhatsApp-Key-Database-Extractor\n\n\n', is_get_time=False, is_print=False)
    os.system('cls' if os.name == 'nt' else 'clear')
    ShowBanner()
    main()


# For zipping and unzipping the extracted folder.
# .\bin\7za.exe a      -t7z     .\extracted\yuvraj    .\extracted\yuvraj\*    -p1234 -mhe
#             (add) (type 7z) (name of ouput archive) (what to archive)  (passowrd) (header ecnryption)
# check if already exists.
# .\bin\7za.exe e -aot .\extracted\yuvraj.7z -oextracted\yuvraj -p1234
