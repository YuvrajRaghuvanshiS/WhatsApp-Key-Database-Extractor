<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![contributors-shield]](contributors-url)
[![forks-shield]](forks-url)
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor">
    <img src="https://raw.githubusercontent.com/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor/master/helpers/banner.png?token=AMT67DWEW6A5EEWXHOVNGGS7X73Q2" alt="Logo" width="320" height="100">
  </a>

  <h3 align="center">WhatsApp Key/DB Extractor</h3>

  <p align="center">
    Extract key/msgstore.db from /data/data/com.whatsapp without root.
    <br />
</p>

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)

<p align="center">
    <a href="https://github.com/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor">View Demo</a>
    ·
    <a href="https://github.com/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor/issues">Report Bug</a>
    ·
    <a href="https://github.com/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor/issues">Request Feature</a>
  </p>
</p>


![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)


<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
  * [Troubleshooting](#troubleshooting)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)


![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/dark.png)


<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://github.com/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor)

This project is inspired by [EliteAndroidApps/WhatsApp-Key-DB-Extractor](https://github.com/EliteAndroidApps/WhatsApp-Key-DB-Extractor). Since Android v4.0+ Google has removed adb backup  and apps no longer supported being abcked up by "adb backup -f myApp.ab -apk com.foobar.app". However there is one catch in this scenario and that is some old version of many apps including WhatsApp support that to this day, and that's the idea...

The idea is to install "Legacy Version" of WhatsApp on you device via adb and use "adb backup"  to fetch files from "/data/data/com.whatsapp" folder which includes both the 'key' and 'msgstore.db' (non encrypted) file and after that restore current WhatsApp.

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/dark.png)

### Built With
* [Python](https://www.python.org/)
* [Bash](https://www.gnu.org/software/bash/)
    ##### Depends upon    
    * [Java](https://www.java.com/)

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/dark.png)

<!-- GETTING STARTED -->
## Getting Started

After [intallation](#installation) follow on screen instructions.

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/dark.png)

### Prerequisites

* O/S: Windows Vista, Windows 7, Windows 8, Windows 10, Mac OS X or Linux  
* Java - If not installed [click here](https://www.java.com/en/download/)
* ADB (Android Debug Bridge) Drivers [download here](https://developer.android.com/studio/releases/platform-tools) 
* USB Debugging must be enabled on the target device. Settings -> Developer Options -> (Debugging) USB debugging  
     If you cannot find Developer Options then please go to: Settings -> About phone/device and tap the Build number  
     multiple times until you're finally declared a developer.  
* Android device with Android 4.0 or higher. i.e. Ice Cream Sandwich, Jelly Bean, KitKat, Lollipop, Marshmallow, Nougat, Oreo, Pie, Q.  


![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/dark.png)

### Installation

1. Clone the repo
```sh
git clone https://github.com/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor.git
```
2. Get python requirements
```sh
python3 -m pip install -r requirements.txt
```
3. Run `wa-kdbe.py`
```JS
python3 wa-kdbe.py
```
![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/dark.png)

### Troubleshooting
* If you have never used USB Debugging before, you may also need to verify the fingerprint.  
* If you have set a default backup password in your Android settings, then this MUST be the  backup password that you PROVIDE when prompted to backup your data. Else it WILL fail!  
* If you get an error saying "AES encryption not allowed" then you need to update your Oracle Java Cryptography Extension (JCE) to Unlimited Strength Jurisdiction Policy Files.  
* Stuck on Linux dependencies installation? Run `bash bin/linux_dependencies.sh` from main directory.
* WhatsApp crashing? Run `python3 restore_whatsapp.py`. Or "clear data/storage" / uninstall and reinstall from Play Store.

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/dark.png)

<!-- USAGE EXAMPLES -->
## Usage

Working on passing params... Make a fork send pulls. Send Help.

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/dark.png)

<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor/issues) for a list of proposed features (and known issues).

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/dark.png)

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/dark.png)

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/dark.png)

<!-- CONTACT -->
## Contact

Yuvraj Raghuvanshi - [Twitter](https://twitter.com/Yuvraj+R_S) - YuvrajRaghuvanshi.S@protonmail.com

Project Link: [https://github.com/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor](https://github.com/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor)

![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/dark.png)

<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
* [Img Shields](https://shields.io)
* [Choose an Open Source License](https://choosealicense.com)
* [GitHub Pages](https://pages.github.com)
* [Animate.css](https://daneden.github.io/animate.css)
* [Loaders.css](https://connoratherton.com/loaders)
* [Slick Carousel](https://kenwheeler.github.io/slick)
* [Smooth Scroll](https://github.com/cferdinandi/smooth-scroll)
* [Sticky Kit](http://leafo.net/sticky-kit)
* [JVectorMap](http://jvectormap.com)
* [Font Awesome](https://fontawesome.com)





<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor?style=flat-square&label=Contributors
[contributors-url]: https://github.com/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor?label=Fork
[forks-url]: https://github.com/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor/network/members
[stars-shield]: https://img.shields.io/github/stars/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor?label=Stars
[stars-url]: https://github.com/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor/stargazers
[issues-shield]: https://img.shields.io/github/issues/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor?label=Issues
[issues-url]: https://github.com/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor/issues
[license-shield]: https://img.shields.io/github/license/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor?label=License
[license-url]: https://github.com/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/YuvrajRaghuvanshiS
[product-screenshot]: https://raw.githubusercontent.com/yuvrajraghuvanshis/WhatsApp-Key-Database-Extractor/master/helpers/banner.png?token=AMT67DWEW6A5EEWXHOVNGGS7X73Q2
