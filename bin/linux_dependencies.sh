#!/bin/bash

echo "Installing dependencies... Hold on."

UNAME=$(uname)
confirm=""

if [ "$UNAME" == "Linux" ] ; then
	echo "Linux detected."
    packages="adb curl grep tar openjdk-11-jdk p7zip-full scrcpy"
    confirm="-y"
    pkg_man="apt-get"
else [ "$UNAME" == "Darwin" ]
	echo "Darwin detected"
    packages="android-platform-tools curl grep gnu-tar openjdk@11 p7zip scrcpy"
    pkg_man="brew"
fi

echo "Updating system."

$pkg_man update

echo "Installing packages."

for package in $packages
do

$pkg_man install $confirm $package

done

echo "Done installing packages. Cheers."

# Do not edit this with any other OS than linux. It will edit the line endings and mess with interpreter and won't work.
