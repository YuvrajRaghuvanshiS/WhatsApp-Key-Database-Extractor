import json
import os
from platform import platform
import subprocess
from custom_ci import custom_input, custom_print


class SerialID():
    def __init__(self, conn_type: str, platform: str, ip_port: str = '') -> None:
        """Get ADB device ID.

        Args:
            conn_type (str): Either of TCP/USB.\n
            platform (str): Windows/Linux.\n
            ip_port (str): In case of TCP, in form of IP:Port.\n
        """
        # Variables assignment.
        self.ip_port = ip_port
        self.conn_type = conn_type
        self.platform = platform

        self.adb = 'bin\\adb.exe' if self.platform == 'Windows' else 'adb'
        # Log method invocation.
        try:
            custom_print(
                f'>>> I am in SerialID.__init__(adb={self.adb}, conn_type={self.conn_type}, ip_port={self.ip_port}, platform={self.platform})', is_print=False)
        except Exception as e:
            custom_print(
                '>>> I am in SerialID.__init__() and could not get arguments.', is_print=False)
            custom_print(e, is_print=False)
            custom_print('\n', is_get_time=False)

        os.system(f'{self.adb} kill-server')
        os.system(f'{self.adb} start-server')
        # TODO: In TCP connect first.

        if (self.conn_type == 'TCP'):
            cmd = f'{self.adb} connect {self.ip_port}'
        else:
            cmd = f'{self.adb} devices'

        proc = subprocess.Popen(cmd.split(), stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        out, err = proc.communicate()
        self.out = out.decode('utf-8')
        self.err = err.decode('utf-8')

        if len(self.out) == 0 or self.err:
            self.out = None
            custom_print(err, 'red')
            self.kill_me()
        else:
            self.out = [x.strip() for x in self.out.split('\n') if len(x.strip()) > 0] if(
                self.conn_type == 'USB') else [x.strip() for x in self.out.split() if len(x.strip()) > 0]

    def get_obj_json(obj):
        return json.dumps(obj,
                          default=lambda obj: vars(obj),
                          indent=2).replace('\n', '\n' + '  ')

    def kill_me(self):
        # Log method invocation.
        try:
            custom_print(
                f'>>> I am in SerialID.kill_me(\n\tself={SerialID.get_obj_json(self)}\n)', is_print=False)
        except Exception as e:
            custom_print(
                '>>> I am in SerialID.kill_me() and could not get arguments.', is_print=False)
            custom_print(e, is_print=False)
            custom_print('\n', is_get_time=False)

        custom_print(
            f'>>> I am in Handler.kill_me(\n\tself={SerialID.get_obj_json(self)}\n)', is_print=False)
        custom_print('\n', is_get_time=False)
        custom_print('Exiting...')
        os.system(f'{self.adb} kill-server')
        custom_print(
            'Turn off USB debugging [and USB debugging (Security Settings)] if you\'re done.', 'cyan')
        custom_input('Hit \"Enter\" key to continue....', 'cyan')
        quit()

    def tcp_mode(self):
        # Log method invocation.
        try:
            custom_print(
                f'>>> I am in SerialID.tcp_mode(\n\tself={SerialID.get_obj_json(self)}\n)', is_print=False)
        except Exception as e:
            custom_print(
                '>>> I am in SerialID.tcp_mode() and could not get arguments.', is_print=False)
            custom_print(e, is_print=False)
            custom_print('\n', is_get_time=False)

        if('connected' in (x.lower() for x in self.out)):
            return self.ip_port
        if('authenticate' in (x.lower() for x in self.out)):
            custom_print(
                'Device unauthorized. Please check the confirmation dialog on your device.', 'red')
            self.kill_me()
        else:
            custom_print(
                'Could not find any connected device. Either USB Debugging is off or device is not running ADB over TCP', 'red')
            custom_print(f'Out: {" ".join(self.out)}', 'red')
            custom_print(f'err: {" ".join(self.err)}', 'red')
            return ''

        # Possible outputs
        # ['connected', 'to', '192.168.43.130:5555']
        # ['failed', 'to', 'authenticate', 'to', '192.168.43.130:5555']
        # ['cannot', 'connect', 'to', '192.168.43.130:5555:', 'No', 'connection', 'could', 'be', 'made', 'because', 'the', 'target', 'machine', 'actively', 'refused', 'it.', '(10061)']

    def usb_mode(self):
        # Log method invocation.
        try:
            custom_print(
                f'>>> I am in SerialID.usb_mode(\n\tself={SerialID.get_obj_json(self)}\n)', is_print=False)
        except Exception as e:
            custom_print(
                '>>> I am in SerialID.usb_mode() and could not get arguments.', is_print=False)
            custom_print(e, is_print=False)
            custom_print('\n', is_get_time=False)

        if(len(self.out) == 1):
            custom_print(
                'Could not find any connected device. Is USB Debugging on?', 'red')
            return ''

        device_to_connect = None
        i = 1
        if(len(self.out) == 2):
            if(self.out[1].split()[1] == 'offline'):
                custom_print(
                    'Device is offline, try turning off USB debugging and turn on again.', 'yellow')
                self.kill_me()
            if(self.out[1].split()[1] == 'unauthorized'):
                custom_print(
                    'Device unauthorized. Please check the confirmation dialog on your device.', 'red')
                self.kill_me()
            return self.out[1].split()[0]

        custom_print(self.out[0])
        custom_print('\n', is_get_time=False)
        if device_to_connect is None:
            for device in self.out[1:]:
                name = f'{self.adb} -s {device.split()[0]} shell getprop ro.product.model'
                custom_print(
                    f'{i}. {device.split()[0]} | \t{device.split()[1]} | \t{subprocess.getoutput(name).strip()}')
                i += 1

        while device_to_connect is None:
            device_index = int(custom_input(
                'Enter device number (for ex: 2): '))
            if device_index <= 0 or device_index + 1 > len(self.out):
                continue
            device_to_connect = self.out[device_index]

        if(device_to_connect.split()[1] == 'offline'):
            custom_print(
                'Device is offline, try turning off USB debugging and turn on again.', 'yellow')
            self.kill_me()
        if(device_to_connect.split()[1] == 'unauthorized'):
            custom_print(
                'Device unauthorized. Please check the confirmation dialog on your device.', 'red')
            self.kill_me()
        return device_to_connect.split()[0]
