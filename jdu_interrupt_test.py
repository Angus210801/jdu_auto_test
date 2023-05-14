import os
import subprocess
from usb_box_action import *
import time

if __name__ == '__main__':
    os.chdir('/usr/local/gn')
    base_url = "/tmp/JABRA_FILI_OTA_V1.1.8.zip"
    subprocess.Popen(['./jfwu', base_url])
    usber=UsbBoxDriver_ubuntu()
# 判断/tmp/jfwu_log/下的jfwu.log中的文本是否有50%这个关键字，如果没有，就每隔一秒钟检查一次，如果有，则执行disconnect_usb_box()这个函数，断开usb box的连接。
    with open("/tmp/jfwu_log/jfwu.log") as f:
        while "50%" in f.read()==False:
            time.sleep(1)
            print('Keyword not found!The zip download still continue.')
    print('Keyword found!')
    usber.disconnect_usb_box()
    time.sleep(10)
    usber.connect_usb_box()
    time.sleep(10)
    subprocess.Popen(['./jfwu', base_url]).wait()


# Todo
# Unzip the xpress package from server
# Then put the pckage to the tmp/fw
# Use characters to match FW files that begin with J
# Update the Device
