import subprocess
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

def run_the_test_case():
    # Delete the logs
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
    # Then we need to update the device via the package in the /tmp/fw,the package is zip file and its name is start with J.
    # So we need to use characters to match it.
    # And the update process is in /usr/local/gn/jfwu
    # So we need to use subprocess to run it. below is the code:
    time.sleep(3)
    os.chdir('/usr/local/gn')
    command = "/usr/local/gn/jfwu /tmp/fw/Firmware/J*"
    subprocess.Popen(command,shell=True)
    # After run the jfwu, we need to wait for the update process to 50%.
    # while not os.path.exists('/tmp/jfwu_log/jfwu.log'):
    #     time.sleep(1)
    #     print("Update not started")


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
    run_the_test_case()