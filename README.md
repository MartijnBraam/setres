# setres

This is a small command line tool to change the resolution for an xorg display, adding the resolution if necessary.

## Usage

```bash
# Set the primary monitor to 1080p
$ setres 1920 1080

# Set the first VGA port to 1080p
$ setres --port VGA1 1920 1080

# Gloat about your expensive hardware. Setting to UHD @ 140Hz
$ setres --port DP1 --rate 140 3840 2160

# For your own safety set the --save flag
$ setres --port VGA1 --save 1280 1280
# This sets the resolution for 20 seconds and then changes it back to the previous setting.

# For setting 1080i
$ setres --port HDMI1 --interlaced 1920 1080
```

## Installation

Install the tool through pypi. 

```bash
$ pip3 install setres
```

The tools also depends on the `xrandr` and `cvt` command.