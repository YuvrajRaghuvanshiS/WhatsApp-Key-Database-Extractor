from CustomCI import CustomPrint
import os

def InstallTermuxDependencies() : 
    CustomPrint("Installing dependencies...")
    CustomPrint("Updating Termux")
    os.system('pkg update && pkg upgrade')
    CustomPrint("Allow storage permission for storing extracted whatsapp.ab in interal storage:")
    os.system('termux-setup-storage')
    CustomPrint("Done. Installing required dependencies...")
    os.system('pkg install curl grep tar proot wget -y')
    os.system('pip install termcolor')
    os.system('wget https://github.com/MasterDevX/Termux-ADB/raw/master/InstallTools.sh && bash InstallTools.sh')
    try : 
        os.system('rm -r -f installjava') # Deleting any previous instance of installjava.
    except Exception as e : 
        pass
    os.system('wget https://raw.githubusercontent.com/MasterDevX/java/master/installjava && sh installjava')
    os.system('proot login')
    CustomPrint("Connecting ADB with local device:")
    os.system('adb connect localhost')
    os.system('cd WhatsApp-Key-Databse-Extractor/')
    CustomPrint("Succesfully installed all dependencies.")

InstallTermuxDependencies()
