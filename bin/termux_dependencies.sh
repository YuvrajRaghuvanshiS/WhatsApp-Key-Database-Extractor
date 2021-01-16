echo "Installing dependencies..."
echo "Updating Termux"
apt update
echo "Allow storage permission for storing extraced whatsapp.ab in interal storage."
termux-setup-storage 
echo "Done. Installing various required components."
apt install curl grep fish tar proot wget -y
echo "Done. Installing ADB for Termux"
wget https://github.com/MasterDevX/Termux-ADB/raw/master/InstallTools.sh && bash InstallTools.sh
echo "Done. Installing Java for termux."
wget https://raw.githubusercontent.com/Hax4us/java/master/installjava && sh installjava
echo "Done installing all dependencies. Now running proot."
fish
proot login