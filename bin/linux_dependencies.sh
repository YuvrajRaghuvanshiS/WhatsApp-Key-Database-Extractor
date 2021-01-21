#!/bin/bash

echo "Installing dependencies... Hold on."
echo "Updating system."

apt-get update

echo "Installing packages."

for package in adb curl grep tar openjdk-11-jdk p7zip-full
do

apt-get install -y $package

done

echo "Done installing packages. Cheers."

# Do not edit this with any other OS than linux. It will edit the line endings and mess with interpreter and won't work.
