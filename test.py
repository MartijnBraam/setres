testdata = """Screen 0: minimum 8 x 8, current 1280 x 1024, maximum 16384 x 16384
   1680x1050     59.95 +
   1440x900      74.98    59.89
   1280x1024     75.02*   60.02
   1280x960      60.00
   1152x864      75.00
   1024x768      75.03    70.07    60.00
   800x600       75.00    72.19    60.32    56.25
   640x480       75.00    72.81    59.94
HDMI-0 disconnected (normal left inverted right x axis y axis)
DP-0 disconnected (normal left inverted right x axis y axis)
DP-1 disconnected (normal left inverted right x axis y axis)
DVI-D-0 disconnected (normal left inverted right x axis y axis)
  1280x1024_60.00 (0x274) 109.000MHz -HSync +VSync
        h: width  1280 start 1368 end 1496 total 1712 skew    0 clock  63.67KHz
        v: height 1024 start 1027 end 1034 total 1063           clock  59.89Hz
"""

from setres.__main__ import Port, REGEX_PORTS

for result in REGEX_PORTS.findall(testdata):

    testport = Port(*result)
