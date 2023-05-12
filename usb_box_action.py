import os
import re
import sys
import traceback
import time

try:
    import serial
except:
    os.system("python -m pip install pyserial")
    import serial


class UsbBoxDriver:

    def __init__(self, usb_driver="CH340"):
        self.usb_driver = usb_driver

    def connect_usb_box(self):
        rst = True
        try:
            com_string = os.popen('wmic path CIM_LogicalDevice get Caption | findstr %s' % self.usb_driver).read()
            serial_port = re.findall(re.compile(r'[(](.*?)[)]', re.S), com_string)[0]
            ser = serial.Serial(serial_port, 115200, timeout=1)
            if not ser.isOpen():
                ser.open()
            ser.write("0".encode())
            time.sleep(10)
        except:
            rst = False
        return rst

    def disconnect_usb_box(self):
        rst = True
        try:
            com_string = os.popen('wmic path CIM_LogicalDevice get Caption | findstr %s' % self.usb_driver).read()
            serial_port = re.findall(re.compile(r'[(](.*?)[)]', re.S), com_string)[0]
            ser = serial.Serial(serial_port, 115200, timeout=1)
            if not ser.isOpen():
                ser.open()
            ser.write("1".encode())
            time.sleep(5)
        except:
            rst = False
        return rst

class UsbBoxDriver_ubuntu:
    def __init__(self, usb_driver="CH340"):
        self.usb_driver = usb_driver

    def connect_usb_box(self):
        rst = True
        try:
            serial_ports = [p for p in os.listdir('/dev/serial/by-id/') if self.usb_driver in p]
            if not serial_ports:
                return False
            serial_port = os.path.realpath('/dev/serial/by-id/' + serial_ports[0])
            ser = serial.Serial(serial_port, 115200, timeout=1)
            if not ser.isOpen():
                ser.open()
            ser.write("0".encode())
            time.sleep(10)
        except:
            rst = False
        return rst

    def disconnect_usb_box(self):
        rst = True
        try:
            serial_ports = [p for p in os.listdir('/dev/serial/by-id/') if self.usb_driver in p]
            if not serial_ports:
                return False
            serial_port = os.path.realpath('/dev/serial/by-id/' + serial_ports[0])
            ser = serial.Serial(serial_port, 115200, timeout=1)
            if not ser.isOpen():
                ser.open()
            ser.write("1".encode())
            time.sleep(5)
        except:
            rst = False
        return rst

if __name__ == '__main__':
    usb = UsbBoxDriver_ubuntu()
    usb.disconnect_usb_box()