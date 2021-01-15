echo "Installing dependencies..."
apt update && apt install curl grep tar proot wget -y && wget https://github.com/MasterDevX/Termux-ADB/raw/master/InstallTools.sh && bash InstallTools.sh
echo "Dependencies installed successfully. Starting..."