import glob
import subprocess
from urllib.parse import urljoin
from main import url_tmp
from usb_box_action import *
import time

def delete_xpress_file():
    dir_path = '/var/run/jabra/'
    command = "find {} -type f -name 'xpress*' -delete".format(dir_path)
    subprocess.run(command, shell=True)

def delete_logs():
    command = "rm -rf /tmp/jdu_log/*"
    subprocess.run(command, shell=True)
    command = "rm -rf /tmp/fw/*"
    subprocess.run(command, shell=True)
    command = "rm -rf /tmp/jfwu_log/*"
    subprocess.run(command, shell=True)

def interrupt_update():
    log_file = "/tmp/jfwu_log/jfwu.log"
    target_text = "40%"
    while True:
        try:
            with open(log_file, "r") as file:
                content = file.read()
                print(content)

                if target_text in content:
                    usber = UsbBoxDriver_ubuntu()
                    usber.disconnect_usb_box()
                    print("Disconnect the device.")
                    break
                    
            time.sleep(1)
        except FileNotFoundError:
            time.sleep(1)



def get_url(prepare_case, case_name):
    # 使用 urllib.parse.urljoin() 函数拼接 URL,default的包和case的包的路徑分開保存
    prepare_url = urljoin(url_tmp, str(prepare_case))
    case_url = urljoin(url_tmp, str(case_name))
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

def get_package_tmp_url():
    base_url = "http://192.168.140.95/xpress/"
    tmp = input("Which SR are you in:") + "/" + input("Which device do you use:") + "/"
    url_tmp = urljoin(base_url, tmp)
    return url_tmp


def clean_the_test_script_logs(file_path):
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
