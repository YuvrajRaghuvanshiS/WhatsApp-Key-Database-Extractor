import os
import platform
import subprocess as sp

from custom_ci import custom_input, custom_print


def init(mode, tcp_ip="", tcp_port=""):
    custom_print(
        f">>> I am in device_serial_id.init(mode={mode}, tcp_ip{tcp_ip}, tcp_port={tcp_port})",
        is_print=False,
    )
    # Detect OS
    is_windows = False
    if platform.system() == "Windows":
        is_windows = True

    # Global command line helpers
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    root_dir = os.path.abspath(os.path.join(curr_dir, ".."))

    if is_windows:
        adb = f"{root_dir}\\bin\\adb.exe"
    else:
        adb = "adb"

    # Kill server before getting list to avoid daemon texts.
    os.system(f"{adb} kill-server")
    os.system(f"{adb} start-server")

    combo = f"{tcp_ip}:{tcp_port}"
    cmd = ""
    if mode == "USB":
        cmd = f"{adb} devices"
    elif mode == "TCP":
        cmd = f"{adb} connect {combo}"
    else:
        pass
        # FIXME: Wrong choice.
    proc = sp.Popen(
        cmd.split(), stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE, shell=False
    )
    output, error = proc.communicate()
    output = output.decode("utf-8")
    error = error.decode("utf-8")

    if len(output) == 0 or error:
        output = None
        custom_print(error, "red")
        kill_me()

    if mode == "USB":
        output = [x.strip() for x in output.split("\n") if len(x.strip()) > 0]

        if len(output) == 1:
            custom_print(
                "Could not find any connected device. Is USB Debugging on?", "red"
            )
            return ""

        device_to_connect = None
        if len(output) == 2:
            if output[1].split()[1] == "offline":
                custom_print(
                    "Device is offline, try turning off USB debugging and turn on again.",
                    "yellow",
                )
                kill_me()
            if output[1].split()[1] == "unauthorized":
                custom_print(
                    "Device unauthorized. Please check the confirmation dialog on your device.",
                    "red",
                )
                kill_me()
            return output[1].split()[0]

        custom_print(output[0])
        custom_print("\n", is_get_time=False)
        if device_to_connect is None:
            padding = f' {" " * 25}'
            for index, device in enumerate(output[1:]):
                serial = device.split()[0]
                state = device.split()[1]
                name = (
                    "Unknown"
                    if state == "unauthorized"
                    else sp.getoutput(
                        f"{adb} -s {device.split()[0]} shell getprop ro.product.model"
                    ).strip()
                )
                custom_print(
                    "{}. {:.15s} {:.15s} {}".format(
                        index + 1, serial + padding, state + padding, name
                    )
                )

        while device_to_connect is None:
            device_index = int(custom_input("Enter device number (for ex: 2): "))
            if device_index <= 0 or device_index + 1 > len(output):
                continue
            device_to_connect = output[device_index]

        if device_to_connect.split()[1] == "offline":
            custom_print(
                "Device is offline, try turning off USB debugging and turn on again.",
                "yellow",
            )
            kill_me()
        if device_to_connect.split()[1] == "unauthorized":
            custom_print(
                "Device unauthorized. Please check the confirmation dialog on your device.",
                "red",
            )
            kill_me()
        return device_to_connect.split()[0]

    elif mode == "TCP":
        output = [x.strip() for x in output.split() if len(x.strip()) > 0]
        if "connected" in (x.lower() for x in output):
            return combo
        if "authenticate" in (x.lower() for x in output):
            custom_print(
                "Device unauthorized. Please check the confirmation dialog on your device.",
                "red",
            )
            kill_me()
        if "refused" in (x.lower() for x in output):
            custom_print(
                "Could not find any connected device. Either USB Debugging is off or device is not running ADB over TCP",
                "red",
            )
            return ""
        """ Possible outputs
        ['connected', 'to', '192.168.43.130:5555']
        ['failed', 'to', 'authenticate', 'to', '192.168.43.130:5555']
        ['cannot', 'connect', 'to', '192.168.43.130:5555:', 'No', 'connection', 'could', 'be', 'made', 'because', 'the', 'target', 'machine', 'actively', 'refused', 'it.', '(10061)']
        """
    else:
        pass
        # FIXME: Wrong choice.


def kill_me():
    custom_print(">>> I am in device_serial_id.kill_me()", is_print=False)
    custom_print("\n", is_get_time=False)
    custom_print("Exiting...")
    custom_print(
        "Turn off USB debugging [and USB debugging (Security Settings)] if you're done.",
        "cyan",
    )
    custom_input('Hit "Enter" key to continue....', "cyan")
    quit()
