#!/bin/bash

echo "Installing dependencies... Hold on."
echo "Which platform are you on?"
echo "L : Linux (Kali, Ubuntu, ParrotSec)"
echo "M : Mac"
read platform
echo $platform

echo "Updating system."

if [ $platform = 'l' ]; then
	pkg_man=apt-get
else
	pkg_man=brew
fi

$pkg_man update

echo "Installing packages."

for package in adb curl grep tar openjdk-11-jdk p7zip-full
do

$pkg_man install -y $package

done

echo "Done installing packages. Cheers."

# Do not edit this with any other OS than linux. It will edit the line endings and mess with interpreter and won't work.
