# python文件只读的时候 -> sudo chmod 777 main.py
import datetime
import glob
import os
import subprocess
#import time
from urllib.parse import urljoin


# 獲取xpress package的下載路徑,將獲取道德內容儲存成臨時路徑,與case名稱進行拼接
def get_package_tmp_url():
    base_url = "http://192.168.140.95/xpress/"
    tmp = input("Which SR are you in:") + "/" + input("Which device do you use:") + "/"
    url_tmp = urljoin(base_url, tmp)
    return url_tmp


# 如果沒有文件夾/文件就創建文件夾/文件("/tmp/auto_log/")
def create_or_clear_file(file_path):
    folder_name = "/tmp/auto_log"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    if os.path.isfile(file_path):
        # 如果文件存在，则删除文件中的所有内容
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
def file_save(prepare_case, case_name):
    with open(file_path, "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"case {case_name} start to run:\n")
        f.write(f"step1:set all settings into default value\n")
        f.flush()
        # 需要一個降級/同級且將setting設置成default的包
        subprocess.Popen(['./jdu.sh', get_url(prepare_case, case_name)[0]], stdout=f).wait()
        setting_compare(f)
        f.write(f"\nstep2:case {case_name} prepare done, start to run case {case_name}:\n")
        f.flush()
        subprocess.Popen(['./jdu.sh', get_url(prepare_case, case_name)[1]], stdout=f).wait()
        f.write(f"\nstep3:check if the settings changed correctly:\n")
        f.flush()
        setting_compare(f)
        f.write(f"The test is finished\n\n\n\n")
'''
#處理特殊的case -> 中斷設備的升級
def copy_usbreset():
    program_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.join(program_dir, 'usbreset-master')
    os.chdir(target_dir)
    subprocess.run(['cc', 'usbreset.c', '-o', 'usbreset'], stdout=subprocess.PIPE)
    sudo_command_1 = 'echo {} | sudo -S {}'.format(password, "sudo cp ./usbreset /usr/sbin/")
    subprocess.Popen(sudo_command_1,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    os.chdir('/usr/local/gn')
    return
def command_disconnect():
    result = []
    file_path = create_or_clear_file("/tmp/auto_log/log_bus")
    with open(file_path, "a+") as f:
        subprocess.Popen('lsusb', stdout=f).wait()
        f.seek(0)
        for line in f:
            if "0b0e" in line:
                result.append(line.strip().split(" "))
                #print(result)
    bus_path = "/dev/bus/usb/" + result[0][1] + "/" + result[0][3][:3]
    usb_reset_cmd = 'sudo /usr/sbin/usbreset ' + bus_path
    sudo_command = 'echo {} | sudo -S {}'.format(password, usb_reset_cmd)
    # 执行重启USB控制器的命令
    os.popen(sudo_command)
    return
def execute_disconnect_device(prepare_case, case_name):
    with open(file_path, "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"\nstep1:case {case_name} prepare work start to run:\n")
        f.flush()
        # 需要一個降級/同級且將setting設置成default的包
        subprocess.Popen(['./jdu.sh', get_url(prepare_case, case_name)[0]], stdout=f).wait()
        f.write(f"\nstep2:case {case_name} is start to run,device will be disconnected and re-connected\n")
        f.flush()
        time.sleep(10)
        subprocess.Popen(['./jdu.sh', get_url(prepare_case, case_name)[1]], stdout=f)
        time.sleep(200)
        command_disconnect()
        f.write(f"\nstep4:re-start the upgrade session\n")
        subprocess.Popen(['./jdu.sh', get_url(prepare_case, case_name)[1]], stdout=f).wait()
        f.write(f"\n{case_name} finished\n\n\n\n")
        return
'''
# def upgrade_throuh_FW():
#1->down 2->keep
if __name__ == '__main__':
    #password = "test@123"
    # 将子进程切换到对应路径下
    # copy_usbreset()
    os.chdir('/usr/local/gn')
    file_path = create_or_clear_file("/tmp/auto_log/log")
    url_tmp = get_package_tmp_url()
    #16990 in ccase_list is ID 47971
    case_list = [7555,7695,7692,7551,7556]
    for case_name in case_list:
        if case_name==7692 or 7695:
            file_save(2301, case_name)
        else:
            file_save(2302,case_name)



