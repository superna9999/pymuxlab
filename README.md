MuxLab HDMI/SDI Signal Analyser Management Library
==================================================

This is an attempt to control the MuxLab HDMI/SDI Signal Analyser model 500831
from Linux or Whatever OS and from CLI.

The current support is :
- Get/Set Volume level
- Get timings and frequency
- Get HDMI/SDI source type
- Get HPD standby status
- Get Picture DATA
- Get Selected EDID mode
- Get Selected EDID content
- Basic Address management
- Support for long frames (>256)
- Set HDMI/SDI source type
- Set HPD standby status
- Get full stream information (audio, HDR, HDCP, ...)
- Get AVI frame (AVI InfoFrame, ...)
- Monitor stream
- Set Custom EDID

Python3 is mandatory.

A single utility called `muxlab-hdmi` is provided to control the HDMI Analyser.

```
usage: muxlab-hdmi [-h] [--version] [--tty TTY] [--group GROUPADDR]
                   [--device DEVICEADDR] [--baudrate BAUDRATE] [--file FILE]
                   [--ratio RATIO] [--edid EDID]
                   {system,source,edid,picture,image,standby-on,standby-off,volume-up,volume-down,change-edid}

MuxLab HDMI Analyser Tool

positional arguments:
  {system,source,edid,picture,image,standby-on,standby-off,volume-up,volume-down,change-edid}
                        Command to run

optional arguments:
  -h, --help            show this help message and exit
  --version, -v         show program's version number and exit
  --tty TTY             tty device to use (default /dev/ttyUSB0) (default:
                        /dev/ttyUSB0)
  --group GROUPADDR     Group Address (default 0) (default: 0)
  --device DEVICEADDR   Device Address (default 0) (default: 0)
  --baudrate BAUDRATE   Baudrate (default 115200) (default: 115200)
  --file FILE           File to save EDID or Picture (default: out.bin)
  --ratio RATIO         Image dump ratio (default 4) (default: 4)
  --edid EDID           EDID Slot to select (no default) (default: None)
```

Useful commands:
- Dump device informations :

```
$ ./muxlab-hdmi system
Device Address: 0:0
Version: 1.0
Volume Level 8
Firmare Info Release: 248.3
Firmare Info Main MCU: 248.3
Firmare Info Main FPGA: 248.3
Firmare Info Power Management Board: 248.3
External 5V Input:
b'\x99\x80\x02'
Battery Voltage: 329
Standby Status: 0 (0=On, 1=Off)
```

- Dump Source informations :

```
$ ./muxlab-hdmi source
Signal Status: 1 (0=Invalid 1=Valid)
Source Type: 0 (0=HDMI, 1=SDI)
Signal Info:
Color Space: YUV444
Color Depth: 24bit
HDCP: Clear
Source: DVI
Audio Rate:Invalid Width:Invalid Channels:Invalid Type:Invalid
Mode: 2D
Pixel Repetition: 1x
Timings:
Video clock: 593960KHz
Mode Flags: HSync+ VSync+ 
Horizontal:
	Active:3840 Blank:560
	Sync Offset:176 Width:88
Vertical:
	Active:2160 Blank:90
	Sync Offset:8 Width:10
Detected Mode: CEA-VIC-97 (3840x2160@60Hz)
```

- Dump current EDID to file

```
$ ./muxlab-hdmi edid --file edid.bin
EDID Configuration: 5
Current EDID written to edid.bin
```

- Change EDID slot

```
$ ./muxlab-hdmi change-edid --edid 2
Current EDID Slot: 5
New EDID Slot: 2
```

- Pump up the volume

```
$ ./muxlab-hdmi volume-up
Volume: 8
```

- Control the Standby

```
$ ./muxlab-hdmi standby-on
$ ./muxlab-hdmi standby-off
```
