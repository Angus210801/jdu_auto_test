import os
import re
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

    def __init__(self, usb_driver="/dev/ttyUSB0"):
        self.usb_driver = usb_driver

    def connect_usb_box(self):
        rst = True
        try:
            ser = serial.Serial(self.usb_driver, 115200, timeout=1)
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
            ser = serial.Serial(self.usb_driver, 115200, timeout=1)
            if not ser.isOpen():
                ser.open()
            ser.write("1".encode())
            time.sleep(5)
        except:
            rst = False
        return rst

if __name__ == '__main__':
    usb = UsbBoxDriver_ubuntu()
    usb.connect_usb_box()