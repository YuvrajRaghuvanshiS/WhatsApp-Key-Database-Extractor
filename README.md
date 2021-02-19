![GitHub repo size](https://img.shields.io/github/repo-size/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor?color=informational&label=Repo%20Size)
![GitHub top language](https://img.shields.io/github/languages/top/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor)
![License](https://img.shields.io/github/license/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor?label=License)
![Depends](https://img.shields.io/badge/Depends-JAVA-informational)


<br />

![Termux](https://img.shields.io/badge/Termux-Beta-red)

# Currently still in developing phase!
# This "Termux Edition" is currently not maintained!

# For this to work on Android devices with Android below version 11, the user first needs to run 'adb tcpip 5555' from their computer which defeats the entire purpose of "no computer" for android devices with android version < 11.

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor">
    <img src="https://raw.githubusercontent.com/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor/termux/helpers/banner.png" alt="Logo" width="200" height="150">
  </a>

  <h3 align="center">WhatsApp Key/DB Extractor Termux Edition (Beta)</h3>

  <p align="center">
    Extract key/msgstore.db from /data/data/com.whatsapp without root.
    <br />
</p>


![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

<details><summary>Table of Contents</summary>

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
  * [Troubleshooting](#troubleshooting)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Agreement](#agreement)
* [Contact](#contact)
</details>

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

## About The Project

[![Glimpse][product-screenshot]](https://github.com/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor)

This project is inspired by [EliteAndroidApps/WhatsApp-Key-DB-Extractor](https://github.com/EliteAndroidApps/WhatsApp-Key-DB-Extractor). Since Android v4.0+ Google has removed adb backup  and apps no longer supported being abcked up by "adb backup -f myApp.ab -apk com.foobar.app". However there is one catch in this scenario and that is some old version of many apps including WhatsApp support that to this day, and that's the idea...

The idea is to install "Legacy Version" of WhatsApp on you device via adb and use "adb backup"  to fetch files from "/data/data/com.whatsapp" folder which includes both the 'key' and 'msgstore.db' (non encrypted) file and after that restore current WhatsApp.

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

### Built With
* [Python](https://www.python.org/)
* [Bash](https://www.gnu.org/software/bash/)
#### Depends upon    
* [Java](https://github.com/Hax4us/java/) (To extract backup)

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

## Getting Started

Before doing anything take a backup of your chats and turn off your phone's internet so you don't lose any new messages.
For that go to 'WhatsApp settings\Chat Settings\Chat Backup' here take a local bacakup. Prepare for the worst.               
After [intallation](#installation) follow on screen instructions.

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

### Prerequisites

* USB Debugging must be enabled on the target device. Settings -> Developer Options -> (Debugging) USB debugging  
     If you cannot find Developer Options then please go to: Settings -> About phone/device and tap the Build number multiple times until you're finally declared a developer. 
* Android device with Android 11 or higher with activated 'ADB over network' setting. Settings -> Developer Options -> ADB over network
* OR an Android device with Android 4 to 10 (i.e. Ice Cream Sandwich, Jelly Bean, KitKat, Lollipop, Marshmallow, Nougat, Oreo, Pie, Q) AND a PC with USB functionality and installed [Android Debug Bridge for PC](https://developer.android.com/studio/releases/platform-tools)
  * Run the following commands in a terminal opened in the 'platform-tools' folder. Authorize on your phone when prompted:
  * `adb devices`
  * `adb tcpip 5555`
* Termux : Install from [Play Store](https://play.google.com/store/apps/details?id=com.termux) or [F-Droid](https://f-droid.org/packages/com.termux)

Run the following commands in the Termux app:
* Python 3.x : `pkg install python -y`
* Proot : To make Java work `pkg install proot -y && proot login`
* [Java](https://github.com/Hax4us/java/) : `pkg update && pkg install wget -y && wget https://raw.githubusercontent.com/Hax4us/java/master/installjava && sh installjava`
* [ADB (Android Debug Bridge)](https://github.com/MasterDevX/Termux-ADB) Drivers : `pkg update && pkg install wget && wget https://github.com/MasterDevX/Termux-ADB/raw/master/InstallTools.sh && bash InstallTools.sh`  



![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

### Installation (Not working?)

0. Connect adb to your phone. Run the following command in the Termux window: `adb connect localhost`

1. Clone the repo
```
wget https://github.com/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor && cd WhatsApp-Key-Databse-Extractor
```
2. Get python requirements
```python
pip install -r requirements.txt
```
3. Get Termux dependencies (skip if already installed proot, adb, java etc.)
```python
python helpers/termux_dependencies.py
```
4. Run `wa-kdbe.py`
```python
python wa-kdbe.py
```
![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

### Troubleshooting

```sh
* daemon not running. starting it now on port 5037 *
* daemon started successfully *
List of devices attached 
0123a4b5678	device
emulator-5554 unauthorized
```
* Choose device from "List of devices attached" : 0123a4b5678
* If you have never used USB Debugging before, you may also need to verify the fingerprint.  
* If you have set a default backup password in your Android settings, then this MUST be the  backup password that you PROVIDE when prompted to backup your data. Else it WILL fail!  
* If you get an error saying "AES encryption not allowed" then you need to update your Oracle Java Cryptography Extension (JCE) to Unlimited Strength Jurisdiction Policy Files.  
* Try to keep screen on getting termux dependencies.
* WhatsApp crashing? Run `python3 restore_whatsapp.py`. Or "clear data/storage" / uninstall and reinstall from Play Store.


![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

## Roadmap

See the [open issues](https://github.com/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor/issues) for a list of proposed features (and known issues).

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

## License

Distributed under the MIT License. See `LICENSE` for more information.

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

## Agreement

I made this project because it was hard for me to kill time and the other one was very old. 
By using this project you agreed that you will be responsible for your actions however you perform them. Do not use this tool to creep on others. Cheers.

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

## Contact

Yuvraj Raghuvanshi - [Twitter](https://twitter.com/Yuvraj+R_S) - YuvrajRaghuvanshi.S@protonmail.com

Project Link: [https://github.com/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor](https://github.com/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor)

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

[license-url]: https://github.com/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor/blob/master/LICENSE
[product-screenshot]: https://raw.githubusercontent.com/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor/termux/helpers/banner.png

