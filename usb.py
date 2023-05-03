import multiprocessing
import os
import subprocess
import time

def file_writer():
    os.chdir('/usr/local/gn')
    subprocess.Popen(['./jdu.sh', 'http://192.168.140.95/xpress/sr99/evolve230/16991'])

def file_checker():
    while True:
        with open("/tmp/jdu_log/wget.log") as f:
            if ".zip’ saved" in f.read():
                print('Keyword found!')
                break
        time.sleep(1)

if __name__ == '__main__':
    file_process = multiprocessing.Process(target=file_writer)
    file_process.start()
    checker_process = multiprocessing.Process(target=file_checker)
    checker_process.start()
    checker_process.join()
    # checker_process.terminate()



# subprocess.Popen(['./jdu.sh', get_url(prepare_case, case_name)[1]], stdout=f)