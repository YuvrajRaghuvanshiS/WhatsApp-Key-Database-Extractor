import argparse
import os
import platform
import re
import shutil
import tarfile
import time
from subprocess import getoutput

import protect
from helpers.custom_ci import custom_input, custom_print

# Detect OS
is_windows = False
is_linux = False
if platform.system() == "Windows":
    is_windows = True
if platform.system() == "Linux":
    is_linux = True


# Global command line helpers
tmp = "tmp/"
helpers = "helpers/"
bin = "bin/"
extracted = "extracted/"
if is_windows:
    adb = "bin\\adb.exe -s "
else:
    adb = "adb -s "


def main():
    custom_print(">>> I am in view_extract.main()", is_print=False)
    os.system("cls" if os.name == "nt" else "clear")
    show_banner()
    check_java()
    extract_self(is_tar_only=is_tar_only)


def check_java():
    custom_print(">>> I am in view_extract.check_java()", is_print=False)
    java_version = ""
    out = getoutput("java -version")
    if out:
        java_version = re.findall('(?<=version ")(.*)(?=")', out)
    else:
        custom_print(
            'Could not get output of "java -version" in "view_extract.py"', "red"
        )
        kill_me()

    if java_version:
        custom_print(
            f"Found Java v{java_version[0]} installed on system. Continuing..."
        )
    else:
        is_no_java_continue = (
            custom_input(
                "It looks like you don't have JAVA installed on your system. If you are sure that JAVA is installed you can (C)ontinue with the process or (S)top?: ",
                "red",
            )
            or "s"
        )
        if is_no_java_continue.upper() == "C":
            custom_print("Continuing without detecting JAVA...", "yellow")
        else:
            kill_me("Can not view extract without java installed on system!")


def clean_tmp():
    custom_print(">>> I am in view_extract.clean_tmp()", is_print=False)
    if os.path.isdir(tmp):
        custom_print(f'Cleaning up "{tmp}" folder...', "yellow")
        try:
            shutil.rmtree(tmp)
        except PermissionError as e:
            custom_print(f'Could not delete "{tmp}" folder...', "red")
            custom_print(e, 'red')
            custom_print('Delete it manually, it\'s important.')


def kill_me(reason: str = ""):
    custom_print(f">>> I am in view_extract.kill_me(reason={reason})", is_print=False)
    custom_print("\n", is_get_time=False)
    if reason:
        custom_print(reason)
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


def extract_ab(is_java_installed, is_tar_only=False):
    custom_print(
        f">>> I am in view_extract.extract_ab(is_java_installed={is_java_installed}, is_tar_only={is_tar_only})",
        is_print=False,
    )
    if not is_java_installed:
        custom_print("\aCan not detect JAVA on system.", "red")
        # move whatsapp.ab from tmp to user specified folder.
        username = custom_input("Enter a name for this user.: ")
        os.mkdir(extracted) if not (os.path.isdir(extracted)) else custom_print(
            f'Folder "{extracted}" already exists.', "yellow"
        )
        if not os.path.isdir(f"{extracted}{username}"):
            os.mkdir(f"{extracted}{username}")
            custom_print(f'Created folder "{extracted}{username}"')
        else:
            while os.path.isdir(f"{extracted}{username}"):
                custom_print("\n", is_get_time=False)
                custom_print(
                    f'Folder "{extracted}{username}" exists, contents may get overwritten.',
                    "red",
                )
                username = custom_input("Enter different name of this user.: ")
                if not (os.path.isdir(f"{extracted}{username}")):
                    os.mkdir(f"{extracted}{username}")
                    custom_print(f'Created folder "{extracted}{username}"')
                    break
        os.rename(f"{tmp}whatsapp.ab", f"{extracted}{username}/whatsapp.ab")
        custom_print(
            f'Moved "whatsapp.ab" to "{extracted}{username}" folder. Size: {os.path.getsize(extracted + username + "/whatsapp.ab")} bytes.'
        )
        custom_print('Run "view_extract.py" after installing Java on system.')
        clean_tmp()
        kill_me()
    if os.path.isfile(f"{tmp}whatsapp.ab"):
        custom_print(
            f'Found "whatsapp.ab" in "tmp" folder. Continuing... Size: {os.path.getsize(tmp + "/whatsapp.ab")} bytes.'
        )
        username = (
            custom_input('Enter a name for this user (default "user").: ') or "user"
        )
        ab_pass = custom_input(
            "Enter same password which you entered on device when prompted earlier.: ",
            is_log=False,
        )
        try:
            unpack_out = getoutput(
                f"java -jar {bin}abe.jar unpack {tmp}whatsapp.ab {tmp}whatsapp.tar {ab_pass}"
            )
            if "Exception" in unpack_out:
                custom_print(f'Could not unpack "{tmp}whatsapp.ab"', "red")
                custom_print(unpack_out, "red")
                kill_me()
            custom_print(
                f'Successfully unpacked "{tmp}whatsapp.ab" to "{tmp}whatsapp.tar". Size: {os.path.getsize(tmp + "whatsapp.tar")} bytes.'
            )
            if is_tar_only:
                taking_out_only_tar(username)
            else:
                taking_out_main_files(username)
        except Exception as e:
            custom_print(e, "red")
            kill_me()
    else:
        custom_print('\aCould not find "whatsapp.ab" in "tmp" folder.', "red")
        kill_me()


def extract_self(is_tar_only=False):
    custom_print(
        f">>> I am in view_extract.extract_self(is_tar_only={is_tar_only})",
        is_print=False,
    )
    list_user_folders()
    username = custom_input("Enter a name of folder from above (case sensitive): ")
    while not os.path.isfile(f"{extracted}{username}/whatsapp.ab"):
        if os.path.isdir(f"{extracted}{username}") and not os.path.isfile(
            f"{extracted}{username}/whatsapp.ab"
        ):
            custom_print(
                f'Folder "{extracted}{username}" does not even contain whatsapp.ab',
                "red",
            )
            kill_me()
        username = custom_input(
            f'No such folder: "{extracted}{username}". Enter correct name (case sensitive).: '
        )
    ab_pass = custom_input(
        "Enter same password which you entered on device when prompted earlier.: ",
        is_log=False,
    )
    try:
        os.mkdir(tmp) if not (os.path.isdir(tmp)) else custom_print(
            f'Folder "{tmp}" already exists.', "yellow"
        )
        unpack_out = getoutput(
            f"java -jar {bin}abe.jar unpack {extracted}{username}/whatsapp.ab {tmp}whatsapp.tar {ab_pass}"
        )
        if "Exception" in unpack_out:
            custom_print(f'Could not unpack "{tmp}whatsapp.ab"', "red")
            custom_print(unpack_out, "red")
            kill_me()
        custom_print(
            f'Successfully unpacked "{extracted}{username}/whatsapp.ab" to "{tmp}whatsapp.tar". Size: {os.path.getsize(tmp + "whatsapp.tar")} bytes.'
        )
        if is_tar_only:
            taking_out_only_tar(username)
        else:
            taking_out_main_files(username)
    except Exception as e:
        custom_print(e, "red")
        kill_me()


def list_user_folders():
    custom_print(">>> I am in view_extract.list_user_folders()", is_print=False)
    custom_print("\n", is_get_time=False)
    custom_print("Available user folders in extracted directory.")
    all_folders = next(os.walk(extracted))[1]
    if len(all_folders) == 0:
        custom_print(f'No folders found in "{extracted}" folder.', "red")
        kill_me()
    for folder in all_folders:
        custom_print(folder)
    custom_print("\n", is_get_time=False)


def show_banner():
    custom_print(">>> I am in view_extract.show_banner()", is_print=False)
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
        "============ WhatsApp Key / Database Extractor for non-rooted Android ==========\n",
        "green",
        ["bold"],
        False,
    )


def taking_out_main_files(username):
    custom_print(
        f">>> I am in view_extract.taking_out_main_files(username={username})",
        is_print=False,
    )
    os.mkdir(extracted) if not (os.path.isdir(extracted)) else custom_print(
        f'Folder "{extracted}" already exists.', "yellow"
    )
    os.mkdir(f"{extracted}{username}") if not (
        os.path.isdir(f"{extracted}{username}")
    ) else custom_print(f'Folder "{extracted}{username}" already exists.', "yellow")
    # If user folder already exists ask user to overwrite or skip.
    custom_print(f'Taking out main files in "{tmp}" folder temporarily.')
    try:
        tar = tarfile.open(f"{tmp}whatsapp.tar")
        all_tar_files = tar.getnames()
        files_to_extract = {
            "axolotl.db": "apps/com.whatsapp/db/axolotl.db",
            "encrypted_backup.key": "apps/com.whatsapp/f/encrypted_backup.key",
            "password_data.key": "apps/com.whatsapp/f/password_data.key",
            "chatsettings.db": "apps/com.whatsapp/db/chatsettings.db",
            "key": "apps/com.whatsapp/f/key",
            "msgstore.db": "apps/com.whatsapp/db/msgstore.db",
            "wa.db": "apps/com.whatsapp/db/wa.db",
        }

        for key in files_to_extract:
            if files_to_extract[key] in all_tar_files:
                tar.extract(files_to_extract[key], tmp)
                os.replace(
                    f"{tmp}{files_to_extract[key]}", f"{extracted}{username}/{key}"
                )
                custom_print(f'Copied to "{extracted}{username}": {key}')
            else:
                if key in ["encrypted_backup.key", "password_data.key"]:
                    custom_print(
                        f'"{key}" is not present in tarfile, if you have crypt15 backups then visit "https://github.com/YuvrajRaghuvanshiS/WhatsApp-Key-Database-Extractor/issues/94" for more details.',
                        "red",
                        ["bold"],
                    )
                else:
                    custom_print(
                        f'"{key}" is not present in tarfile, visit "https://github.com/YuvrajRaghuvanshiS/WhatsApp-Key-Database-Extractor/issues/73" for more details.',
                        "red",
                        ["bold"],
                    )
        tar.close()
        time.sleep(2)  # So that 'tar' is free to delete.
        try:
            clean_tmp()
        except Exception as e:
            custom_print(e, "red")
            custom_print("\n", is_get_time=False)
            custom_print(
                f'Go & delete "{tmp}" folder yourself (It\'s important, DO IT.)', "red"
            )
            custom_print("\n", is_get_time=False)
            # TODO: Major security risk: Data in tmp is not deleted.

        custom_print(
            "You should not leave these extracted database and other files hanging in folder, it is very insecure."
        )
        is_create_archive = (
            custom_input(
                "Would you like to create a password protected archive? (default y): "
            )
            or "Y"
        )
        if is_create_archive.upper() == "Y":
            custom_print("\n", is_get_time=False)
            custom_print(
                'Now an archive will be created in extracted folder and original files will be deleted. To later "un-archive" and access these files you need to run "python protect.py" from root directory of this project.',
                "yellow",
            )
            protect.compress(username)
        else:
            custom_print("\n", is_get_time=False)
            custom_print(
                f'\aYour WhatsApp database along with other files is in "{os.path.realpath(extracted + username)}" folder.',
                "yellow",
            )
            custom_print("\n", is_get_time=False)
            custom_input('Hit "Enter" key to continue.')

            try:  # Open in explorer.
                if is_windows:
                    os.startfile(os.path.realpath(f"{extracted}{username}"))
                elif is_linux:
                    os.system(f"xdg-open {os.path.realpath(extracted + username)}")
                else:
                    try:
                        os.system(f"open {os.path.realpath(extracted + username)}")
                    except Exception as e:
                        custom_print(e, is_print=False)
            except Exception as e:
                custom_print(e, is_print=False)
                kill_me()
    except Exception as e:
        custom_print(e, "red")
        clean_tmp()
        kill_me()


def taking_out_only_tar(username):
    custom_print(
        f">>> I am in view_extract.taking_out_only_tar(username={username})",
        is_print=False,
    )
    os.mkdir(extracted) if not (os.path.isdir(extracted)) else custom_print(
        f'Folder "{extracted}" already exists.', "yellow"
    )
    try:
        custom_print(f'Moving "tmp/whatsapp.tar" to "{extracted}{username}.tar"')
        os.replace(f"{tmp}whatsapp.tar", f"{extracted}{username}.tar")
    except Exception as e:
        custom_print(f"\a{e}", "red")
        kill_me()

    clean_tmp()
    custom_print("\n", is_get_time=False)
    custom_print(
        f'\aYour "{username}.tar" is in "{os.path.realpath(extracted)}" folder.',
        "yellow",
    )

    custom_print("\n", is_get_time=False)
    custom_input('Hit "Enter" key to continue.')

    try:  # Open in explorer.
        if is_windows:
            os.startfile(os.path.realpath(extracted))
        elif is_linux:
            os.system(f"xdg-open {os.path.realpath(extracted)}")
        else:
            try:
                os.system(f"open {os.path.realpath(extracted)}")
            except Exception as e:
                custom_print(e, is_print=False)
    except Exception as e:
        custom_print(e, is_print=False)
        kill_me()


if __name__ == "__main__":
    from datetime import datetime

    dt = datetime.now()

    custom_print(
        f'\n\n\n====== Logging starts here. ====== \nFile: {os.path.basename(__file__)}\nDate: {dt.strftime("%A %d/%m/%Y, %H:%M:%S")}\nIf you see any password here then do let know @github.com/YuvrajRaghuvanshiS/WhatsApp-Key-Database-Extractor\n\n\n',
        is_get_time=False,
        is_print=False,
    )

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-tip", "--tcp-ip", help="Connects to a remote device via TCP mode."
    )
    parser.add_argument(
        "-tp", "--tcp-port", help="Port number to connect to. Default: 5555"
    )

    parser.add_argument(
        "-to",
        "--tar-only",
        action="store_true",
        help='Get entire WhatsApp\'s data in "<username>.tar" file instead of just getting few important files.',
    )
    args = parser.parse_args()
    # args = parser.parse_args('--tcp-ip 192.168.43.130 -tp 555'.split())

    tcp_ip = args.tcp_ip
    tcp_port = args.tcp_port
    is_tar_only = args.tar_only

    main()
