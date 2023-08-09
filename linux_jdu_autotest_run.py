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

    case_id = str(case_id)

    if case_id not in test_case_dict.keys():
        print('The test case id is not in the test case dict.')
        sys.exit(1)
    else:
        test_case_name = test_case_dict[case_id]

    with open(log_path, "a") as f:
        # Output the information to the terminal window
        print('Start to run the test case: {}'.format(case_id) + "--" + test_case_name)

        write_and_flush(f, f"Case {case_id}: {test_case_name}start to run:\n")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        write_and_flush(f, f"Start time: {timestamp}\n")
        write_and_flush(f, f"step1:Run the prepare package{prepare_case_id} for the {case_id}\n")

        prepare_case_url = get_xpress_url(prepare_case_id, case_id, server_address, tmp)[0]
        test_case_url = get_xpress_url(prepare_case_id, case_id, server_address, tmp)[1]
        write_and_flush(f, f"{prepare_case_url}\n")
        write_and_flush(f, f"{test_case_url}\n")

        write_and_flush(f, f"step1:case {case_id} prepare start:\n")
        subprocess.Popen(['./jdu.sh', prepare_case_url], stdout=f).wait()
        time.sleep(80)

        write_and_flush(f, f"Now, check the device settings is in prepare status: \n")
        time.sleep(2)
        setting_compare(f)

        write_and_flush(f, f"\nstep2:case {case_id} prepare done, start to run case {case_id}:\n")
        subprocess.Popen(['./jdu.sh', test_case_url], stdout=f).wait()

        write_and_flush(f, f"\nstep3:check if the settings changed correctly:\n")
        time.sleep(10)
        setting_compare(f)

        write_and_flush(f, f"Test case {case_id} is finished.\n-----------------\n\n\n\n")
        print('Test case {} is finished.'.format(case_id))
        time.sleep(80)


def run_testcase_update_settings_for_new_device(prepare_case_id, case_id, server_address, current_test_rc):
    test_case_dict = {
        '7551': 'JX-ThinC:Install a ZIP file on end user environment with a later FW and set all settings are changed.',
        '7555': 'JX-ThinC:Install a ZIP file on end user environment with a later FW and no setting change.',
        '7556': 'JX-ThinC:Install a ZIP file on end user environment with a later FW and set all settings set to default.'
    }
    case_id = str(case_id)
    test_case_name = test_case_dict.get(case_id)
    if not test_case_name:
        print('The test case id is not in the test case dict.')
        sys.exit(1)

    with open(log_path, "a") as f:
        print('Start to run the test case: {} -- {}'.format(case_id, test_case_name))
        write_and_flush(f, f"Case {case_id}: {test_case_name} start to run:\n")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        write_and_flush(f, f"Timestamp: {timestamp}\n")
        write_and_flush(f, f"step1:Run the prepare package {prepare_case_id} for the {case_id}\n")

        prepare_case_url, test_case_url = get_xpress_url(prepare_case_id, case_id, server_address, current_test_rc)
        write_and_flush(f, f"{prepare_case_url}\n")
        write_and_flush(f, f"{test_case_url}\n")

        lowerfw_url = server_address + current_test_rc + 'lowerfw.zip'
        write_and_flush(f,
                        f"{lowerfw_url}\n-----step1.1:download the lower fw and update the device to lower fw-----\n")

        subprocess.Popen(['wget', '-P', '/tmp/', lowerfw_url], stdout=f).wait()
        subprocess.run(['./jfwu', '/tmp/lowerfw.zip'], stdout=f)
        write_and_flush(f, f"Done the lower fw update.\n")

        time.sleep(80)

        subprocess.Popen(['./jdu.sh', prepare_case_url], stdout=f).wait()
        time.sleep(80)

        write_and_flush(f, f"Now, check the device settings is in prepare status: \n")
        setting_compare(f)

        write_and_flush(f, f"\nstep2:case {case_id} prepare done, start to run case {case_id}:\n")
        subprocess.Popen(['./jdu.sh', test_case_url], stdout=f).wait()

        write_and_flush(f, f"\nstep3:check if the settings changed correctly:\n")
        time.sleep(10)

        setting_compare(f)

        write_and_flush(f, f"Test case {case_id} is finished.\n-----------------\n\n\n\n")
        print('Test case {} is finished.'.format(case_id))
        time.sleep(80)


def run_testcase_interrupt_jx_package(prepare_case_id, case_id, server_address, current_test_rc):
    case_id = str(case_id)
    test_case_dict = {
        '16990': 'Disconnect the DUT during the FW update.[Use JX Package][Allow downgrade]',
        '16991': 'Disconnect the DUT during the FW udpate.[Use JX Package][Not allow downgrade]',
    }

    test_case_name = test_case_dict.get(case_id)
    if not test_case_name:
        print('The test case id is not in the test case dict.')
        sys.exit(1)

    with open(log_path, "a") as f:
        # Print the timestamp to the log file
        print('Start to run the test case: {}'.format(case_id))
        write_and_flush(f, f"case {case_id}: {test_case_name} start to run:")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        write_and_flush(f, f"Timestamp: {timestamp}")
        write_and_flush(f, f"step1:Run the prepare package {prepare_case_id} for the {case_id}")

        delete_xpress_file()
        delete_jduandjfwu_logs()

        os.chdir('/usr/local/gn')

        prepare_case_url, test_case_url = get_xpress_url(prepare_case_id, case_id, server_address, current_test_rc)
        write_and_flush(f, f"{prepare_case_url}")
        write_and_flush(f, f"{test_case_url}")

        if prepare_case_url.endswith('lowerfw.zip'):
            lowerfw_url = server_address + current_test_rc + 'lowerfw.zip'
            if os.path.exists('/tmp/lowerfw.zip'):
                subprocess.run(['./jfwu', '/tmp/lowerfw.zip'], stdout=f)
            else:
                subprocess.Popen(['wget', '-P', '/tmp/', lowerfw_url], stdout=f).wait()
                subprocess.run(['./jfwu', '/tmp/lowerfw.zip'], stdout=f)

            write_and_flush(f, f"Device update to the lowfw.")
            time.sleep(80)
        else:
            subprocess.Popen(['./jdu.sh', prepare_case_url], stdout=f).wait()

        time.sleep(80)

        write_and_flush(f, f"The prepare case is finished.")
        # Start to run the test case
        write_and_flush(f, f"\nstep2:case {case_id} prepare done, start to run case {case_id}:")
        command = "rm -rf /tmp/jdu_log/*"
        subprocess.run(command, shell=True)
        subprocess.Popen(['./jdu.sh', test_case_url], stdout=f)
        # Interrupt the update process
        interrupt_update_jx_package()
        # Wait for the jdu_firmware process to finish
        judge_jdu_process_ongoing()
        # Reconnect the usb box
        write_and_flush(f, f'--Usb box is reconnected!')
        write_and_flush(f, f'--Interrupt update completed!')
        write_and_flush(f, f'--Next, re-run the test case!')
        # Set up the wait time for the usb box to be ready
        time.sleep(5)
        # Start to re-run the test case
        subprocess.Popen(['./jdu.sh', test_case_url], stdout=f).wait()
        write_and_flush(f, f"{case_id}: {test_case_name} test is finished.")
        # Print the dividing line to the log file
        write_and_flush(f, "------------------------------------------------------------\n\n\n\n")
        print('Test case {} is finished.\n'.format(case_id))
        time.sleep(80)


def run_testcase_interrupt_fw_file(prepare_case_id, case_id, server_address, current_test_rc):
    testcase_name = "16992 JXDU:Disconnect the DUT during the FW update,for all individual components.[Use FW File]"

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

        prepare_case_url = get_xpress_url(prepare_case_id, case_id, server_address, current_test_rc)[0]
        test_case_utl = get_xpress_url(prepare_case_id, case_id, server_address, current_test_rc)[1]
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
            if os.path.exists('/tmp/higherfw.zip'):
                subprocess.Popen(['rm', '-rf', '/tmp/higherfw.zip'])

            subprocess.Popen(['wget', '-P', '/tmp/', prepare_case_url], stdout=f).wait()
            # Use ./jfwu + lowerfw.zip to update the device
            subprocess.run(['./jfwu', '/tmp/lowerfw.zip'], stdout=f)
            f.write(f"Device update to the lowfw.\n")
        else:
            subprocess.Popen(['./jdu.sh', prepare_case_url], stdout=f).wait()

        f.write(f"The prepare case is run finished.")
        f.flush()

        delete_xpress_file()
        delete_jduandjfwu_logs()

        time.sleep(60)

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
        time.sleep(20)
        f.write('Interrupt update completed!')
        f.flush()

        command = "/usr/local/gn/jfwu /tmp/higherfw.zip"
        subprocess.run(command, shell=True)
        f.write(f'--Reupdate is finish.\n')

        f.write(f"{case_id} test is finished.")
        f.flush()
        # Print the dividing line to the log file
        f.write("------------------------------------------------------------\n\n\n\n")
        f.flush()
        print('Test case {} is finished.'.format(case_id))
        time.sleep(80)


def run_testcase_update_jx_package(prepare_case_id, case_id, server_address, current_test_rc):
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
        prepare_case_url = get_xpress_url(prepare_case_id, case_id, server_address, current_test_rc)[0]
        test_case_utl = get_xpress_url(prepare_case_id, case_id, server_address, current_test_rc)[1]

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


def testcase_17950(prepare_case_id, case_id, server_address, current_test_rc):
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
        prepare_case_url = get_xpress_url(prepare_case_id, case_id, server_address, current_test_rc)[0]
        test_case_utl = get_xpress_url(prepare_case_id, case_id, server_address, current_test_rc)[1]
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

        f.write(f'{case_id} JX package downlaod completed!\n')
        os.chdir('/usr/local/gn')
        command = "/usr/local/gn/jfwu /tmp/higherfw.zip"
        subprocess.Popen(command, shell=True).wait()

        f.write(f"{case_id} test is finished.")
        f.flush()
        # Print the dividing line to the log file
        f.write("------------------------------------------------------------\n\n\n\n")
        print('Test case {} is finished.'.format(case_id))

        time.sleep(80)


def run_testcase_fw_update(case_name, server_address, current_test_rc, new_device_or_not):
    prepare_case = "lowerfw.zip" if new_device_or_not == 'y' else "16990p"

    test_case_mapping = {
        16992: run_testcase_interrupt_fw_file,
        16990: run_testcase_interrupt_jx_package,
        16991: run_testcase_interrupt_jx_package,
        17950: testcase_17950,
    }
    # If case_name is not found in the mapping, default to run_testcase_update_jx_package
    test_case_function = test_case_mapping.get(case_name, run_testcase_update_jx_package)
    test_case_function(prepare_case, case_name, server_address, current_test_rc)


def run_testcase_update_settings_index(case_name, server_address, current_test_rc, new_device_or_not):
    test_case_mapping = {
        7692: ("7556",),
        7695: ("7556",),
        7556: ("7556p",) if new_device_or_not == 'y' else ("7556p",),
        6134: ("6134p",),
        7555: ("7555p",) if new_device_or_not == 'y' else ("7555p",),
    }
    default_case = ("7551p",)

    test_case_args = test_case_mapping.get(case_name, default_case)
    run_testcase_update_settings(*test_case_args, server_address, current_test_rc)

def print_log():
    with open('/tmp/auto_log/log', 'r') as file:
        data = file.read()
        print(data)


if __name__ == '__main__':
    start_time = time.time()
    os.chdir('/usr/local/gn')
    log_path = create_log_file("/tmp/auto_log/log")

    server_address = "http://192.168.140.95/xpress/"
    current_test_rc = input("Which SR are you in:") + "/"
    device_name = input("Which device are you test:")
    new_device_or_not = input("Is it a new device? (y/n)")
    current_test_rc = current_test_rc + device_name + "/"
    print_log()

    with open(log_path, "a") as f:
        os_version = get_os_version()
        f.write(f"OS version is {os_version}\n")
        f.flush()
        subprocess.run(['dpkg', '-l', 'jdu'], stdout=f)

    if device_name == 'panacast20':
        # Panacast20 update is very fast, so we don't need to run the interrupt update case.
        update_fw_case_list = [17950, 17951]
        print_log()
    else:
        update_fw_case_list = [16992, 16990, 16991, 17950, 17951]
        # update_fw_case_list = [16992,17950]
        print_log()

    for case_name in update_fw_case_list:
        run_testcase_fw_update(case_name, server_address, current_test_rc, new_device_or_not)
        print_log()

    print("FW update case is finished.\n")
    print("Start to run the settings update case.\n")

    update_settings_case_list = [7551, 7695, 7692, 6134, 7555, 7556]
    for case_name in update_settings_case_list:
        run_testcase_update_settings_index(case_name, server_address, current_test_rc, new_device_or_not)
        print_log()

    rename_log_file(device_name)

    end_time = time.time()
    total_time = end_time - start_time

    switch_network()
    sleep(15)
    send_email(device_name, os_version)
    sleep(15)
    recover_network()

    print("Test finish, the test run time is: " + str(total_time))
