#!/bin/bash

echo "Installing dependencies... Hold on."

UNAME=$(uname)
confirm=""

if [ "$UNAME" == "Linux" ] ; then
	echo "Linux detected."
    packages="adb tar openjdk-11-jdk p7zip-full scrcpy"
    confirm="-y"
    pkg_man="apt-get"
else [ "$UNAME" == "Darwin" ]
	echo "Darwin detected"
    packages="android-platform-tools gnu-tar openjdk@11 p7zip scrcpy"
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

# Line ending should be LF.