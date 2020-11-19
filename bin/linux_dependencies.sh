#!/usr/bin/env bash
run_install()
{
    sudo apt-get install ${dependencies[@]} -y
}

echo "test"
dependencies=("adb" "curl" "grep" "tar")
dpkg -s "${dependencies[@]}" >/dev/null 2>&1 || run_install