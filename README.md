<p align="center">
  <img src="https://img.shields.io/github/repo-size/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor?color=informational&label=repo%20size">
  <img src="https://tokei.rs/b1/github/yuvrajraghuvanshis/whatsapp-key-database-extractor?category=code">
  <img src="https://img.shields.io/github/languages/top/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor">
  <img src="https://img.shields.io/github/license/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor?label=license">
  <img src="https://img.shields.io/badge/depends-JAVA-informational">
  <img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fyuvrajraghuvanshis%2Fwhatsapp-key-database-extractor&count_bg=%233D64C8&title_bg=%23555555&icon=github.svg&icon_color=%23E7E7E7&title=hits&edge_flat=false">
</p>

<br />

<p align="center">
  <img src="https://img.shields.io/badge/windows-tested-success">
  <img src="https://img.shields.io/badge/kali-tested-success">
  <img src="https://img.shields.io/badge/ubuntu-tested-success">
  <img src="https://img.shields.io/badge/mac-tested-success">  
</p>


<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor">
    <img src="https://raw.githubusercontent.com/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor/master/helpers/banner.png" alt="Logo" width="320" height="100">
  </a>

  <h3 align="center">WhatsApp Key/Database Extractor </h3>
  <h4 align="center">NO LONGER MAINTAINED </h4>

  <p align="center">
    Extract key/msgstore.db from /data/data/com.whatsapp in Android v4.0+ without root.
    <br />
</p>


![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation-for-pipreleases-specific-instructions-go-to-builds-branch)
  * [Standalone Operations](#standalone-operations)
  * [Features & ToDo](#features--todo)
  * [Demo](#demo)
  * [Troubleshooting](#troubleshooting)
* [Roadmap](#roadmap)
* [Limitations](#limitations)
* [Contributing](#contributing)
* [License](#license)
* [Agreement](#agreement)
* [Contact](#contact)

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

## About The Project

<!--[![Glimpse][product-screenshot]](https://github.com/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor)-->

This project is inspired by [EliteAndroidApps/WhatsApp-Key-DB-Extractor](https://github.com/EliteAndroidApps/WhatsApp-Key-DB-Extractor). Since Android v4.0+ Google has removed adb backup and apps no longer supported being backed up by "adb backup -f myApp.ab -apk com.foobar.app". However there is one catch in this scenario and that is some old version of many apps including WhatsApp support that to this day, and that's the idea...

The idea is to install "Legacy Version" of WhatsApp on you device via adb and use "adb backup"  to fetch files from "/data/data/com.whatsapp" folder which includes both the "key" and "msgstore.db" (non encrypted) file and after that restore current WhatsApp.


### Built With
* [Python](https://www.python.org/)
* [Bash](https://www.gnu.org/software/bash/) (for Linux and OS X)

**Depends on**   

* [Java](https://www.java.com/) (To extract backup)

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

## Getting Started

***1) Before doing anything take a backup of your chats and turn off your phone's internet so you don't lose any new messages.
For that go to "WhatsApp Settings &#8594; Chat Settings &#8594; Chat Backup" here take a local backup.***

***2) If you see a folder "Android/media/com.whatsapp" copy it somewhere safe before running the script, new versions of WhatsApp are saving data here (including images and videos), I try to keep it intact during the process but you never know when code messes up.***

***Hope for best, prepare for Worst.***

After [installation](#installation-for-pipreleases-specific-instructions-go-to-builds-branch) follow on screen instructions.


### Prerequisites

* O/S: Any Windows/Mac/Linux. Do not have access to any of these? Try [Termux Edition.](https://github.com/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor/tree/termux) 
* [Python 3.x](https://www.python.org/downloads/)
* [Java](https://www.java.com/en/download/)
* USB Debugging must be enabled on the target device. Settings &#8594; Developer Options &#8594; USB debugging.
  * If you cannot find Developer Options then go to: Settings &#8594; About phone/device and tap the Build number multiple times until you're finally declared a developer.  
* Android device with Android 4.0 or higher. i.e. Ice Cream Sandwich, Jelly Bean, KitKat, Lollipop, Marshmallow, Nougat, Oreo, Pie, Q.  



### Installation (for pip/releases specific instructions go to [builds](https://github.com/YuvrajRaghuvanshiS/WhatsApp-Key-Database-Extractor/tree/builds) branch)

1. Clone the repo
```bash
git clone https://github.com/YuvrajRaghuvanshiS/WhatsApp-Key-Database-Extractor.git && cd WhatsApp-Key-Database-Extractor
```
2. Install dependencies (for linux and OSX only): skip `sudo` for mac.
```bash
sudo ./bin/linux_dependencies.sh
```
If you're getting any error while running above command you need to install the following manually for your linux distro.: [adb](https://developer.android.com/studio/command-line/adb) [tar]() [openjdk11]() [7zip](https://www.7-zip.org/download.html) [scrcpy](https://github.com/Genymobile/scrcpy)

3. Run `wa_kdbe.py` by double clicking the file on Windows or by
```python
python3 wa_kdbe.py
```

**Command Line Flags**

| Short | Flag                | Mode | Required? | Type   | Behavior                                                              | Status |
| ----- | ------------------- | ---- | --------- | ------ | ---------------------------------------------------------------------- | ------ |
| -ar   |--allow-reboot       | USB  | Optional  | Bool   | Reboots device before installing Legacy WhatsApp.                      | Stable |
| -tip  | --tcp-ip IP_ADDRESS | TCP  | Required  | String | Connects to a remote device via TCP mode.                              | Stable |
| -tp   |--tcp-port PORT      | TCP  | Optional  | String | Port number to connect to. Default: 5555.                             | Stable |
| -s    | --scrcpy            | Both | Optional  | Bool   | Show device screen as a window using ScrCpy.                           | Stable |
| -to   | --tar-only          | Both | Optional  | Bool   | Get ALL files as a tarball instead of main files from WhatsApp backup. | Stable |

Note that TCP mode and USB mode are mutually exclusive. Either use with TCP mode or USB mode. When Android is plugged with USB don't use TCP flags.

| Mode | **Example usage**: Long command **OR** Short command                                                                                                                |
| ---- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| TCP  | `python3 wa_kdbe.py --tcp-ip 192.168.43.130 --tcp-port 5555 --scrcpy --tar-only` **OR** `python3 wa_kdbe.py -tip 192.168.43.130 -tp 5555 -s -to` |
| USB  | `python3 wa_kdbe.py -ar -s -to` **OR** `python3 wa_kdbe.py --allow-reboot --scrcpy --tar-only`                                                   |

### Standalone Operations
**These operations are standalone implementation of their defined task. One should run these when specifically needed. For ex: Process finished but WhatsApp was not reinstalled on device.**

1. Run `python3 view_extract.py` to unpack whatsapp.ab to whatsapp.tar and extract files. For this to work there should be "whatsapp.ab" file either in "extracted/\<username\>" folder or in "tmp" folder. Where "username" is name of user you entered earlier.


2. Run `python3 protect.py` to compress/decompress user folder with(out) password for safekeeping. For this to work there should either be "username" folder or "username.7z" file in "extracted" folder.


3. Run `python3 restore_whatsapp.py` to reinstall WhatsApp on device.

### Features & ToDo
<!--https://github.com/StylishThemes/GitHub-Dark/wiki/Emoji-->

*  :heavy_check_mark: Extracts msgstore.db from /data/data/com.whatsapp. (duh)
*  :heavy_check_mark: Works wireless-ly without USB cable using "ADB over TCP" with `--tcp-ip IP --tcp-port PORT` flags.
*  :heavy_check_mark: See and control your android phone with your computer using [ScrCpy](https://github.com/Genymobile/scrcpy) using `--scrcpy` flag.
*  :heavy_check_mark: Works with any android device v4.0+ so far.
*  :heavy_check_mark: Works with any android device no matter where it is in universe as long as it is running ADB over TCP.
*  :heavy_check_mark: Moves msgstore.db to your phone.
*  :heavy_check_mark: Creates password protected 7z file so keep your extraction safe.
*  :heavy_check_mark: Continues without JAVA installed and make "whatsapp.tar" out of "whatsapp.ab" once java is installed by running `python3 view_extract.py`.
*  :heavy_check_mark: Command line arguments
*  :heavy_check_mark: ADB Devices menu.
*  :heavy_check_mark: Implement datetime.
*  :heavy_check_mark: Extracts backup created over TCP ~~{ #24 bin\tar.exe: Unexpected EOF on archive file in Windows.}.~~
*  :heavy_check_mark: Finally logging in "log/wa_kdbe.log". Log excludes passwords, if you see any password in log file then do let know.
*  :x: Works with WhatsApp Business.


### Demo

Following gif shows the output of `python3 wa_kdbe.py -ar -s -to`

<img src="https://raw.githubusercontent.com/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor/master/non_essentials/wa-kdbe.gif" alt="Project GIF">

### Troubleshooting

* If running `python3 wa_kdbe.py` or any other file is throwing error like "python3 is recognized as internal or external command." AND python3 is "already added to path (in case of windows)" try running files with `py wa_kdbe.py` instead. [Read more.](https://github.com/YuvrajRaghuvanshiS/WhatsApp-Key-Database-Extractor/issues/57)
* If list is empty close terminal, remove and re-plug the device, and re-run the script. [Read more.](https://github.com/YuvrajRaghuvanshiS/WhatsApp-Key-Database-Extractor/issues/11#issuecomment-768500899)
* If you have never used USB Debugging before, you may also need to verify the fingerprint by ticking the checkbox and tapping "allow" on device popup.  
* If you have set a default backup password in your Android settings, then this MUST be the  backup password that you PROVIDE when prompted to backup your data. Else it WILL fail!  
* If you get an error saying "AES encryption not allowed" then you need to update your Oracle Java Cryptography Extension (JCE) to Unlimited Strength Jurisdiction Policy Files.  
* WhatsApp crashing? Run `python3 restore_whatsapp.py`. Or "clear data/storage" / uninstall and reinstall from Play Store.
* In MIUI, "Failure [INSTALL_FAILED_USER_RESTRICTED: Install canceled by user]" occurs during installation of LegacyWhatsapp.apk, fix it by [allowing install via adb](https://github.com/YuvrajRaghuvanshiS/WhatsApp-Key-Database-Extractor/issues/16#issuecomment-768927639)
* If "[INSTALL_FAILED_VERSION_DOWNGRADE]" run with `--allow-reboot` flag.

  ```
  python3 wa_kdbe.py --allow-reboot
  ```
* If "[INSTALL_PARSE_FAILED_NOT_APK]" delete helpers/LegacyWhatsApp.apk and re-run.
* If "adb: error: cannot create 'tmp/WhatsAppbackup.apk': Permission denied" on macOS run script with `sudo`.

  ```
  sudo python3 wa_kdbe.py
  ```


![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

## Roadmap

See the [open issues](https://github.com/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor/issues) for a list of proposed features (and known issues).

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

## Limitations

There always are limitations on how much we can make it work  and this is what allows us to keep going. Well no matter what I do sometimes this tool just won't work on some devices and if that's your case you can try [this fork of MarcoG3's WhatsDump](https://github.com/Tkd-Alex/WhatsDump) by [Alessandro Maggio](https://github.com/Tkd-Alex/).

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. "Draft" a pull request and mark it "Ready for review" once work is done.

Other ways to contribute is to buy me a coffee but let's just say it is to test out new features of the project. **No new features to test.**

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

## License

Distributed under the MIT License. See [`LICENSE`](https://github.com/YuvrajRaghuvanshiS/WhatsApp-Key-Database-Extractor/blob/master/LICENSE) for more information.

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

## Agreement

I made this project because it was hard for me to kill time and the other one was very old. 
This tool is provided "as-is" and hence you will be responsible however you use it. Cheers☕

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

## Contact

Yuvraj Raghuvanshi - [@Yuvraj_R_S](https://twitter.com/Yuvraj_R_S) - [Send me a mail](mailto:YuvrajRaghuvanshi.S%40protonmail.com?subject=From%20GitHub%20WA-KDBE%20:%20%3CAdd%20subject%20here.%3E "Send me a mail, Don't change subject line.")

Project Link: [https://github.com/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor](https://github.com/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor)

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

[license-url]: https://github.com/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor/blob/master/LICENSE
[product-screenshot]: https://raw.githubusercontent.com/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor/master/helpers/banner.png
