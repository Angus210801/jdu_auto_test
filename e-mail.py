import os
import smtplib
import subprocess
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from time import sleep


def send_email():
    # 电子邮件参数
    sender_email = "jdu_test_result@163.com"
    receiver_email = "anlin@jabra.com"
    #反正我写啥名你都会改 就随便写一个了
    subject = "Linux JDU test result of"
    message = "log is in the sttachment"

    # 创建邮件对象
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    # 添加邮件正文
    msg.attach(MIMEText(message, "plain"))

    # 添加附件
    filename = "/tmp/auto_log/link380a_log"  # 附件文件路径
    attachment = open(filename, "rb")

    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename= {filename}")
    msg.attach(part)

    # SMTP服务器设置
    smtp_server = "smtp.163.com"
    smtp_port = 25
    smtp_username = "jdu_test_result@163.com"
    smtp_password = "JIYZJQBNRCNWSFPY"

    # 创建SMTP连接并发送邮件
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
if __name__ == '__main__':
    switch_network()
    sleep(10)
    send_email()
