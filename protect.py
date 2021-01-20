from helpers.CustomCI import CustomInput, CustomPrint
import os
import platform

# Detect OS
isWindows = False
isLinux = False
if platform.system() == 'Windows' : isWindows = True 
if platform.system() == 'Linux' : isLinux = True

# Global command line helpers
currDir = os.path.dirname(os.path.realpath(__file__))
extracted = 'extracted\\'
bin = 'bin\\'
if(isLinux) : 
    extracted = 'extracted/'

def init() : 
    currDir = os.path.dirname(os.path.realpath(__file__))

def main() : 
    CustomPrint('This utility is for archiving your output folder with password to enchance it\'s security. Secure is a relative term. Choose longer password.')
    isCompressing = CustomInput('Are you (C)ompressing or (D)ecompressing? : ')
    while(True) : 
        if(isCompressing.upper() == 'C') : 
            ListUserFolders()
            userFolder = CustomInput('\nEnter a name of folder from above (case sensitive) : ')
            Compress(userFolder)
            break
        elif(isCompressing.upper() == 'D') : 
            ListUserFiles()
            userZip = CustomInput('\nEnter a name of file from above (case sensitive) : ')
            Uncompress(userZip)
            break
        else : 
            isCompressing = CustomInput('Choose either \'c\' or \'d\' : ')
            continue

def Compress(userFolder) : 
    if(not os.path.isdir(extracted + userFolder)) : 
        CustomPrint('Could not find directory ' + extracted + userFolder)
    elif(len(os.listdir(extracted + userFolder)) == 0) : 
        CustomPrint('User folder is empty.')
        Exit()
    else : 
        password = CustomInput('Choose a password for zip : ')
        if(password) : 
            password = ' -p' + password 
        os.system(bin + '7za.exe a -t7z -mhe ' + extracted + userFolder + ' ' + extracted + userFolder + '/* ' + password)
        CustomPrint('\nIf you see \'Everything is OK\' in above line then it is recommended to delete user folder.')
        deleteUserFolder = CustomInput('Delete ' + userFolder + ' folder? (default y) : ') or 'y'
        if(deleteUserFolder.upper() == 'Y') : 
            DeleteUserFolder(userFolder)
        else : 
            Exit()

def DeleteUserFolder(userFolder) : 
    CustomPrint('Deleting...')
    try : 
        os.remove(extracted + userFolder)
    except Exception as e : 
        CustomPrint(e)
        CustomPrint('Please manually delete it.')
    Exit()

def DeleteUserZip(userZip) : 
    CustomPrint('Deleting...')
    try : 
        os.remove(extracted + userZip)
    except Exception as e : 
        CustomPrint(e)
        CustomPrint('Please manually delete it.')
        Exit()

def Exit():
    CustomPrint('\nExiting...')
    quit()

def ListUserFiles() : 
    CustomPrint('\nAvailable user files in extracted directory.\n')
    allFies = next(os.walk(extracted))[2]
    for file in allFies : 
        CustomPrint(file)

def ListUserFolders() : 
    CustomPrint('\nAvailable user folders in extracted directory.\n')
    allFolders = next(os.walk(extracted))[1]
    for folder in allFolders : 
        CustomPrint(folder)

def Uncompress(userZip) : 
    if(not str(userZip).endswith('7z')) : 
        userZip = userZip + '.7z'

    if(not os.path.isfile(extracted + userZip)) : 
        CustomPrint('Could not find ' + extracted + userZip)
    elif(os.path.getsize(extracted + userZip) <= 0) : 
        CustomPrint(extracted + userZip + ' is empty.')
        Exit()
    else : 
        password = CustomInput('Enter password, leave empty for none : ')
        if(password) : 
            password = ' -p' + password
        os.system(bin + '7za.exe e -aot ' + extracted + userZip + ' -o' + extracted + userZip.replace('.7z', '') + password)
        CustomPrint('\nIf you see \'Everything is OK\' in above line then you can delete user zip file.')
        deleteUserZip = CustomInput('Delete ' + userZip + ' ? (default n) : ') or 'n'
        if(deleteUserZip.upper() == 'Y') : 
            DeleteUserZip(userZip)
        else : 
            Exit()

if __name__ == "__main__":
    main()


# For zipping and unzipping the extracted folder.
# .\bin\7za.exe a      -t7z     .\extracted\yuvraj    .\extracted\yuvraj\*    -p1234 -mhe
#             (add) (type 7z) (name of ouput archive) (what to archive)  (passowrd) (header ecnryption)
#check if already exists.
# .\bin\7za.exe e -aot .\extracted\yuvraj.7z -oextracted\yuvraj -p1234
