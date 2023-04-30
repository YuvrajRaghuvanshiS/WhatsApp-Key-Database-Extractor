import os
import re
import shutil
import subprocess
from subprocess import getoutput

try:
    import requests
    from packaging import version
    from tqdm import tqdm
except ImportError:
    try:
        os.system("pip3 install packaging requests tqdm")
    except Exception:
        os.system("python3 -m pip install packaging requests tqdm")

from custom_ci import custom_input, custom_print

# Global variables
app_url_primary_cdn = "https://web.archive.org/web/20141111030303if_/http://www.whatsapp.com/android/current/WhatsApp.apk"
app_url_alternate_cdn = "https://legacy-static-assets.androidapksfree.com/earth/androidbucket/WhatsApp-v2.11.431-AndroidBucket.com.apk"


def after_connect(adb):
    custom_print(f">>> I am in handler.after_connect(adb={adb})", is_print=False)
    sdk_version = int(getoutput(f"{adb} shell getprop ro.build.version.sdk"))
    if sdk_version <= 13:
        custom_print(
            "Unsupported device. This method only works on Android v4.0 or higher.",
            "red",
        )
        custom_print('Cleaning up "tmp" folder.', "red")
        shutil.rmtree("tmp")
        kill_me()
    _wa_path_text = f"{adb} shell pm path com.whatsapp"
    whatsapp_apk_path_in_device = subprocess.getoutput(_wa_path_text)
    if not whatsapp_apk_path_in_device:
        custom_print("Looks like WhatsApp is not installed on device.", "red")
        kill_me()
    whatsapp_apk_path_in_device = whatsapp_apk_path_in_device.split(":")[1]
    # To check if APK even exists at a given path to download!
    # Since that obviously is not available at whatsapp cdn defaulting that content_length to 0 for GH #46
    try:
        resp = requests.head(app_url_primary_cdn, timeout=5)
        try:
            content_length = resp.headers["content-length"]
        except KeyError as e:
            custom_print(e, is_print=False)
            custom_print('No "content-length" field in header, defaulting to 0.')
            content_length = 0
    except requests.exceptions.RequestException as e:
        custom_print(e, is_print=False)
        custom_print(
            "An exception has occured while checking for LegacyWhatsApp existence at web.archive.org, defaulting to alternate CDN server, check log for futher details.",
            "yellow",
        )
        content_length = 0
    _version_name_text = f"{adb} shell dumpsys package com.whatsapp"
    version_name = re.findall(
        "(?<=versionName=)(.*?)(?=\n)", getoutput(_version_name_text)
    )[0]
    custom_print(f"WhatsApp v{version_name} installed on device")
    download_app_from = (
        app_url_primary_cdn if (content_length == 18329558) else app_url_alternate_cdn
    )
    if version.parse(version_name) > version.parse("2.11.431"):
        if not (os.path.isfile("helpers/LegacyWhatsApp.apk")):
            custom_print('Downloading legacy WhatsApp V2.11.431 to "helpers" folder')
            download_apk(download_app_from, "helpers/LegacyWhatsApp.apk")
            # wget.download(downloadAppFrom, 'helpers/LegacyWhatsApp.apk')
            custom_print("\n", is_get_time=False)
        else:
            custom_print('Found legacy WhatsApp V2.11.431 apk in "helpers" folder')
    else:
        # Version lower than 2.11.431 installed on device.
        pass

    return 1, sdk_version, whatsapp_apk_path_in_device, version_name


def download_apk(url, file_name):
    custom_print(
        f">>> I am in handler.download_apk(url={url}, file_name={file_name})",
        is_print=False,
    )
    # Streaming, so we can iterate over the response.
    response = requests.get(url, stream=True)
    # For WayBackMachine only.
    total_size_in_bytes = int(
        response.headers.get("x-archive-orig-content-length", 0)
    ) or int(response.headers.get("content-length", 0))
    if total_size_in_bytes:
        # Fixed where it stuck on "Downloading legacy WhatsApp V2.11.431 to helpers folder"
        total_size_in_bytes = int(total_size_in_bytes)
    else:
        # totalSizeInBytes must be null
        custom_print(
            "\aFor some reason I could not download Legacy WhatsApp, you need to download it on your own now from either of the links given below: ",
            "red",
        )
        custom_print("\n", is_get_time=False)
        custom_print(f'1. "{app_url_primary_cdn}" (official\'s archive)', "red")
        custom_print(f'2. "{app_url_alternate_cdn}" unofficial website.', "red")
        custom_print("\n", is_get_time=False)
        custom_print(
            'Once downloaded rename it to "LegacyWhatsApp.apk" exactly and put in "helpers" folder.',
            "red",
        )
        kill_me()
    block_size = 1024  # 1 Kibibyte
    progress_bar = tqdm(total=total_size_in_bytes, unit="iB", unit_scale=True)
    with open("helpers/temp.apk", "wb") as f:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            f.write(data)
    progress_bar.close()
    os.rename("helpers/temp.apk", file_name)
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        custom_print("\aSomething went during downloading LegacyWhatsApp.apk")
        kill_me()


def kill_me():
    custom_print(">>> I am in handler.kill_me()", is_print=False)
    custom_print("\n", is_get_time=False)
    custom_print("Exiting...")
    os.system("bin\\adb.exe kill-server") if (os.name == "nt") else os.system(
        "adb kill-server"
    )
    custom_print(
        "Turn off USB debugging [and USB debugging (Security Settings)] if you're done.",
        "cyan",
    )
    custom_input('Hit "Enter" key to continue....', "cyan")
    quit()


def handler(adb):
    custom_print(f">>> I am in handler.handler(adb={adb})", is_print=False)
    custom_print(f'Connected to {getoutput(adb + " shell getprop ro.product.model")}')
    return after_connect(adb)
