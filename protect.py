import argparse
from helpers.CustomCI import CustomInput, CustomPrint
import os
import platform
import shutil

# Detect OS
isWindows = False
isLinux = False
if platform.system() == 'Windows' : isWindows = True 
if platform.system() == 'Linux' : isLinux = True

# Global command line helpers
extracted = 'extracted/'
bin = 'bin/'
sevenZip = 'bin\\7za.exe'
if(isLinux) : 
    sevenZip = '7z'

def main() : 
    CustomPrint('This utility is for archiving your output folder with password to enchance it\'s security. Secure is a relative term. Choose longer password.')
    if(isCompress) : 
        Compress(userName, protectPass)

    if(isDecompress) : 
        Decompress(userName, protectPass)

def Compress(userFolder, protectPass) : 
    if(not os.path.isdir(extracted + userFolder)) : 
        CustomPrint('Could not find directory ' + extracted + userFolder)
    elif(len(os.listdir(extracted + userFolder)) == 0) : 
        CustomPrint('User folder is empty.')
        Exit()
    else :  
        protectPass = ' -p' + protectPass 
        os.system(sevenZip + ' a -t7z -mhe ' + extracted + userFolder + ' ' + extracted + userFolder + '/* ' + protectPass)
        CustomPrint('\nIf you see \'Everything is OK\' in above line then it is recommended to delete user folder.')
        deleteUserFolder = CustomInput('Delete ' + userFolder + ' folder? (default y) : ') or 'y'
        # TODO : use -y flag to deleteuserfolder automatically.
        if(deleteUserFolder.upper() == 'Y') : 
            DeleteUserFolder(userFolder)
        else : 
            Exit()

def DeleteUserFolder(userFolder) : 
    CustomPrint('Deleting...')
    try : 
        shutil.rmtree(extracted + userFolder)
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

def Decompress(userZip, protectPass) : 
    if(not str(userZip).endswith('7z')) : 
        userZip = userZip + '.7z'

    if(not os.path.isfile(extracted + userZip)) : 
        CustomPrint('Could not find ' + extracted + userZip)
    elif(os.path.getsize(extracted + userZip) <= 0) : 
        CustomPrint(extracted + userZip + ' is empty.')
        Exit()
    else : 
        if(protectPass) : 
            protectPass = ' -p' + protectPass
        os.system(sevenZip + ' e -aot ' + extracted + userZip + ' -o' + extracted + userZip.replace('.7z', '') + protectPass)
        CustomPrint('\nIf you see \'Everything is OK\' in above line then you can delete user zip file.')
        deleteUserZip = CustomInput('Delete ' + userZip + ' ? (default n) : ') or 'n'
        if(deleteUserZip.upper() == 'Y') : 
            DeleteUserZip(userZip)
        else : 
            Exit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required = True)
    group.add_argument('-c', '--compress', help='Compress user folder', action='store_true')
    group.add_argument('-d', '--decompress', help='Decompress user 7z file.', action='store_true')
    parser.add_argument('userName', help='Reference name of this user.')
    parser.add_argument('-p', '--password', help='Password to compress database into encrypted archive format.')
    # parser.add_argument('-s', '--save', help='Save to log file.', action='store_true') TODO : add a logger later.

    # args=parser.parse_args('-c yuvraj -p 1234'.split())
    args = parser.parse_args()
    isCompress = args.compress
    isDecompress = args.decompress
    userName = args.userName
    protectPass = args.password
    main()


# For zipping and unzipping the extracted folder.
# .\bin\7za.exe a      -t7z     .\extracted\yuvraj    .\extracted\yuvraj\*    -p1234 -mhe
#             (add) (type 7z) (name of ouput archive) (what to archive)  (passowrd) (header ecnryption)
#check if already exists.
# .\bin\7za.exe e -aot .\extracted\yuvraj.7z -oextracted\yuvraj -p1234
