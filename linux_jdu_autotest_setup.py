"""
#-------------------------------------------------------------------
#                   CONFIDENTIAL --- Linux JDU auto test script
#-------------------------------------------------------------------
#
#                   @Project Name : Sisyphus
#
#                   @File Name    : linux_jdu_setup
#
#                   @Programmer   : Angus/Ella
#
#                   @Start Date   : 2023/04/24
#
#                   @Last Update  : 2021/05/19
#
#-------------------------------------------------------------------
"""

import glob
import subprocess
from urllib.parse import urljoin
from linux_jdu_autotest_usb_box_new import *
import time

def delete_xpress_file():
    try:
        dir_path = '/var/run/jabra/'
        command = "find {} -type f -name 'xpress*' -delete".format(dir_path)
        subprocess.run(command, shell=True)
    except:
        print("No Xpress file")

def delete_jduandjfwu_logs():
    try:
        command = "rm -rf /tmp/jdu_log/*"
        subprocess.run(command, shell=True)
    except:
        print("No jdu log file in the /tmp/jdu_log/ folder")

    try:
        command = "rm -rf /tmp/fw/*"
        subprocess.run(command, shell=True)
    except:
        print("No fw file in the /tmp/fw/ folder")

    try:
        command = "rm -rf /tmp/jfwu_log/*"
        subprocess.run(command, shell=True)
    except:
        print("No jfwu log file in the /tmp/jfwu_log/ folder")

def interrupt_update_fw_file():
    log_file = "/tmp/jfwu_log/jfwu.log"
    target_text = "60%"
    while True:
        try:
            with open(log_file, "r") as file:
                content = file.read()
                if target_text in content:
                    usber = UsbBoxDriver_ubuntu()
                    usber.disconnect_usb_box()
                    print("Disconnect the device.")
                    break
                    
            time.sleep(1)
        except FileNotFoundError:
            time.sleep(1)
def judge_jdu_process_ongoing():
    log_file = "/tmp/jdu_log/jdu_firmware.log"
    target_text = "100%"
    while True:
        try:
            with open(log_file, "r") as file:
                content = file.read()
                if target_text in content:
                    usber = UsbBoxDriver_ubuntu()
                    usber.connect_usb_box()
                    break

            time.sleep(1)
        except FileNotFoundError:
            time.sleep(1)

def interrupt_update_jx_package():
    log_file = "/tmp/jdu_log/jdu_firmware.log"
    target_text = "60%"
    while True:
        try:
             with open(log_file, "r") as file:
                content = file.read()
                if target_text in content:
                    usber = UsbBoxDriver_ubuntu()
                    usber.disconnect_usb_box()
                    print("Disconnect the device.")
                    break
                time.sleep(1)
        except FileNotFoundError:
            time.sleep(1)


def get_xpress_url(prepare_case, case_name,base_url,tmp):

    package_dir = urljoin(base_url, tmp)
    prepare_url = urljoin(package_dir, str(prepare_case))
    case_url = urljoin(package_dir, str(case_name))
    return prepare_url, case_url


def setting_compare(f):
    dir_path = "/var/run/jabra"
    file_pattern = "xpress_package_*.zip"
    file_names = glob.glob(os.path.join(dir_path, file_pattern))
    cmd = "./jdu_settings"
    option1 = "-c"
    option2 = "-V"
    # 使用 subprocess.Popen() 函数执行命令
    subprocess.Popen([cmd, option1, option2, file_names[0]], stdout=f).wait()



def create_log_file(file_path):
    folder_name = "/tmp/auto_log"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    if os.path.isfile(file_path):
        # If the file exists, delete everything in the file
        with open(file_path, "w") as f:
            f.seek(0)
            f.truncate()
    else:
        # 如果文件不存在，则在指定路径下创建文件
        with open(file_path, "w") as f:
            pass
    return file_path
