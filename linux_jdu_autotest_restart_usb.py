"""
#-------------------------------------------------------------------
#                   CONFIDENTIAL --- Linux JDU auto test script
#-------------------------------------------------------------------
#
#                   @Project Name : Sisyphus
#
#                   @File Name    : linux_jdu_setup
#
#                   @Programmer   : Ella
#
#                   @Start Date   : 2023/04/24
#
#                   @Last Update  : 2021/05/19
#
#This file is used to interrupt the update process of Jabra device by restarting the USB bus.
#But after discuss with Younger, we decide to use the usb box to interrupt the update process.
#Just keep this file for future use.
#
#-------------------------------------------------------------------
"""

import os
import subprocess


"""

"""

result = []  # Keep the result of the command

def create_or_clear_file(file_path):
    if os.path.isfile(file_path):
        with open(file_path, "w") as f:
            f.seek(0)
            f.truncate()
    return file_path


file_path = create_or_clear_file("/tmp/auto_log/log_bus")
password = "test@123"

os.chdir('usbreset-master')
subprocess.run(['cc', 'usbreset.c', '-o', 'usbreset'], stdout=subprocess.PIPE)
subprocess.run('ls')
sudo_command_1 = 'echo {} | sudo -S {}'.format(password, "sudo cp ./usbreset /usr/sbin/")
os.popen(sudo_command_1)

with open(file_path, "a+") as f:

    subprocess.Popen('lsusb', stdout=f).wait()
    f.seek(0)
    for line in f:
        if "0b0e" in line:
            result.append(line.strip().split(" "))
            print(result)
bus_path = "/dev/bus/usb/" + result[0][1] + "/" + result[0][3][:3]
usb_reset_cmd = 'sudo /usr/sbin/usbreset ' + bus_path
sudo_command = 'echo {} | sudo -S {}'.format(password, usb_reset_cmd)
# 执行重启USB控制器的命令
os.popen(sudo_command)

