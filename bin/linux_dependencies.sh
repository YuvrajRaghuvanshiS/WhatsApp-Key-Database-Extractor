#!/usr/bin/env bash
run_install()
{
    sudo apt-get install ${dependencies[@]} -y
}


dependencies=("adb" "curl" "grep" "tar" "openjdk-11-jdk")
dpkg -s "${dependencies[@]}" >/dev/null 2>&1 || run_install
echo "Dependencies installed successfully. Starting..."