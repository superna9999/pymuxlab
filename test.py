#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymuxlab.pymuxlab import *
from struct import Struct, unpack, pack

if __name__ == '__main__':
    dev = HDMIAnalyser("/dev/ttyUSB0", 0, 0)

    print("Volume Level %d" % dev.getVolumeLevel())
    print("Standby Status: %d (0=On, 1=Off)" % dev.getStandbyStatus())
    print("Source Type: %d (0=HDMI, 1=SDI)" % dev.getSourceType())
    print("Signal Info:\n%s" % dev.getSignalInfo())
    print("Timings:\n%s" % dev.getTimings())
    print("AVI InfoFrame: %s" % dev.getSignalPackageInfo(HDMIAnalyser.SIGNAL_PACKAGE_INFO_INDEX_AVI))
    print("Picture: %s" % dev.getPicture())
    print("Monitoring Data: %s" % dev.getMonitoringData())
    print("Pixel 0:0 RGB: %s" % dev.getPixelRGB(0, 0))
    print("Battery Voltage: %d" % dev.getBatteryVoltage())
    print("External 5V Input:\n%s" % dev.getGetExternal5VInput())
    print("Signal Status: %d (0=Invalid 1=Valid)" % dev.getSignalStatus())
    addr = dev.getAddr()
    print("Device Address: %d:%d" % (addr[0], addr[1]))
    version = dev.getVersion()
    print("Version: %s.%d" % (int(version[0]), int(version[1])))
    print("EDID Configuration: %d" % dev.getEDIDNumber())
    print("EDID: %s" % dev.getEDID(dev.getEDIDNumber()))
    version = dev.getFirmwareInfo(HDMIAnalyser.COMPONENT_RELEASE)
    print("Firmare Info Release: %s.%d" % (version[0], version[1]))
    version = dev.getFirmwareInfo(HDMIAnalyser.COMPONENT_MAIN_MCU)
    print("Firmare Info Main MCU: %s.%d" % (version[0], version[1]))
    version = dev.getFirmwareInfo(HDMIAnalyser.COMPONENT_MAIN_FPGA)
    print("Firmare Info Main FPGA: %s.%d" % (version[0], version[1]))
    version = dev.getFirmwareInfo(HDMIAnalyser.COMPONENT_POWER_MNG_BOARD)
    print("Firmare Info Power Management Board: %s.%d" % (version[0], version[1]))
