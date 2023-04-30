import argparse
import os
import platform
import subprocess

import helpers.device_serial_id as device_id
from helpers.custom_ci import custom_input, custom_print

# Detect OS
is_windows = False
is_linux = False
if platform.system() == "Windows":
    is_windows = True
if platform.system() == "Linux":
    is_linux = True


def kill_me():
    custom_print(">>> I am in restore_whatsapp.kill_me()", is_print=False)
    custom_print("\n", is_get_time=False)
    custom_print("Exiting...")
    os.system("bin\\adb.exe kill-server") if (is_windows) else os.system(
        "adb kill-server"
    )
    custom_print(
        "Turn off USB debugging [and USB debugging (Security Settings)] if you're done.",
        "cyan",
    )
    custom_input('Hit "Enter" key to continue....', "cyan")
    quit()


def reinstall_whatsapp(adb):
    custom_print(
        f">>> I am in restore_whatsapp.restore_whatsapp(adb={adb})", is_print=False
    )
    custom_print("Reinstalling original WhatsApp.")
    if "/data/local/tmp/WhatsAppbackup.apk" in subprocess.getoutput(
        f"{adb} shell ls /data/local/tmp/WhatsAppbackup.apk"
    ):
        try:
            reinstall_whatsapp_out = subprocess.getoutput(
                f"{adb} shell pm install /data/local/tmp/WhatsAppbackup.apk"
            )
            if "Success" in reinstall_whatsapp_out:
                custom_print("Reinstallation complete.")
                kill_me()
            else:
                custom_print(
                    'Could not install WhatsApp, install by running "restore_whatsapp.py" or manually installing from Play Store.\nHowever if it crashes then you have to clear storage/clear data from "Settings \u2192 App Settings \u2192 WhatsApp".',
                    "red",
                )
                custom_print(reinstall_whatsapp_out, "red")
                kill_me()

        except Exception as e:
            custom_print(e, "red")
            kill_me()
    else:
        custom_print(
            'Could not find backup APK, install from play store.\nHowever if it crashes then you have to clear storage/clear data from "Settings \u2192 App Settings \u2192 WhatsApp".',
            "red",
        )
        kill_me()


def show_banner():
    custom_print(">>> I am in restore_whatsapp.show_banner()", is_print=False)
    banner_content = """
================================================================================
========                                                                ========
========  db   d8b   db  .d8b.         db   dD d8888b. d8888b. d88888b  ========
========  88   I8I   88 d8' `8b        88 ,8P' 88  `8D 88  `8D 88'      ========
========  88   I8I   88 88ooo88        88,8P   88   88 88oooY' 88ooooo  ========
========  Y8   I8I   88 88~~~88 C8888D 88`8b   88   88 88~~~b. 88~~~~~  ========
========  `8b d8'8b d8' 88   88        88 `88. 88  .8D 88   8D 88.      ========
========   `8b8' `8d8'  YP   YP        YP   YD Y8888D' Y8888P' Y88888P  ========
========                                                                ========
================================================================================
    """
    custom_print(banner_content, "green", ["bold"], False)
    custom_print(
        "============ WhatsApp Key / Database Extrator for non-rooted Android ===========\n",
        "green",
        ["bold"],
        False,
    )


if __name__ == "__main__":
    from datetime import datetime

    dt = datetime.now()

    custom_print(
        f'\n\n\n====== Logging starts here. ====== \nFile: {os.path.basename(__file__)}\nDate: {dt.strftime("%A %d/%m/%Y, %H:%M:%S")}\nIf you see any password here then do let know @github.com/YuvrajRaghuvanshiS/WhatsApp-Key-Database-Extractor\n\n\n',
        is_get_time=False,
        is_print=False,
    )
    os.system("cls" if os.name == "nt" else "clear")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-tip", "--tcp-ip", help="Connects to a remote device via TCP mode."
    )
    parser.add_argument(
        "-tp",
        "--tcp-port",
        default="5555",
        help="Port number to connect to. Default: 5555",
    )
    args = parser.parse_args()
    # args = parser.parse_args('--tcp-ip 192.168.168.117'.split())

    tcp_ip = args.tcp_ip
    tcp_port = args.tcp_port
    if tcp_ip:
        adb_device_serial_id = device_id.init("TCP", tcp_ip, tcp_port)
    else:
        adb_device_serial_id = device_id.init("USB")
    if not adb_device_serial_id:
        kill_me()

    # Global command line helpers
    helpers = "helpers/"
    if is_windows:
        adb = f"bin\\adb.exe -s {adb_device_serial_id}"
    else:
        adb = f"adb -s {adb_device_serial_id}"

    os.system("cls" if os.name == "nt" else "clear")
    show_banner()
    reinstall_whatsapp(adb)
