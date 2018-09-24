# -*- coding: utf-8 -*-
"""
MuxLab HDMI/SDI Signal Analyser Management Library

   Copyright 2018 BayLibre SAS
   Author: Neil Armstrong <narmstrong@baylibre.com>

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

@author: Neil Armstrong <narmstrong@baylibre.com>
"""

import string
import os
import serial
from struct import Struct, unpack, pack

# If DIRECT_GROUP_ADDR & DIRECT_DEVICE_ADDRESS, then talk in broadcast
# to a device but get reply. Useful when a single device on the link

# If BROADCAST_GROUP_ADDR & BROADCAST_DEVICE_ADDR, then talk to all
# deviced on the link, without a reply

# With BROADCAST_DEVICE_ADDR and a specific groupAddress, then talks to
# all deviced within thi specific group address, without any reply

# With DIRECT_DEVICE_ADDRESS and a specific groupAddress, then talks to
# all deviced within thi specific group address, with a reply

# With a specific deviceAddress and groupAddress, then talk to a single
# device and get a reply

class HDMISignalInfo(object):

	RGB444 = 0
	YUV422 = 1
	YUV444 = 2
	YUV420 = 3

	colorSpaceStr = {
		RGB444 : "RGB444",
		YUV422 : "YUV422",
		YUV444 : "YUV444",
		YUV420 : "YUV420",
	}

	DEPTH_24BIT = 0
	DEPTH_30BIT = 1
	DEPTH_36BIT = 2
	DEPTH_48BIT = 3

	colorDepthStr = {
		DEPTH_24BIT : "24bit",
		DEPTH_30BIT : "30bit",
		DEPTH_36BIT : "36bit",
		DEPTH_48BIT : "48bit",
	}

	NO_HDCP = 0
	HDCP_V1_X = 1
	HDCP_V2_0 = 2
	HDCP_V2_2 = 3

	hdcpStr = {
		NO_HDCP : "Clear",
		HDCP_V1_X : "v1.x",
		HDCP_V2_0 : "v2.0",
		HDCP_V2_2 : "v2.2",
	}

	HDMI_SOURCE = 0
	DVI_SOURCE = 1

	sourceStr = {
		HDMI_SOURCE : "HDMI",
		DVI_SOURCE : "DVI",
	}

	AUDIO_RATE_INVALID = 0
	AUDIO_RATE_32K = 1
	AUDIO_RATE_44_1K = 2
	AUDIO_RATE_48K = 3
	AUDIO_RATE_88K = 4
	AUDIO_RATE_96K = 5
	AUDIO_RATE_176K = 6
	AUDIO_RATE_192K = 7

	audioRateStr = {
		AUDIO_RATE_INVALID : "Invalid",
		AUDIO_RATE_32K : "32KHz",
		AUDIO_RATE_44_1K : "44.1KHz",
		AUDIO_RATE_48K : "48KHz",
		AUDIO_RATE_88K : "88KHz",
		AUDIO_RATE_96K : "96KHz",
		AUDIO_RATE_176K : "176KHz",
		AUDIO_RATE_192K : "192KHz",
	}

	AUDIO_BITS_INVALID = 0
	AUDIO_BITS_16 = 1
	AUDIO_BITS_20 = 2
	AUDIO_BITS_24 = 3

	audioBitsStr = {
		AUDIO_BITS_INVALID : "Invalid",
		AUDIO_BITS_16 : "16bit",
		AUDIO_BITS_20 : "20bit",
		AUDIO_BITS_24 : "24bit",
	}

	AUDIO_CHANNELS_INVALID = 0
	AUDIO_CHANNELS_2 = 1
	AUDIO_CHANNELS_3 = 2
	AUDIO_CHANNELS_4 = 3
	AUDIO_CHANNELS_5 = 4
	AUDIO_CHANNELS_6 = 5
	AUDIO_CHANNELS_7 = 6
	AUDIO_CHANNELS_8 = 7

	audioChannelsStr = {
		AUDIO_CHANNELS_INVALID : "Invalid",
		AUDIO_CHANNELS_2 : "2",
		AUDIO_CHANNELS_3 : "3",
		AUDIO_CHANNELS_4 : "4",
		AUDIO_CHANNELS_5 : "5",
		AUDIO_CHANNELS_6 : "6",
		AUDIO_CHANNELS_7 : "7",
		AUDIO_CHANNELS_8 : "8",
	}

	AUDIO_TYPE_INVALID = 0
	AUDIO_TYPE_PCM = 1
	AUDIO_TYPE_AC3 = 2
	AUDIO_TYPE_MPEG1 = 3
	AUDIO_TYPE_MP3 = 4
	AUDIO_TYPE_MPEG2 = 5
	AUDIO_TYPE_AAC = 6
	AUDIO_TYPE_DTS = 7
	AUDIO_TYPE_ATRAC = 8
	AUDIO_TYPE_ONEBITAUDIO = 9
	AUDIO_TYPE_DOLBY = 10
	AUDIO_TYPE_DTSHD = 11
	AUDIO_TYPE_MAT = 12
	AUDIO_TYPE_DST = 13
	AUDIO_TYPE_WMAPRO = 14

	audioTypeStr = {
		AUDIO_TYPE_INVALID : "Invalid",
		AUDIO_TYPE_PCM : "PCM",
		AUDIO_TYPE_AC3 : "AC3",
		AUDIO_TYPE_MPEG1 : "MPEG1",
		AUDIO_TYPE_MP3 : "MP3",
		AUDIO_TYPE_MPEG2 : "MPEG2",
		AUDIO_TYPE_AAC : "AAC",
		AUDIO_TYPE_DTS : "DTS",
		AUDIO_TYPE_ATRAC : "ATRAC",
		AUDIO_TYPE_ONEBITAUDIO : "OneBitAudio",
		AUDIO_TYPE_DOLBY : "DolbyDigital",
		AUDIO_TYPE_DTSHD : "DTS-HD",
		AUDIO_TYPE_MAT : "MAT",
		AUDIO_TYPE_DST : "DST",
		AUDIO_TYPE_WMAPRO : "WMA Pro",
	}

	MODE_3D_2D = 0
	MODE_3D_3D_FRAME_PACKING = 1
	MODE_3D_3D_TOP_BOTTOM = 2
	MODE_3D_SIDE_BY_SIDE = 3

	mode3DStr = {
		MODE_3D_2D : "2D",
		MODE_3D_3D_FRAME_PACKING : "3D (Frame Packing)",
		MODE_3D_3D_TOP_BOTTOM : "3D (Top & Bottom)",
		MODE_3D_SIDE_BY_SIDE : "3D (Side by Side)",
	}

	PIXEL_REPETITION_1X = 0
	PIXEL_REPETITION_2X = 1
	PIXEL_REPETITION_3X = 2
	PIXEL_REPETITION_4X = 3

	pixelRepStr = {
		PIXEL_REPETITION_1X : "1x",
		PIXEL_REPETITION_2X : "2x",
		PIXEL_REPETITION_3X : "3x",
		PIXEL_REPETITION_4X : "4x",
	}

	def __init__(self, data):
		self.colorSpace = int(data[0])
		self.colorDepth = int(data[1])
		self.HDCP = int(data[2])
		self.HDMI_DVI = int(data[3])
		self.audioSampleRate = int(data[4])
		self.audioBits = int(data[5])
		self.audioChannels = int(data[6])
		self.audioType = int(data[7])
		self.mode3D = int(data[8])
		self.pixelRepetition = int(data[9])

	def __str__(self):
		desc = "Color Space: %s\n" % self.colorSpaceStr[self.colorSpace]
		desc = desc + "Color Depth: %s\n" % self.colorDepthStr[self.colorDepth]
		desc = desc + "HDCP: %s\n" % self.hdcpStr[self.HDCP]
		desc = desc + "Source: %s\n" % self.sourceStr[self.HDMI_DVI]
		desc = desc + "Audio Rate:%s " % self.audioRateStr[self.audioSampleRate]
		desc = desc + "Width:%s " % self.audioBitsStr[self.audioBits]
		desc = desc + "Channels:%s " % self.audioChannelsStr[self.audioChannels]
		desc = desc + "Type:%s\n" % self.audioTypeStr[self.audioType]
		desc = desc + "Mode: %s\n" % self.mode3DStr[self.mode3D]
		desc = desc + "Pixel Repetition: %s" % self.pixelRepStr[self.pixelRepetition]
		return desc

class HDMITimings(object):

	FLAG_INTERLACE = 1
	FLAG_HPOL_POSITIVE = 2
	FLAG_VPOL_POSITIVE = 4

	def __init__(self, data):
		self.clock = unpack("<H", data[1:3])[0] * 10
		if data[3] & self.FLAG_INTERLACE:
			self.interlace = True
		else:
			self.interlace = False
		if data[3] & self.FLAG_HPOL_POSITIVE:
			self.hsyncPosivite = True
		else:
			self.hsyncPosivite = False
		if data[3] & self.FLAG_VPOL_POSITIVE:
			self.vsyncPosivite = True
		else:
			self.vsyncPosivite = False
		self.hActive = unpack("<H", data[4:6])[0]
		self.hBlank = unpack("<H", data[6:8])[0]
		self.hsOffset = unpack("<H", data[8:10])[0]
		self.hsWidth = unpack("<H", data[10:12])[0]
		self.vActive = unpack("<H", data[12:14])[0]
		self.vBlank = unpack("<H", data[14:16])[0]
		self.vsOffset = unpack("<H", data[16:18])[0]
		self.vsWidth = unpack("<H", data[18:20])[0]

	def __str__(self):
		desc = "Video clock: %dKHz\n" % self.clock
		desc = desc + "Mode Flags: "
		if self.interlace:
			desc = desc + "Interlaced "
		if self.hsyncPosivite:
			desc = desc + "HSync+ "
		else:
			desc = desc + "HSync- "
		if self.vsyncPosivite:
			desc = desc + "VSync+ "
		else:
			desc = desc + "VSync- "
		desc = desc + "\n"
		desc = desc + "Horizontal:\n\tActive:%d " % self.hActive
		desc = desc + "Blank:%d\n" % self.hBlank
		desc = desc + "\tSync Offset:%d " % self.hsOffset
		desc = desc + "Width:%d\n" % self.hsWidth
		desc = desc + "Vertical:\n\tActive:%d " % self.vActive
		desc = desc + "Blank:%d\n" % self.vBlank
		desc = desc + "\tSync Offset:%d " % self.vsOffset
		desc = desc + "Width:%d" % self.vsWidth
		return desc

class HDMIAnalyser(object):
	"""Represent a MuxLab HDMI/SDI Signal Analyser"""

	DIRECT_GROUP_ADDR = 0x00
	BROADCAST_GROUP_ADDR = 0xFF

	DIRECT_DEVICE_ADDRESS = 0x0
	BROADCAST_DEVICE_ADDR = 0xFF

	CMD_PC_TO_DEVICE = 0xAA
	CMD_DEVICE_TO_PC = 0xAB
	CMD_DEVICE_ID = 0x0001

	CMD_SET_VOLUME = 0x0080
	CMD_SET_STANDBY = 0x0081
	CMD_SET_MONITOR_SETTINGS = 0x0096
	CMD_SET_ADDR = 0x7801
	CMD_SET_RX_EDID = 0x7850
	CMD_DOWNLOAD_USER_EDID = 0x7851
	CMD_DOWNLOAD_SPI_FLASH_DATA = 0x7878
	CMD_SET_BAUD_RATE = 0x7879
	CMD_GET_VOLUME = 0x8080
	CMD_GET_STANDBY = 0x8081
	CMD_GET_SOURCE = 0x8082
	CMD_GET_SIGNAL_INFO = 0x8090
	CMD_GET_TIMING = 0x8091
	CMD_GET_SIGNAL_PACKAGE_INFO = 0x8092
	CMD_GET_PICTURE = 0x8095
	CMD_GET_MONITORING_DATA = 0x8096
	CMD_GET_PIXEL_RGB_DATA = 0x8097
	CMD_GET_BATTERY_VOLTAGE = 0x8098
	CMD_GET_EXT_5V_INPUT = 0x8099
	CMD_GET_SIGNAL_STATUS = 0x809f
	CMD_GET_DEVICE_ADDR = 0xF801
	CMD_GET_DEVICE_VERSION = 0xF802
	CMD_GET_RX_EDID_INDEX = 0xF850
	CMD_GET_RX_EDID_DATA = 0xF851
	CMD_GET_FW_INFO = 0xF858
	CMD_FEEDBACK = 0xffff

	FEEDBACK_OK = 0x00
	FEEDBACK_CHECKSUM_ERROR = 0x1
	FEEDBACK_WRONG_COMMAND = 0x2
	FEEDBACK_EXEC_ERROR = 0x3
	FEEDBACK_INVALID_MODE = 0x4
	FEEDBACK_ADDRESS_ERROR = 0x5

	SIGNAL_PACKAGE_INFO_INDEX_ACP = 0x4
	SIGNAL_PACKAGE_INFO_INDEX_ISRC1 = 0x5
	SIGNAL_PACKAGE_INFO_INDEX_ISRC2 = 0x6
	SIGNAL_PACKAGE_INFO_INDEX_GAMUT = 0xa
	SIGNAL_PACKAGE_INFO_INDEX_VS = 0x81
	SIGNAL_PACKAGE_INFO_INDEX_AVI = 0x82
	SIGNAL_PACKAGE_INFO_INDEX_SPD = 0x83
	SIGNAL_PACKAGE_INFO_INDEX_AUDIO = 0x84
	SIGNAL_PACKAGE_INFO_INDEX_MPEG = 0x85

	COMPONENT_RELEASE = 0
	COMPONENT_MAIN_MCU = 1
	COMPONENT_MAIN_FPGA = 0x10
	COMPONENT_POWER_MNG_BOARD = 0x30

	def __init__(self, portName, groupAddress = DIRECT_GROUP_ADDR, \
			deviceAddress = DIRECT_DEVICE_ADDRESS,
			baudrate = 115200):
		self.cmdGroupAddress = groupAddress
		self.cmdDeviceAddress = deviceAddress
		self.ser = serial.Serial(portName, baudrate)

	def calcCRC(self, data):
		crc = 0
		for v in data:
			crc = crc + int(v)
		return (256 - (crc % 256)) % 256

	def sendCommand(self, cmd):
		data = pack('<BHHBB', self.CMD_PC_TO_DEVICE, \
			    self.CMD_DEVICE_ID, \
			    len(cmd) + 3, self.cmdGroupAddress, \
			    self.cmdDeviceAddress)
		data = data + cmd
		data = data + pack('<B', self.calcCRC(data))
		self.ser.write(data)

	def readReply(self):
		head = self.ser.read(5)
		data = unpack('<BHH', head)
		if data[0] != self.CMD_DEVICE_TO_PC:
			raise ValueError("Protocol Error: bad Header value %x" % data[0])
		if data[1] != self.CMD_DEVICE_ID:
			raise ValueError("Protocol Error: had Device ID %x" % data[1])
		payload = self.ser.read(data[2])
		feedback = unpack('<H', payload[0:2])
		if feedback[0] == self.CMD_FEEDBACK:
			status = unpack('<HB', payload[0:3])
			if status[1] != FEEDBACK_OK:
				reason = "Unknown Error"
				if status[1] == FEEDBACK_CHECKSUM_ERROR:
					reason = "Checksum Error"
				elif status[1] == FEEDBACK_WRONG_COMMAND:
					reason = "Wrong command"
				elif status[1] == FEEDBACK_EXEC_ERROR:
					reason = "Command Execution Error"
				elif status[1] == FEEDBACK_INVALID_MODE:
					reason = "Invalid mode for command"
				elif status[1] == FEEDBACK_ADDRESS_ERROR:
					reason = "Invalid Error"
				raise ValueError("Command Error: %s for %x" % (reason, status[1]))
		return payload[4:-1]

	def setVolumeLevel(self, level):
		if level < 0 or level > 8:
			raise ValueError("Invalid volume level")
		self.sendCommand(pack('<HB', self.CMD_SET_VOLUME, level))
		self.readReply()
	
	def setStandbyStatus(self, status):
		if status < 0 or status > 1:
			raise ValueError("Invalid standby status")
		self.sendCommand(pack('<HB', self.CMD_SET_STANDBY, status))
		self.readReply()

	def setMonitorSettings(self, time_slot_unit, time_slot_value, \
			       triggle_mode, start_date, start_hour, \
			       start_minute, start_second):
		self.sendCommand(pack('<HBBBBBBB', self.CMD_SET_MONITOR_SETTINGS, \
					time_slot_unit, time_slot_value,
					triggle_mode, start_date, start_hour,
					start_minute, start_second))
		self.readReply()

	def setAddr(self, address):
		self.sendCommand(pack('<HB', self.CMD_SET_ADDR, address))
		self.readReply()

	def setEDIDNumber(self, index):
		self.sendCommand(pack('<HB', self.CMD_SET_RX_EDID, index))
		self.readReply()

	def setEDID(self, index, edid):
		self.sendCommand(pack('<HB', self.CMD_DOWNLOAD_USER_EDID, index) + edid)
		self.readReply()

	def setBaudrate(self, baudrate):
		self.sendCommand(pack('<H', self.CMD_SET_BAUD_RATE) + \
				 pack('<I', baudrate)[1:3])
		self.readReply()

	def getVolumeLevel(self):
		self.sendCommand(pack('<H', self.CMD_GET_VOLUME));
		reply = self.readReply()
		return int(reply[0])
	
	def getStandbyStatus(self):
		self.sendCommand(pack('<H', self.CMD_GET_STANDBY));
		reply = self.readReply()
		return int(reply[0])
	
	def getSourceType(self):
		self.sendCommand(pack('<H', self.CMD_GET_SOURCE));
		reply = self.readReply()
		return int(reply[0])

	def getSignalInfo(self):
		self.sendCommand(pack('<H', self.CMD_GET_SIGNAL_INFO));
		reply = self.readReply()
		return HDMISignalInfo(reply)

	def getTimings(self):
		self.sendCommand(pack('<H', self.CMD_GET_TIMING));
		reply = self.readReply()
		return HDMITimings(reply)

	def getSignalPackageInfo(self, index):
		self.sendCommand(pack('<HB', self.CMD_GET_SIGNAL_PACKAGE_INFO, index));
		reply = self.readReply()
		return reply

	def getPicture(self):
		self.sendCommand(pack('<H', self.CMD_GET_PICTURE));
		img = bytes() 
		for i in range(0, 64):
			img = img + self.readReply()[3:]
		return img

	def getMonitoringData(self):
		self.sendCommand(pack('<H', self.CMD_GET_MONITORING_DATA));
		reply = self.readReply()
		return reply

	def getPixelRGB(self, x, y):
		self.sendCommand(pack('<HHH', self.CMD_GET_PIXEL_RGB_DATA, x + 1, y + 1));
		reply = self.readReply()
		return reply

	def getBatteryVoltage(self):
		self.sendCommand(pack('<H', self.CMD_GET_BATTERY_VOLTAGE));
		reply = self.readReply()
		return unpack('<H', reply[0:2])[0] / 100

	def getGetExternal5VInput(self):
		self.sendCommand(pack('<H', self.CMD_GET_EXT_5V_INPUT));
		reply = self.readReply()
		return reply

	def getSignalStatus(self):
		self.sendCommand(pack('<H', self.CMD_GET_SIGNAL_STATUS));
		reply = self.readReply()
		return bool(reply[0])

	def getAddr(self):
		self.sendCommand(pack('<H', self.CMD_GET_DEVICE_ADDR));
		reply = self.readReply()
		return reply

	def getVersion(self):
		self.sendCommand(pack('<H', self.CMD_GET_DEVICE_VERSION));
		reply = self.readReply()
		return unpack("<BB", reply[0:2])
	
	def getEDIDNumber(self):
		self.sendCommand(pack('<H', self.CMD_GET_RX_EDID_INDEX));
		reply = self.readReply()
		return int(reply[0])
	
	def getEDID(self, number):
		self.sendCommand(pack('<HB', self.CMD_GET_RX_EDID_DATA, number));
		reply = self.readReply()
		return reply
	
	def getFirmwareInfo(self, component):
		self.sendCommand(pack('<HB', self.CMD_GET_FW_INFO, component));
		reply = self.readReply()
		return unpack("<BB", reply[1:3])

