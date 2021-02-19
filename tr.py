from CustomCI import CustomPrint
import os

def InstallTermuxDependencies() : 
    CustomPrint("Installing dependencies...")
    CustomPrint("Updating Termux")
    os.system('pkg update')
    CustomPrint("Allow storage permission for storing extracted whatsapp.ab in interal storage:")
    os.system('termux-setup-storage')
    CustomPrint("Done. Installing required dependencies:")
    os.system('pkg install curl grep tar proot wget termcolor -y')
    #CustomPrint("Done. Installing ADB for Termux")
    os.system('wget https://github.com/MasterDevX/Termux-ADB/raw/master/InstallTools.sh && bash InstallTools.sh')
    #CustomPrint("Done. Installing Java for termux.")
    try : 
        os.system('rm -rf installjava') # Deleting any previous instance of installjava.
    except Exception as e : 
        pass
    os.system('wget https://raw.githubusercontent.com/Hax4us/java/master/installjava && sh installjava')
    os.system('proot login')
    CustomPrint("Succesfully installed all dependencies.")

InstallTermuxDependencies()
