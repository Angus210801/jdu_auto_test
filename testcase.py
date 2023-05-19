from action import *
from usb_box_action import *
import subprocess
import datetime

def run_testcase_settings(prepare_case, case_name,base_url,tmp):
    with open(log_path, "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"case {case_name} start to run:\n")
        # Run the prepare case first
        f.write(f"step1:Run the prepare package{prepare_case} for the {case_name}\n")
        f.flush()
        subprocess.Popen(['./jdu.sh', get_xpress_url(prepare_case, case_name,base_url,tmp)[0]], stdout=f).wait()
        # Print the download link to the terminal for debug, below 2 sentences can be deleted
        print(get_xpress_url(prepare_case, case_name,base_url,tmp)[0])
        print(get_xpress_url(prepare_case, case_name,base_url,tmp)[1])
        # Compare the settings before and after the prepare case
        f.write(f"Now, check the device settings is in prepare status: \n")
        setting_compare(f)
        # Run the test case
        f.write(f"\nstep2:case {case_name} prepare done, start to run case {case_name}:\n")
        f.flush()
        subprocess.Popen(['./jdu.sh', get_xpress_url(prepare_case, case_name,base_url,tmp)[1]], stdout=f).wait()
        f.write(f"\nstep3:check if the settings changed correctly:\n")
        f.flush()
        setting_compare(f)
        f.write(f"{case_name} test is finished.")
        # Print the dividing line to the log file
        f.write("------------------------------------------------------------\n\n\n\n")

def run_testcase_interrupt_jx_package(prepare_case, case_name,base_url,tmp):
    with open(log_path, "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"case {case_name} start to run:\n")
        f.write(f"step1:Run the prepare package{prepare_case} for the {case_name}\n")
        f.flush()

        subprocess.Popen(['./jdu.sh', get_xpress_url(prepare_case, case_name,base_url,tmp)[0]], stdout=f)

        print(get_xpress_url(prepare_case, case_name,base_url,tmp)[0])
        print(get_xpress_url(prepare_case, case_name,base_url,tmp)[1])
        print("The prepare case is finished.")

        f.write(f"\nstep2:case {case_name} prepare done, start to run case {case_name}:\n")
        f.flush()
        subprocess.Popen(['./jdu.sh', get_xpress_url(prepare_case, case_name,base_url,tmp)[1]], stdout=f)

        interrupt_update_jx_package()

        while "100%" not in open('/tmp/jdu_log/jdu_firmware.log').read():
            time.sleep(1)
            print('JDU is still going!')

        # Reconnect the usb box
        usber = UsbBoxDriver_ubuntu()
        usber.connect_usb_box()
        time.sleep(10)

        subprocess.Popen(['./jdu.sh', get_xpress_url(prepare_case, case_name,base_url,tmp)[1]], stdout=f).wait()

        print('Interrupt update completed!')

        f.write(f"{case_name} test is finished.")
        # Print the dividing line to the log file
        f.write("------------------------------------------------------------\n\n\n\n")


def run_testcase_interrupt_fw_file(prepare_case, case_name,base_url,tmp):
    with open(log_path, "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"case {case_name} start to run:\n")
        # Run the prepare case first
        f.write(f"step1:set all settings into default value\n")
        f.flush()
        # Delete the old log file and old xpress file
        delete_xpress_file()
        delete_logs()
        os.chdir('/usr/local/gn')
        subprocess.Popen(['./jdu.sh', get_xpress_url(prepare_case, case_name,base_url,tmp)[0]], stdout=f).wait()

        print(get_xpress_url(prepare_case, case_name,base_url,tmp)[0])
        print(get_xpress_url(prepare_case, case_name,base_url,tmp)[1])
        print("The prepare case is finished.")

        # Move the jdu_firmware file to /tmp/fw because the jdu.sh will call the jdu_firmware process.
        command = "mv /usr/local/gn/jdu_firmware /tmp/fw/"
        subprocess.run(command, shell=True)

        # Run the test case
        process=subprocess.Popen(['./jdu.sh', get_xpress_url(prepare_case, case_name,base_url,tmp)[1]], stdout=f)
        # Wait until the download is completed
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

        # Once it is up to 40%, we need to disconnect the usb box.
        interrupt_update_fw_file()

        # Wait until the jdu is reported update failed.
        while "100%" not in open('/tmp/jfwu_log/jfwu.log').read():
            time.sleep(1)
            print('JDU is still going!')

        # Reconnect the usb box
        usber = UsbBoxDriver_ubuntu()
        usber.connect_usb_box()
        time.sleep(10)


        command = "/usr/local/gn/jfwu /tmp/fw/Firmware/J*"
        subprocess.run(command, shell=True)
        command = "mv /tmp/fw/Firmware/jdu_firmware /usr/local/gn/"
        subprocess.run(command, shell=True)

        print('Interrupt update completed!')

        f.write(f"{case_name} test is finished.")
        # Print the dividing line to the log file
        f.write("------------------------------------------------------------\n\n\n\n")


def run_testcase_update_jx_package(prepare_case, case_name,base_url,tmp):
    with open(log_path, "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"case {case_name} start to run:\n")
        f.write(f"step1:Run the prepare package{prepare_case} for the {case_name}\n")
        f.flush()

        subprocess.Popen(['./jdu.sh', get_xpress_url(prepare_case, case_name,base_url,tmp)[0]], stdout=f)

        print(get_xpress_url(prepare_case, case_name,base_url,tmp)[0])
        print(get_xpress_url(prepare_case, case_name,base_url,tmp)[1])
        print("The prepare case is finished.")

        f.write(f"\nstep2:case {case_name} prepare done, start to run case {case_name}:\n")
        f.flush()
        subprocess.Popen(['./jdu.sh', get_xpress_url(prepare_case, case_name,base_url,tmp)[1]], stdout=f).wait()

        print('Interrupt update completed!')

        f.write(f"{case_name} test is finished.")
        # Print the dividing line to the log file
        f.write("------------------------------------------------------------\n\n\n\n")

def run_testcase_update_fw_file(prepare_case, case_name,base_url,tmp):
    with open(log_path, "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"case {case_name} start to run:\n")
        # Run the prepare case first
        f.write(f"step1:set all settings into default value\n")
        f.flush()
        # Delete the old log file and old xpress file
        delete_xpress_file()
        delete_logs()
        os.chdir('/usr/local/gn')
        subprocess.Popen(['./jdu.sh', get_xpress_url(prepare_case, case_name,base_url,tmp)[0]], stdout=f).wait()

        print(get_xpress_url(prepare_case, case_name,base_url,tmp)[0])
        print(get_xpress_url(prepare_case, case_name,base_url,tmp)[1])
        print("The prepare case is finished.")

        # Move the jdu_firmware file to /tmp/fw because the jdu.sh will call the jdu_firmware process.
        command = "mv /usr/local/gn/jdu_firmware /tmp/fw/"
        subprocess.run(command, shell=True)

        # Run the test case
        process=subprocess.Popen(['./jdu.sh', get_xpress_url(prepare_case, case_name,base_url,tmp)[1]], stdout=f)
        # Wait until the download is completed
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

        command = "/usr/local/gn/jfwu /tmp/fw/Firmware/J*"
        subprocess.run(command, shell=True)
        command = "mv /tmp/fw/Firmware/jdu_firmware /usr/local/gn/"
        subprocess.run(command, shell=True)

        print('Interrupt update completed!')

        f.write(f"{case_name} test is finished.")
        # Print the dividing line to the log file
        f.write("------------------------------------------------------------\n\n\n\n")



if __name__ == '__main__':
    os.chdir('/usr/local/gn')
    log_path = create_log_file("/tmp/auto_log/log")
    
    base_url = "http://192.168.140.95/xpress/"
    tmp = input("Which SR are you in:") + "/" + input("Which device do you use:") + "/"
    
    update_fw_case_list = [16990, 16991, 16992, 17950, 17951]
    upadte_settings_case_list = [6134, 7692, 7695, 7551, 7555, 7556]

    for case_name in update_fw_case_list:
        if case_name == 16992:
            run_testcase_interrupt_fw_file("7556p", case_name,base_url,tmp)
        elif case_name in [16990, 16991]:
            run_testcase_interrupt_jx_package("7556p", case_name,base_url,tmp)
        elif case_name == 17950:
            run_testcase_update_fw_file("7556p", case_name,base_url,tmp)
        else:
            run_testcase_update_jx_package("7556p", case_name,base_url,tmp)


    for case_name in upadte_settings_case_list:
        if case_name in [7692, 7695, 7556]:
            run_testcase_settings("7556p", case_name,base_url,tmp)
        elif case_name == 6134:
            run_testcase_settings("6134p", case_name,base_url,tmp)
        elif case_name == 7555 or case_name == 16990:
            run_testcase_settings("7555p", case_name,base_url,tmp)
        else:
            run_testcase_settings("7551p", case_name,base_url,tmp)

'''
Group01 : FW Update case:

    16990 JXDU:Disconnect the DUT during the FW update.[Use JX Package][Allow downgrade]
    16991 JXDU:Disconnect the DUT during the FW udpate.[Use JX Package][Not allow downgrade]
    16992 JXDU:Disconnect the DUT during the FW update,for all individual components.[Use FW File]
    17950 JXDU:Normal FW update without Interruption.[Use FW File](Linux JXDU 6.x or above)
    17951 JXDU:Normal FW Update without Interruption.[Use JX Package](Linux JXDU 6.x or Above)

Group02 :FW Update & Settings Configure case:

    6098 JX-ThinC: Verify zip package content and JXDU version by creating a ZIP file. - - It is a check test case, not need tu run code so dont need another prepare pakcage for this.
    6134 JX-ThinC:All device settings and FW set to "Leave Unchange",all settings set to Protected.
    7692 JX-ThinC:All settings in the device can be change from default value to min.value with installation of .zip file at the end user PC,no FW change.
    7695 JX-ThinC:All settings in the device can be change from default value to max.value with installation of .zip file at the end user PC,no FW change.
    7551 JX-ThinC:Install a ZIP file on end user environment with a later FW and set all settings are changed.
    7555 JX-ThinC:Install a ZIP file on end user environment with a later FW and no setting change.
    7556 JX-ThinC:Install a ZIP file on end user environment with a later FW and set all settings set to default.

Group03 :Prepare package for 01:
    16990p: use 7556p package.
    16991p: use 7556p package.
    16992p: use 7556p package.
    17950p: use 7556p package.
    17951p: use 7556p package.

Group04 :Prepare testcase for 02:
    6134p: Latest FW and Random settings, Protect = Not.
    7692p: Use the pacakge == 7556.
    7695p: Use the pacakge == 7556.
    7551p: Lower FW and Random settigns.
    7555p: Lower FW and settings = Max value.
    7556p: Lower FW and not default settings.
'''
