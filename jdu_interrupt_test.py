import os
import subprocess
from usb_box_action import *
import time

if __name__ == '__main__':

    os.chdir('/usr/local/gn')
    base_url = "http://192.168.140.95/xpress/sr99/evolve230/16990"
    subprocess.Popen(['./jdu.sh', base_url])

    while not os.path.exists('/tmp/jdu_log/wget.log'):
        time.sleep(1)

    while ".zip saved" not in open('/tmp/jdu_log/wget.log').read():
        time.sleep(1)
        print('Download not completed!')
    print('Downlaod completed!')
    #when download completed, end the ./jdu.sh process
    subprocess.Popen(['pkill', 'jdu.sh'])
    # if Download zip completed, then start to unzip the package.
    # The zip is in /var/run/jabra/
    # And it has not stable name, so we need to use characters to match it.
    # its name is start with xpress_package_ and end with .zip
    # Then unzip it to /tmp/fw/
    # The zip also has the password - gn123,so we need to use 7z to unzip it.
    # Before unzip the package, we need to ensure that the directroy is existed and empty.
    # if not, we need to create it and empty it.
    if not os.path.exists('/tmp/fw'):
        os.makedirs('/tmp/fw')
    else:
        subprocess.Popen(['rm', '-rf', '/tmp/fw/*'])

    subprocess.Popen(['7z', '/var/run/jabra/xpress_package_*.zip', '-pgn123', '-o/tmp/fw'])

    # Then we need to update the device via the package in the /tmp/fw,the package is zip file and its name is start with J.
    # So we need to use characters to match it.
    # And the update process is in /usr/local/gn/jfwu
    # So we need to use subprocess to run it. below is the code:
    os.chdir('/usr/local/gn')
    base_url = "/tmp/fw/J*.zip"
    subprocess.Popen(['./jfwu', base_url])
    # After run the jfwu, we need to wait for the update process to 50%.
    while not os.path.exists('/tmp/jfwu_log/jfwu.log'):
        time.sleep(1)
    while "50%" not in open('/tmp/jfwu_log/jfwu.log').read():
        time.sleep(1)
        print('Update not up to 50%!')
    # Once it is up to 50%, we need to disconnect the usb box.
    usber = UsbBoxDriver_ubuntu()
    print("Disconnecting USB box...")
    usber.disconnect_usb_box()

    while "failed" not in open('/tmp/jfwu_log/jfwu.log').read():
        time.sleep(1)
        print('Update not completed!')

    usber.connect_usb_box()
    time.sleep(10)
    subprocess.Popen(['./jfwu', base_url]).wait()
    print('Interrupt update completed!')