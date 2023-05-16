import subprocess
import os, time, signal, shutil

from usb_box_action import UsbBoxDriver_ubuntu


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
def download_package(base_url):
    subprocess.Popen(['./jdu.sh', base_url])

    while not os.path.exists('/tmp/jdu_log/wget.log'):
        time.sleep(1)

    while "zip’ saved" not in open('/tmp/jdu_log/wget.log').read():
        time.sleep(1)
        print('Download not completed!')

    print('Download completed!')

    process = subprocess.Popen(['pgrep', '-f', './jdu.sh'])
    pid = process.communicate()[0]

    if pid:
        pid = pid.strip()
        os.kill(int(pid), signal.SIGTERM)

    command = "mv /usr/local/gn/jdu_firmware /tmp/fw/"
    subprocess.run(command, shell=True)

    if not os.path.exists('/tmp/fw'):
        os.mkdir('/tmp/fw')
    else:
        shutil.rmtree('/tmp/fw')
        os.mkdir('/tmp/fw')

    time.sleep(2)
    subprocess.run(['7z', 'x', '/var/run/jabra/xpress_package_*.zip', '-pgn123!', '-o/tmp/fw/'])

    return '/tmp/fw/Firmware/J*'

def update_device(package_path):
    os.chdir('/usr/local/gn')
    command = "/usr/local/gn/jfwu " + package_path
    subprocess.Popen(command, shell=True)

    while "50%" not in open('/tmp/jfwu_log/jfwu.log').read():
        time.sleep(1)
        print("Update not started")

    interrupt_update()

    while "100%" not in open('/tmp/jfwu_log/jfwu.log').read():
        time.sleep(1)
        print('Update not completed!')

    usber = UsbBoxDriver_ubuntu()
    usber.connect_usb_box()
    time.sleep(10)

    command = "mv " + package_path + "/jdu_firmware /usr/local/gn/"
    subprocess.run(command, shell=True)

def run_the_test_case(): # Delete the logs delete_xpress_file() delete_logs()
    # Set working directory to /usr/local/gn
    os.chdir('/usr/local/gn')

    # Download the firmware package
    base_url = "http://192.168.140.95/xpress/sr99/evolve230/16990"
    package_path = download_package(base_url)

    # Update the device
    update_device(package_path)

    # Print completion statement
    print('Interrupt update completed!')