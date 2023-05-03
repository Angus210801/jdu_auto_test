import multiprocessing
import os
import subprocess
import time

def file_writer():
    os.chdir('/usr/local/gn')
    subprocess.Popen(['./jdu.sh', 'http://192.168.140.95/xpress/sr99/evolve230/16991'])

def file_checker():
    while True:
        with open('/tmp/jdu_log/wget.log') as f:
            if '.zip saved' in f.read():
                print('Keyword found')
                break
        time.sleep(1)

if __name__ == '__main__':
    file_process = multiprocessing.Process(target=file_writer)
    file_process.start()
    checker_process = multiprocessing.Process(target=file_checker)
    checker_process.start()

    while True:
        if not checker_process.is_alive():
            print("checker_process has terminated")
            break

        # Keep file_process running
        if not file_process.is_alive():
            print("file_process has terminated, restarting...")
            file_process = multiprocessing.Process(target=file_writer)
            file_process.start()

        time.sleep(1)
