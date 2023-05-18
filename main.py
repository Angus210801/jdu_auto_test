from jdu_interrupt_test import *
from usb_box_action import *
import subprocess
import datetime
# Get the download link from the server


# If there are no files / files, create the files / files (tmp/auto_log/;)


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
                print('The zip download still continue.')
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

def run_testcase_interrupt_JX_package(prepare_case, case_name):
    delete_xpress_file()
    delete_logs()
    os.chdir('/usr/local/gn')
    base_url = "http://192.168.140.95/xpress/sr99/evolve230/16990"
    process=subprocess.Popen(['./jdu.sh', base_url])


    command = "mv /usr/local/gn/jdu_firmware /tmp/fw/"
    subprocess.run(command, shell=True)

    while not os.path.exists('/tmp/jdu_log/wget.log'):
        time.sleep(1)

    while "zip’ saved" not in open('/tmp/jdu_log/wget.log').read():
        time.sleep(1)
        print('Download not completed!')

    print('Downlaod completed!')
    #when download completed, end the ./jdu.sh process
    process.terminate()


    if not os.path.exists('/tmp/fw'):
        os.makedirs('/tmp/fw')
    else:
        subprocess.Popen(['rm', '-rf', '/tmp/fw/*'])

    time.sleep(2)
    subprocess.Popen(['7z','x', '/var/run/jabra/xpress_package_*.zip', '-pgn123!', '-o/tmp/fw/'])

    time.sleep(3)
    os.chdir('/usr/local/gn')
    command = "/usr/local/gn/jfwu /tmp/fw/Firmware/J*"
    subprocess.Popen(command,shell=True)

    # Once it is up to 50%, we need to disconnect the usb box.
    interrupt_update()

    while "100%" not in open('/tmp/jfwu_log/jfwu.log').read():
        time.sleep(1)
        print('Update not completed!')

    usber = UsbBoxDriver_ubuntu()
    usber.connect_usb_box()
    time.sleep(10)
    command = "/usr/local/gn/jfwu /tmp/fw/Firmware/J*"
    subprocess.run(command, shell=True)
    command = "mv /tmp/fw/Firmware/jdu_firmware /usr/local/gn/"
    subprocess.run(command, shell=True)

    print('Interrupt update completed!')


if __name__ == '__main__':
    os.chdir('/usr/local/gn')
    file_path = clean_the_test_script_logs("/tmp/auto_log/log")
    url_tmp = get_package_tmp_url()

    update_fw_case_list = [16990, 16991, 16992, 17950, 17951]
    upadte_settings_case_list = [16990]

    for case_name in update_fw_case_list:
        if case_name == 16990:
            run_testcase_interrupt_JX_package()


    for case_name in upadte_settings_case_list:
        if case_name in [7692, 7695, 7556]:
            run_testcase_settings("7556p", case_name)
        elif case_name == 6134:
            run_testcase_settings("6134p", case_name)
        elif case_name == 7555 or case_name == 16990:
            run_testcase_settings("7555p", case_name)
        else:
            run_testcase_settings("7551p", case_name)



