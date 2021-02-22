#!/bin/bash

echo "Installing dependencies... Hold on."

UNAME=$(uname)

if [ "$UNAME" == "Linux" ] ; then
	echo "Linux detected."
    pkg_man=apt-get
else [ "$UNAME" == "Darwin" ]
	echo "Darwin detected"
    pkg_man=brew
fi

echo "Updating system."

$pkg_man update

echo "Installing packages."

for package in adb curl grep tar openjdk-11-jdk p7zip-full
do

$pkg_man install -y $package

done

echo "Done installing packages. Cheers."

# Do not edit this with any other OS than linux. It will edit the line endings and mess with interpreter and won't work.
