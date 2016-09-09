import subprocess
import re

REGEX_PORTS = re.compile(r'^([A-Z]+\d+) (connected|disconnected) (primary|)', re.MULTILINE)


def get_ports():
    output = subprocess.check_output(['xrandr'], universal_newlines=True)
    ports = REGEX_PORTS.findall(output)
    return ports


if __name__ == '__main__':
    import argparse

    ports = get_ports()
    primary = None
    port_list = []
    for port in ports:
        port_list.append(port[0])
        if port[2] == "primary":
            primary = port[0]

    parser = argparse.ArgumentParser(description="Xorg display resolution tool")
    parser.add_argument('width', type=int, help="Horisontal resolution")
    parser.add_argument('height', type=int, help="Vertical resolution")
    parser.add_argument('--fps', type=float, help='Refresh rate')
    parser.add_argument('--port', type=str, help="Use this port if multiple exist", default=primary, choices=port_list)
    args = parser.parse_args()
