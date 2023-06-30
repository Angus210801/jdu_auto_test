"""
#-------------------------------------------------------------------
#                   CONFIDENTIAL --- Linux JDU auto test script
#-------------------------------------------------------------------
#
#                   @Project Name : Sisyphus
#
#                   @File Name    : linux_jdu_autotest_usb_box_new
#
#                   @Programmer   : Ezreal/Angus
#
#                   @Start Date   : 2023/04/24
#
#                   @Last Update  : 2023/05/23
#
#                   @Note: This is the new usb box code that works on the test now.
#-------------------------------------------------------------------
"""

import os
import re
import time
try:
    import serial
except:
    os.system("python -m pip install pyserial")
    import serial

open_channel1_str = "A0 01 01 A2"
open_channel4_str = "A0 04 01 A5"
close_channel1_str = "A0 01 00 A1"
close_channel4_str = "A0 04 00 A4"


class UsbBoxDriver_windows:

    def __init__(self, usb_driver="CH340"):
        self.usb_driver = usb_driver

    def connect_usb_box(self):
        rst = True
        try:
            com_string = os.popen('wmic path CIM_LogicalDevice get Caption | findstr %s' % self.usb_driver).read()
            serial_port = re.findall(re.compile(r'[(](.*?)[)]', re.S), com_string)[0]
            # ser = serial.Serial(serial_port, 115200, timeout=1)
            ser = serial.Serial(serial_port, 9600, timeout=1)
            if not ser.isOpen():
                ser.open()
            # ser.write("0".encode())
            ser.write(bytes.fromhex(open_channel1_str))
            time.sleep(0.1)
            ser.write(bytes.fromhex(open_channel4_str))
            time.sleep(10)
            # Logger.ins().std_logger().info("---> [PY][ConnectDutViaUsbBox] rst=%s." % rst)
        except:
            rst = False
            # Logger.ins().file_logger().error(traceback.format_exc())
        return rst

    def disconnect_usb_box(self):
        rst = True
        try:
            com_string = os.popen('wmic path CIM_LogicalDevice get Caption | findstr %s' % self.usb_driver).read()
            serial_port = re.findall(re.compile(r'[(](.*?)[)]', re.S), com_string)[0]
            # ser = serial.Serial(serial_port, 115200, timeout=1)
            ser = serial.Serial(serial_port, 9600, timeout=1)
            if not ser.isOpen():
                ser.open()
            # ser.write("1".encode())
            ser.write(bytes.fromhex(close_channel1_str))
            time.sleep(0.1)
            ser.write(bytes.fromhex(close_channel4_str))
            time.sleep(5)
            # Logger.ins().std_logger().info("---> [PY][DisConnectDutViaUsbBox] rst=%s." % rst)
        except:
            rst = False
            # Logger.ins().file_logger().error(traceback.format_exc())
        return rst

try:
    import serial
except:
    os.system("python -m pip install pyserial")
    import serial

open_channel1_str = "A0 01 01 A2"
open_channel4_str = "A0 04 01 A5"
close_channel1_str = "A0 01 00 A1"
close_channel4_str = "A0 04 00 A4"


class UsbBoxDriver_ubuntu:
    def __init__(self, usb_driver="CH340"):
        self.usb_driver = usb_driver

    def connect_usb_box(self):
        rst = True
        try:
            serial_port = "/dev/ttyUSB0"
            ser = serial.Serial(serial_port, 9600, timeout=1)
            if not ser.isOpen():
                ser.open()
            ser.write(bytes.fromhex(open_channel1_str))
            time.sleep(0.1)
            ser.write(bytes.fromhex(open_channel4_str))
            time.sleep(10)
        except Exception as e:
            print(e)
            rst = False
        return rst

    def disconnect_usb_box(self):
        rst = True
        try:
            serial_port = "/dev/ttyUSB0"
            ser = serial.Serial(serial_port, 9600, timeout=1)
            if not ser.isOpen():
                ser.open()
            ser.write(bytes.fromhex(close_channel1_str))
            time.sleep(0.1)
            ser.write(bytes.fromhex(close_channel4_str))
            time.sleep(5)
        except:
            rst = False
        return rst

if __name__ == '__main__':
    usb = UsbBoxDriver_ubuntu()
    usb.connect_usb_box()