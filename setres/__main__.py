import subprocess
import re

REGEX_PORTS = re.compile(r'^([eA-Z\-]+\d+) (connected|disconnected) (primary|).+?$([0-9x *\n\.\+i_]+)', re.MULTILINE)


class Mode:
    def __init__(self, name, width, height, rate, interlaced, custom, current):
        self.name = name
        self.width = width
        self.height = height
        self.rate = rate
        self.interlaced = interlaced
        self.custom = custom
        self.current = current

    def __repr__(self):
        return '<Mode {} {}x{} {}>'.format(self.name, self.width, self.height, self.rate)


class Port:
    def __init__(self, name, status, primary, resolutions):
        self.name = name
        self.connected = status == 'connected'
        self.primary = primary == 'primary'
        self.modes = []
        self._parse_resolutions(resolutions)

    def _parse_resolutions(self, raw):
        for row in raw.strip().splitlines():
            row = row.strip()
            parts = re.split('\s+', row)

            width, height = parts[0].split('x')
            custom = False
            if '_' in height:
                custom = True
                height, name_rate = height.split('_')

            interlaced = False
            if 'i' in height:
                interlaced = True
                height = height.replace('i', '')

            width = int(width)
            height = int(height)
            rates = parts[1:]
            for rate in rates:
                current = False
                if '*' in rate:
                    current = True
                rate = rate.replace('+', '').replace('*', '')
                if rate.strip() == '':
                    continue
                rate = float(rate)
                self.modes.append(Mode(parts[0], width, height, rate, interlaced, custom, current))

    def has_mode(self, width, height, rate=None, interlaced=False):
        for mode in self.modes:
            if mode.width == width and mode.height == height and mode.interlaced == interlaced:
                if rate and not mode.rate == rate:
                    continue
                return True
        return False

    def add_mode(self, width, height, rate=None):
        if not rate:
            rate = 60.0

        command = ['cvt', str(width), str(height), str(rate)]
        modeline = subprocess.check_output(command, universal_newlines=True)
        modeline = modeline.splitlines()[1].replace('Modeline ', '')

        command = 'xrandr --newmode ' + modeline
        subprocess.check_call(command, shell=True)

        mode_name = modeline.split(' ')[0].replace('"', '')
        command = ['xrandr', '--addmode', self.name, mode_name]
        subprocess.check_call(command)

    def get_mode(self):
        for mode in self.modes:
            if mode.current:
                return mode

    def set_mode(self, width, height, rate=None, interlaced=False):
        for mode in self.modes:
            if mode.width == width and mode.height == height and mode.interlaced == interlaced:
                if rate and not mode.rate == rate:
                    continue

                command = ['xrandr', '--output', self.name, '--mode', mode.name]
                subprocess.check_output(command)

    def __repr__(self):
        return '<Port {}>'.format(self.name)


def get_ports():
    output = subprocess.check_output(['xrandr'], universal_newlines=True)
    ports = REGEX_PORTS.findall(output)
    port_objects = []
    for port in ports:
        port = Port(*port)
        port_objects.append(port)
    return port_objects


def main():
    import argparse
    import time

    ports = get_ports()
    primary = None
    port_list = []
    for port in ports:
        port_list.append(port.name)
        if port.primary:
            primary = port.name

    parser = argparse.ArgumentParser(description="Xorg display resolution tool")
    parser.add_argument('width', type=int, help="Horisontal resolution")
    parser.add_argument('height', type=int, help="Vertical resolution")
    parser.add_argument('--rate', type=float, help='Refresh rate')
    parser.add_argument('--port', type=str, help="Use this port if multiple exist", default=primary, choices=port_list)
    parser.add_argument('--interlaced', action='store_true', help='Make the resolution interlaced', default=False)
    parser.add_argument('--safe', action='store_true', help='Try the mode for 20 seconds and return to old mode',
                        default=False)
    args = parser.parse_args()

    active_port = None
    for port in ports:
        if port.name == args.port:
            active_port = port

    if not active_port.has_mode(args.width, args.height, args.rate, args.interlaced):
        print("This mode does not exist for port {}".format(args.port))
        if args.interlaced:
            print("Cannot create interlaced resolutions")
            exit(1)
        print("Adding new mode to {}".format(active_port.name))
        active_port.add_mode(args.width, args.height, args.rate)

    current_mode = active_port.get_mode()
    active_port.set_mode(args.width, args.height, args.rate, args.interlaced)
    if args.safe:
        time.sleep(20)
        active_port.set_mode(current_mode.width, current_mode.height, current_mode.rate, current_mode.interlaced)


if __name__ == '__main__':
    main()
