__author__ = 'Yuvraj Raghuvanshi'

__license__ = 'MIT'
__version__ = '2.0.0'
__maintainer__ = 'Yuvraj Raghuvanshi'
__email__ = 'YuvrajRaghuvanshi.S@protonmail.com'
__status__ = 'Production'


import json
import os
import re
import subprocess
from subprocess import check_output, getoutput

# TODO: Docstrings.

try:
    import requests
    from packaging import version
    from tqdm import tqdm
except ImportError:
    try:
        os.system('pip3 install packaging requests tqdm')
    except:
        os.system('python3 -m pip install packaging requests tqdm')

# FIXME: # from custom_ci import CustomCI
from custom_ci import custom_input, custom_print


class Handler():
    # Handler Variables
    urls = {
        'whatsapp_cdn': {
            'url': 'https://web.archive.org/web/20141111030303if_/http://www.whatsapp.com/android/current/WhatsApp.apk',
            'content_length': 0
        },
        'whatscrypt_cdn': {
            'url': 'https://whatcrypt.com/WhatsApp-2.11.431.apk',
            'content_length': 0
        }
    }
    folders = {
        'tmp': 'tmp/',
        'helpers': 'helpers/'
    }

    def __init__(self, platform: str) -> None:
        # def __init__(self, ci_obj: CustomCI, platform: str) -> None:
        """This class handles/manages WhatsApp in phone. 

        Args:
            * ci_obj (CustomCI): This helps to get custom_input and custom_print methods with re-initializing CustomCI object.
            * platform (str): Windows/Linux.
        """
        # Variable assignments.
        # custom_input = ci_obj.custom_input
        # custom_print = ci_obj.custom_print
        self.platform = platform

        # Log method invocation.
        try:
            # FIXME: ci_obj's class attributes are not getting printed.
            custom_print(
                f'>>> I am in Handler.__init__(\n\tci_obj={Handler.get_obj_json("ci_obj")},\n\tplatform={platform}\n)', is_print=False)
        except Exception as e:
            custom_print(
                '>>> I am in Handler.__init__() and could not get arguments.', is_print=False)
            custom_print(e, is_print=False)
            custom_print('\n', is_get_time=False)

        # Define adb.
        if self.platform == 'Windows':
            # FIXME: Find other occurrence.
            self.adb = 'bin\\adb.exe'
        else:
            self.adb = 'adb'

    def after_connect(self):
        # Log method invocation.
        try:
            custom_print(
                f'>>> I am in Handler.after_connect(\n\tself={Handler.get_obj_json(self)}\n)', is_print=False)
        except Exception as e:
            custom_print(
                '>>> I am in Handler.after_connect() and could not get arguments.', is_print=False)
            custom_print(e, is_print=False)
            custom_print('\n', is_get_time=False)

        self.sdk_version = int(
            getoutput(f'{self.adb} -s {self.serial_id} shell getprop ro.build.version.sdk'))

        if (self.sdk_version <= 13):
            custom_print(
                'Unsupported device. This method only works on Android v4.0 or higher.', 'red')
            custom_print(
                f'Cleaning up {Handler.folders["tmp"]} folder.', 'red')

            # FIXME: Machine independent delete.
            os.system(
                'rm -rf tmp/*') if self.platform == 'Linux' else os.remove(Handler.folders['tmp'])
            self.kill_me()

        _wa_path_text = f'{self.adb} -s  {self.serial_id} shell pm path com.whatsapp'
        proc = subprocess.Popen(_wa_path_text.split(), stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        out, err = proc.communicate()
        out = out.decode('utf-8')

        if(not out):
            custom_print(
                'Looks like WhatsApp is not installed on device.', 'red')
            self.kill_me()

        self.whatsapp_apk_path = re.search(
            '(?<=package:)(.*)(?=apk)', getoutput(_wa_path_text)).group(1) + 'apk'

        _version_name_text = f'{self.adb} -s {self.serial_id} shell dumpsys package com.whatsapp'
        if(self.platform == 'Windows'):
            self.version_name = re.search("(?<=versionName=)(.*?)(?=\\\\r)", str(check_output(
                f'{self.adb} shell dumpsys package com.whatsapp'))).group(1)
        else:
            self.version_name = re.search(
                "(?<=versionName=)(.*?)(?=\\\\n)", getoutput(_version_name_text)).group(1)

        custom_print(
            f'WhatsApp V{self.version_name} installed on device.')

        if (version.parse(self.version_name) > version.parse('2.11.431')):
            if not (os.path.isfile(f'{Handler.folders["helpers"]}LegacyWhatsApp.apk')):
                custom_print(
                    f'Downloading legacy WhatsApp V2.11.431 to {Handler.folders["helpers"]} folder')
                self.download_apk()
                # wget.download(downloadAppFrom, 'helpers/LegacyWhatsApp.apk')
                custom_print('\n', is_get_time=False)

            else:
                custom_print(
                    f'Found legacy WhatsApp V2.11.431 apk in {Handler.folders["helpers"]} folder.')

        else:
            # Version lower than 2.11.431 installed on device.
            pass

        # Else return False
        return True, self.sdk_version, self.whatsapp_apk_path, self.version_name

    def could_not_download(self):
        # Log method invocation.
        try:
            custom_print(
                f'>>> I am in Handler.could_not_download(\n\tself={Handler.get_obj_json(self)}\n)', is_print=False)
        except Exception as e:
            custom_print(
                '>>> I am in Handler.could_not_download() and could not get arguments.', is_print=False)
            custom_print(e, is_print=False)
            custom_print('\n', is_get_time=False)

        custom_print(
            '\aFor some reason I could not download Legacy WhatsApp, you need to download it on your own now from either of the links given below: ', 'red')
        custom_print('\n', is_get_time=False)
        custom_print(Handler.urls)
        custom_print('\n', is_get_time=False)
        custom_print(
            f'Once downloaded rename it to \"LegacyWhatsApp.apk\" exactly and put in {Handler.folders["helpers"]} folder.', 'red')
        self.kill_me()

    def download_apk(self):
        # Log method invocation.
        try:
            custom_print(
                f'>>> I am in Handler.download_apk(\n\tself={Handler.get_obj_json(self)}\n)', is_print=False)
        except Exception as e:
            custom_print(
                '>>> I am in Handler.download_apk() and could not get arguments.', is_print=False)
            custom_print(e, is_print=False)
            custom_print('\n', is_get_time=False)

        # TODO: Remove curl dependency.
        custom_print(
            'Checking for availability of whatsapp online, may take time....')
        self.url = ''
        try:
            r = requests.head(Handler.urls['whatsapp_cdn']['url'])
            Handler.urls['whatsapp_cdn']['content_length'] = r.headers['content-length']
            self.url = Handler.urls['whatsapp_cdn']['url'] if(
                Handler.urls['whatsapp_cdn']['content_length'] == '18329558') else ''

        except:
            custom_print(
                'Official WhatsApp\'s mirror from \"Archive.org\" seems to be down. Checking \"WhatsCrypt.com\" instead.', 'red')

            try:
                r = requests.head(Handler.urls['whatscrypt_cdn']['url'])
                Handler.urls['whatscrypt_cdn']['content_length'] = r.headers['content-length']
                self.url = Handler.urls['whatscrypt_cdn']['url'] if(
                    Handler.urls['whatscrypt_cdn']['content_length'] == '18329558') else ''

            except:
                custom_print(
                    'WhatsCrypt is also down.', 'red')
                self.could_not_download()

        finally:
            custom_print('\n', is_print=False)
            custom_print(
                f'>>> I have chosen url={self.url}.', is_print=False)
            custom_print('\n', is_print=False)

        # Streaming, so we can iterate over the response.
        response = requests.get(self.url, stream=True)
        total_size_in_bytes = response.headers.get(
            'x-archive-orig-content-length') or response.headers.get('content-length', 0)

        if(total_size_in_bytes):
            # Fixed where it stuck on "Downloading legacy WhatsApp V2.11.431 to helpers folder"
            total_size_in_bytes = int(total_size_in_bytes)

        else:
            # total_size_in_bytes must be null
            self.could_not_download()

        block_size = 1024  # 1 Kibibyte
        progress_bar = tqdm(total=total_size_in_bytes,
                            unit='iB', unit_scale=True)
        with open(f'{Handler.folders["helpers"]}temp.apk', 'wb') as f:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                f.write(data)
        progress_bar.close()
        os.rename(f'{Handler.folders["helpers"]}temp.apk',
                  f'{Handler.folders["helpers"]}LegacyWhatsApp.apk')
        custom_print('')

        if (total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes):
            custom_print(
                '\aSomething went during downloading LegacyWhatsApp.apk.')
            self.kill_me()

    def get_obj_json(obj):
        return json.dumps(obj,
                          default=lambda obj: vars(obj),
                          indent=2).replace('\n', f'\n  ')

    def handle(self, serial_id: str):
        """
        How do I explain this?

        - Arguments:
            * serial_id {str}: ADB device id retrieved from SerialID class.

        - Returns: 
            * return_code {bool}: True if everything goes well.
            * sdk_version {int}: Android sdk version of device.
            * whatsapp_apk_path {str}: Original WhatsApp's path in device.
            * version_name {str}: Original WhatsApp's version.
            * sdcard_path {str}: sdcard path of device, defaults to '/sdcard'.
        """

        # Variables assignment.
        self.serial_id = serial_id
        # Log method invocation.
        try:
            custom_print(
                f'>>> I am in Handler.handle(\n\tself={Handler.get_obj_json(self)},\n\tserial_id={serial_id}\n)', is_print=False)
        except Exception as e:
            custom_print(
                '>>> I am in Handler.handle() and could not get arguments.', is_print=False)
            custom_print(e, is_print=False)
            custom_print('\n', is_get_time=False)

        custom_print(
            'Connected to ' + getoutput(f'{self.adb} -s {self.serial_id} shell getprop ro.product.model') + '.')
        return self.after_connect()

    def kill_me(self):
        custom_print(
            f'>>> I am in Handler.kill_me(\n\tself={Handler.get_obj_json(self)}\n)', is_print=False)
        custom_print('\n', is_get_time=False)
        custom_print('Exiting...')
        os.system(f'{self.adb} kill-server')
        custom_print(
            'Turn off USB debugging [and USB debugging (Security Settings)] if you\'re done.', 'cyan')
        custom_input('Hit \"Enter\" key to continue....', 'cyan')
        quit()
