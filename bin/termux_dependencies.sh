run_install()
{
    apt update && apt install curl grep tar proot wget -y && wget https://github.com/MasterDevX/Termux-ADB/raw/master/InstallTools.sh && bash InstallTools.sh
}

echo "Installing dependencies..."
run_install
echo "Dependencies installed successfully. Starting..."