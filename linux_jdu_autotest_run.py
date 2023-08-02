"""
#-------------------------------------------------------------------
#                   CONFIDENTIAL --- Linux JDU auto test script
#-------------------------------------------------------------------
#
#                   @Project Name : Sisyphus
#
#                   @File Name    : linux_jdu_autotest_run
#
#                   @Programmer   : Angus/Ella
#
#                   @Start Date   : 2023/04/24
#
#                   @Last Update  : 2021/06/07
#
#-------------------------------------------------------------------
"""
import datetime
import os
import subprocess
import sys
import time

from linux_jdu_autotest_sendlog_email import *

def run_testcase_update_settings(prepare_case_id, case_id, server_address, tmp):
    # Create a dict to store the test case name.
    # The key is the test case id, and the value is the test case name.
    test_case_dict = {
        '6134': 'JX-ThinC:All device settings and FW set to "Leave Unchange",all settings set to Protected.',
        '7692': 'JX-ThinC:All settings in the device can be change from default value to min.value with installation of .zip file at the end user PC,no FW change.',
        '7695': 'JX-ThinC:All settings in the device can be change from default value to max.value with installation of .zip file at the end user PC,no FW change.',
        '7551': 'JX-ThinC:Install a ZIP file on end user environment with a later FW and set all settings are changed.',
        '7555': 'JX-ThinC:Install a ZIP file on end user environment with a later FW and no setting change.',
        '7556': 'JX-ThinC:Install a ZIP file on end user environment with a later FW and set all settings set to default.'
    }

    case_id=str(case_id)

    if case_id not in test_case_dict.keys():
        print('The test case id is not in the test case dict.')
        sys.exit(1)
    else:
        test_case_name = test_case_dict[case_id]

    with open(log_path, "a") as f:
        # Output the information to the terminal window
        print('Start to run the test case: {}'.format(case_id) + "--" + test_case_name)

        f.write(f"Case {case_id}: {test_case_name}start to run:\n")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"Timestamp: {timestamp}\n")
        # 1. Run the prepared case first
        f.write(f"step1:Run the prepare package{prepare_case_id} for the {case_id}\n")
        f.flush()


        prepare_case_url = get_xpress_url(prepare_case_id, case_id, server_address, tmp)[0]
        test_case_url = get_xpress_url(prepare_case_id, case_id, server_address, tmp)[1]
        f.write(f"{prepare_case_url}\n")
        f.write(f"{test_case_url}\n")
        f.flush()

        subprocess.Popen(['./jdu.sh', prepare_case_url], stdout=f).wait()
        time.sleep(80)


        # 2. Compare the settings before and after the prepare case
        f.write(f"Now, check the device settings is in prepare status: \n")
        setting_compare(f)
        # 3. Run the test case
        f.write(f"\nstep2:case {case_id} prepare done, start to run case {case_id}:\n")
        f.flush()
        subprocess.Popen(['./jdu.sh', test_case_url], stdout=f).wait()
        # 4. Compare the settings after the test case
        f.write(f"\nstep3:check if the settings changed correctly:\n")
        f.flush()
        time.sleep(10)
        setting_compare(f)

        # 5. Print the test finish info and dividing line to the log file
        f.write(f"{case_id} test is finished.")
        f.write("------------------------------------------------------------\n\n\n\n")
        f.flush()
        print('Test case {} is finished.'.format(case_id))
        time.sleep(80)

def run_testcase_update_settings_for_new_device(prepare_case_id, case_id, server_address, tmp):
    # Create a dict to store the test case name.
    # The key is the test case id, and the value is the test case name.
    test_case_dict = {
        '7551': 'JX-ThinC:Install a ZIP file on end user environment with a later FW and set all settings are changed.',
        '7555': 'JX-ThinC:Install a ZIP file on end user environment with a later FW and no setting change.',
        '7556': 'JX-ThinC:Install a ZIP file on end user environment with a later FW and set all settings set to default.'
    }

    case_id=str(case_id)

    if case_id not in test_case_dict.keys():
        print('The test case id is not in the test case dict.')
        sys.exit(1)
    else:
        test_case_name = test_case_dict[case_id]

    with open(log_path, "a") as f:
        # Output the information to the terminal window
        print('Start to run the test case: {}'.format(case_id) + "--" + test_case_name)


        f.write(f"Case {case_id}: {test_case_name}start to run:\n")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"Timestamp: {timestamp}\n")
        # 1. Run the prepared case first
        f.write(f"step1:Run the prepare package{prepare_case_id} for the {case_id}\n")
        f.flush()

        prepare_case_url = get_xpress_url(prepare_case_id, case_id, server_address, tmp)[0]
        test_case_url = get_xpress_url(prepare_case_id, case_id, server_address, tmp)[1]
        f.write(f"{prepare_case_url}\n")
        f.write(f"{test_case_url}\n")
        f.flush()

        lowerfw='lowerfw.zip'
        lowerfw_url = server_address + tmp + lowerfw
        f.write(f"{lowerfw_url}\n")
        f.flush()
        subprocess.Popen(['wget', '-P', '/tmp/', lowerfw_url], stdout=f).wait()
        subprocess.run(['./jfwu', '/tmp/lowerfw.zip'], stdout=f)
        f.write(f"Device update to the lowfw.\n")
        f.flush()
        time.sleep(80)

        subprocess.Popen(['./jdu.sh', prepare_case_url], stdout=f).wait()
        time.sleep(80)


        # 2. Compare the settings before and after the prepare case
        f.write(f"Now, check the device settings is in prepare status: \n")
        setting_compare(f)
        # 3. Run the test case
        f.write(f"\nstep2:case {case_id} prepare done, start to run case {case_id}:\n")
        f.flush()
        subprocess.Popen(['./jdu.sh', test_case_url], stdout=f).wait()
        # 4. Compare the settings after the test case
        f.write(f"\nstep3:check if the settings changed correctly:\n")
        f.flush()
        time.sleep(10)
        setting_compare(f)

        # 5. Print the test finish info and dividing line to the log file
        f.write(f"{case_id} test is finished.")
        f.write("------------------------------------------------------------\n\n\n\n")
        f.flush()
        print('Test case {} is finished.'.format(case_id))
        time.sleep(80)
def run_testcase_interrupt_jx_package(prepare_case_id, case_id, server_address, tmp):
    """ This test case process is:
        1. Download the lower fw package from the server.
        2. Run the lower fw package.
        3. Run the test case fw package from the server.
        4. When update to the 60%, interrupt the update.
        5. Connect the usb box again.
        6. Run the test case jx package again.
    """
    case_id= str(case_id)
    test_case_dict = {
        '16990': 'Disconnect the DUT during the FW update.[Use JX Package][Allow downgrade]',
        '16991': 'Disconnect the DUT during the FW udpate.[Use JX Package][Not allow downgrade]',
        '16992': 'Disconnect the DUT during the FW update,for all individual components.[Use FW File]',
    }

    test_case_name = test_case_dict[case_id]

    with open(log_path, "a") as f:
        # Print the timestamp to the log file
        print('Start to run the test case: {}'.format(case_id))
        f.write(f"case {case_id}: {test_case_name} start to run:\n")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"step1:Run the prepare package {prepare_case_id} for the {case_id}\n")
        f.flush()

        delete_xpress_file()
        delete_jduandjfwu_logs()

        os.chdir('/usr/local/gn')
        # Get the download_url and print the download link to the logs
        prepare_case_url = get_xpress_url(prepare_case_id, case_id, server_address, tmp)[0]
        test_case_url = get_xpress_url(prepare_case_id, case_id, server_address, tmp)[1]
        f.write(f"{prepare_case_url}\n")
        f.write(f"{test_case_url}\n")
        f.flush()

        if prepare_case_url.endswith('lowerfw.zip'):
            # judge the lowerfw.zip is exist or not,if existed,delete it.
            if os.path.exists('/tmp/lowerfw.zip'):
                subprocess.Popen(['rm', '-rf', '/tmp/lowerfw.zip'])

            subprocess.Popen(['wget', '-P', '/tmp/', prepare_case_url], stdout=f).wait()
            # Use ./jfwu + lowerfw.zip to update the device
            time.sleep(10)
            subprocess.run(['./jfwu', '/tmp/lowerfw.zip'], stdout=f)
        else:
            subprocess.Popen(['./jdu.sh', prepare_case_url], stdout=f).wait()

        time.sleep(80)


        f.write(f"The prepare case is finished.\n")
        f.flush()
        # Start to run the test case
        f.write(f"\nstep2:case {case_id} prepare done, start to run case {case_id}:\n")
        f.flush()
        command = "rm -rf /tmp/jdu_log/*"
        subprocess.run(command, shell=True)
        subprocess.Popen(['./jdu.sh', test_case_url], stdout=f)
        # Interrupt the update process
        interrupt_update_jx_package()
        # Wait for the jdu_firmware process to finish
        judge_jdu_process_ongoing()
        # Reconnect the usb box
        f.write(f'--Usb box is reconnected!\n')
        f.write(f'--Interrupt update completed!\n')
        f.write(f'--Next, re-run the test case!\n')
        f.flush()
        # Set up the wait time for the usb box to be ready
        time.sleep(5)
        # Start to re-run the test case
        subprocess.Popen(['./jdu.sh', test_case_url], stdout=f).wait()
        f.write(f"{case_id}: {test_case_name} test is finished.\n")
        # Print the dividing line to the log file
        f.write("------------------------------------------------------------\n\n\n\n")
        f.flush()
        print('Test case {} is finished.'.format(case_id))
        time.sleep(80)


def run_testcase_interrupt_fw_file(prepare_case_id, case_id, server_address, tmp):


    testcase_name= "16992 JXDU:Disconnect the DUT during the FW update,for all individual components.[Use FW File]"

    with open(log_path, "a") as f:
        print('Start to run the test case: {}'.format(case_id) + testcase_name)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"case {case_id} start to run:\n")
        f.write(f"Timestamp: {timestamp}\n")

        f.write(f"step1:set all settings into default value\n")
        f.flush()

        # Delete the old log file and old xpress file
        delete_xpress_file()
        delete_jduandjfwu_logs()
        # Get the download_url and print the download link to the logs

        prepare_case_url = get_xpress_url(prepare_case_id, case_id, server_address, tmp)[0]
        test_case_utl=get_xpress_url(prepare_case_id, case_id, server_address, tmp)[1]
        f.write(f"{prepare_case_url}\n")
        f.write(f"{test_case_utl}\n")
        f.flush()

        # Prepare work for clean the old fw file.
        if not os.path.exists('/tmp/fw'):
            os.makedirs('/tmp/fw')
        else:
            subprocess.Popen(['rm', '-rf', '/tmp/fw/*'])

        if not os.path.exists('/tmp/jdufirmware'):
            os.makedirs('/tmp/jdufirmware')


        os.chdir('/usr/local/gn')

        if prepare_case_url.endswith('lowerfw.zip'):
            # judge the lowerfw.zip is exist or not,if existed,delete it.
            if os.path.exists('/tmp/lowerfw.zip'):
                subprocess.Popen(['rm', '-rf', '/tmp/lowerfw.zip'])
            if os.path.exists('/tmp/fw/higerfw.zip'):
                subprocess.Popen(['rm', '-rf', '/tmp/fw/higerfw.zip'])
           
            subprocess.Popen(['wget', '-P', '/tmp/', prepare_case_url], stdout=f).wait()
            # Use ./jfwu + lowerfw.zip to update the device
            subprocess.run(['./jfwu', '/tmp/lowerfw.zip'], stdout=f)
            print("The lowerfw.zip is updated successfully.")

        else:
             subprocess.Popen(['./jdu.sh', prepare_case_url], stdout=f).wait()

        f.write(f"The prepare case is run finished.")
        f.flush()

        delete_xpress_file()
        delete_jduandjfwu_logs()
        # Move the jdu_firmware file to /tmp/fw because the jdu.sh will call the jdu_firmware process.
        # command = "mv /usr/local/gn/jdu_firmware /tmp/jdufirmware/"
        # subprocess.Popen(command, shell=True).wait()
        # f.write(f'jdu_firmware process is moved to /tmp/fw\n')

        # # Run the test case
        # process = subprocess.Popen(['./jdu.sh', test_case_utl], stdout=f)
        # # Wait until the download is completed
        # while not os.path.exists('/tmp/jdu_log/wget.log'):
        #     time.sleep(3)
        # while "zip’ saved" not in open('/tmp/jdu_log/wget.log').read():
        #     time.sleep(3)
        #     f.write(f'{case_id} JX package download not completed!\n'

        # when download completed, end the ./jdu.sh process
        # process.terminate()

        # f.write(
        #     f'This firmware update failed is because of the interrupt jdu update,we just want to download the fw package from server.\n')
        # f.flush()

        time.sleep(10)
        #
        # subprocess.Popen(['7z', 'x', '/var/run/jabra/xpress_package_*.zip', '-pgn123!', '-o/tmp/fw/']).wait()
        # f.write(f'Unzip the xpress package completed!\n')
        # f.flush()
        # time.sleep(10)

        subprocess.Popen(['wget', '-P', '/tmp/', test_case_utl], stdout=f).wait()
        os.chdir('/usr/local/gn')
        command = "/usr/local/gn/jfwu /tmp/higherfw.zip"
        process = subprocess.Popen(command, shell=True)

        # Once it is up to 40%, we need to disconnect the usb box.
        interrupt_update_fw_file()

        time_account = 0
        # Wait until the jdu is reported update failed.
        while "100%" not in open('/tmp/jfwu_log/jfwu.log').read():
            time.sleep(1)
            time_account += 1
            if time_account > 120:
                f.write(f'Update failed!\n')
                f.flush()
                process.terminate()
                break

        # Reconnect the usb box
        usber = UsbBoxDriver_ubuntu()
        usber.connect_usb_box()
        time.sleep(5)
        f.write('Interrupt update completed!')
        f.flush()

        command = "/usr/local/gn/jfwu /tmp/higherfw.zip"
        subprocess.run(command, shell=True)

        f.write(f"{case_id} test is finished.")
        f.flush()
        # Print the dividing line to the log file
        f.write("------------------------------------------------------------\n\n\n\n")
        f.flush()
        print('Test case {} is finished.'.format(case_id))
        time.sleep(80)


def run_testcase_update_jx_package(prepare_case_id, case_id, server_address, tmp):
    testcase_name = "17951 JXDU:Normal FW Update without Interruption.[Use JX Package](Linux JXDU 6.x or Above)"
    print('Start to run the test case: {}'.format(case_id) + testcase_name)
    with open(log_path, "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"case {case_id} start to run:\n")
        f.write(f"step1:Run the prepare package{prepare_case_id} for the {case_id}\n")
        f.flush()

        delete_xpress_file()
        delete_jduandjfwu_logs()
        # Get the download_url and print the download link to the logs
        prepare_case_url = get_xpress_url(prepare_case_id, case_id, server_address, tmp)[0]
        test_case_utl = get_xpress_url(prepare_case_id, case_id, server_address, tmp)[1]

        f.write(f"{prepare_case_url}\n")
        f.write(f"{test_case_utl}\n")
        f.flush()

        if prepare_case_url.endswith('lowerfw.zip'):
            # judge the lowerfw.zip is exist or not,if existed,delete it.
            if os.path.exists('/tmp/lowerfw.zip'):
                subprocess.Popen(['rm', '-rf', '/tmp/lowerfw.zip'])

            subprocess.Popen(['wget', '-P', '/tmp/', prepare_case_url], stdout=f).wait()
            # Use ./jfwu + lowerfw.zip to update the device
            subprocess.run(['./jfwu', '/tmp/lowerfw.zip'], stdout=f)
        else:
            subprocess.Popen(['./jdu.sh', prepare_case_url], stdout=f).wait()

        time.sleep(80)

        f.write(f"\nstep2:case {case_id} prepare done, start to run case {case_id}:\n")
        f.flush()
        subprocess.Popen(['./jdu.sh', test_case_utl], stdout=f).wait()

        f.write(f"{case_id} test is finished.")
        # Print the dividing line to the log file
        f.write("------------------------------------------------------------\n\n\n\n")
        print('Test case {} is finished.'.format(case_id))
        time.sleep(80)

def testcase_17950(prepare_case_id, case_id, server_address, tmp):
    testcase_name = "17950 JXDU:Normal FW update without Interruption.[Use FW File](Linux JXDU 6.x or above)"
    print('Start to run the test case: {}'.format(case_name) + testcase_name)
    with open(log_path, "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"case {case_id} start to run:\n")

        f.write(f"step1:Downgrade the device fw to the lower fw.\n")
        f.flush()

        # Delete the old log file and old xpress file
        delete_xpress_file()
        delete_jduandjfwu_logs()
        # Get the download_url and print the download link to the logs
        prepare_case_url = get_xpress_url(prepare_case_id, case_id, server_address, tmp)[0]
        test_case_utl = get_xpress_url(prepare_case_id, case_id, server_address, tmp)[1]
        f.write(f"{prepare_case_url}\n")
        f.write(f"{test_case_utl}\n")
        f.flush()

        # Prepare work for clean the old fw file.
        # if not os.path.exists('/tmp/fw'):
        #     os.makedirs('/tmp/fw')
        # else:
        #     subprocess.Popen(['rm', '-rf', '/tmp/fw/*'])
        #
        # if not os.path.exists('/tmp/jdufirmware'):
        #     os.makedirs('/tmp/jdufirmware')
        #
        # os.chdir('/usr/local/gn')

        if prepare_case_url.endswith('lowerfw.zip'):
            # judge the lowerfw.zip is exist or not,if existed,delete it.
            if os.path.exists('/tmp/lowerfw.zip'):
                subprocess.Popen(['rm', '-rf', '/tmp/lowerfw.zip'])
            subprocess.Popen(['wget', '-P', '/tmp/', prepare_case_url], stdout=f).wait()
            # Use ./jfwu + lowerfw.zip to update the device
            subprocess.run(['./jfwu', '/tmp/lowerfw.zip'], stdout=f)
        else:
            subprocess.Popen(['./jdu.sh', prepare_case_url], stdout=f).wait()

        time.sleep(80)

        f.write(f"The prepare case is run finished\n")
        f.flush()

        delete_xpress_file()
        delete_jduandjfwu_logs()
        # Move the jdu_firmware file to /tmp/fw because the jdu.sh will call the jdu_firmware process.
        # command = "mv /usr/local/gn/jdu_firmware /tmp/jdufirmware/"
        # subprocess.Popen(command, shell=True).wait()
        # f.write(f'jdu_firmware process is moved to /tmp/jdufirmware/\n')
        # f.flush()

        # process = subprocess.Popen(['./jdu.sh', test_case_utl], stdout=f)
        #
        # while not os.path.exists('/tmp/jdu_log/wget.log'):
        #     time.sleep(1)
        # while "zip’ saved" not in open('/tmp/jdu_log/wget.log').read():
        #     time.sleep(2)
        #     f.write(f'Download not completed!\n')

        f.write(f'{case_id} JX package downlaod completed!\n')

        # when download completed, end the ./jdu.sh process
        # process.terminate()
        # f.write(f'Terminate the process once the download complete.\n')
        # f.flush()
        time.sleep(2)
        #
        # subprocess.run(['7z', 'x', '/var/run/jabra/xpress_package_*.zip', '-pgn123!', '-o/tmp/fw/'])
        # f.write(f'The pacakge has unzip to the /tmp/fw\n')
        # f.flush()
        # time.sleep(5)
        # subprocess.Popen(['wget', '-P', '/tmp/', test_case_utl], stdout=f).wait()

        os.chdir('/usr/local/gn')
        command = "/usr/local/gn/jfwu /tmp/higherfw.zip"
        subprocess.Popen(command, shell=True).wait()

        f.write(f"{case_id} test is finished.")
        f.flush()
        # Print the dividing line to the log file
        f.write("------------------------------------------------------------\n\n\n\n")
        print('Test case {} is finished.'.format(case_id))

        time.sleep(80)


if __name__ == '__main__':
    start_time = time.time()

    os.chdir('/usr/local/gn')
    log_path = create_log_file("/tmp/auto_log/log")

    server_address = "http://192.168.140.95/xpress/"
    current_test_rc = input("Which SR are you in:") + "/"
    device_name = input("Which device are you test:")
    new_device_or_not=input("Is it a new device? (y/n)")
    current_test_rc = current_test_rc + device_name + "/"

    with open(log_path, "a") as f:
        os_version=get_os_version()
        # subprocess.run(['cat', '/etc/issue'], stdout=f)
        f.write(f"OS version is {os_version}\n")
        f.flush()
        subprocess.run(['dpkg', '-l','jdu'], stdout=f)


    if device_name == 'panacast20':
        # Panacast20 update is very fast, so we don't need to run the interrupt update case.
        update_fw_case_list = [17950, 17951]
    else:
        update_fw_case_list = [16990, 16991, 16992, 17950, 17951]
        # update_fw_case_list = [16992,17950]

    update_settings_case_list = [7551,7695,7692,6134,7555,7556]
    # update_settings_case_list = []


    for case_name in update_fw_case_list:
        if new_device_or_not == 'y':
            prepare_case = "lowerfw.zip"
        else:
            prepare_case = "16990p"

        if case_name == 16992:
            run_testcase_interrupt_fw_file(prepare_case, case_name, server_address, current_test_rc)
        elif case_name in [16990, 16991]:
            run_testcase_interrupt_jx_package(prepare_case, case_name, server_address, current_test_rc)
        elif case_name == 17950:
            testcase_17950(prepare_case, case_name, server_address, current_test_rc)
        else:
            run_testcase_update_jx_package(prepare_case, case_name, server_address, current_test_rc)

    print("FW update case is finished.\n")
    print("Start to run the settings update case.\n")

    for case_name in update_settings_case_list:
        if case_name == 7692 or case_name == 7695:
            run_testcase_update_settings("7556", case_name, server_address, current_test_rc)
        elif case_name == 7556:
            if new_device_or_not == 'y':
                run_testcase_update_settings_for_new_device("7556p", case_name, server_address, current_test_rc)
            else:
                run_testcase_update_settings("7556p", case_name, server_address, current_test_rc)
        elif case_name == 6134:
            run_testcase_update_settings("6134p", case_name, server_address, current_test_rc)
        elif case_name == 7555:
            if new_device_or_not == 'y':
                run_testcase_update_settings_for_new_device("7555p", case_name, server_address, current_test_rc)
            else:
                run_testcase_update_settings("7555p", case_name, server_address, current_test_rc)
        else:
            if new_device_or_not == 'y':
                run_testcase_update_settings_for_new_device("7551p", case_name, server_address, current_test_rc)
            else:
                run_testcase_update_settings("7551p", case_name, server_address, current_test_rc)

    rename_log_file(device_name)

    end_time = time.time()
    total_time = end_time - start_time

    switch_network()
    sleep(15)
    send_email(device_name,os_version)
    sleep(15)
    recover_network()

    print("Test finish, the test run time is: " + str(total_time))

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
    16990p: Lower FW and not settings change,downgrade==allow.
    16991p: same with 16990p
    16992p: same with 16990p
    17950p: same with 16990p
    17951p: same with 16990p

Group04 :Prepare testcase for 02:
    6134p: Latest FW and Random settings, Protect = Not.
    7692p: Use the pacakge == 7556.
    7695p: Use the pacakge == 7556.
    7551p: Lower FW and Random settigns.
    7555p: Lower FW and settings = Max value.
    7556p: Lower FW and not default settings.
'''
