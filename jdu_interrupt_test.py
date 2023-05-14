import os
import subprocess
from usb_box_action import *
import time

if __name__ == '__main__':
    os.chdir('/usr/local/gn')
    base_url = "/tmp/JABRA_FILI_OTA_V1.1.8.zip"
    subprocess.Popen(['./jfwu', base_url])
    time.sleep(35)
    usber=UsbBoxDriver_ubuntu()
    usber.disconnect_usb_box()
    time.sleep(10)
    usber.connect_usb_box()
    time.sleep(10)
    subprocess.Popen(['./jfwu', base_url]).wait()


