import subprocess
import time

# 指定USB控制器的设备名称
usb_controller = '/sys/bus/usb/devices/usb1'

# 禁用USB子系统
subprocess.run(['sudo', 'sh', '-c', f'echo 0 > {usb_controller}/authorized'])

# 等待几秒钟
time.sleep(2)

# 启用USB子系统
subprocess.run(['sudo', 'sh', '-c', f'echo 1 > {usb_controller}/authorized'])

