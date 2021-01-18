#!/bin/bash

echo "Installing dependencies... Hold on."
echo "Updating system."

apt-get update

echo "Installing packages."

for package in adb curl grep tar openjdk-11-jdk
do

apt-get install -qq --print-uris $package >> script.log 2>>script_error.log

done

echo "Done installing packages. Cheers."
