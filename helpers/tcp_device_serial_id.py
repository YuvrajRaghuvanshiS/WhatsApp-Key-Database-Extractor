import os
import platform
import subprocess as sp

from custom_ci import custom_print, custom_input


def init(tcp_ip, tcp_port):
    custom_print('>>> I am in tcp_device_serial_id.init(tcp_ip=' +
                 tcp_ip + ', tcp_port=' + tcp_port + ')', is_print=False)
    # Detect OS
    is_windows = False
    is_linux = False
    if platform.system() == 'Windows':
        is_windows = True
    if platform.system() == 'Linux':
        is_linux = True

    # Global command line helpers
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    root_dir = os.path.abspath(os.path.join(curr_dir, '..'))

    if(is_windows):
        adb = root_dir + '\\bin\\adb.exe'
    else:
        adb = 'adb'

    combo = tcp_ip + ':' + tcp_port
    cmd = adb + ' connect ' + combo
    os.system(adb + ' kill-server')
    os.system(adb + ' start-server')
    proc = sp.Popen(cmd.split(), stdin=sp.PIPE, stdout=sp.PIPE,
                    stderr=sp.PIPE, shell=False)
    output, error = proc.communicate()
    output = output.decode('utf-8')
    error = error.decode('utf-8')

    if len(output) == 0 or error:
        output = None
        custom_print(error, 'red')
        kill_me()
    else:
        output = [x.strip() for x in output.split() if len(x.strip()) > 0]

    if('connected' in (x.lower() for x in output)):
        return combo
    if('authenticate' in (x.lower() for x in output)):
        custom_print(
            'Device unauthorized. Please check the confirmation dialog on your device.', 'red')
        kill_me()
    if('refused' in (x.lower() for x in output)):
        custom_print(
            'Could not find any connected device. Either USB Debugging is off or device is not running ADB over TCP', 'red')
        return ''

    ''' Possible outputs
    ['connected', 'to', '192.168.43.130:5555']
    ['failed', 'to', 'authenticate', 'to', '192.168.43.130:5555'] 
    ['cannot', 'connect', 'to', '192.168.43.130:5555:', 'No', 'connection', 'could', 'be', 'made', 'because', 'the', 'target', 'machine', 'actively', 'refused', 'it.', '(10061)']
    '''


def kill_me():
    custom_print('>>> I am in tcp_device_serial_id.kill_me()', is_print=False)
    custom_print('\n', is_get_time=False)
    custom_print('Exiting...')
    custom_input('Hit \"Enter\" key to continue....', 'cyan')
    quit()
