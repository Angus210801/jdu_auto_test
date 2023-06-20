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
#                   @Last Update  : 2023/05/19
#
#-------------------------------------------------------------------
"""

import glob
import subprocess
from urllib.parse import urljoin
from linux_jdu_autotest_usb_box_new import *
import time

def get_os_version():
    import subprocess

    # 使用subprocess模块执行lsb_release命令获取系统版本
    result = subprocess.run(['lsb_release', '-a'], stdout=subprocess.PIPE)

    # 将输出转换为字符串
    output = result.stdout.decode('utf-8')

    # 在输出中查找Description行并提取系统版本信息
    for line in output.split('\n'):
        if 'Description' in line:
            version = line.split(':')[1].strip()

    return version
def check_network(server_address):
    # Check the network connection
    try:
        subprocess.run(["ping", "-c", "1", server_address], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

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
    # Use the subprocess command to compare the device settings.
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
        # If file not exist, create it.
        with open(file_path, "w") as f:
            pass
    return file_path

def rename_log_file(new_file_name):
    old_file_path = "/tmp/auto_log/log"
    new_file_path = f"/tmp/auto_log/{new_file_name}_log.txt"
    os.rename(old_file_path, new_file_path)