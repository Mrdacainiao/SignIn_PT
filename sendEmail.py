import smtplib
from email.mime.text import MIMEText
from email.header import Header
import configparser


def get_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def send_email(config_path, send_message):
    config = get_config(config_path)

    sender = config.get('email', 'sender')
    receiver = config.get('email', 'receiver')

    # 第三方 SMTP 服务
    mail_host = config.get('email', 'mail_host')
    mail_user = config.get('email', 'mail_user')
    mail_pass = config.get('email', 'mail_pass')

    # 发送文本
    message = MIMEText(send_message, 'plain', 'utf-8')
    message['From'] = Header(config.get('email', 'From'), 'utf-8')
    message['To'] = Header(config.get('email', 'To'), 'utf-8')
    message['Subject'] = Header(config.get('email', 'subject'), 'utf-8')

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receiver, message.as_string())
        print("邮件发送成功")
    except smtpObj.SMTPException:
        print("Error: 无法发送邮件")


if __name__ == '__main__':
    config_path = "config.ini"
    send_email(config_path, "PT签到成功")
