import os
import subprocess

if __name__ == '__main__':
    os.chdir('/usr/local/gn')
    base_url = "http://192.168.140.95/xpress/sr99/evolve230/7551"
    subprocess.Popen(['./jdu.sh', base_url]).wait()


