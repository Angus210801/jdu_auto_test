import datetime
import glob
import subprocess
from urllib.parse import urljoin
from usb_box_action import *

# Get the download link from the server
def get_package_tmp_url():
    base_url = "http://192.168.140.95/xpress/"
    tmp = input("Which SR are you in:") + "/" + input("Which device do you use:") + "/"
    url_tmp = urljoin(base_url, tmp)
    return url_tmp


# If there are no files / files, create the files / files (tmp/auto_log/;)
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


# 获取下载下来的xpress包名
def setting_compare(f):
    dir_path = "/var/run/jabra"
    file_pattern = "xpress_package_*.zip"
    file_names = glob.glob(os.path.join(dir_path, file_pattern))
    cmd = "./jdu_settings"
    option1 = "-c"
    option2 = "-V"
    # 使用 subprocess.Popen() 函数执行命令
    subprocess.Popen([cmd, option1, option2, file_names[0]], stdout=f).wait()


# 获取完整的XPRESS包的url -> 針對與第一次獲取鏈接做default配置
def get_url(prepare_case, case_name):
    # 使用 urllib.parse.urljoin() 函数拼接 URL,default的包和case的包的路徑分開保存
    prepare_url = urljoin(url_tmp, str(prepare_case))
    case_url = urljoin(url_tmp, str(case_name))
    return prepare_url, case_url

# LOG的輸出格式
def run_testcase_settings(prepare_case, case_name):
    with open(file_path, "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"case {case_name} start to run:\n")
        f.write(f"step1:set all settings into default value\n")
        f.flush()
        # 需要一個降級/同級且將setting設置成default的包
        subprocess.Popen(['./jdu.sh', get_url(prepare_case, case_name)[0]], stdout=f).wait()
        print(get_url(prepare_case, case_name)[0])
        print(get_url(prepare_case, case_name)[1])

        setting_compare(f)
        f.write(f"\nstep2:case {case_name} prepare done, start to run case {case_name}:\n")
        f.flush()
        subprocess.Popen(['./jdu.sh', get_url(prepare_case, case_name)[1]], stdout=f).wait()
        f.write(f"\nstep3:check if the settings changed correctly:\n")
        f.flush()
        setting_compare(f)
        f.write(f"The test is finished\n\n\n\n")

def run_testcase_update_fw_file(prepare_case, case_name):
    with open(file_path, "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"case {case_name} start to run:\n")
        f.write(f"step1:set all settings into default value\n")
        f.flush()

        subprocess.Popen(['./jdu.sh', get_url(prepare_case, case_name)[0]], stdout=f)
        with open("/tmp/jdu_log/wget.log") as f:
            while ".zip’ saved" in f.read()==False:
                time.sleep(3)
                print('Keyword not found!The zip download still continue.')
        print('Keyword found!')
        usb = UsbBoxDriver()
        usb.connect_usb_box()
        print(get_url(prepare_case, case_name)[0])
        print(get_url(prepare_case, case_name)[1])

        setting_compare(f)
        f.write(f"\nstep2:case {case_name} prepare done, start to run case {case_name}:\n")
        f.flush()
        subprocess.Popen(['./jdu.sh', get_url(prepare_case, case_name)[1]], stdout=f).wait()
        f.write(f"\nstep3:check if the settings changed correctly:\n")
        f.flush()
        setting_compare(f)
        f.write(f"The test is finished\n\n\n\n")

def run_testcase_update_fw_JX_package():
    with open(file_path, "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"case {case_name} start to run:\n")
        f.write(f"step1:set all settings into default value\n")
        f.flush()

# def upgrade_throuh_FW():
#1->down 2->keep
if __name__ == '__main__':


    os.chdir('/usr/local/gn')
    file_path = clean_the_test_script_logs("/tmp/auto_log/log")
    url_tmp = get_package_tmp_url()
    # 16990 in case_list is ID 47971
    # case_list = [6134,7551,7555,7556,7692,7695]
    # case_list = [7555,7692]
    update_fw_case_list = [16990, 16991, 16992, 17950, 17951]
    upadte_settings_case_list = [16990]

    for case_name in update_fw_case_list:
        if case_name == 16990:
            run_testcase_update_fw_JX_package()


    for case_name in upadte_settings_case_list:
        if case_name in [7692, 7695, 7556]:
            run_testcase_settings("7556p", case_name)
        elif case_name == 6134:
            run_testcase_settings("6134p", case_name)
        elif case_name == 7555 or case_name == 16990:
            run_testcase_settings("7555p", case_name)
        else:
            run_testcase_settings("7551p", case_name)



'''
FW Update case:

16990 JXDU:Disconnect the DUT during the FW update.[Use JX Package][Allow downgrade]
16991 JXDU:Disconnect the DUT during the FW udpate.[Use JX Package][Not allow downgrade]

For this, Place the lower FW to the /home/swtest/Downloads/lowerfw folder.

16992 JXDU:Disconnect the DUT during the FW update,for all individual components.[Use FW File]
17950 JXDU:Normal FW update without Interruption.[Use FW File](Linux JXDU 6.x or above)
17951 JXDU:Normal FW Update without Interruption.[Use JX Package](Linux JXDU 6.x or Above)

FW Update & Settings Configure case:

6134 JX-ThinC:All device settings and FW set to "Leave Unchange",all settings set to Protected.
7692 JX-ThinC:All settings in the device can be change from default value to min.value with installation of .zip file at the end user PC,no FW change.
7695 JX-ThinC:All settings in the device can be change from default value to max.value with installation of .zip file at the end user PC,no FW change.
7551 JX-ThinC:Install a ZIP file on end user environment with a later FW and set all settings are changed.
7555 JX-ThinC:Install a ZIP file on end user environment with a later FW and no setting change.
7556 JX-ThinC:Install a ZIP file on end user environment with a later FW and set all settings set to default.

'''