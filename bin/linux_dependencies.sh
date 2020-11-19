#!/usr/bin/env bash
run_install()
{
    apt-get install ${dependencies[@]}
}

dependencies=("adb" "curl" "grep" "tar")
dpkg -s "${dependencies[@]}" >/dev/null 2>&1 || run_install