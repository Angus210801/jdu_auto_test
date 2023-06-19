import os
import smtplib
import subprocess
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from time import sleep
from linux_jdu_autotest_run import *
from linux_jdu_autotest_setup import *

def send_email(device_name):
    sender_email = "jdu_test_result@163.com"
    #add two revicer:extawei
    receiver_email = ["anlin@jabra.com","extawei@jabra.com"]
    subject = "Linux JDU test result of" + device_name
    message = "The log of" + device_name + "is in the attachment"

    # Create a multipart message and set headers
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = ','.join(receiver_email)
    msg["Subject"] = subject

    # Add message
    msg.attach(MIMEText(message, "plain"))

    # Add attachment
    filename = "/tmp/auto_log/"+ device_name +"_log.txt"  # 附件文件路径
    attachment = open(filename, "rb")

    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename= {device_name}")
    msg.attach(part)

    # setup SMTP service
    smtp_server = "smtp.163.com"
    smtp_port = 25
    smtp_username = "jdu_test_result@163.com"
    smtp_password = "JIYZJQBNRCNWSFPY"

    # Create SMTP connection and send e-mail
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
        print("The e-mail had been sent successfully！")
    except smtplib.SMTPException as e:
        print("The e-mail had been sent failed！:", str(e))
def switch_network():
    password = "test@123"
    shut_down_wired = 'echo {} | sudo -S {}'.format(password, "sudo nmcli connection down 'Wired connection 1'")
    os.popen(shut_down_wired)
    subprocess.run(['nmcli', 'radio', 'wifi', 'on'], stdout=subprocess.PIPE)
    Connect_WiFi = 'echo {} | sudo -S {}'.format(password,"sudo nmcli dev wifi connect GN-Hotspot password Denc@2022110")
    os.popen(Connect_WiFi)
def recover_network():
    password = "test@123"
    disConnect_WiFi = 'echo {} | sudo -S {}'.format(password,"nmcli radio wifi off")
    os.popen(disConnect_WiFi)
    open_wired = 'echo {} | sudo -S {}'.format(password, "sudo nmcli connection up 'Wired connection 1'")
    os.popen(open_wired)

if __name__ == '__main__':
    # Ask what device to test
    device_name=input("Please input the device name:")
    switch_network()
    sleep(15)
    send_email(device_name)
    sleep(15)
    recover_network()
